import { Component, inject, signal, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Auth, user, signOut } from '@angular/fire/auth';
import { FormsModule } from '@angular/forms';
import { StewardshipService, Persona } from '../../services/stewardship';
import { ChatService, ChatMessage } from '../../services/chat';
import { DiscoveryGridComponent } from '../discovery-grid/discovery-grid';
import { MarkdownPipe } from '../../pipes/markdown';

@Component({
  selector: 'app-portal',
  standalone: true,
  imports: [CommonModule, FormsModule, DiscoveryGridComponent, MarkdownPipe],
  template: `
    <div class="flex h-screen bg-diocese-cream overflow-hidden">
      <!-- Sidebar -->
      <aside class="w-72 bg-diocese-blue text-white flex flex-col shadow-2xl z-10">
        <div class="p-6">
          <h1 class="text-xl font-bold flex items-center gap-2">
            <span>🕊️</span>
            Portal
          </h1>
          <p class="text-xs text-blue-200 mt-1 opacity-70">Catholic Diocese of Wichita</p>
        </div>

        <nav class="flex-1 px-4 py-4 space-y-6">
          <div class="space-y-3">
            <h3 class="text-xs font-semibold text-blue-300 uppercase tracking-wider px-2">I am a...</h3>
            <div class="space-y-1">
              <button 
                (click)="setPersona('parishioner')"
                [class.bg-white]="stewardship.persona() === 'parishioner'"
                [class.text-diocese-blue]="stewardship.persona() === 'parishioner'"
                [class.bg-transparent]="stewardship.persona() !== 'parishioner'"
                class="w-full text-left px-3 py-2 rounded-lg transition-all text-sm font-medium hover:bg-white/10"
              >
                Parishioner
              </button>
              <button 
                (click)="setPersona('priest')"
                [class.bg-white]="stewardship.persona() === 'priest'"
                [class.text-diocese-blue]="stewardship.persona() === 'priest'"
                [class.bg-transparent]="stewardship.persona() !== 'priest'"
                class="w-full text-left px-3 py-2 rounded-lg transition-all text-sm font-medium hover:bg-white/10"
              >
                Priest / Leader
              </button>
            </div>
          </div>
        </nav>

        <div class="p-4 border-t border-blue-800">
          <div class="flex items-center gap-3 px-2 py-3 bg-blue-900/50 rounded-xl mb-3 overflow-hidden">
            <div class="w-8 h-8 rounded-full bg-diocese-gold flex items-center justify-center text-diocese-blue font-bold shrink-0">
              {{ (user$ | async)?.email?.charAt(0)?.toUpperCase() }}
            </div>
            <div class="min-w-0">
              <p class="text-xs font-medium truncate">{{ (user$ | async)?.email }}</p>
            </div>
          </div>
          <button 
            (click)="logout()"
            class="w-full px-4 py-2 text-xs font-semibold text-blue-300 hover:text-white transition-colors flex items-center justify-center gap-2"
          >
            <span>🚪</span> Sign Out
          </button>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 flex flex-col relative overflow-hidden">
        <header class="h-16 border-b border-diocese-blue/5 bg-white/50 backdrop-blur-md flex items-center px-8 justify-between shrink-0">
          <h2 class="text-sm font-semibold text-diocese-blue uppercase tracking-widest">
            Stewardship Guide
          </h2>
          <button 
            *ngIf="messages().length > 0"
            (click)="clearChat()"
            class="text-xs font-bold text-diocese-blue/40 hover:text-diocese-blue transition-colors"
          >
            Reset Chat
          </button>
        </header>

        <div #scrollContainer class="flex-1 overflow-y-auto p-8 custom-scrollbar">
           <div class="max-w-3xl mx-auto space-y-8 pb-12">
             
             <!-- Welcome View -->
             <div *ngIf="messages().length === 0" class="text-center py-20">
               <h1 class="text-4xl font-bold text-diocese-blue mb-4">Welcome to the Portal</h1>
               <p class="text-lg text-diocese-blue/60 max-w-lg mx-auto mb-12">
                 How can we help you live out your mission of stewardship today?
               </p>
               
               <app-discovery-grid (select)="submitPrompt($event)"></app-discovery-grid>
             </div>

             <!-- Chat Messages -->
             <div *ngFor="let msg of messages()" class="flex flex-col gap-2">
               <div 
                 [class.items-end]="msg.role === 'user'"
                 [class.items-start]="msg.role === 'assistant'"
                 class="flex flex-col max-w-[85%]"
                 [class.self-end]="msg.role === 'user'"
               >
                 <div class="text-[10px] uppercase font-bold tracking-widest text-diocese-blue/30 px-4 mb-1">
                   {{ msg.role === 'user' ? 'You' : 'Guide' }}
                 </div>
                 <div 
                   [class.bg-diocese-blue]="msg.role === 'user'"
                   [class.text-white]="msg.role === 'user'"
                   [class.bg-white]="msg.role === 'assistant'"
                   [class.text-diocese-blue]="msg.role === 'assistant'"
                   [class.shadow-xl]="msg.role === 'assistant'"
                   [class.rounded-2xl]="true"
                   [class.rounded-tr-none]="msg.role === 'user'"
                   [class.rounded-tl-none]="msg.role === 'assistant'"
                   class="px-5 py-4 text-[15px] leading-relaxed border border-diocese-blue/5"
                 >
                   <ng-container *ngIf="msg.role === 'assistant' && !msg.content && pendingResponse()">
                     <div class="pending-dots">
                       <div class="pending-dot"></div>
                       <div class="pending-dot"></div>
                       <div class="pending-dot"></div>
                     </div>
                   </ng-container>
                   <div *ngIf="msg.content || msg.role === 'user'" [innerHTML]="msg.content | markdown"></div>
                 </div>
               </div>
             </div>

             <!-- Error or Interrupted State -->
             <div *ngIf="isLoading()" class="flex flex-col items-start max-w-[85%] animate-pulse">
                <div class="text-[10px] uppercase font-bold tracking-widest text-diocese-blue/30 px-4 mb-1">Guide</div>
                <div class="px-5 py-4 bg-white rounded-2xl rounded-tl-none border border-diocese-blue/5 italic text-sm text-diocese-blue/40">
                  Reflecting on stewardship resources...
                </div>
             </div>

           </div>
        </div>

        <!-- Chat Input -->
        <div class="p-6 bg-gradient-to-t from-diocese-cream via-diocese-cream/95 to-transparent shrink-0">
          <div class="max-w-3xl mx-auto">
            <form (submit)="submitChat($event)" class="relative group">
              <input 
                type="text" 
                [(ngModel)]="currentInput"
                name="chatInput"
                [disabled]="isLoading()"
                placeholder="Ask about Time, Talent, or Treasure..."
                class="w-full px-6 py-4 bg-white rounded-2xl shadow-xl border border-diocese-blue/10 focus:outline-none focus:ring-2 focus:ring-diocese-gold/30 transition-all pr-12 text-diocese-blue placeholder-diocese-blue/40 disabled:opacity-50"
              >
              <button 
                type="submit"
                [disabled]="!currentInput || isLoading()"
                class="absolute right-3 top-3 w-10 h-10 bg-diocese-blue text-white rounded-xl flex items-center justify-center hover:bg-diocese-gold hover:text-diocese-blue transition-all disabled:opacity-30"
              >
                ↑
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  `
})
export class PortalComponent implements AfterViewChecked {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  private auth = inject(Auth);
  stewardship = inject(StewardshipService);
  chatService = inject(ChatService);
  user$ = user(this.auth);

