import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { MainPageComponent } from './main-page/main-page.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { ImageUploadComponent } from './image-upload/image-upload.component';

export const routes: Routes = [
    { path: '', component: MainPageComponent },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },
    { path: 'image-upload', component: ImageUploadComponent},
    { path: '**', pathMatch: 'full', 
        component: NotFoundComponent },
  ];