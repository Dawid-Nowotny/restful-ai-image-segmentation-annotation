import { Component, OnInit } from '@angular/core';
import { ServerService } from '../services/server.service';
import { CommonModule } from '@angular/common';
import { LoggedUserService } from '../services/logged-user.service';

type UserData = {
	username: string,
	email: string,
	role: string
};

@Component({
	selector: 'app-admin-assign-moderator',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './admin-assign-moderator.component.html',
	styleUrl: './admin-assign-moderator.component.css'
})
export class AdminAssignModeratorComponent implements OnInit{

	userList: UserData[] = [];
	successMessage: string = '';
	errorMessage: string = '';
	

	constructor(private serverService: ServerService, private loggedUserService: LoggedUserService) {}

	ngOnInit(): void {
		this.getUsers();
	}

	getUsers(){
		this.serverService.getUsers().subscribe({
			next: (response) => {
				this.userList = response;
				console.log(this.userList);
			},
			error: (error) => {
				console.log(error);
			}
		})
	}

	assignModeratorRole(username: string){
		this.serverService.assignModeratorRole(this.loggedUserService.getAccessToken(), username).subscribe({
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

	resetMessages(){
		this.successMessage = '';
		this.errorMessage = '';
	}

}
