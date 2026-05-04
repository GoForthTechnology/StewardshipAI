import { Pipe, PipeTransform, inject } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Marked } from 'marked';

@Pipe({
  name: 'markdown',
  standalone: true
})
export class MarkdownPipe implements PipeTransform {
  private sanitizer = inject(DomSanitizer);
  private marked = new Marked();

  transform(value: string | null | undefined): SafeHtml {
    if (!value) return '';
    
    try {
      // Use synchronous parse
      const html = this.marked.parse(value, { async: false }) as string;
      return this.sanitizer.bypassSecurityTrustHtml(html);
    } catch (e) {
      console.error('Markdown parsing error:', e);
      return value;
    }
  }
}
