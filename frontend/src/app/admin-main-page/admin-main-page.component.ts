import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { PaginationModule } from 'ngx-bootstrap/pagination';
import { ImageGalleryComponent } from '../image-gallery/image-gallery.component';

@Component({
	selector: 'app-admin-main-page',
	standalone: true,
	imports: [CommonModule, PaginationModule, ImageGalleryComponent],
	templateUrl: './admin-main-page.component.html',
	styleUrl: './admin-main-page.component.css'
})
export class AdminMainPageComponent{
	
	constructor() { }
}
