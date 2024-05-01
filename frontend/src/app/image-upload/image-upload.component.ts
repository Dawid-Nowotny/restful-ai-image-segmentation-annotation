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
            threshold: [this.uploadImageData.threshold, Validators.required],
        })
    }

    get f() {
        return this.form.controls;
    }

    uploadImage(event: any) {
        this.uploadImageData.file = event.target.files[0];
    }

    handleThresholdChange(event: any) {
        this.uploadImageData.threshold = event.target.value
    }

    onSubmit() {
        this.submitted = true;
        this.successMessage = "";
        this.errorMessage = "";

        if (this.form.invalid) {
            return
        }

        this.submitDisabled = true;

        const formData = new FormData();
        formData.append("file", this.uploadImageData.file);
        formData.append("uploader_id", this.uploadImageData.uploaderId.toString());
        formData.append("moderator_id", "");
        formData.append("threshold", this.uploadImageData.threshold.toString());

        this.serverService.postImage(formData).subscribe(
            {
                next: (response: any) => {
                    this.successMessage = "Zdjęcie zostało dodane!";
                    this.submitted = false;
                    this.submitDisabled = false;
                },
                error: (error: HttpErrorResponse) => {
                    if (error.status === 0) {
                        this.errorMessage = "Wystąpił błąd po stronie serwera.";
                    } else {
                        this.errorMessage = error.error.detail;
                    }

                    this.submitted = false;
                    this.submitDisabled = false;
                }
            }
        )

    }
}
