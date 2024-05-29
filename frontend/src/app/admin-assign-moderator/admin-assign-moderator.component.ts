import { Component, OnInit } from '@angular/core';
import { ServerService } from '../services/server.service';
import { CommonModule } from '@angular/common';

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
	constructor(private serverService: ServerService) {}

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

}
