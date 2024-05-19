import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { LoggedUserService } from '../services/logged-user.service';

@Component({
    selector: 'app-register',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './register.component.html',
    styleUrl: './register.component.css'
})
export class RegisterComponent {
    username: string;
    email: string;
    password: string;
    passwordCheck: string;
    errorMessage: string;
    successMessage: string;
    agreedToTerms: boolean = false;
    userId: string | null = null;

    constructor(private serverService: ServerService, private router: Router, private loggedUserService: LoggedUserService) {
        this.username = '';
        this.email = '';
        this.password = '';
        this.passwordCheck = '';
        this.errorMessage = '';
        this.successMessage = '';
    }

    onSubmit() {
        if (!this.username || !this.email || !this.password || !this.passwordCheck) {
            this.errorMessage = 'Musisz wypełnić wszystkie dane!';
            return;
        } else if (!this.isValidEmail(this.email)) {
            this.errorMessage = 'Podaj poprawny adres email!';
            return;
        } else if (this.password.length < 6) {
            this.errorMessage = 'Hasło musi być dłuższe niż 6 znaków!';
            return;
        } else if (this.password !== this.passwordCheck) {
            this.errorMessage = 'Hasła nie są takie same!';
            return;
        } else if (!this.agreedToTerms) {
            this.errorMessage = 'Musisz zaznaczyć wymagane zgody!';
            return;
        }

        const data = {
            username: this.username,
            email: this.email,
            password: this.password
        };

        this.serverService.postRegister(data).subscribe({
            next: (registerResponse: any) => {

                this.serverService.getLoggedUserCredentials(registerResponse.access_token).subscribe(
                    {
                        next: (userDataResponse: any) => {
                            this.loggedUserService.saveLoggedUserData({
                                JWTToken: registerResponse.access_token,
                                id: userDataResponse.id,
                                username: userDataResponse.username,
                                email: userDataResponse.email,
                                role: userDataResponse.role,
                                totp_enabled: userDataResponse.totp_enabled,
                            });

                            this.successMessage = 'Zarejestrowano!';
                            this.errorMessage = '';
                            this.router.navigate(['/']);
                        },
                        error: (error: HttpErrorResponse) => {
                            this.errorMessage = error.error.detail;
                        }
                    }
                )
            },
            error: (error: HttpErrorResponse) => {
                this.errorMessage = error.error.detail;
            }
        }
        );
    }

    isValidEmail(email: string): boolean {
        const emailRegex: RegExp = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }
}
