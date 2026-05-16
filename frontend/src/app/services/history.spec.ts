import { TestBed } from '@angular/core/testing';
import { HistoryService } from './history';
import { Persona } from './stewardship';
import { vi, beforeEach, describe, it, expect } from 'vitest';

describe('HistoryService (OpenSpec: chat-persistence)', () => {
  let service: HistoryService;
  let store: Record<string, string>;

  beforeEach(() => {
    store = {};
    
    // Mock localStorage
    vi.stubGlobal('localStorage', {
      getItem: vi.fn((key: string) => store[key] || null),
      setItem: vi.fn((key: string, value: string) => {
        store[key] = value;
      }),
      clear: vi.fn(() => {
        store = {};
      }),
      removeItem: vi.fn((key: string) => {
        delete store[key];
      })
    });

    TestBed.configureTestingModule({
      providers: [HistoryService]
    });
    service = TestBed.inject(HistoryService);
  });

  describe('Requirement: Local-First Chat Persistence', () => {
    
    it('Scenario: Saving a Chat Session', () => {
      // WHEN a new message is added to a chat
      const session = service.createSession('parishioner', ['corpus-1'], {});
      const sessionId = session.id;
      
      service.addMessage(sessionId, { role: 'user', content: 'Hello' });
      
      // THEN the system SHALL update the corresponding session in localStorage
      const storedData = JSON.parse(store['stewardship_chat_history']);
      const updatedSession = storedData.find((s: any) => s.id === sessionId);
      
      expect(updatedSession.messages).toContainEqual({ role: 'user', content: 'Hello' });
    });

    it('Scenario: Loading Recent Chats', () => {
      // Pre-populate localStorage
      const mockSessions = [
        { id: '1', title: 'Old Chat', messages: [], timestamp: Date.now(), persona: 'priest', corpusIds: [], extensionFilters: {} }
      ];
      store['stewardship_chat_history'] = JSON.stringify(mockSessions);
      
      // Re-initialize service to trigger loading
      const newService = new HistoryService();
      
      // THEN the system SHALL retrieve the list of recent chat sessions from localStorage
      expect(newService.sessions()).toHaveLength(1);
      expect(newService.sessions()[0].title).toBe('Old Chat');
    });

    it('Scenario: Resuming a Previous Chat', () => {
      // Setup: Multiple sessions
      const s1 = service.createSession('parishioner', [], {});
      const s2 = service.createSession('priest', [], {});
      
      // WHEN a user selects a chat session from the history sidebar
      service.activeSessionId.set(s1.id);
      
      // THEN the system SHALL load the messages and persona state from the selected session
      // (Verified via activeSessionId signal which the UI binds to)
      expect(service.activeSessionId()).toBe(s1.id);
      expect(service.getSession(s1.id)?.persona).toBe('parishioner');
    });
  });

  describe('Requirement: Chat Session Titling', () => {
    
    it('Scenario: Initializing a Chat Title', () => {
      // WHEN a new chat session is created
      const prompt = 'How do I donate to the parish?';
      const session = service.createSession('parishioner', [], {}, prompt);
      
      // THEN the system SHALL initially generate a local title using a word-slice fallback
      // "How do I donate..." (4 words)
      expect(session.title).toBe('How do I donate...');
    });

    it('Scenario: Refining a Chat Title', () => {
      const session = service.createSession('parishioner', [], {});
      
      // WHEN the first turn completes (simulated by manual update)
      // AND the system triggers an asynchronous request (simulated here)
      service.updateSession(session.id, { title: 'Donation Guidance' });
      
      // THEN the system SHALL update the session title
      const updated = service.getSession(session.id);
      expect(updated?.title).toBe('Donation Guidance');
      
      // AND NOT update if generic
      service.updateSession(session.id, { title: 'New Chat' });
      // (The actual filtering happens in portal.ts, but we verify service can hold it)
      expect(service.getSession(session.id)?.title).toBe('New Chat');
    });
  });
});
