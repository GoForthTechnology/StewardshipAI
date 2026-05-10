import { Injectable, inject } from '@angular/core';
import { Auth } from '@angular/fire/auth';
import { environment } from '../../environments/environment';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private auth = inject(Auth);

  async uploadFile(file: File): Promise<{ file_uri: string, display_name: string, mime_type: string }> {
    const currentUser = this.auth.currentUser;
    if (!currentUser) throw new Error('Not authenticated');

    const token = await currentUser.getIdToken();
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${environment.apiUrl}/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Upload failed');
    }

    return response.json();
  }

  async *streamChat(prompt: string, persona: string, history: ChatMessage[] = [], file_uri?: string, mime_type?: string) {
    const currentUser = this.auth.currentUser;
    if (!currentUser) throw new Error('Not authenticated');

    const token = await currentUser.getIdToken();
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // Increased timeout for large files

    try {
      const response = await fetch(`${environment.apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ prompt, persona, history, file_uri, mime_type }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No readable stream in response');

      const decoder = new TextDecoder();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              yield data;
            } catch (e) {
              console.error('Error parsing SSE chunk:', e);
            }
          }
        }
      }
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }
}
