import { Component, OnInit, Input, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavigationEnd, Router, ActivatedRoute, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs/operators';
import { Title } from '@angular/platform-browser';
import { LoggedUserService } from '../services/logged-user.service';

@Component({
    selector: 'app-navbar',
    standalone: true,
    imports: [RouterLink, RouterLinkActive, RouterOutlet, CommonModule],
    templateUrl: './navbar.component.html',
    styleUrl: './navbar.component.css'
})
export class NavbarComponent implements OnInit, AfterViewInit {
    currentComponent: string | null = null;
    routeParams: any;
    @Input() notFound: string = '';

    constructor(
        private router: Router, 
        private titleService: Title, 
        private route: ActivatedRoute,
        public loggedUserService: LoggedUserService
    ) { }

    ngOnInit(): void {
        this.router.events
            .pipe(filter(event => event instanceof NavigationEnd))
            .subscribe(() => {
                this.currentComponent = this.getCurrentComponentName();

            });
    }

    ngAfterViewInit(): void {
        const currentUrl = this.router.url;
        let pageTitle = '';

        this.route.queryParams.subscribe(params => {
            if (currentUrl === '/') {
                pageTitle = 'Strona główna';
            } else if (currentUrl === '/login') {
                pageTitle = 'Logowanie';
            } else if (currentUrl === '/register') {
                pageTitle = 'Rejestracja';
            } else if (this.notFound) {
                pageTitle = 'Nie znaleziono podanej strony';
            } else {
                pageTitle = 'Strona główna';
            }

            this.setPageTitle(pageTitle);
        });
    }

    private getCurrentComponentName(): string | null {
        const currentUrl = this.router.url;
        return currentUrl;
    }

    isCurrentComponent(componentName: string): boolean {
        return this.router.url.startsWith(componentName);
    }

    setPageTitle(title: string): void {
        this.titleService.setTitle(title);
    }

    logOut(){
        this.loggedUserService.logOut();
    }
}
