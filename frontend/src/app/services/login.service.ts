import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { LoggedUserService } from './logged-user.service';
import { ServerService } from './server.service';

@Injectable({
    providedIn: 'root'
})
export class LoginService {

    successMessage: string;
    errorMessage: string;

    constructor(private serverService: ServerService, private router: Router, private loggedUserService: LoggedUserService) {
        this.successMessage = '';
        this.errorMessage = '';
    }

    handleVeryfication(verificationCode: string) {
		const data = {
			verificationCode: verificationCode,
		}
        console.log()
		this.serverService.verifyTOTP(data).subscribe({
			next: (response: any) => {
				this.getLoggedUserDetails();
			},
			error: (error: HttpErrorResponse) => {
                this.errorMessage = error.error.detail;
				console.log(error);
			}
		})
	}

    getLoggedUserDetails(){
        this.serverService.getLoggedUserCredentials().subscribe(
            {
                next: (userDataResponse: any) => {
                    this.loggedUserService.saveLoggedUserData({
                        id: userDataResponse.id,
                        username: userDataResponse.username,
                        email: userDataResponse.email,
                        role: userDataResponse.role,
                        totp_enabled: userDataResponse.totp_enabled,
                    });

                    this.successMessage = 'Zalogowano!';
                    this.errorMessage = '';
                    this.redirectBasedOnRole(userDataResponse.role);
                },
                error: (error: HttpErrorResponse) => {
                    this.errorMessage = error.error.detail;
                }
            }
        )
    }

    redirectBasedOnRole(role: string): void {
        if (role === 'Admin') {
            this.router.navigate(['/admin']);
        } else if (role === 'User') {
            this.router.navigate(['/']);
        } else if (role === 'Moderator') {
            this.router.navigate(['/admin']);
        }
    }

    resetMessages(): void {
        this.successMessage = '';
        this.errorMessage = '';
    }
}
