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

    file: any;
    submitted = false;

    form: any;
    uploadImageData = new UploadImageData();
    data: any;

    constructor(private formBuilder: FormBuilder, private serverService: ServerService) { }

    ngOnInit() {
        this.creatForm();
    }

    creatForm() {
        this.form = this.formBuilder.group({
            image: [null, Validators.required],
            uploader_id: [0, Validators.required],
            iou_treshold: [0.5, Validators.required],
        })
    }

    get f() {
        return this.form.controls;
    }

    uploadImage(event: any) {
        this.file = event.target.files[0];
        console.log(this.file);
    }

    onSubmit() {
        this.submitted = true;
        if (this.form.invalid) {
            return
        }
        
        const formData = new FormData();
        formData.append("file", this.file);
        formData.append("uploader_id", "0");
        formData.append("moderator_id", "0");
        formData.append("iou_threshold", "0.5");

        this.serverService.postImage(formData).subscribe(res => {
            this.data = res;
            console.log(this.data)
            if (this.data.status = true) {
                console.log("Success: " + this.data.message);
                // this.toastr.success(JSON.stringify(this.data.message), '', {
                //     timeOut: 2000,
                //     progressBar: true
                // })
            }
            else {
                console.log("Fail: " + this.data.message);
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
