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

	getJWTToken(): string {
		return this.localStorageService.getItem('JWTToken') ?? "";
	}

	getId(): number {
		return parseInt(this.localStorageService.getItem('id') ?? "1-");
	}

	getUsername(): string {
		return this.localStorageService.getItem('username') ?? "";
	}

	getEmail(): string {
		return this.localStorageService.getItem('email') ?? "";
	}

	getRole(): string {
		return this.localStorageService.getItem('role') ?? "";
	}

	isTotpEnabled(): boolean | null {
		let isTotpEnabledAsString = this.localStorageService.getItem('totp_enabled');

		if(isTotpEnabledAsString == null) {
			return null;
		}

		return Boolean(isTotpEnabledAsString);
	}

	clearLoggedUserData(): void {
		this.localStorageService.clear();
	}
}
