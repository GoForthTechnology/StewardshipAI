import { Injectable, signal } from '@angular/core';

export type Persona = 'parishioner' | 'priest';

@Injectable({
  providedIn: 'root'
})
export class StewardshipService {
  persona = signal<Persona>('parishioner');

  setPersona(newPersona: Persona) {
    this.persona.set(newPersona);
  }
}
