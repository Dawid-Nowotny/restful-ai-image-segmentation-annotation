import { Component, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { ImageFileData, ImageService } from '../services/image.service';
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
