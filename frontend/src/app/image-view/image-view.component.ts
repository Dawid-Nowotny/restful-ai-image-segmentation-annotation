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

      this.getImage();
      this.getImageAuthor();
      this.getSuperTagsAuthor();
    }

    getImage(): void {
      this.serverService.getImage(this.image_id).subscribe({
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
    }

    getImageAuthor() {
      this.serverService.getImageAuthor(this.image_id).subscribe({
        next: (result: any) => {
          this.imageAutor = result.image_uploader;
        },
        error: (error: Error)=> {
          console.error('Error fetching image author', error);
        }
      });
    }

    getSuperTagsAuthor() {
      this.serverService.getSuperTagsAuthor(this.image_id).subscribe({
        next: (result: any) => {
          this.superTagsAutor = result.super_tag_author;
        },
        error: (error: Error)=> {
          console.error('Error fetching super tags author', error);
        }
      });
    }

    async changeImage(): Promise<void> {
      if (this.image == this.imageURL) {
        if (this.segmentedImageURL == null) {
          await this.getSegmentedImage();
        }
        this.image = this.segmentedImageURL;
        this.buttonLabel = 'Wyświetl oryginał';
      } else {
        this.image = this.imageURL;
        this.buttonLabel = 'Wyświetl segmentację';
      }
    }

    getSegmentedImage(): Promise<void> {
      return new Promise((resolve, reject) => {
        this.serverService.getSegmentedImage(this.image_id).subscribe({
          next: (blob: Blob) => {
            this.segmentedImageBLOB = blob;
            const reader = new FileReader();
            reader.onload = () => {
              this.segmentedImageURL = reader.result;
              resolve();
            };
            reader.readAsDataURL(blob);
          },
          error: (error: Error) => {
            console.error('Error fetching segmented image:', error);
            reject(error);
          }
        });
      });
    }

    downloadImage(): void {
      if (this.image == this.imageURL && this.imageBLOB) {
        const link =  window.URL.createObjectURL(this.imageBLOB);
        this.triggerDownload(link, `${this.image_id}.jpg`);
      } else if (this.image == this.segmentedImageURL && this.segmentedImageBLOB) {
        const link =  window.URL.createObjectURL(this.segmentedImageBLOB);
        this.triggerDownload(link, `${this.image_id}-segmented.jpg`);
      } else {
        console.error('Nie można zapisać obrazu');
      }
    }

    triggerDownload(link: string, filename: string) {
      const a = document.createElement('a');
      a.href = link;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(link);
    }
}