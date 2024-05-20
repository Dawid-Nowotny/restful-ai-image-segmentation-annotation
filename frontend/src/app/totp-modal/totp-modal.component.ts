import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { LoginService } from '../services/login.service';

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

	constructor(private serverService: ServerService, private loginService: LoginService) {
		this.isOpen = false;
		this.accessToken = '';
		this.verificationCode = '';
	}

	openModal() {
		this.isOpen = true;
	}

	closeModal() {
		this.isOpen = false;
	}

	onSubmit(){
		this.loginService.handleVeryfication(this.verificationCode)
	}

}
