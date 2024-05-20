import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { LoggedUserService } from '../services/logged-user.service';
import { TotpModalComponent } from '../totp-modal/totp-modal.component';
import { bootstrapApplication } from '@angular/platform-browser';
import { LoginService } from '../services/login.service';

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


    constructor(
        private serverService: ServerService,
        private loginService: LoginService,
    ) {
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
                    if (loginResponse.totp_enabled == true) {
                        this.loginService.saveAccessToken(loginResponse.access_token);
                        this.totpModalComponent.openModal();
                    } else {
                        this.loginService.getLoggedUserDetails(loginResponse.access_token);
                    }
                },
                error: (error: HttpErrorResponse) => {
                    this.errorMessage = error.error.detail;
                }
            }
        );
    }
}
