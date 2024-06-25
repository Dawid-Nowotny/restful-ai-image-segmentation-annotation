import { Component, EventEmitter, Output } from '@angular/core';
import { ServerService } from '../services/server.service';
import { LoggedUserService } from '../services/logged-user.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
	selector: 'app-profile-edit-modal',
	standalone: true,
	imports: [CommonModule, FormsModule],
	templateUrl: './profile-edit-modal.component.html',
	styleUrl: './profile-edit-modal.component.css'
})
export class ProfileEditModalComponent {
	@Output() closeModalEvent = new EventEmitter<void>();
	isModalOpen: boolean = false;
	modalMessage: string = "";
	username: string = "";
	email: string = "";
	password: string = "";
	old_password: string = "";
	errorMessage: string = "";
	successMessage: string = "";
	userId: string | null = null;

	constructor(private serverService: ServerService, private loggedUserService: LoggedUserService, private router: Router) { }

	ngOnInit() {
		this.username = this.loggedUserService.getUsername();
		this.email = this.loggedUserService.getEmail();
	}

	openModal() {
		this.isModalOpen = true;
	}

	closeModal() {
		this.isModalOpen = false;
		this.closeModalEvent.emit();
	}

	confirm() {
		if (this.validateFields()) {
			if (this.password) {
				this.updateUser({ username: this.username, email: this.email, password: this.password, old_password: this.old_password });
			} else {
				this.updateUser({ username: this.username, email: this.email, old_password: this.old_password });
			}
		}
	}

	private isValidEmail(email: string): boolean {
		const emailRegex: RegExp = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
		return emailRegex.test(email);
	}

	private validateFields(): Boolean {
		if (!this.username || !this.email || !this.old_password) {
			this.errorMessage = 'Pola: username i email nie mogą być puste!';
			return false;
		}
		if (!this.isValidEmail(this.email)) {
			this.errorMessage = 'Podaj poprawny adres email!';
			return false;
		}
		if (this.password && this.password.length < 6) {
			this.errorMessage = 'Hasło musi być dłuższe niż 6 znaków!';
			return false;
		}
		if (this.old_password === this.password) {
			this.errorMessage = 'Hasła nie mogą być takie same!';
			return false;
		}
		return true;
	}

	private updateUser(userDataUpdate: any) {
		this.serverService.updateUser(userDataUpdate).subscribe({
			next: () => {
				this.successMessage = 'Dane zostały zaktualizowane';
				this.errorMessage = "";

				let previousUsername = this.loggedUserService.getLoggedUserData().username;

				let data = this.loggedUserService.getLoggedUserData();
				data.username = userDataUpdate.username;
				data.email = userDataUpdate.email;
				this.loggedUserService.saveLoggedUserData(data);

				console.log(previousUsername);
				console.log(userDataUpdate.username);

				if (this.loggedUserService.getUsername() !== previousUsername)
					this.router.navigate([`user/`, this.loggedUserService.getUsername()]);

			},
			error: (error: HttpErrorResponse) => {
				console.error('Error updating user', error);
				this.errorMessage = 'Wystąpił błąd po stronie serwera';
				this.successMessage = '';
			}
		});
	}
}
