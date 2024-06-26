import { Component, OnInit } from '@angular/core';
import { ServerService } from '../services/server.service';
import { CommonModule } from '@angular/common';
import { LoggedUserService } from '../services/logged-user.service';
import { TabsModule } from 'ngx-bootstrap/tabs';

type UserData = {
	username: string,
	email: string,
	role: string
};

@Component({
	selector: 'app-admin-make-moderator',
	standalone: true,
	imports: [CommonModule, TabsModule],
	templateUrl: './admin-make-moderator.component.html',
	styleUrl: './admin-make-moderator.component.css'
})
export class AdminMakeModeratorComponent implements OnInit{

	userList: UserData[] = [];
	moderatorList: UserData[] = [];
	successMessage: string = '';
	errorMessage: string = '';
	

	constructor(private serverService: ServerService) {}

	ngOnInit(): void {
		this.getUsers();
		this.getModerators();
	}

	getUsers(){
		this.serverService.getUsers().subscribe({
			next: (response) => {
				this.userList = response;
			},
			error: (error) => {
				console.log(error);
			}
		})
	}

	getModerators(){
		this.serverService.getModerators().subscribe({
			next: (response: any) => {
				this.moderatorList = response;
			},
			error: (error) => {
				console.log(error);
			}
		})
	}

	assignModeratorRole(username: string){
		this.serverService.assignModeratorRole(username).subscribe({
			next: (response: any) => {
				this.getUsers();
				this.successMessage = response.message + ` (${username})`;
			},
			error: (error) => {
				this.errorMessage = error.error.detail;
				console.log(error);
			}
		})
	}

	removeModeratorRole(username: string){
		this.serverService.removeModeratorRole(username).subscribe({
			next: (response: any) => {
				this.getModerators();
				this.successMessage = response.message + ` (${username})`;
			},
			error: (error) => {
				this.errorMessage = error.error.detail;
				console.log(error);
			}
		})
	}

	handleSelectUserTab(event: any){
		this.resetMessages();
		this.getUsers();
	}

	handleSelectModeratorTab(event:any){
		this.resetMessages();
		this.getModerators();
	}

	resetMessages(){
		this.successMessage = '';
		this.errorMessage = '';
	}

}
