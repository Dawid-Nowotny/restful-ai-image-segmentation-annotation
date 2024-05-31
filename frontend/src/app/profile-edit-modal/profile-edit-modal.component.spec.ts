import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileEditModalComponent } from './profile-edit-modal.component';

describe('ProfileEditModalComponent', () => {
  let component: ProfileEditModalComponent;
  let fixture: ComponentFixture<ProfileEditModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProfileEditModalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ProfileEditModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
