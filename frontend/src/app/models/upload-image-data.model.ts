export class UploadImageData {
    file: any;
    uploaderId: Number;
    threshold: Number;

    constructor(uploaderId: number) {
        this.uploaderId = uploaderId;
        this.threshold = 0.5;
    }
}
