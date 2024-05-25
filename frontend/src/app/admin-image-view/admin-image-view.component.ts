import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

@Component({
	selector: 'app-admin-image-view',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './admin-image-view.component.html',
	styleUrls: ['./admin-image-view.component.css']
})
export class AdminImageViewComponent implements OnInit {
	id: number;
	image: Blob;
	imageUrl: string;
	moderatorList: string[];
	selectedModerator: string;

	ngOnInit(): void {
		this.id = parseInt(this.route.snapshot.paramMap.get('id') ?? "-1");

		this.fetchImage();
		this.getModeratorsList();
	}

	constructor(private route: ActivatedRoute, private serverService: ServerService) { 
		this.id = -1;
		this.moderatorList = [];
		this.selectedModerator = '';
		this.image = new Blob();
		this.imageUrl = '';
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

	handleModeratorSelect(event: Event) {
		const selectElement = event.target as HTMLSelectElement;
		this.selectedModerator = selectElement.value;
	}

	assignModerator() {
		console.log(this.selectedModerator);
	}
}
