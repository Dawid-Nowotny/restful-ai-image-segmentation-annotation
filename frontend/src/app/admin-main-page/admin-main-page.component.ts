import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ImageFileData, ImageService } from '../services/image.service';
import { Router } from '@angular/router';
import { ServerService } from '../services/server.service';

@Component({
	selector: 'app-admin-main-page',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './admin-main-page.component.html',
	styleUrl: './admin-main-page.component.css'
})
export class AdminMainPageComponent implements OnInit {

	imagesArray: ImageFileData[] = [];

	ngOnInit(): void {
		this.getImages();
	}


	constructor(private router: Router, private serverService: ServerService, private imageService: ImageService) { }

	getImages() {
		this.serverService.getImagesAsZip(1, 20).subscribe({
			next: (response: any) => {
				const blob = new Blob([response], { type: 'application/zip' });
				this.imagesArray = this.imageService.getImagesArrayFromZip(blob);
			}
		})
	}

	navigateToImageDetails(image: ImageFileData) {
		this.router.navigate(['admin/image-view/', image.id]); //imageDetails.id
	}



}
