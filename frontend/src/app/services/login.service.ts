import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { LoggedUserService } from './logged-user.service';
import { ServerService } from './server.service';

@Injectable({
    providedIn: 'root'
})
export class LoginService {

    accessToken: string;
    successMessage: string;
    errorMessage: string;

    constructor(private serverService: ServerService, private router: Router, private loggedUserService: LoggedUserService) {
        this.accessToken = "";
        this.successMessage = '';
        this.errorMessage = '';
    }

    handleVeryfication(verificationCode: string) {
		const data = {
			JWTToken: this.accessToken,
			verificationCode: verificationCode,
		}
		this.serverService.verify2FA(data).subscribe({
			next: (response: any) => {
				this.getLoggedUserDetails(this.accessToken);
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})
	}

    getLoggedUserDetails: (JWTToken: string) => void = (JWTToken) => {
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

    saveAccessToken(accessToken: string): void {
        this.accessToken = accessToken;
    }
}
