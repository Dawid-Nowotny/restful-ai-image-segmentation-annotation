import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { LoggedUserService } from '../services/logged-user.service';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {
    username: string;
    password: string;
    errorMessage: string;
    successMessage: string;

    constructor(private serverService: ServerService, private router: Router, private loggedUserService: LoggedUserService) {
        this.username = '';
        this.password = '';
        this.errorMessage = '';
        this.successMessage = '';
    }

    onSubmit() {
        if (!this.username || !this.password) {
            this.errorMessage = 'Wprowadź nazwę użytkownika lub email i hasło!';
            return;
        }

        const data = {
            username: this.username,
            password: this.password
        };

        this.serverService.postLogin(data).subscribe(
            {
                next: (loginResponse: any) => {
                    this.serverService.getLoggedUserCredentials(loginResponse.access_token).subscribe(
                        {
                            next: (userDataResponse: any) => {
                                this.loggedUserService.saveLoggedUserData({
                                    JWTToken: loginResponse.access_token,
                                    id: userDataResponse.id,
                                    username: userDataResponse.username,
                                    email: userDataResponse.email,
                                    role: userDataResponse.role,
                                    totp_enabled: userDataResponse.totp_enabled,
                                });

                                this.successMessage = 'Zalogowano!';
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
}
