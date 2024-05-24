import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import JSZip from 'jszip';
import { CommonModule } from '@angular/common';
import { ImageFileData, ImageService } from '../services/image.service';

@Component({
    selector: 'app-main-page',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './main-page.component.html',
    styleUrls: ['./main-page.component.css']
})
export class MainPageComponent {

    imagesArray: ImageFileData[];

    constructor(private router: Router, private serverService: ServerService, private imageService: ImageService) {
        this.imagesArray = [];
    }

    ngOnInit() {
        this.getImages();
    }

    getImages() {
        this.serverService.getImagesAsZip(1, 6).subscribe({
            next: async (response: any) => {
                let blob = new Blob([response], { type: 'application/zip' });
                this.imagesArray = this.imageService.getImagesArrayFromZip(blob);
            },
            error: (error: HttpErrorResponse) => {
                console.log(error);
            }
        })
    }

    navigateToImageView(imageId: number) {
        this.router.navigate(['/image-view', imageId]);
    }
}
