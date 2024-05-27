import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServerService } from '../services/server.service';
import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { LoggedUserService } from '../services/logged-user.service';


@Component({
  selector: 'app-user-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './user-panel.component.html',
  styleUrl: './user-panel.component.css'
})

export class UserPanelComponent {

  currentComponent: string | null = null;
  username: string = "";
  role: string = "";
  image_count: number = 0;
  isAuthorizationEnabled: boolean | null = this.loggedUserService.isTotpEnabled();
  authorizationButtonMessage: string = "";
  isLoggedUser: boolean = false;
  errorMessage: string | undefined;

  constructor(private route: ActivatedRoute,
              private router: Router,
              private serverService: ServerService, 
              private loggedUserService: LoggedUserService) { }

  ngOnInit() {
    const usernameFromRoute = this.route.snapshot.paramMap.get('username');
    const loggedUser = this.loggedUserService.getUsername();
    console.log(usernameFromRoute);
    console.log(loggedUser);

    if (usernameFromRoute === loggedUser) {
      this.isLoggedUser = true;
      this.authorizationButtonMessage = (this.isAuthorizationEnabled)? "Deaktywuj 2FA" : "Aktywuj 2FA";
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


}
