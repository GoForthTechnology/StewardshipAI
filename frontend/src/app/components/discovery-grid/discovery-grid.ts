import { Component, inject, output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StewardshipService } from '../../services/stewardship';

@Component({
  selector: 'app-discovery-grid',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6 w-full max-w-3xl mx-auto px-4 lg:px-0">
      <ng-container *ngIf="stewardship.persona() === 'parishioner'">
        <button 
          (click)="select.emit('How can I serve my community with my time and talent?')"
          class="flex flex-col items-start p-5 lg:p-6 bg-white rounded-2xl shadow-sm border border-brand-primary/5 hover:border-brand-accent hover:shadow-md transition-all text-left group"
        >
          <span class="text-2xl lg:text-3xl mb-2 lg:mb-3">🕊️</span>
          <h3 class="font-bold text-sm lg:text-base text-brand-primary group-hover:text-brand-accent transition-colors">How can I serve?</h3>
          <p class="text-xs lg:text-sm text-brand-primary/60 mt-1">Discover ways to share your Time & Talent.</p>
        </button>

        <button 
          (click)="select.emit('Explain the concept of tithing and sacrificial giving.')"
          class="flex flex-col items-start p-5 lg:p-6 bg-white rounded-2xl shadow-sm border border-brand-primary/5 hover:border-brand-accent hover:shadow-md transition-all text-left group"
        >
          <span class="text-2xl lg:text-3xl mb-2 lg:mb-3">💰</span>
          <h3 class="font-bold text-sm lg:text-base text-brand-primary group-hover:text-brand-accent transition-colors">Explain Tithing</h3>
          <p class="text-xs lg:text-sm text-brand-primary/60 mt-1">Learn about Treasure & sacrificial giving.</p>
        </button>
      </ng-container>

      <ng-container *ngIf="stewardship.persona() === 'priest'">
        <button 
          (click)="select.emit('Give me some inspiration for a homily about stewardship.')"
          class="flex flex-col items-start p-5 lg:p-6 bg-white rounded-2xl shadow-sm border border-brand-primary/5 hover:border-brand-accent hover:shadow-md transition-all text-left group"
        >
          <span class="text-2xl lg:text-3xl mb-2 lg:mb-3">📜</span>
          <h3 class="font-bold text-sm lg:text-base text-brand-primary group-hover:text-brand-accent transition-colors">Homily Inspiration</h3>
          <p class="text-xs lg:text-sm text-brand-primary/60 mt-1">Reflections and scripture for your next homily.</p>
        </button>

        <button 
          (click)="select.emit('What are the most common questions parishioners ask about stewardship?')"
          class="flex flex-col items-start p-5 lg:p-6 bg-white rounded-2xl shadow-sm border border-brand-primary/5 hover:border-brand-accent hover:shadow-md transition-all text-left group"
        >
          <span class="text-2xl lg:text-3xl mb-2 lg:mb-3">❓</span>
          <h3 class="font-bold text-sm lg:text-base text-brand-primary group-hover:text-brand-accent transition-colors">Parishioner FAQ</h3>
          <p class="text-xs lg:text-sm text-brand-primary/60 mt-1">Address common concerns and questions.</p>
        </button>
      </ng-container>

      <ng-container *ngIf="stewardship.persona() === 'researcher'">
        <button 
          (click)="select.emit('Synthesize the main theological themes regarding stewardship across the available documents.')"
          class="flex flex-col items-start p-5 lg:p-6 bg-white rounded-2xl shadow-sm border border-brand-primary/5 hover:border-brand-accent hover:shadow-md transition-all text-left group"
        >
          <span class="text-2xl lg:text-3xl mb-2 lg:mb-3">🏛️</span>
          <h3 class="font-bold text-sm lg:text-base text-brand-primary group-hover:text-brand-accent transition-colors">Theological Synthesis</h3>
          <p class="text-xs lg:text-sm text-brand-primary/60 mt-1">Explore core themes across the corpus.</p>
        </button>

        <button 
          (click)="select.emit('Analyze the shift in stewardship language in official documents over the last decade.')"
          class="flex flex-col items-start p-5 lg:p-6 bg-white rounded-2xl shadow-sm border border-brand-primary/5 hover:border-brand-accent hover:shadow-md transition-all text-left group"
        >
          <span class="text-2xl lg:text-3xl mb-2 lg:mb-3">📈</span>
          <h3 class="font-bold text-sm lg:text-base text-brand-primary group-hover:text-brand-accent transition-colors">Language Analysis</h3>
          <p class="text-xs lg:text-sm text-brand-primary/60 mt-1">Study evolution of stewardship concepts.</p>
        </button>
      </ng-container>
    </div>
  `
})
export class DiscoveryGridComponent {
  stewardship = inject(StewardshipService);
  select = output<string>();
}
