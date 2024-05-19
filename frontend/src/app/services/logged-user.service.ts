import { Inject, Injectable } from '@angular/core';
import { LocalStorageService } from './local-storage.service';

type LoggedUserData = {
	JWTToken: string,
	username: string,
	email: string,
	role: string
}

@Injectable({
	providedIn: 'root'
})
export class LoggedUserService {

	constructor(private localStorageService: LocalStorageService) { }

	saveLoggedUserData(LoggedUserData: LoggedUserData): void {
		this.localStorageService.setItem('JWTToken', LoggedUserData.JWTToken);
		this.localStorageService.setItem('username', LoggedUserData.username);
		this.localStorageService.setItem('email', LoggedUserData.email);
		this.localStorageService.setItem('role', LoggedUserData.role);
	}

	clearLoggedUserData(): void {
		this.localStorageService.clear();
	}
}
