import { Component, inject } from '@angular/core';
import { Auth, GoogleAuthProvider, signInWithPopup, user } from '@angular/fire/auth';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="min-h-screen flex items-center justify-center bg-diocese-cream">
      <div class="max-w-md w-full p-8 bg-white rounded-xl shadow-lg border border-diocese-blue/10">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-diocese-blue mb-2">🕊️ Stewardship Portal</h1>
          <p class="text-gray-600">Catholic Diocese of Wichita</p>
        </div>
        
        <button 
          (click)="loginWithGoogle()"
          class="w-full flex items-center justify-center gap-3 px-6 py-3 bg-diocese-blue text-white rounded-lg hover:bg-opacity-90 transition-all font-medium shadow-md"
        >
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" class="w-5 h-5" alt="Google">
          Sign in with Google
        </button>
        
        <div class="mt-6 text-center text-sm text-gray-500">
          <p>Please sign in with your authorized account.</p>
        </div>
      </div>
    </div>
  `
})
export class LoginComponent {
  private auth = inject(Auth);
  user$ = user(this.auth);

  async loginWithGoogle() {
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(this.auth, provider);
    } catch (error) {
      console.error('Login failed:', error);
    }
  }
}
