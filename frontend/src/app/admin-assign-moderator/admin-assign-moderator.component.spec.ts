import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminAssignModeratorComponent } from './admin-assign-moderator.component';

describe('AdminAssignModeratorComponent', () => {
	let component: AdminAssignModeratorComponent;
	let fixture: ComponentFixture<AdminAssignModeratorComponent>;

	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [AdminAssignModeratorComponent]
		})
			.compileComponents();

		fixture = TestBed.createComponent(AdminAssignModeratorComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
