import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-image-view',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './image-view.component.html',
    styleUrl: './image-view.component.css'
})
export class ImageViewComponent implements OnInit {
    imageAutor: string = '';
    superTagsAutor: string = '';
    
    ngOnInit() {
        this.imageAutor = 'Jan Nowak';
        this.superTagsAutor = 'Adam Nowak';
    }
}
