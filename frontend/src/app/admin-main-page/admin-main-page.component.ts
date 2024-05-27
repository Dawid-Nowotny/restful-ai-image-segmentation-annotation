import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ImageFileData, ImageService } from '../services/image.service';
import { Router } from '@angular/router';
import { ServerService } from '../services/server.service';
import { PageChangedEvent, PaginationModule} from 'ngx-bootstrap/pagination'
import { HttpErrorResponse } from '@angular/common/http';

@Component({
	selector: 'app-admin-main-page',
	standalone: true,
	imports: [CommonModule, PaginationModule],
	templateUrl: './admin-main-page.component.html',
	styleUrl: './admin-main-page.component.css'
})
export class AdminMainPageComponent implements OnInit {

	numberOfImages: number = 0;
	imagesArray: ImageFileData[] = [];
	
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

	getImagesNumber(){
		this.serverService.getImagesNumber().subscribe({
			next: (response: any) => {
				this.numberOfImages = response.number_of_images;
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})
	}

	navigateToImageDetails(image: ImageFileData) {
		this.router.navigate(['admin/image-view/', image.id]); //imageDetails.id
	}

	handlePageChange(event: PageChangedEvent) {

		let currentPage = event.page;
		this.getImages(currentPage * 10 - 10, currentPage * 10 - 1);
	}

}
