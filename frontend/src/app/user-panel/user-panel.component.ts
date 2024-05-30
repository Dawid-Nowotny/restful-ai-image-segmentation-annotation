import { Component, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServerService } from '../services/server.service';
import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { LoggedUserService } from '../services/logged-user.service';
import { TotpUserPanelModalComponent } from '../totp-user-panel-modal/totp-user-panel-modal.component';
import { ImageFileData, ImageService } from '../services/image.service';


@Component({
  selector: 'app-user-panel',
  standalone: true,
  imports: [CommonModule, TotpUserPanelModalComponent],
  templateUrl: './user-panel.component.html',
  styleUrl: './user-panel.component.css'
})

export class UserPanelComponent {

  currentComponent: string | null = null;
  username: string = "";
  role: string = "";
  image_count: number = 0;
  isAuthorizationEnabled: boolean | null = null;
  isLoggedUser: boolean = false;
  errorMessage: string | undefined;
  @ViewChild(TotpUserPanelModalComponent) totpUserPanelModalModalComponent!: TotpUserPanelModalComponent;
	imagesArray: ImageFileData[] = [];
  baseUrlToImageDetails: string = "image-view";

  constructor(private route: ActivatedRoute,
              private router: Router,
              private serverService: ServerService, 
              private loggedUserService: LoggedUserService,
              private imageService: ImageService) { }

  ngOnInit() {
    const usernameFromRoute = this.route.snapshot.paramMap.get('username');
    const loggedUser = this.loggedUserService.getUsername();
    this.isAuthorizationEnabled = this.loggedUserService.isTotpEnabled();
    
    if(usernameFromRoute)
      this.getImages(usernameFromRoute, 0, 6);

    if (usernameFromRoute === loggedUser) {
      this.isLoggedUser = true;
    }
    this.getProfileInfo(usernameFromRoute);
      
  }


  private getProfileInfo(usernameFromRoute: any) {
    this.serverService.getProfileInfo(usernameFromRoute).subscribe({
      next: (data: any) => {
        this.username = data.username;
        this.role = data.role;
        this.image_count = data.images_count;
        console.log(this.image_count);
      },
      error: (error: HttpErrorResponse) => {
        if (error.status === 0) {
            this.errorMessage = "Wystąpił błąd po stronie serwera.";
        } else {
            this.router.navigate(['/404']);
        }
        }
    })
  }

  openModal(){
    this.totpUserPanelModalModalComponent.openModal();
}

  getImages(username: string, startId: number, endId: number) {
    this.serverService.getUserImages(username, startId, endId).subscribe({
      next: (response: any) => {
        const blob = new Blob([response], { type: 'application/zip' });
        this.imagesArray = this.imageService.getImagesArrayFromZip(blob);
      },
      error: (error: HttpErrorResponse) => {
        console.log(error);
      }
    })
  }

  navigateToImageDetails(routeParam: string) {
		this.router.navigate([`${this.baseUrlToImageDetails}/` , routeParam]);
	}

}
