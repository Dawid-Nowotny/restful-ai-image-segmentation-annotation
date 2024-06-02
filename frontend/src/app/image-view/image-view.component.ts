import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { ServerService } from '../services/server.service';

@Component({
    selector: 'app-image-view',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule],
    templateUrl: './image-view.component.html',
    styleUrl: './image-view.component.css'
})

export class ImageViewComponent implements OnInit {
    imageAuthor: string = '';
    superTagsAutor: string = '';
    threshold: string = '';
    annotations: string = '';
    suggestedAnnotations: string[] = [];
    commentForm: FormGroup;
    image_id: number = 0;
    imageURL: string | ArrayBuffer | null = null;
    imageBLOB: Blob | null = null;
    segmentedImageURL: string | ArrayBuffer | null = null;
    segmentedImageBLOB: Blob | null = null;
    image: string | ArrayBuffer | null = null;
    buttonLabel: string = 'Wyświetl segmentację';

    constructor(private route: ActivatedRoute, private serverService: ServerService) {
      this.commentForm = new FormGroup({
        comment: new FormControl('', [Validators.required, Validators.pattern(/\S+/)])
      });
    }

    ngOnInit() {
      this.route.params.subscribe(params => {
          this.image_id = params['id'];
      })

      this.getImage();
      this.getImageAuthor();
      this.getSuperTagsAuthor();
      this.getImageDetections();
      this.getSuggestedAnnotations();
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
          this.imageAuthor = result.image_uploader;
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
        error: (error: Error) => {
          console.error('Error fetching super tags author', error);
        }
      });
    }

    getImageDetections() {
      this.serverService.getImageDetections(this.image_id).subscribe({
        next: (result: any) => {
          this.threshold = result.threshold;
          this.annotations = result.coordinates_classes;
        },
        error: (error: Error) => {
          console.error("Error fetching detections", error);
        }
      })
    }

    getSuggestedAnnotations() {
      this.serverService.getSuggestAnnotations(this.image_id).subscribe({
        next: (result: any) => {
          this.suggestedAnnotations = result.annotations;
        },
        error: (error: Error) => {
          console.error('Error fetching suggested annotations', error);
        }
      });
    }

    clickSuggestedAnnotation(annotation: string) {
      let newValue = '';
      let oldValue = this.commentForm.controls['comment'].value;
      if (oldValue.trim().length != 0)
        oldValue += ', ';
      newValue = oldValue + annotation;

      this.commentForm.controls['comment'].setValue(newValue);
    }

    addComment() {
      if (this.commentForm.valid) {
        console.log(this.commentForm.controls['comment'].value);
        this.commentForm.reset();
      }
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