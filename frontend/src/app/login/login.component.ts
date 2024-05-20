import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { LoggedUserService } from '../services/logged-user.service';
import { TotpModalComponent } from '../totp-modal/totp-modal.component';
import { bootstrapApplication } from '@angular/platform-browser';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [CommonModule, FormsModule, TotpModalComponent],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {
    username: string;
    password: string;
    errorMessage: string;
    successMessage: string;
    @ViewChild(TotpModalComponent) totpModalComponent!: TotpModalComponent;


    constructor(private serverService: ServerService, private router: Router, private loggedUserService: LoggedUserService) {
        this.username = '';
        this.password = '';
        this.errorMessage = '';
        this.successMessage = '';
    }

    passUserIn: (JWTToken: string) => void = (JWTToken) => {
        this.serverService.getLoggedUserCredentials(JWTToken).subscribe(
            {
                next: (userDataResponse: any) => {
                    this.loggedUserService.saveLoggedUserData({
                        JWTToken: JWTToken,
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
                    if (loginResponse.totp_enabled == true) {
                        this.totpModalComponent.accessToken = loginResponse.access_token;
                        this.totpModalComponent.handleSuccessfulVerification = this.passUserIn;
                        this.totpModalComponent.openModal();
                    } else {
                        this.passUserIn(loginResponse.access_token);
                    }
                },
                error: (error: HttpErrorResponse) => {
                    this.errorMessage = error.error.detail;
                }
            }
        );
    }
}