  messages = signal<ChatMessage[]>([]);
  currentInput = '';
  isLoading = signal(false);
  pendingResponse = signal(false);

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
    } catch(err) {}
  }

  setPersona(persona: Persona) {
    this.stewardship.setPersona(persona);
  }

  clearChat() {
    this.messages.set([]);
  }

  async logout() {
    await signOut(this.auth);
  }

  async submitPrompt(prompt: string) {
    this.currentInput = prompt;
    await this.submitChat();
  }

  async submitChat(event?: Event) {
    if (event) event.preventDefault();
    if (!this.currentInput || this.isLoading()) return;

    const prompt = this.currentInput;
    this.currentInput = '';
    
    // Add user message
    this.messages.update(msgs => [...msgs, { role: 'user', content: prompt }]);
    
    this.isLoading.set(true);
    this.pendingResponse.set(true);
    
    try {
      // Initialize assistant message
      this.messages.update(msgs => [...msgs, { role: 'assistant', content: '' }]);
      
      const stream = this.chatService.streamChat(prompt, this.stewardship.persona());
      
      this.isLoading.set(false);

      for await (const data of stream) {
        if (data.text && this.pendingResponse()) {
          this.pendingResponse.set(false);
        }
        this.messages.update(msgs => {
          const lastMsg = msgs[msgs.length - 1];
          if (lastMsg && lastMsg.role === 'assistant') {
            if (data.text) {
              lastMsg.content += data.text;
            }
          }
          return [...msgs];
        });
      }
    } catch (error) {
      console.error('Chat error:', error);
      this.isLoading.set(false);
      this.pendingResponse.set(false);
      this.messages.update(msgs => [...msgs, { role: 'assistant', content: 'I encountered an error connecting to our resources. Please try again later.' }]);
    }
  }
}
