import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

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

    constructor(private serverService: ServerService, private router: Router) {
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
            Username: this.username,
            Email: this.email,
            Password: this.password
        };

        this.serverService.postRegister(data).subscribe(
            (response: any) => {
                if (response.success == true) {
                    this.successMessage = 'Zarejestrowano!';
                    this.errorMessage = '';
                    this.router.navigate(['/']);
                } else {
                    this.errorMessage = response.message;
                }
            },
            (error: HttpErrorResponse) => {
                if (error.error instanceof ErrorEvent) {
                    this.errorMessage = 'Wystąpił błąd po stronie klienta!';
                } else {
                    this.errorMessage = 'Wystąpił błąd po stronie serwera!';
                }
            }
        );
    }

    isValidEmail(email: string): boolean {
        const emailRegex: RegExp = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }
}
