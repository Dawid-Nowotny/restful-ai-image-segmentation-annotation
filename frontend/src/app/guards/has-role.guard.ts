import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { LoggedUserService } from '../services/logged-user.service';

export const hasRoleGuard: CanActivateFn = (route) => {
	const router: Router = inject(Router);
	const userRole: string = inject(LoggedUserService).getRole();
	const expectedRoles: string[] = route.data['roles'];
	
	const hasRole: boolean = expectedRoles.some((role) => {
		return userRole === role
	});
	
	return hasRole || router.navigate(['unauthorized']);
};
