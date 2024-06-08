import { Injectable } from '@angular/core';
import { LocalStorageService } from './local-storage.service';
import { ServerService } from './server.service';
import { HttpErrorResponse } from '@angular/common/http';

type LoggedUserData = {
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

	constructor(
		private localStorageService: LocalStorageService,
		private serverService: ServerService
	) { }

	saveLoggedUserData(LoggedUserData: LoggedUserData): void {
		this.localStorageService.setItem('id', LoggedUserData.id.toString());
		this.localStorageService.setItem('username', LoggedUserData.username);
		this.localStorageService.setItem('email', LoggedUserData.email);
		this.localStorageService.setItem('role', LoggedUserData.role);
		this.localStorageService.setItem('totp_enabled', LoggedUserData.totp_enabled.toString());
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

	getLoggedUserData(): LoggedUserData {
		return {
			id: this.getId(),
			username: this.getUsername(),
			email: this.getEmail(),
			role: this.getRole(),
			totp_enabled: this.isTotpEnabled() ?? false
		}
	}

	setUsername(username: string): void {
		this.localStorageService.setItem('username', username);
	}

	setEmail(email: string): void {
		this.localStorageService.setItem('email', email);
	}

	isTotpEnabled(): boolean | null {
		let isTotpEnabledAsString = this.localStorageService.getItem('totp_enabled');

		if(isTotpEnabledAsString == null) {
			return null;
		}

		return isTotpEnabledAsString === 'true';
	}

	clearLoggedUserData(): void {
		this.localStorageService.clear();
	}

	logOut(): void {
		this.clearLoggedUserData();

		this.serverService.postLogout().subscribe({
			next: (response: any) => {
				console.log("logged out");	
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})

	}
}
