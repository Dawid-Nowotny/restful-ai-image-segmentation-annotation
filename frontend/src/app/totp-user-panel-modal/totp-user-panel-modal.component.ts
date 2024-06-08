import { Component, Output, EventEmitter } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { LoggedUserService } from '../services/logged-user.service';
import { ServerService } from '../services/server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-totp-user-panel-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './totp-user-panel-modal.component.html',
  styleUrls: ['./totp-user-panel-modal.component.css']
})
export class TotpUserPanelModalComponent {
    @Output() closeModalEvent = new EventEmitter<void>();
    isModalOpen: boolean = false;
    imageUrl: SafeUrl | null = null;
    modalMessage: string = "";
    password: string = "";
    isConfirmButtonDisable: boolean = false;
    isAuthorizationEnabled: boolean | null = null;

    constructor(private serverService: ServerService, private loggedUserService: LoggedUserService, private sanitizer: DomSanitizer) { }

    ngOnInit() {
        this.isAuthorizationEnabled = this.loggedUserService.isTotpEnabled();
    }

    openModal() {
        this.isModalOpen = true;
        if(this.loggedUserService.isTotpEnabled())
            this.modalMessage = "Uwierzytelnianie dwuskładnikowe jest aktywne. Czy chcesz je wyłączyć?";
        else {
            this.modalMessage = "Czy na pewno chcesz aktywować uwierzytelnianie dwuskładnikowe?";
        }
    }

    closeModal() {
        this.isModalOpen = false;
        this.closeModalEvent.emit();
    }

    confirm() {
        if(this.loggedUserService.isTotpEnabled())
            this.disable2FA(this.password);
        else 
            this.enable2FA();
    }

    private enable2FA() {
        const accessToken = this.loggedUserService.getAccessToken();
        
        this.serverService.generateQrCode().subscribe({
            next: (response: Blob) => {
                const objectURL = URL.createObjectURL(response);
                this.imageUrl = this.sanitizer.bypassSecurityTrustUrl(objectURL);
                this.modalMessage = "Uwierzytelnianie dwuskładnikowe zostało aktywowane. Zeskanuj kod QR w aplikacji Google Authenticator.";
                localStorage.setItem('totp_enabled', 'true');
                this.isConfirmButtonDisable = true;
            },
            error: (error: HttpErrorResponse) => {
                console.error('Error fetching QR code', error);
                this.modalMessage = "Token wygasł. Spróbuj ponownie po jakims czasie.";
            }
        });
    }

    private disable2FA(password: string) {
        const accessToken = this.loggedUserService.getAccessToken();
        
        this.serverService.disableTOTP(password).subscribe({
            next: (response: any) => {
                console.log('2FA disabled', response);
                this.isAuthorizationEnabled = false;
                localStorage.setItem('totp_enabled', 'false');
                this.closeModal();
            },
            error: (error: HttpErrorResponse) => {
                console.error('Error disabling 2FA', error);
                this.modalMessage = "Niepoprawne hasło."
            }
        });
    }
}
