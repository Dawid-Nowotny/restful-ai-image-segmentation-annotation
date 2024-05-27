import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminImageViewComponent } from './admin-image-view.component';

describe('AdminImageViewComponent', () => {
	let component: AdminImageViewComponent;
	let fixture: ComponentFixture<AdminImageViewComponent>;

	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [AdminImageViewComponent]
		})
			.compileComponents();

		fixture = TestBed.createComponent(AdminImageViewComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
