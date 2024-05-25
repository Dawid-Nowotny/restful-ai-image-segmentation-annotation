import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
	selector: 'app-admin-image-view',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './admin-image-view.component.html',
	styleUrls: ['./admin-image-view.component.css']
})
export class AdminImageViewComponent implements OnInit {
	moderatorList: string[] = ['test1', 'test2', 'test3'];
	selectedModerator: string = this.moderatorList[0];

	ngOnInit(): void {
		this.serverService.getModerators().subscribe({
			next: (response: any) => {
				this.moderatorList = response.map((moderator: any) => moderator.username);
			},
			error: (error: HttpErrorResponse) => {
				console.log(error);
			}
		})
	}

	constructor(private serverService: ServerService) { }

	handleModeratorSelect(event: Event) {
		const selectElement = event.target as HTMLSelectElement;
		this.selectedModerator = selectElement.value;
	}

	assignModerator() {
		console.log(this.selectedModerator);
	}
}
