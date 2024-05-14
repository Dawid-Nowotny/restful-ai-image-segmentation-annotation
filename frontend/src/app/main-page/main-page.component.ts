import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { ServerService } from '../server.service';
import { HttpErrorResponse } from '@angular/common/http';
import JSZip from 'jszip';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-main-page',
    standalone: true,
    imports: [CommonModule, RouterLink, RouterLinkActive, RouterOutlet],
    templateUrl: './main-page.component.html',
    styleUrl: './main-page.component.css'
})
export class MainPageComponent {

    imagesArray: any[];
    constructor(private serverService: ServerService){ 
        this.imagesArray = [];
    }

    getImages(){
        const jsZipService = new JSZip();

        this.serverService.getImagesAsZip(30, 40).subscribe({
            next: async (response: any) => {
                let blob = new Blob([response], { type: 'application/zip' });

                jsZipService.loadAsync(blob).then(async(zip) => {
                    zip.forEach(async (relativePath, file) => {
                        let imageBlob = await file.async('blob');
                        let imageURL = URL.createObjectURL(imageBlob)
                        let imageFile = new File([imageBlob], file.name, { type: 'image/jpeg' });

                        this.imagesArray.push({
                            name: file.name,
                            url: imageURL,
                            file: imageFile,
                        });
                    })
                })
                
            },
            error: (error: HttpErrorResponse) => {
                console.log(error);
            }
        })
    }

}
