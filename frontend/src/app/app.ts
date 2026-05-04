import { Component, inject } from '@angular/core';
import { Auth, user } from '@angular/fire/auth';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './components/login/login';
import { PortalComponent } from './components/portal/portal';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, LoginComponent, PortalComponent],
  template: `
    <ng-container *ngIf="user$ | async as user; else login">
      <app-portal></app-portal>
    </ng-container>
    <ng-template #login>
      <app-login></app-login>
    </ng-template>
  `
})
export class AppComponent {
  private auth = inject(Auth);
  user$ = user(this.auth);
}
