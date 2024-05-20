import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
	selector: 'app-totp-modal',
	standalone: true,
	imports: [CommonModule, FormsModule],
	templateUrl: './totp-modal.component.html',
	styleUrl: './totp-modal.component.css'
})
export class TotpModalComponent {

	isOpen: boolean;
	accessToken: string;
	verificationCode: string;
	handleSuccessfulVerification: (JWTToken: string) => void;

	constructor(private serverService: ServerService) {
		this.isOpen = false;
		this.accessToken = '';
		this.verificationCode = '';
		this.handleSuccessfulVerification = () => {};
	}

	openModal() {
		this.isOpen = true;
	}

	closeModal() {
		this.isOpen = false;
	}

	handleVeryfication(){
		const data = {
			JWTToken: this.accessToken,
			verificationCode: this.verificationCode,
		}
		this.serverService.verify2FA(data).subscribe({
			next: (response: any) => {
				this.handleSuccessfulVerification(this.accessToken);
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})
	}

}
