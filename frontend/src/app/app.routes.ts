import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { MainPageComponent } from './main-page/main-page.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { ImageViewComponent } from './image-view/image-view.component';
import { ImageUploadComponent } from './image-upload/image-upload.component';
import { UserPanelComponent } from './user-panel/user-panel.component';
import { AdminMainPageComponent } from './admin-main-page/admin-main-page.component';
import { AdminImageViewComponent } from './admin-image-view/admin-image-view.component';
import { UnauthorizedComponent } from './unauthorized/unauthorized.component';
import { hasRoleGuard } from './guards/has-role.guard';
import { AdminMakeModeratorComponent } from './admin-assign-moderator/admin-make-moderator.component';
import { StatisticsPanelComponent } from './statistics-panel/statistics-panel.component';

export const routes: Routes = [
    { path: '', component: MainPageComponent },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },
    { path: 'statistics', component: StatisticsPanelComponent},
    { path: 'image-view/:id', component: ImageViewComponent },
    { path: 'image-upload', component: ImageUploadComponent },
    { path: 'user/:username', component: UserPanelComponent },
    {
        path: 'admin',
        component: AdminMainPageComponent,
        canActivate: [hasRoleGuard],
        data: {
            roles: ['Admin', 'Moderator']
        }
    },
    {
        path: 'admin/image-view/:id',
        component: AdminImageViewComponent,
        canActivate: [hasRoleGuard],
        data: {
            roles: ['Admin']
        }
    },
    {
        path: 'admin/make-moderators',
        component: AdminMakeModeratorComponent,
        canActivate: [hasRoleGuard],
        data: {
            roles: ['Admin']
        }
    },
    { path: 'unauthorized', component: UnauthorizedComponent },
    {
        path: '**',
        pathMatch: 'full',
        component: NotFoundComponent
    },
];