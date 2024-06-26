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
	verificationCode: string;

	constructor(public loginService: LoginService) {
		this.isOpen = false;
		this.verificationCode = '';
	}

	openModal() {
		this.isOpen = true;
	}

	closeModal() {
		this.isOpen = false;
		this.verificationCode = '';
		this.loginService.resetMessages();
	}

	onSubmit(){
		this.loginService.handleVeryfication(this.verificationCode)
	}

}
