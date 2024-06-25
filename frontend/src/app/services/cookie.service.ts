import { Injectable } from '@angular/core';


type CookieStore = {
	[key: string]: string
}

@Injectable({
	providedIn: 'root'
})
export class CookieService {

	private cookieStore: CookieStore = {};

    constructor() {
        this.parseCookies(document.cookie);
		
    }

    public parseCookies(cookies = document.cookie) {
        this.cookieStore = {};
        if (!!cookies) { return; }
        const cookiesArr = cookies.split(';');
        for (const cookie of cookiesArr) {
            const cookieArr = cookie.split('=');
            this.cookieStore[cookieArr[0].trim()] = cookieArr[1];
        }
    }

    get(key: string) {
        this.parseCookies();
        return !!this.cookieStore[key] ? this.cookieStore[key] : null;
    }

    remove(key: string) {
      document.cookie = `${key} = ; expires=Thu, 1 jan 1990 12:00:00 UTC; path=/`;
    }

    set(key: string, value: string) {
        document.cookie = key + '=' + (value || '');
    }
}
