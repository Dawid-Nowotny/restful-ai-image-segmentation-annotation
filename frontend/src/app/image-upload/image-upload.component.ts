import { Component } from '@angular/core';
import { FormGroup, Validators, FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { UploadImageData } from '../models/upload-image-data.model';
import { CommonModule } from '@angular/common';
import { ServerService } from '../server.service';


@Component({
    selector: 'app-image-upload',
    standalone: true,
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
    ],
    templateUrl: './image-upload.component.html',
    styleUrl: './image-upload.component.css'
})
export class ImageUploadComponent {
    title = 'Image Upload';

    submitted = false;

    form: any;
    uploadImageData = new UploadImageData();


    constructor(private formBuilder: FormBuilder, private serverService: ServerService) { }

    ngOnInit() {
        this.creatForm();
    }

    creatForm() {
        this.form = this.formBuilder.group({
            image: [null, Validators.required],
            iou_threshold: [this.uploadImageData.iou_treshold, Validators.required],
        })
    }

    get f() {
        return this.form.controls;
    }

    uploadImage(event: any) {
        this.uploadImageData.file = event.target.files[0];
    }

    handleThresholdChange(event: any) {
        this.uploadImageData.iou_treshold = event.target.value
    }

    onSubmit() {
        this.submitted = true;
        if (this.form.invalid) {
            return
        }

        const formData = new FormData();
        formData.append("file", this.uploadImageData.file);
        formData.append("uploader_id", this.uploadImageData.uploader.toString());
        formData.append("moderator_id", "");
        formData.append("iou_threshold", this.uploadImageData.iou_treshold.toString());

        this.serverService.postImage(formData).subscribe(res => {
            if (res.status = true) {
                console.log("Upload successful");
                // this.toastr.success(JSON.stringify(this.data.message), '', {
                //     timeOut: 2000,
                //     progressBar: true
                // })
            }
            else {
                console.log("upload failed");
                // this.toastr.error(JSON.stringify(this.data.message), '', {
                //     timeOut: 2000,
                //     progressBar: true
                // })
            }
            this.submitted = false;
            //this.form.get('image').reset();
        })
    }
}
