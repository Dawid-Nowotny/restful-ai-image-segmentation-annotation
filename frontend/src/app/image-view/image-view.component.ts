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
    imageUrl: string | ArrayBuffer | null = null;
    
    constructor(private route: ActivatedRoute, private serverService: ServerService) { }

    ngOnInit() {
        this.imageAutor = 'Jan Nowak';
        this.superTagsAutor = 'Adam Nowak';
        this.route.params.subscribe(params => {
            this.image_id = params['id'];
        })

        this.getImage(this.image_id)
    }

    getImage(imageId: number): void {
        this.serverService.getImage(imageId).subscribe(
          (blob: Blob) => {
            const reader = new FileReader();
            reader.onload = () => this.imageUrl = reader.result;
            reader.readAsDataURL(blob);
          },
          error => {
            console.error('Error fetching image:', error);
          }
        );
      }
}
