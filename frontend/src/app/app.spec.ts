import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app';
import { Auth } from '@angular/fire/auth';
import { of } from 'rxjs';

describe('AppComponent', () => {
  let mockAuth: any;

  beforeEach(async () => {
    mockAuth = {
      currentUser: null
    };

    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [
        { provide: Auth, useValue: mockAuth }
      ]
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });
});
