import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { HttpClientModule, provideHttpClient, withInterceptors } from "@angular/common/http";
import { enableProdMode, importProvidersFrom } from "@angular/core";
import { provideRouter } from '@angular/router';
import { routes } from './app/app.routes';
import { universalInterceptor } from './app/universal.interceptor';


bootstrapApplication(AppComponent, {
    providers: [
        importProvidersFrom(HttpClientModule),
        provideRouter(routes),
        provideHttpClient(withInterceptors([universalInterceptor]))
    ],
    
})
    .catch((err) => console.error(err));