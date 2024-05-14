import { Component, Inject } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import JSZip from 'jszip';
import { CommonModule } from '@angular/common';
import { ImageFileData, ImageService } from '../services/image.service';

@Component({
    selector: 'app-main-page',
    standalone: true,
    imports: [CommonModule, RouterLink, RouterLinkActive, RouterOutlet],
    templateUrl: './main-page.component.html',
    styleUrl: './main-page.component.css'
})
export class MainPageComponent {

    imagesArray: ImageFileData[];

    constructor(private serverService: ServerService, private imageService: ImageService) {
        this.imagesArray = [];
    }

    ngOnInit() {
        this.getImages();
    }

    getImages() {
        this.serverService.getImagesAsZip(30, 40).subscribe({
            next: async (response: any) => {
                let blob = new Blob([response], { type: 'application/zip' });
                this.imagesArray = this.imageService.getImagesArrayFromZip(blob);
            },
            error: (error: HttpErrorResponse) => {
                console.log(error);
            }
        })
    }
}
