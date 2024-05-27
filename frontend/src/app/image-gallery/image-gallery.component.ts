import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { PageChangedEvent, PaginationModule } from 'ngx-bootstrap/pagination';
import { ImageFileData, ImageService } from '../services/image.service';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { ServerService } from '../services/server.service';

@Component({
	selector: 'app-image-gallery',
	standalone: true,
	imports: [CommonModule, PaginationModule],
	templateUrl: './image-gallery.component.html',
	styleUrl: './image-gallery.component.css'
})
export class ImageGalleryComponent implements OnInit {

	numberOfImages: number = 0;
	imagesArray: ImageFileData[] = [];
	itemsPerPage: number = 9;
	@Input() baseUrlToImageDetails: string = "";

	ngOnInit(): void {
		this.getImagesNumber();
		this.getImages(0, 9);
	}

	constructor(private router: Router, private serverService: ServerService, private imageService: ImageService) { }

	getImages(startId: number, endId: number) {
		this.serverService.getImagesAsZip(startId, endId).subscribe({
			next: (response: any) => {
				const blob = new Blob([response], { type: 'application/zip' });
				this.imagesArray = this.imageService.getImagesArrayFromZip(blob);
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})
	}

	getImagesNumber() {
		this.serverService.getImagesNumber().subscribe({
			next: (response: any) => {
				this.numberOfImages = response.number_of_images;
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})
	}

	handlePageChange(event: PageChangedEvent) {
		let currentPage = event.page;
		this.getImages(currentPage * 10 - 10, currentPage * 10 - 1);
	}

	navigateToImageDetails(routeParam: string) {
		this.router.navigate([`${this.baseUrlToImageDetails}/` , routeParam]);
	}

}
