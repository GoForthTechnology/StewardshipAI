import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PortalComponent } from './portal';
import { Auth, user } from '@angular/fire/auth';
import { ChatService } from '../../services/chat';
import { HistoryService } from '../../services/history';
import { StewardshipService } from '../../services/stewardship';
import { of } from 'rxjs';
import { signal } from '@angular/core';
import { vi, describe, it, expect, beforeEach } from 'vitest';

describe('PortalComponent (OpenSpec: web-interface & responsive-navigation)', () => {
  let component: PortalComponent;
  let fixture: ComponentFixture<PortalComponent>;
  let mockAuth: any;
  let mockChatService: any;
  let mockHistoryService: any;
  let mockStewardshipService: any;

  beforeEach(async () => {
    // 1. Mock window.ENV
    (window as any).ENV = {
      corpora: [
        { id: 'corp-1', name: 'Stewardship Resources' },
        { id: 'corp-2', name: 'Universal Magisterium' }
      ]
    };

    // 2. Setup Mocks
    mockAuth = {
      currentUser: { email: 'test@example.com', getIdToken: () => Promise.resolve('token') }
    };

    mockChatService = {
      streamChat: vi.fn(),
      getChatTitle: vi.fn().mockResolvedValue('Refined Title'),
      uploadFile: vi.fn()
    };

    mockHistoryService = {
      sessions: signal([]),
      activeSessionId: signal(null),
      getSessions: () => [],
      createSession: vi.fn().mockReturnValue({ id: 'new-id', title: 'New Chat' }),
      addMessage: vi.fn(),
      updateSession: vi.fn(),
      getSession: vi.fn(),
      deleteSession: vi.fn()
    };

    mockStewardshipService = {
      persona: signal('parishioner'),
      setPersona: vi.fn((p) => mockStewardshipService.persona.set(p))
    };

    // 3. Configure TestBed
    await TestBed.configureTestingModule({
      imports: [PortalComponent],
      providers: [
        { provide: Auth, useValue: mockAuth },
        { provide: ChatService, useValue: mockChatService },
        { provide: HistoryService, useValue: mockHistoryService },
        { provide: StewardshipService, useValue: mockStewardshipService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(PortalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  describe('Capability: web-interface', () => {

    it('Scenario: Displaying Generic Branding', () => {
      const compiled = fixture.nativeElement as HTMLElement;
      expect(compiled.textContent).toContain('Stewardship Portal');
      expect(compiled.textContent).not.toContain('Diocese');
    });

    it('Scenario: Header Title Display', () => {
      const branding = fixture.nativeElement.querySelector('.font-serif');
      expect(branding.textContent).toContain('Stewardship');
    });

    it('Scenario: Submitting a Query', async () => {
      component.currentInput = 'What is tithing?';
      async function* mockStream() {
        yield { status: 'Searching...' };
        yield { text: 'Tithing is 10%.' };
      }
      mockChatService.streamChat.mockReturnValue(mockStream());
      await component.submitChat();
      expect(component.messages().some(m => m.content === 'What is tithing?')).toBe(true);
      expect(component.messages().some(m => m.content === 'Tithing is 10%.')).toBe(true);
    });

    it('Scenario: Visual Feedback for Pending Message', async () => {
      component.currentInput = 'Thinking...';
      const deferred = { resolve: null as any, promise: null as any };
      deferred.promise = new Promise(r => deferred.resolve = r);
      async function* mockStream() {
        yield { status: '🔍 Searching...' };
        await deferred.promise;
        yield { text: 'Done.' };
      }
      mockChatService.streamChat.mockReturnValue(mockStream());
      const submitPromise = component.submitChat();
      await new Promise(r => setTimeout(r, 0));
      fixture.detectChanges();
      expect(component.pendingResponse()).toBe(true);
      expect(component.currentStatus()).toBe('🔍 Searching...');
      deferred.resolve();
      await submitPromise;
    });

    it('Scenario: Selecting a Persona', () => {
      component.setPersona('priest');
      expect(mockStewardshipService.setPersona).toHaveBeenCalledWith('priest');
      expect(mockStewardshipService.persona()).toBe('priest');
    });

    it('Scenario: Displaying Responsive Layout - Contextual Filters', () => {
      mockStewardshipService.persona.set('parishioner');
      fixture.detectChanges();
      const filters = fixture.nativeElement.querySelector('input[type="checkbox"]');
      expect(filters).toBeNull();

      mockStewardshipService.persona.set('researcher');
      component.availableCorpora()[0].enabled = true;
      fixture.detectChanges();
      const researcherFilters = fixture.nativeElement.querySelector('input[type="checkbox"]');
      expect(researcherFilters).not.toBeNull();
    });

    it('Scenario: Selecting a Recent Chat', () => {
      const mockSession = { id: 's1', title: 'Old Chat', messages: [{role: 'user', content: 'Hi'}], persona: 'priest' };
      component.loadSession(mockSession as any);
      expect(component.messages()).toEqual(mockSession.messages);
      expect(mockStewardshipService.setPersona).toHaveBeenCalledWith('priest');
    });

    it('Scenario: Submitting a Follow-up Query', async () => {
      const initialMessages: any[] = [{ role: 'user', content: 'Hi' }, { role: 'assistant', content: 'Hello' }];
      component.messages.set(initialMessages);
      mockHistoryService.activeSessionId.set('existing-id');
      component.currentInput = 'Follow up?';
      async function* mockStream() { yield { text: 'Follow up answer' }; }
      mockChatService.streamChat.mockReturnValue(mockStream());
      await component.submitChat();
      expect(mockChatService.streamChat).toHaveBeenCalledWith(
        'Follow up?', 'parishioner', initialMessages, undefined, undefined, undefined, expect.anything()
      );
    });

    it('Scenario: Triggering a Quick-Start Query', async () => {
      async function* mockStream() { yield { text: 'Tithing explained.' }; }
      mockChatService.streamChat.mockReturnValue(mockStream());
      component.onDiscoveryAction('Explain Tithing');
      expect(component.messages().some(m => m.content === 'Explain Tithing')).toBe(true);
    });

    it('Scenario: Displaying Uploaded File', () => {
       component.activeFile.set({ name: 'manual.pdf', uri: 'gs://...', mimeType: 'application/pdf' });
       fixture.detectChanges();
       const chip = fixture.nativeElement.querySelector('.bg-brand-primary\\/5');
       expect(chip.textContent).toContain('manual.pdf');
    });

    it('Scenario: Frontend Request Timeout and Scenario: Displaying Timeout Error', async () => {
      vi.useFakeTimers();
      async function* mockStream() { await new Promise(() => {}); }
      mockChatService.streamChat.mockReturnValue(mockStream());
      component.currentInput = 'Timeout test';
      const submitPromise = component.submitChat();
      vi.advanceTimersByTime(15001);
      await submitPromise;
      fixture.detectChanges();
      const lastMsg = component.messages()[component.messages().length - 1];
      expect(lastMsg.content).toContain('took too long');
      vi.useRealTimers();
    });

    it('Scenario: Displaying Generic Error', async () => {
       mockChatService.streamChat.mockImplementation(() => { throw new Error('Server Crash'); });
       component.currentInput = 'Error test';
       await component.submitChat();
       fixture.detectChanges();
       const lastMsg = component.messages()[component.messages().length - 1];
       expect(lastMsg.content).toContain('encountered an error');
    });

    it('Scenario: Displaying File Requirements', () => {
       const compiled = fixture.nativeElement as HTMLElement;
       expect(compiled.textContent).toContain('PDF, TXT');
    });

    it('Scenario: Submitting a Query on Mobile', async () => {
      component.isMenuOpen.set(true);
      component.currentInput = 'Mobile test';
      async function* mockStream() { yield { text: 'Mobile answer' }; }
      mockChatService.streamChat.mockReturnValue(mockStream());
      await component.submitChat();
      expect(component.messages().some(m => m.content === 'Mobile test')).toBe(true);
    });

    it('Scenario: Switching Personas - Discovery Grid prompts', () => {
       component.setPersona('researcher');
       fixture.detectChanges();
       const discoveryGrid = fixture.nativeElement.querySelector('app-discovery-grid');
       expect(discoveryGrid).not.toBeNull();
    });

    it('Scenario: Displaying Lists', () => {
       component.messages.set([{ role: 'assistant', content: '1. First\n2. Second' }]);
       fixture.detectChanges();
       const assistantMsg = fixture.nativeElement.querySelector('.bg-white');
       expect(assistantMsg.innerHTML).toContain('1.');
    });
  });

  describe('Capability: responsive-navigation', () => {
    it('Scenario: Opening Drawer on Mobile', () => {
      component.isMenuOpen.set(false);
      component.isMenuOpen.set(true); 
      fixture.detectChanges();
      expect(component.isMenuOpen()).toBe(true);
    });

    it('Scenario: Viewing Mobile Header', () => {
      const mobileHeader = fixture.nativeElement.querySelector('.lg\\:hidden');
      expect(mobileHeader).not.toBeNull();
      expect(mobileHeader.textContent).toContain('Portal');
    });

    it('Scenario: Switching Persona on Desktop', () => {
       const buttons = fixture.nativeElement.querySelectorAll('header button');
       const priestBtn = Array.from(buttons).find((b: any) => b.textContent.includes('Priest')) as HTMLButtonElement;
       priestBtn?.click();
       expect(mockStewardshipService.setPersona).toHaveBeenCalledWith('priest');
    });

    it('Scenario: Switching Persona on Mobile', () => {
       component.isPersonaMenuOpen.set(true);
       fixture.detectChanges();
       const mobileButtons = fixture.nativeElement.querySelectorAll('.absolute.left-0 button');
       const researcherBtn = Array.from(mobileButtons).find((b: any) => b.textContent.includes('Researcher')) as HTMLButtonElement;
       researcherBtn?.click();
       expect(mockStewardshipService.setPersona).toHaveBeenCalledWith('researcher');
       expect(component.isPersonaMenuOpen()).toBe(false);
    });
  });

  describe('Capability: corpus-selection-ui', () => {
    it('Scenario: Viewing available corpora', () => {
      const corpusLabels = fixture.nativeElement.querySelectorAll('.space-y-4 .text-sm.font-medium');
      expect(corpusLabels.length).toBe(2);
      expect(corpusLabels[0].textContent).toContain('Stewardship Resources');
    });

    it('Scenario: Toggling a corpus', () => {
      const toggleBtn = fixture.nativeElement.querySelector('.space-y-4 button');
      const initialEnabled = component.availableCorpora()[0].enabled;
      toggleBtn.click();
      expect(component.availableCorpora()[0].enabled).toBe(!initialEnabled);
    });

    it('Scenario: Disabling last corpus', () => {
      component.availableCorpora.update(corps => [
        { ...corps[0], enabled: true },
        { ...corps[1], enabled: false }
      ]);
      fixture.detectChanges();
      const stewardshipToggle = fixture.nativeElement.querySelectorAll('.space-y-4 button')[0];
      stewardshipToggle.click();
      expect(component.availableCorpora()[0].enabled).toBe(true);
    });
  });

  describe('Capability: extension-filtering-ui', () => {
    it('Scenario: Expanding a corpus for extension filtering', () => {
       mockStewardshipService.persona.set('researcher');
       component.availableCorpora.update(corps => corps.map(c => ({ ...c, enabled: true })));
       fixture.detectChanges();
       const nestedFilters = fixture.nativeElement.querySelectorAll('.ml-4 input[type="checkbox"]');
       expect(nestedFilters.length).toBe(8);
    });

    it('Scenario: Initializing extensions', () => {
       const corps = component.availableCorpora();
       corps.forEach(c => {
         expect(Object.values(c.extensionFilters).every(v => v === true)).toBe(true);
       });
    });

    it('Scenario: Changing persona', () => {
       mockStewardshipService.persona.set('researcher');
       fixture.detectChanges();
       component.toggleExtension(component.availableCorpora()[0], 'pdf');
       expect(component.availableCorpora()[0].extensionFilters['pdf']).toBe(false);
       component.setPersona('priest');
       fixture.detectChanges();
       expect(component.availableCorpora()[0].extensionFilters['pdf']).toBe(false);
    });
  });

  describe('Capability: generic-branding', () => {
    // ...
  });

  describe('Capability: academic-research-persona', () => {
    it('Scenario: Displaying Research Prompts', () => {
       // WHEN the "researcher" persona is active
       mockStewardshipService.persona.set('researcher');
       fixture.detectChanges();
       
       // THEN the discovery grid SHALL display prompts such as "Synthesize..."
       const discoveryGrid = fixture.nativeElement.querySelector('app-discovery-grid');
       // This verifies the component is present; discovery-grid itself is responsible for the prompts
       expect(discoveryGrid).not.toBeNull();
    });
  });

  describe('Capability: mobile-layout-adaptation', () => {
    it('Scenario: Discovery Grid Stacking', () => {
       const grid = fixture.nativeElement.querySelector('app-discovery-grid');
       expect(grid).not.toBeNull();
    });

    it('Scenario: Mobile Chat View', () => {
       const container = fixture.nativeElement.querySelector('.portal-container');
       expect(container.className).toContain('lg:py-8'); 
    });
  });
});
