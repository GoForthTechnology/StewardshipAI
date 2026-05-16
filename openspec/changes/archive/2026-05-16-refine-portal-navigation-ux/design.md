## Context

The current `PortalComponent` in `portal.ts` uses a single sidebar to house all controls. This includes `HistoryService` integration for recent chats, `StewardshipService` for persona, and internal `availableCorpora` signals for RAG configuration. The result is a crowded sidebar where configuration options overwhelm the primary navigation task (chatting).

## Goals / Non-Goals

**Goals:**
- Move Persona selection to the main chat header.
- Implement contextual visibility for extension filters.
- Improve sidebar layout to focus on History and basic Corpus selection.

**Non-Goals:**
- Changing the backend API or RAG logic.
- Adding new personas or corpora.
- Changing the authentication flow.

## Decisions

### Decision 1: Header Persona Switcher (Segmented Control)
- **Rationale**: On desktop, a segmented control (button group) in the header provides immediate visibility of the active "mode". On mobile, this will collapse into a dropdown or a single active pill to save space.
- **Alternatives**: Keeping it in the sidebar (rejected as it adds clutter).

### Decision 2: Contextual Extension Filters (v-if / ngIf)
- **Rationale**: Using a simple conditional check on the active persona (`persona === 'researcher'`) allows us to hide the technical checkboxes for non-researchers, reducing cognitive load for the majority of users.
- **Alternatives**: A "Power User" toggle (rejected as it's an extra step compared to persona-based context).

### Decision 3: Sidebar Sectioning
- **Rationale**: We will use clear semantic headings and spacing to separate "Recent Chats" (top priority) from "Settings" (Corpus toggles at the bottom). 
- **Alternatives**: Moving Corpus toggles to the header as well (rejected to avoid overcrowding the header).

## Risks / Trade-offs

- **[Risk] Mobile Header Space** → **Mitigation**: Use a condensed UI (icon-only or single-label dropdown) for persona selection on small screens.
- **[Risk] Discovery of Filters** → **Mitigation**: Ensure that when a user switches to "Researcher," the expansion of the sidebar filters is visually hinted (using an animation).
