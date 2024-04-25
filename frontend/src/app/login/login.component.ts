import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';
import { HttpErrorResponse } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  username: string;
  password: string;
  errorMessage: string;
  successMessage: string;

  constructor(private serverService: ServerService, private router: Router) {
    this.username = '';
    this.password = '';
    this.errorMessage = '';
    this.successMessage = '';
  }

  onSubmit() {
    if (!this.username || !this.password) {
      this.errorMessage = 'Wprowadź nazwę użytkownika lub email i hasło!';
      return;
    } 

    const data = {
      Username: this.username,
      Password: this.password
    };
  
    this.serverService.postLogin(data).subscribe(
      (response: any) => {
        if (response.success == true) {
          this.successMessage = 'Zalogowano!';
          this.errorMessage = '';
          this.router.navigate(['/']);
        } else {
          this.errorMessage = 'Podano błędną nazwę użytkownika, email lub hasło!';
        }
      },
      (error: HttpErrorResponse) => {
        if (error.error instanceof ErrorEvent) {
          this.errorMessage = 'Wystąpił błąd po stronie klienta!';
        } else {
          this.errorMessage = 'Wystąpił błąd po stronie serwera!';
        }
      }
    );
  }
}
