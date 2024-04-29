import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { MainPageComponent } from './main-page/main-page.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { ImageViewComponent } from './image-view/image-view.component';

export const routes: Routes = [
    { path: '', component: MainPageComponent },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },
    { path: 'image-view/:id', component: ImageViewComponent },
    { path: '**', pathMatch: 'full', 
        component: NotFoundComponent },
  ];