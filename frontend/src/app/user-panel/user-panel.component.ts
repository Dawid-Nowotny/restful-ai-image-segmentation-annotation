import { Component } from '@angular/core';

@Component({
  selector: 'app-user-panel',
  standalone: true,
  imports: [],
  templateUrl: './user-panel.component.html',
  styleUrl: './user-panel.component.css'
})
export class UserPanelComponent {

  username = "Ardon";
  role = "użytkownik";
  opis = "jakiś opis";
  image_count = "33";

}
