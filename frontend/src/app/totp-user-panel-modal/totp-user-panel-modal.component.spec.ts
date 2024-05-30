import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TotpUserPanelModalComponent } from './totp-user-panel-modal.component';

describe('TotpUserPanelModalComponent', () => {
  let component: TotpUserPanelModalComponent;
  let fixture: ComponentFixture<TotpUserPanelModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TotpUserPanelModalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TotpUserPanelModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
