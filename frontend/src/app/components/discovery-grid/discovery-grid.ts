import { Component, inject, output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StewardshipService } from '../../services/stewardship';

@Component({
  selector: 'app-discovery-grid',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl mx-auto">
      <ng-container *ngIf="stewardship.persona() === 'parishioner'">
        <button 
          (click)="select.emit('How can I serve my parish with my time and talent?')"
          class="flex flex-col items-start p-6 bg-white rounded-2xl shadow-sm border border-diocese-blue/5 hover:border-diocese-gold hover:shadow-md transition-all text-left group"
        >
          <span class="text-3xl mb-3">🕊️</span>
          <h3 class="font-bold text-diocese-blue group-hover:text-diocese-gold transition-colors">How can I serve?</h3>
          <p class="text-sm text-diocese-blue/60 mt-1">Discover ways to share your Time & Talent.</p>
        </button>

        <button 
          (click)="select.emit('Explain the concept of tithing and sacrificial giving.')"
          class="flex flex-col items-start p-6 bg-white rounded-2xl shadow-sm border border-diocese-blue/5 hover:border-diocese-gold hover:shadow-md transition-all text-left group"
        >
          <span class="text-3xl mb-3">💰</span>
          <h3 class="font-bold text-diocese-blue group-hover:text-diocese-gold transition-colors">Explain Tithing</h3>
          <p class="text-sm text-diocese-blue/60 mt-1">Learn about Treasure & sacrificial giving.</p>
        </button>
      </ng-container>

      <ng-container *ngIf="stewardship.persona() === 'priest'">
        <button 
          (click)="select.emit('Give me some inspiration for a homily about stewardship.')"
          class="flex flex-col items-start p-6 bg-white rounded-2xl shadow-sm border border-diocese-blue/5 hover:border-diocese-gold hover:shadow-md transition-all text-left group"
        >
          <span class="text-3xl mb-3">📜</span>
          <h3 class="font-bold text-diocese-blue group-hover:text-diocese-gold transition-colors">Homily Inspiration</h3>
          <p class="text-sm text-diocese-blue/60 mt-1">Reflections and scripture for your next homily.</p>
        </button>

        <button 
          (click)="select.emit('What are the most common questions parishioners ask about stewardship?')"
          class="flex flex-col items-start p-6 bg-white rounded-2xl shadow-sm border border-diocese-blue/5 hover:border-diocese-gold hover:shadow-md transition-all text-left group"
        >
          <span class="text-3xl mb-3">❓</span>
          <h3 class="font-bold text-diocese-blue group-hover:text-diocese-gold transition-colors">Parishioner FAQ</h3>
          <p class="text-sm text-diocese-blue/60 mt-1">Address common concerns and questions.</p>
        </button>
      </ng-container>
    </div>
  `
})
export class DiscoveryGridComponent {
  stewardship = inject(StewardshipService);
  select = output<string>();
}
