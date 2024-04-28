import { Component } from '@angular/core';
import { Validators, FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { UploadImageData } from '../models/upload-image-data.model';
import { CommonModule } from '@angular/common';
import { ServerService } from '../server.service';
import { HttpErrorResponse } from '@angular/common/http';


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

    submitted: boolean;
    submitDisabled: boolean;
    form: any;
    uploadImageData: UploadImageData;
    successMessage: string;
    errorMessage: string;

    constructor(private formBuilder: FormBuilder, private serverService: ServerService) {
        this.submitted = false;
        this.submitDisabled = false;
        this.uploadImageData = new UploadImageData();
        this.successMessage = '';
        this.errorMessage = '';

    }

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
        this.submitDisabled = true;
        this.successMessage = "";
        this.errorMessage = "";

        if (this.form.invalid) {
            return
        }

        const formData = new FormData();
        formData.append("file", this.uploadImageData.file);
        formData.append("uploader_id", this.uploadImageData.uploader.toString());
        formData.append("moderator_id", "");
        formData.append("iou_threshold", this.uploadImageData.iou_treshold.toString());

        this.serverService.postImage(formData).subscribe(
            {
                next: (response: any) => {
                    this.successMessage = "File uploaded successfully!";
                    this.submitted = false;
                    this.submitDisabled = false;
                },
                error: (error: HttpErrorResponse) => {
                    this.errorMessage = error.error.detail;
                    this.submitted = false;
                    this.submitDisabled = false;
                }
            }
        )

    }
}
