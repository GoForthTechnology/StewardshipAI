import { Injectable, signal, effect } from '@angular/core';
import { ChatMessage } from './chat';
import { Persona } from './stewardship';

export interface ChatSession {
  id: string;
  title: string;
  timestamp: number;
  persona: Persona;
  messages: ChatMessage[];
  activeFile?: { name: string, uri: string, mimeType: string };
  corpusIds: string[];
  extensionFilters: Record<string, string[]>;
}

@Injectable({
  providedIn: 'root'
})
export class HistoryService {
  private readonly STORAGE_KEY = 'stewardship_chat_history';
  
  sessions = signal<ChatSession[]>([]);
  activeSessionId = signal<string | null>(null);

  constructor() {
    this.loadSessions();
    
    // Auto-save sessions whenever they change
    effect(() => {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.sessions()));
    });
  }

  private loadSessions() {
    const stored = localStorage.getItem(this.STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        this.sessions.set(parsed);
      } catch (e) {
        console.error('Failed to parse chat history:', e);
        this.sessions.set([]);
      }
    }
  }

  getSessions() {
    return this.sessions().sort((a, b) => b.timestamp - a.timestamp);
  }

  getSession(id: string) {
    return this.sessions().find(s => s.id === id);
  }

  private generateId(): string {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      return crypto.randomUUID();
    }
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
  }

  createSession(persona: Persona, corpusIds: string[], extensionFilters: Record<string, string[]>, firstPrompt?: string): ChatSession {
    console.log('HistoryService: Creating new session', { persona });
    
    // Generate a local fallback title from the first prompt if available
    let initialTitle = 'New Chat';
    if (firstPrompt) {
      initialTitle = firstPrompt.trim().split(/\s+/).slice(0, 4).join(' ');
      if (firstPrompt.length > initialTitle.length) initialTitle += '...';
    }

    const newSession: ChatSession = {
      id: this.generateId(),
      title: initialTitle,
      timestamp: Date.now(),
      persona,
      messages: [],
      corpusIds,
      extensionFilters
    };
    
    this.sessions.update(s => [...s, newSession]);
    this.activeSessionId.set(newSession.id);
    return newSession;
  }

  updateSession(id: string, updates: Partial<ChatSession>) {
    this.sessions.update(sessions => 
      sessions.map(s => s.id === id ? { ...s, ...updates, timestamp: Date.now() } : s)
    );
  }

  deleteSession(id: string) {
    this.sessions.update(sessions => sessions.filter(s => s.id !== id));
    if (this.activeSessionId() === id) {
      this.activeSessionId.set(null);
    }
  }

  addMessage(sessionId: string, message: ChatMessage) {
    this.sessions.update(sessions => 
      sessions.map(s => {
        if (s.id === sessionId) {
          return { ...s, messages: [...s.messages, message], timestamp: Date.now() };
        }
        return s;
      })
    );
  }

  updateLastMessage(sessionId: string, content: string) {
    this.sessions.update(sessions => 
      sessions.map(s => {
        if (s.id === sessionId) {
          const newMessages = [...s.messages];
          if (newMessages.length > 0) {
            newMessages[newMessages.length - 1] = { 
              ...newMessages[newMessages.length - 1], 
              content 
            };
          }
          return { ...s, messages: newMessages, timestamp: Date.now() };
        }
        return s;
      })
    );
  }
}
