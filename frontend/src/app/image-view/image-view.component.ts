import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { ServerService } from '../services/server.service';

@Component({
    selector: 'app-image-view',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './image-view.component.html',
    styleUrl: './image-view.component.css'
})

export class ImageViewComponent implements OnInit {
    imageAutor: string = '';
    superTagsAutor: string = '';
    image_id: number = 0;
    imageURL: string | ArrayBuffer | null = null;
    imageBLOB: Blob | null = null;
    segmentedImageURL: string | ArrayBuffer | null = null;
    segmentedImageBLOB: Blob | null = null;
    image: string | ArrayBuffer | null = null;
    buttonLabel: string = 'Wyświetl segmentację';

    constructor(private route: ActivatedRoute, private serverService: ServerService) { }

    ngOnInit() {
      this.route.params.subscribe(params => {
          this.image_id = params['id'];
      })

      this.getImages(this.image_id);
      this.getImageAndSuperTagsAuthors(this.image_id);
    }

    getImages(imageId: number): void {
      this.serverService.getImage(imageId).subscribe({
        next: (blob: Blob) => {
          this.imageBLOB = blob;
          const reader = new FileReader();
          reader.onload = () => {
            this.imageURL = reader.result;
            this.image = reader.result;
          }
          reader.readAsDataURL(blob);
        },
        error: (error: Error)=> {
          console.error('Error fetching image:', error);
        }
      });

      this.serverService.getSegmentedImage(imageId).subscribe({
        next: (blob: Blob) => {
          this.segmentedImageBLOB = blob;
          const reader = new FileReader();
          reader.onload = () => this.segmentedImageURL = reader.result;
          reader.readAsDataURL(blob);
        },
        error: (error: Error)=> {
          console.error('Error fetching segmented image:', error);
        }
      });
    }

    getImageAndSuperTagsAuthors(imageId: number) {
      this.serverService.getImageAndSuperTagsAuthors(imageId).subscribe({
        next: (result: any) => {
          this.imageAutor = result.image_uploader;
          this.superTagsAutor = result.super_tag_author;
        },
        error: (error: Error)=> {
          console.error('Error fetching authors', error);
        }
      });
    }

    changeImage(): void {
      if (this.image == this.imageURL) {
        this.image = this.segmentedImageURL;
        this.buttonLabel = 'Wyświetl oryginał';
      }
      else {
        this.image = this.imageURL;
        this.buttonLabel = 'Wyświetl segmentację';
      }
    }

    downloadImage(): void {
      let blob: Blob | null = null;
      let fileName: string = '';

      if (this.image == this.imageURL && this.imageBLOB) {
        blob = this.imageBLOB;
        fileName = `${this.image_id}.jpg`;
      }
      else if (this.image == this.segmentedImageURL && this.segmentedImageBLOB) {
        blob = this.segmentedImageBLOB;
        fileName = `${this.image_id}-segmented.jpg`;
      }
      else {
        console.error('Nie można zapisać obrazu');
        return;
      }
    
      const link = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = link;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(link);
    }
}