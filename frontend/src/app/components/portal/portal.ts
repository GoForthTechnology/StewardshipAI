import { Component, inject, signal, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Auth, user, signOut } from '@angular/fire/auth';
import { FormsModule } from '@angular/forms';
import { BehaviorSubject } from 'rxjs';
import { StewardshipService, Persona } from '../../services/stewardship';
import { ChatService, ChatMessage } from '../../services/chat';
import { HistoryService, ChatSession } from '../../services/history';
import { DiscoveryGridComponent } from '../discovery-grid/discovery-grid';
import { MarkdownPipe } from '../../pipes/markdown';

export interface Corpus {
  id: string;
  name: string;
  enabled: boolean;
  extensionFilters: {
    pdf: boolean;
    word: boolean;
    txt: boolean;
    other: boolean;
  };
}

@Component({
  selector: 'app-portal',
  standalone: true,
  imports: [CommonModule, FormsModule, DiscoveryGridComponent, MarkdownPipe],
  styles: [`
    .portal-container {
      padding-left: var(--spacing-portal-padding);
      padding-right: var(--spacing-portal-padding);
    }
    @media (min-width: 1024px) {
      .portal-container {
        padding-left: var(--spacing-portal-gutter);
        padding-right: var(--spacing-portal-gutter);
      }
    }
  `],
  template: `
    <div class="flex h-screen bg-brand-background overflow-hidden relative">
      
      <!-- Mobile Header -->
      <header class="lg:hidden fixed top-0 left-0 right-0 h-16 bg-brand-primary text-white flex items-center px-4 z-20 shadow-md">
        <button (click)="isMenuOpen.set(true)" class="p-2 -ml-2">
          <span class="text-2xl">☰</span>
        </button>
        <h1 class="text-lg font-bold ml-2 flex items-center gap-2">
          <span>🕊️</span>
          Stewardship Portal
        </h1>
      </header>

      <!-- Sidebar / Mobile Drawer -->
      <aside 
        [class.translate-x-0]="isMenuOpen()"
        class="fixed lg:static inset-y-0 left-0 w-72 bg-brand-primary text-white flex flex-col shadow-2xl z-30 transition-transform duration-300 ease-in-out -translate-x-full lg:translate-x-0"
      >
        <div class="p-6 flex items-center justify-between lg:block">
          <div>
            <h1 class="text-xl font-bold flex items-center gap-2">
              <span>🕊️</span>
              Stewardship Portal
            </h1>
            <p class="text-xs text-blue-200 mt-1 opacity-70">Guided by Doctrine & Practice</p>
          </div>
          <button (click)="isMenuOpen.set(false)" class="lg:hidden p-2 -mr-2">
            <span class="text-xl">✕</span>
          </button>
        </div>

        <nav class="flex-1 px-4 py-4 space-y-6 overflow-y-auto">
          
          <div class="space-y-3">
            <button 
              (click)="createNewChat()"
              class="w-full flex items-center gap-3 px-4 py-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all group"
            >
              <span class="text-xl group-hover:scale-110 transition-transform">+</span>
              <span class="text-sm font-semibold tracking-wide">New Chat</span>
            </button>
          </div>

          <!-- Recent Chats -->
          <div class="space-y-3" *ngIf="history.sessions().length > 0">
            <h3 class="text-xs font-semibold text-blue-300 uppercase tracking-wider px-2">Recent Chats</h3>
            <div class="space-y-1">
              <div *ngFor="let session of history.getSessions()" class="group relative">
                <button 
                  (click)="loadSession(session)"
                  [class.bg-white/10]="history.activeSessionId() === session.id"
                  class="w-full text-left px-3 py-2 rounded-lg transition-all text-sm truncate pr-10 hover:bg-white/5"
                >
                  <span class="opacity-70 mr-2">{{ session.persona === 'priest' ? '⛪' : session.persona === 'researcher' ? '🎓' : '🕊️' }}</span>
                  {{ session.title }}
                </button>
                <button 
                  (click)="history.deleteSession(session.id); $event.stopPropagation()"
                  class="absolute right-2 top-1/2 -translate-y-1/2 p-1 opacity-0 group-hover:opacity-40 hover:!opacity-100 transition-opacity"
                >
                  ✕
                </button>
              </div>
            </div>
          </div>

          <div class="space-y-3">
            <h3 class="text-xs font-semibold text-blue-300 uppercase tracking-wider px-2">I am a...</h3>
            <div class="space-y-1">
              <button 
                (click)="setPersona('parishioner')"
                [class.bg-white]="stewardship.persona() === 'parishioner'"
                [class.text-brand-primary]="stewardship.persona() === 'parishioner'"
                [class.bg-transparent]="stewardship.persona() !== 'parishioner'"
                class="w-full text-left px-3 py-2 rounded-lg transition-all text-sm font-medium hover:bg-white/10"
              >
                Parishioner
              </button>
              <button 
                (click)="setPersona('priest')"
                [class.bg-white]="stewardship.persona() === 'priest'"
                [class.text-brand-primary]="stewardship.persona() === 'priest'"
                [class.bg-transparent]="stewardship.persona() !== 'priest'"
                class="w-full text-left px-3 py-2 rounded-lg transition-all text-sm font-medium hover:bg-white/10"
              >
                Priest / Leader
              </button>
              <button 
                (click)="setPersona('researcher')"
                [class.bg-white]="stewardship.persona() === 'researcher'"
                [class.text-brand-primary]="stewardship.persona() === 'researcher'"
                [class.bg-transparent]="stewardship.persona() !== 'researcher'"
                class="w-full text-left px-3 py-2 rounded-lg transition-all text-sm font-medium hover:bg-white/10"
              >
                Academic / Researcher
              </button>
            </div>
          </div>

          <div class="space-y-3">
            <h3 class="text-xs font-semibold text-blue-300 uppercase tracking-wider px-2">Resources</h3>
            <div class="space-y-4 px-2">
              <div *ngFor="let corpus of availableCorpora()" class="space-y-2">
                <div class="flex items-center justify-between group">
                  <span class="text-sm font-medium text-white/80 group-hover:text-white transition-colors">{{ corpus.name }}</span>
                  <button 
                    (click)="toggleCorpus(corpus)"
                    class="w-8 h-4 rounded-full transition-all relative flex items-center"
                    [class.bg-brand-accent]="corpus.enabled"
                    [class.bg-blue-800]="!corpus.enabled"
                  >
                    <div 
                      class="w-3 h-3 bg-white rounded-full shadow-sm transition-transform duration-200"
                      [class.translate-x-4]="corpus.enabled"
                      [class.translate-x-1]="!corpus.enabled"
                    ></div>
                  </button>
                </div>
                
                <!-- Extension Filters -->
                <div *ngIf="corpus.enabled" class="ml-4 space-y-2 border-l border-blue-800 pl-3 py-1 animate-in fade-in slide-in-from-left-2">
                  <div class="flex items-center justify-between group/ext" *ngFor="let ext of availableExtensions">
                    <span class="text-[11px] uppercase tracking-wider text-blue-300 group-hover/ext:text-white transition-colors">{{ ext }}</span>
                    <input 
                      type="checkbox" 
                      [checked]="getExtensionValue(corpus, ext)"
                      (change)="toggleExtension(corpus, ext)"
                      class="w-3 h-3 rounded border-blue-800 bg-blue-900 text-brand-accent focus:ring-offset-brand-primary"
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <div class="p-4 border-t border-blue-800">
          <div class="flex items-center gap-3 px-2 py-3 bg-blue-900/50 rounded-xl mb-3 overflow-hidden">
            <div class="w-8 h-8 rounded-full bg-brand-accent flex items-center justify-center text-brand-primary font-bold shrink-0">
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

      <!-- Overlay for Mobile -->
      <div 
        *ngIf="isMenuOpen()" 
        (click)="isMenuOpen.set(false)"
        class="fixed inset-0 bg-black/50 z-20 lg:hidden"
      ></div>

      <!-- Main Content -->
      <main class="flex-1 flex flex-col relative overflow-hidden pt-16 lg:pt-0">
        <header class="h-16 border-b border-brand-primary/5 bg-white/50 backdrop-blur-md flex items-center justify-between shrink-0 portal-container">
          <h2 class="text-sm font-semibold text-brand-primary uppercase tracking-widest">
            Stewardship Guide
          </h2>
          <button 
            *ngIf="messages().length > 0"
            (click)="clearChat()"
            class="text-xs font-bold text-brand-primary/40 hover:text-brand-primary transition-colors"
          >
            Reset Chat
          </button>
        </header>

        <div #scrollContainer class="flex-1 overflow-y-auto custom-scrollbar portal-container py-4 lg:py-8">
           <div class="max-w-3xl mx-auto space-y-6 lg:space-y-8 pb-12">
             
             <!-- Welcome View -->
             <div *ngIf="messages().length === 0" class="text-center py-12 lg:py-20">
               <h1 class="text-3xl lg:text-4xl font-bold text-brand-primary mb-4 px-4">Welcome to the Portal</h1>
               <p class="text-base lg:text-lg text-brand-primary/60 max-w-lg mx-auto mb-8 lg:mb-12 px-6">
                 How can we help you live out your mission of stewardship today?
               </p>
               
               <app-discovery-grid (select)="submitPrompt($event)"></app-discovery-grid>
             </div>

             <!-- Chat Messages -->
             <div *ngFor="let msg of messages()" class="flex flex-col gap-2">
               <div 
                 [class.items-end]="msg.role === 'user'"
                 [class.items-start]="msg.role === 'assistant'"
                 class="flex flex-col max-w-[90%] lg:max-w-[85%]"
                 [class.self-end]="msg.role === 'user'"
               >
                 <div class="text-[10px] uppercase font-bold tracking-widest text-brand-primary/30 px-4 mb-1">
                   {{ msg.role === 'user' ? 'You' : 'Guide' }}
                 </div>
                 <div 
                   [class.bg-brand-primary]="msg.role === 'user'"
                   [class.text-white]="msg.role === 'user'"
                   [class.bg-white]="msg.role === 'assistant'"
                   [class.text-brand-primary]="msg.role === 'assistant'"
                   [class.shadow-xl]="msg.role === 'assistant'"
                   [class.rounded-2xl]="true"
                   [class.rounded-tr-none]="msg.role === 'user'"
                   [class.rounded-tl-none]="msg.role === 'assistant'"
                   class="px-4 py-3 lg:px-5 lg:py-4 text-[14px] lg:text-[15px] leading-relaxed border border-brand-primary/5"
                 >
                   <ng-container *ngIf="msg.role === 'assistant' && !msg.content && (pendingResponse() || currentStatus())">
                     <div class="flex flex-col gap-2">
                        <div class="pending-dots">
                          <div class="pending-dot"></div>
                          <div class="pending-dot"></div>
                          <div class="pending-dot"></div>
                        </div>
                        <div *ngIf="currentStatus()" class="text-[11px] font-bold text-brand-primary/40 animate-pulse tracking-tight">
                          {{ currentStatus() }}
                        </div>
                     </div>
                   </ng-container>
                   <div *ngIf="msg.content || msg.role === 'user'" [innerHTML]="msg.content | markdown"></div>
                 </div>
               </div>
             </div>

             <!-- Error or Interrupted State -->
             <div *ngIf="isLoading()" class="flex flex-col items-start max-w-[90%] lg:max-w-[85%] animate-pulse">
                <div class="text-[10px] uppercase font-bold tracking-widest text-brand-primary/30 px-4 mb-1">Guide</div>
                <div class="px-4 py-3 lg:px-5 lg:py-4 bg-white rounded-2xl rounded-tl-none border border-brand-primary/5 italic text-sm text-brand-primary/40">
                  Reflecting on stewardship resources...
                </div>
             </div>

           </div>
        </div>

        <!-- Chat Input -->
        <div class="p-4 lg:p-6 bg-gradient-to-t from-brand-background via-brand-background/95 to-transparent shrink-0">
          <div class="max-w-3xl mx-auto">
            
            <!-- File Chip -->
            <div *ngIf="activeFile()" class="flex items-center gap-2 mb-3 px-4 py-2 bg-brand-accent/10 border border-brand-accent/20 rounded-xl w-fit animate-in fade-in slide-in-from-bottom-2">
              <span class="text-xs font-bold text-brand-primary/60 uppercase tracking-tighter">📄 Document:</span>
              <span class="text-sm font-medium text-brand-primary truncate max-w-[200px]">{{ activeFile()?.name }}</span>
              <button (click)="removeFile()" class="ml-1 text-brand-primary/40 hover:text-red-500 transition-colors">✕</button>
            </div>

            <form (submit)="submitChat($event)" class="relative group">
              <input 
                #fileInput
                type="file" 
                class="hidden" 
                accept=".pdf,.txt"
                (change)="onFileSelected($event)"
              >
              
              <button 
                type="button"
                (click)="fileInput.click()"
                [disabled]="isLoading() || !!activeFile()"
                class="absolute left-2 top-2 lg:left-3 lg:top-3 w-8 h-8 lg:w-10 lg:h-10 bg-white text-brand-primary/40 rounded-xl flex flex-col items-center justify-center hover:bg-brand-primary/5 hover:text-brand-primary transition-all disabled:opacity-30 border border-brand-primary/10"
                title="Upload Document (PDF/TXT only)"
              >
                <span class="text-lg">📎</span>
                <span class="text-[8px] font-bold -mt-1 hidden lg:block">PDF/TXT</span>
              </button>

              <input 
                type="text" 
                [(ngModel)]="currentInput"
                name="chatInput"
                [disabled]="isLoading()"
                placeholder="Ask about Time, Talent, or Treasure..."
                class="w-full pl-12 lg:pl-16 pr-12 py-3 lg:px-6 lg:py-4 bg-white rounded-2xl shadow-xl border border-brand-primary/10 focus:outline-none focus:ring-2 focus:ring-brand-accent/30 transition-all text-sm lg:text-base text-brand-primary placeholder-brand-primary/40 disabled:opacity-50"
              >
              <button 
                type="submit"
                [disabled]="!currentInput || isLoading()"
                class="absolute right-2 top-2 lg:right-3 lg:top-3 w-8 h-8 lg:w-10 lg:h-10 bg-brand-primary text-white rounded-xl flex items-center justify-center hover:bg-brand-accent hover:text-brand-primary transition-all disabled:opacity-30"
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
  history = inject(HistoryService);
  user$ = user(this.auth);

  messages = signal<ChatMessage[]>([]);
  currentInput = '';
  isLoading = signal(false);
  pendingResponse = signal(false);
  currentStatus = signal<string | null>(null);
  isMenuOpen = signal(false);

  // Corpus Selection State
  availableCorpora = signal<Corpus[]>([]);
  availableExtensions = ['pdf', 'word', 'txt', 'other'];

  // Active File State
  activeFile = signal<{ name: string, uri: string, mimeType: string } | null>(null);

  constructor() {
    // Initialize available corpora from window.ENV
    const envCorpora = (window as any).ENV?.corpora || [];
    this.availableCorpora.set(envCorpora.map((c: any) => ({
      id: c.id,
      name: c.name,
      enabled: !!c.default,
      extensionFilters: {
        pdf: true,
        word: true,
        txt: true,
        other: true
      }
    })));
  }

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
    const sessionId = this.history.activeSessionId();
    if (sessionId) {
      this.history.updateSession(sessionId, { persona });
    }
  }

  clearChat() {
    this.messages.set([]);
    this.removeFile();
  }

  async logout() {
    await signOut(this.auth);
  }

  async submitPrompt(prompt: string) {
    this.currentInput = prompt;
    await this.submitChat();
  }

  async onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (!file) return;

    // Frontend validation: Size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('File too large. Maximum size is 10MB.');
      return;
    }

    // Frontend validation: Type
    const allowedTypes = ['application/pdf', 'text/plain'];
    if (!allowedTypes.includes(file.type)) {
      alert('Invalid file type. Please upload a PDF or Text document.');
      return;
    }

    this.isLoading.set(true);
    try {
      const result = await this.chatService.uploadFile(file);
      this.activeFile.set({ name: result.display_name, uri: result.file_uri, mimeType: result.mime_type });
    } catch (error: any) {
      alert(`Upload failed: ${error.message}`);
    } finally {
      this.isLoading.set(false);
      event.target.value = ''; // Reset input
    }
  }

  removeFile() {
    this.activeFile.set(null);
  }

  toggleCorpus(corpus: Corpus) {
    const current = this.availableCorpora();
    const enabledCount = current.filter(c => c.enabled).length;
    
    if (corpus.enabled && enabledCount === 1) {
      alert('At least one resource must be selected.');
      return;
    }

    this.availableCorpora.update(corpora => 
      corpora.map(c => c.id === corpus.id ? { ...c, enabled: !c.enabled } : c)
    );
  }

  toggleExtension(corpus: Corpus, extension: string) {
    this.availableCorpora.update(corpora => 
      corpora.map(c => {
        if (c.id === corpus.id) {
          const filters = c.extensionFilters as any;
          const newFilters = { ...filters, [extension]: !filters[extension] };
          return { ...c, extensionFilters: newFilters };
        }
        return c;
      })
    );
  }

  getExtensionValue(corpus: Corpus, ext: string): boolean {
    return (corpus.extensionFilters as any)[ext];
  }

  createNewChat() {
    this.messages.set([]);
    this.removeFile();
    this.history.activeSessionId.set(null);
  }

  loadSession(session: ChatSession) {
    this.history.activeSessionId.set(session.id);
    this.messages.set(session.messages);
    this.stewardship.setPersona(session.persona);
    this.activeFile.set(session.activeFile || null);
    
    // Sync available corpora from session if present
    const envCorpora = (window as any).ENV?.corpora || [];
    this.availableCorpora.set(envCorpora.map((c: any) => {
      const isEnabled = session.corpusIds.includes(c.id);
      return {
        id: c.id,
        name: c.name,
        enabled: isEnabled,
        extensionFilters: session.extensionFilters[c.id] ? {
          pdf: session.extensionFilters[c.id].includes('pdf'),
          word: session.extensionFilters[c.id].includes('word'),
          txt: session.extensionFilters[c.id].includes('txt'),
          other: session.extensionFilters[c.id].includes('other')
        } : {
          pdf: true, word: true, txt: true, other: true
        }
      };
    }));

    if (this.isMenuOpen()) {
      this.isMenuOpen.set(false);
    }
  }

  async submitChat(event?: Event) {
    if (event) event.preventDefault();
    if (!this.currentInput || this.isLoading()) return;

    const prompt = this.currentInput;
    this.currentInput = '';
    
    console.log('Portal: Submitting chat', { prompt });

    try {
      // 1. Get or Create Session
      let sessionId = this.history.activeSessionId();
      let isNewSession = false;

      if (!sessionId) {
        console.log('Portal: No active session, creating one');
        const corpusIds = this.availableCorpora()
          .filter(c => c.enabled)
          .map(c => c.id);

        const extensionFilters: Record<string, string[]> = {};
        this.availableCorpora().forEach(c => {
          if (c.enabled) {
            const activeExtensions = Object.entries(c.extensionFilters || {})
              .filter(([_, enabled]) => enabled)
              .map(([ext, _]) => ext);
            extensionFilters[c.id] = activeExtensions;
          }
        });

        const session = this.history.createSession(
          this.stewardship.persona(),
          corpusIds,
          extensionFilters,
          prompt
        );
        sessionId = session.id;
        isNewSession = true;

        if (this.activeFile()) {
          this.history.updateSession(sessionId, { activeFile: this.activeFile()! });
        }
      }

      if (!sessionId) throw new Error('Failed to establish a chat session');

      const userMsg: ChatMessage = { role: 'user', content: prompt };
      this.history.addMessage(sessionId, userMsg);
      this.messages.set(this.history.getSession(sessionId)?.messages || []);
      
      this.isLoading.set(true);
      this.pendingResponse.set(true);
      this.currentStatus.set('🔍 Searching Stewardship Resources...');
      
      // Initialize assistant message in history
      this.history.addMessage(sessionId, { role: 'assistant', content: '' });
      this.messages.set(this.history.getSession(sessionId)?.messages || []);
      
      const currentSession = this.history.getSession(sessionId);
      if (!currentSession) throw new Error('Session lost after message update');
      
      const stream = this.chatService.streamChat(
        prompt, 
        currentSession.persona, 
        currentSession.messages.slice(0, -2), // History excluding current user/assistant turn
        currentSession.activeFile?.uri,
        currentSession.activeFile?.mimeType,
        currentSession.corpusIds,
        currentSession.extensionFilters
      );
      
      this.isLoading.set(false);

      let fullContent = '';
      for await (const data of stream) {
        if (data.status) {
          console.log('Portal: Status update', data.status);
          this.currentStatus.set(data.status);
          continue;
        }

        if (data.text !== undefined) {
          if (this.pendingResponse()) {
            this.pendingResponse.set(false);
            this.currentStatus.set(null);
          }
          fullContent += data.text;
          this.history.updateLastMessage(sessionId, fullContent);
          this.messages.set(this.history.getSession(sessionId)?.messages || []);
        }
        
        if (data.error) {
          throw new Error(data.error);
        }
      }

      // Trigger auto-titling for new sessions
      if (isNewSession) {
        this.chatService.getChatTitle(prompt).then(title => {
          this.history.updateSession(sessionId!, { title });
        }).catch(err => console.error('Auto-titling failed:', err));
      }

    } catch (error: any) {
      console.error('Portal: Chat error:', error);
      this.isLoading.set(false);
      this.pendingResponse.set(false);
      this.currentStatus.set(null);
      
      let errorMessage = 'I encountered an error connecting to our resources. Please try again later.';
      
      if (error.name === 'AbortError') {
        errorMessage = 'The request took too long to process. Please try again.';
      } else if (error.message) {
        errorMessage = error.message;
      }

      const sid = this.history.activeSessionId();
      if (sid) {
        this.history.updateLastMessage(sid, errorMessage);
        this.messages.set(this.history.getSession(sid)?.messages || []);
      } else {
        // Fallback for UI if no session
        this.messages.update(msgs => [...msgs, { role: 'assistant', content: errorMessage }]);
      }
    }
  }
}
