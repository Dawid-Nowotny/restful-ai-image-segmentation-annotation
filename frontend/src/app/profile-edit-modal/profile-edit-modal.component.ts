import { Component, EventEmitter, Output } from '@angular/core';
import { ServerService } from '../services/server.service';
import { LoggedUserService } from '../services/logged-user.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-profile-edit-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './profile-edit-modal.component.html',
  styleUrl: './profile-edit-modal.component.css'
})
export class ProfileEditModalComponent {
  @Output() closeModalEvent = new EventEmitter<void>();
  isModalOpen: boolean = false;
  modalMessage: string = "";
  password: string = "";
  isConfirmButtonDisable: boolean = false;

  constructor(private serverService: ServerService, private loggedUserService: LoggedUserService) { }

  ngOnInit() {
    console.log("xd");
  }

  openModal() {
      this.isModalOpen = true;
  }

  closeModal() {
      this.isModalOpen = false;
      this.closeModalEvent.emit();
  }

  confirm() {
  }

}