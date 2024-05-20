import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TotpModalComponent } from './totp-modal.component';

describe('TotpModalComponent', () => {
	let component: TotpModalComponent;
	let fixture: ComponentFixture<TotpModalComponent>;

	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [TotpModalComponent]
		})
			.compileComponents();

		fixture = TestBed.createComponent(TotpModalComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
