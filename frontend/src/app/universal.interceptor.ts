import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { CookieService } from './services/cookie.service';

export const universalInterceptor: HttpInterceptorFn = (req, next) => {

	const cookieService = inject(CookieService);

	const  modifiedRequest = req.clone({
		withCredentials: true,
		setHeaders: {
			'x-csrftoken': cookieService.get("csrftoken") ?? ""
		}
	})
	return next(modifiedRequest);
};
