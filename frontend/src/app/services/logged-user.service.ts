import { Inject, Injectable } from '@angular/core';
import { LocalStorageService } from './local-storage.service';

type LoggedUserData = {
	JWTToken: string,
	id: number,
	username: string,
	email: string,
	role: string
	totp_enabled: boolean
}

@Injectable({
	providedIn: 'root'
})
export class LoggedUserService {

	constructor(private localStorageService: LocalStorageService) { }

	saveLoggedUserData(LoggedUserData: LoggedUserData): void {
		this.localStorageService.setItem('JWTToken', LoggedUserData.JWTToken);
		this.localStorageService.setItem('id', LoggedUserData.id.toString());
		this.localStorageService.setItem('username', LoggedUserData.username);
		this.localStorageService.setItem('email', LoggedUserData.email);
		this.localStorageService.setItem('role', LoggedUserData.role);
		this.localStorageService.setItem('totp_enabled', LoggedUserData.totp_enabled.toString());
	}

	clearLoggedUserData(): void {
		this.localStorageService.clear();
	}
}
