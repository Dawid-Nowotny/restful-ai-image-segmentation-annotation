import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ImageGalleryComponent } from '../image-gallery/image-gallery.component';

@Component({
    selector: 'app-main-page',
    standalone: true,
    imports: [CommonModule, ImageGalleryComponent],
    templateUrl: './main-page.component.html',
    styleUrls: ['./main-page.component.css']
})
export class MainPageComponent {
    
    constructor() {}
}
