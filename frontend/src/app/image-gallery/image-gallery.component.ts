import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { PageChangedEvent, PaginationModule } from 'ngx-bootstrap/pagination';
import { ImageFileData, ImageService } from '../services/image.service';
import { ServerService } from '../services/server.service';
import { TooltipModule } from 'ngx-bootstrap/tooltip';

type FilterData = {
	thresholdFrom: number,
	thresholdTo: number,
	tags: string[],
	classes: string[],
}

@Component({
	selector: 'app-image-gallery',
	standalone: true,
	imports: [CommonModule, FormsModule, PaginationModule, TooltipModule],
	templateUrl: './image-gallery.component.html',
	styleUrl: './image-gallery.component.css'
})
export class ImageGalleryComponent implements OnInit {

	numberOfImages: number = 0;
	imagesArray: ImageFileData[] = [];
	itemsPerPage: number = 9;
	useFilters: boolean = false;
	filterTagsInput: string = '';
	filterClassesInput: string = '';
	filterData: FilterData = {
		thresholdFrom: 0.1,
		thresholdTo: 1.0,
		tags: [],
		classes: []
	}
	@Input() baseUrlToImageDetails: string = "";
	errorMessage: string = "";

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

	getFilteredImages(startId: number, endId: number, thresholdFrom: number, thresholdTo: number, tags: string[], classes: string[]) {
		this.serverService.getFilteredImagesAsZip(
			startId, endId,
			thresholdFrom,
			thresholdTo,
			tags,
			classes
		).subscribe({
			next: (response: any) => {
				const blob = new Blob([response], { type: 'application/zip' });
				this.imagesArray = this.imageService.getImagesArrayFromZip(blob);
			},
			error: (error: HttpErrorResponse) => {
				switch(error.status) {
					case 400:
						this.errorMessage = "Wartości zakresu muszą mieścić się w przedziale od 0.01 do 1"; break;
					case 404:
						this.errorMessage = "Nie znaleziono obrazów spełniających podane kryteria filtrowania."; break;
				}
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

	applyFilters() {
		this.resetMessages();

		this.useFilters = true;
		this.imagesArray = [];
		this.filterData.tags = this.filterTagsInput.trim().replaceAll(' ', '').split(',').filter(tag => tag !== '');
		this.filterData.classes = this.filterClassesInput.trim().replaceAll(' ', '').split(',').filter(tag => tag !== '');
		this.getFilteredImages(
			0, 100,
			this.filterData.thresholdFrom,
			this.filterData.thresholdTo,
			this.filterData.tags,
			this.filterData.classes
		);
	}

	handlePageChange(event: PageChangedEvent) {
		let currentPage = event.page;

		if (!this.useFilters) {
			this.getImages(currentPage * 10 - 10, currentPage * 10 - 1);
		}
	}

	navigateToImageDetails(routeParam: string) {
		this.router.navigate([`${this.baseUrlToImageDetails}/`, routeParam]);
	}

	resetMessages() {
		this.errorMessage = "";
	}

	cleanFilters() {
		this.resetMessages();
		this.useFilters = false;
		this.getImages(0, 9);
		this.filterTagsInput = '';
		this.filterClassesInput = '';
		this.filterData = {
			thresholdFrom: 0.1,
			thresholdTo: 1.0,
			tags: [],
			classes: []
		}
	}

	filterOnInput(event: any, inputValue: string) {
		const input = event.target as HTMLInputElement;
		input.value = input.value.replace(/[^a-zA-Z0-9,]/g, '');
		inputValue = input.value;
	}

}
