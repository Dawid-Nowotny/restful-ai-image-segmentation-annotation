import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminMakeModeratorComponent } from './admin-make-moderator.component';

describe('AdminAssignModeratorComponent', () => {
	let component: AdminMakeModeratorComponent;
	let fixture: ComponentFixture<AdminMakeModeratorComponent>;

	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [AdminMakeModeratorComponent]
		})
			.compileComponents();

		fixture = TestBed.createComponent(AdminMakeModeratorComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
