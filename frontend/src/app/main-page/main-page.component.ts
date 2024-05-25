import { Component, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
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

    imagesArray: ImageFileData[] = [];
    currentPage: number = 1;
    itemsPerPage: number = 6;
    imagesLoaded: boolean = false;

    constructor(private router: Router, 
                private serverService: ServerService, 
                private imageService: ImageService,
                private cdRef: ChangeDetectorRef) {}

    ngOnInit() {
        this.getImages(this.currentPage);
    }  

    getImages(page: number) {
        this.imagesLoaded = false;
        const startImageIndex = (page - 1) * this.itemsPerPage + 1;
        const endImageIndex = startImageIndex + this.itemsPerPage - 1;
        this.serverService.getImagesAsZip(startImageIndex, endImageIndex).subscribe({
            next: (response: ArrayBuffer) => {
                const blob = new Blob([response], { type: 'application/zip' });
                this.imagesArray = this.imageService.getImagesArrayFromZip(blob);
                console.log('Images for page', page, ':', this.imagesArray);
                this.imagesLoaded = true;
                this.cdRef.detectChanges();
            },
            error: (error: HttpErrorResponse) => {
                console.error(error);
            }
        });
    }
    
    navigateToImageView(index: number) {
        const adjustedIndex = (this.currentPage - 1) * this.itemsPerPage + index;
        this.router.navigate(['/image-view', adjustedIndex]);
    }

    nextPage() {
        this.currentPage++;
        this.getImages(this.currentPage);
    }

    prevPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.getImages(this.currentPage);
        }
    }
}
