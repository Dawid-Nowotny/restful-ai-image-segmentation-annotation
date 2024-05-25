import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ServerService } from '../services/server.service';
import { CommonModule } from '@angular/common';


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
  isAuthorizationEnabled: boolean = false;
  authorizationButtonMessage = (this.isAuthorizationEnabled)? "Deaktywuj 2FA" : "Aktywuj 2FA";
  isLoggedUser: boolean = false;

  constructor(private route: ActivatedRoute, private serverService: ServerService) { }

  ngOnInit(): void {
    this.serverService.getProfileInfo("radek").subscribe(data => {
      this.username = data.username;
      this.role = data.role;
      this.image_count = data.images_count;
    })

  }



}
