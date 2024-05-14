import { Injectable } from '@angular/core';
import JSZip from 'jszip';

export type ImageFileData = {
    name: string,
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

        jsZipService.loadAsync(zipBlob).then(async (zip) => {

            zip.forEach(async (relativePath, file) => {
                let imageBlob = await file.async('blob');
                let imageURL = URL.createObjectURL(imageBlob)
                let imageExtension = this.getExtensionFromName(file.name);
                let imageFile = new File([imageBlob], file.name, { type: `image/${imageExtension}` });

                imagesArray.push({
                    name: file.name,
                    url: imageURL,
                    file: imageFile,
                });
            })
        })

        return imagesArray;
    }

    getExtensionFromName(name: string){
        return name.split('.').pop();
    }
}
