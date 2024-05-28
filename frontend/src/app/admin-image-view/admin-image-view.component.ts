import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { LoggedUserService } from '../services/logged-user.service';
import { TabDirective, TabsModule } from 'ngx-bootstrap/tabs';

@Component({
	selector: 'app-admin-image-view',
	standalone: true,
	imports: [CommonModule, TabsModule],
	templateUrl: './admin-image-view.component.html',
	styleUrls: ['./admin-image-view.component.css']
})
export class AdminImageViewComponent implements OnInit {
	id: number;
	image: Blob;
	imageUrl: string;
	moderatorList: string[];
	selectedModerator: string;
	currentModerator: string;
	imageSuperTags: {
		author: string;
		superTags: string[];
	}
	successMessage: string;
	errorMessage: string;

	ngOnInit(): void {
		this.id = parseInt(this.route.snapshot.paramMap.get('id') ?? "-1");

		this.fetchImage();
		this.getImageModerator();
		this.getModeratorsList();
	}

	constructor(
		private route: ActivatedRoute, 
		private serverService: ServerService, 
		private loggedUserService: LoggedUserService
	) {
		this.id = -1;
		this.moderatorList = [];
		this.selectedModerator = '';
		this.currentModerator = '';
		this.image = new Blob();
		this.imageUrl = '';
		this.imageSuperTags = {
			author: '',
			superTags: []
		};
		this.successMessage = '';
		this.errorMessage = '';
	}

	fetchImage(){
		this.serverService.getImage(this.id).subscribe({
			next: (response: any) => {
				this.image = response;
				this.imageUrl = URL.createObjectURL(this.image);
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})
	}

	getModeratorsList(){
		this.serverService.getModerators().subscribe({
			next: (response: any) => {
				this.moderatorList = response.map((moderator: any) => moderator.username);
				this.selectedModerator = this.moderatorList[0];
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})
	}

	getImageModerator() {
		this.serverService.getImageModerator(this.id).subscribe({
			next: (response: any) => {
				this.currentModerator = response.username;
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})
	}

	getImageSuperTags(imageId: number) {
		this.serverService.getImageSuperTags(imageId).subscribe({
			next: (response: any) => {
				this.imageSuperTags.author = response.author;
				this.imageSuperTags.superTags = response.tags.map((tag: any) => tag.tag);
				console.log(response);
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})
	}

	handleModeratorSelect(event: Event) {
		this.resetMessages();
		const selectElement = event.target as HTMLSelectElement;
		this.selectedModerator = selectElement.value;
	}

	handleTabChange(data: TabDirective) {
		this.getImageSuperTags(this.id);
	}

	assignModerator() {
		this.resetMessages();
		let accessToken = this.loggedUserService.getAccessToken();

		this.serverService.assignModeratorToImage(accessToken, this.id, this.selectedModerator).subscribe({
			next: (response: any) => {
				this.successMessage = response.message;
				this.getImageModerator();
			},
			error: (error: HttpErrorResponse) => {
				this.errorMessage = error.error.message;
			}
		})
	}

	resetMessages(){
		this.successMessage = "";
		this.errorMessage = "";
	}
}
