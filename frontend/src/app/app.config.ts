import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { HttpClientModule, provideHttpClient, withInterceptors } from '@angular/common/http';
import { universalInterceptor } from './universal.interceptor';

export const appConfig: ApplicationConfig = {
    providers: [
        importProvidersFrom(HttpClientModule),
        provideRouter(routes),
        provideHttpClient(withInterceptors([universalInterceptor]))
    ]
};
