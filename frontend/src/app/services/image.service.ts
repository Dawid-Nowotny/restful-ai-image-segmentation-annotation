import { Injectable } from '@angular/core';
import JSZip from 'jszip';

export type ImageFileData = {
    id: string,
    extension: string,
    url: string,
    file: File
}

@Injectable({
    providedIn: 'root'
})
export class ImageService {

    constructor() { }

    getImagesArrayFromZip(zipBlob: Blob) {
        const jsZipService = new JSZip();
        let imagesArray: ImageFileData[] = [];

        jsZipService.loadAsync(zipBlob).then((zip) => {

            zip.forEach(async (relativePath, file) => {
                let imageBlob = await file.async('blob');
                let imageURL = URL.createObjectURL(imageBlob)
                let imageExtension = this.getExtension(file.name);
                let imageFile = new File([imageBlob], file.name, { type: `image/${imageExtension}` });

                imagesArray.push({
                    id: this.getId(file.name),
                    extension: this.getExtension(file.name),
                    url: imageURL,
                    file: imageFile,
                });
            })
        })

        return imagesArray;
    }

    getId(fileName: string){
        return fileName.split('.')[0];
    }

    getExtension(fileName: string){
        return fileName.split('.')[1];
    }
}
