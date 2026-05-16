## Why

The current portal sidebar is becoming cluttered with a mix of navigation, persona settings, and technical configuration. Moving persona selection to the chat header and making technical filters contextual will simplify the UI for general users while maintaining power-user capabilities for researchers.

## What Changes

- **Persona Selection Relocation**: Move the Persona selection from the sidebar to the chat header as a high-level "Mode" switcher.
- **Contextual Resource Filters**: Hide technical extension filters (PDF, Word, etc.) in the sidebar by default, showing them only when the "Researcher" persona is active.
- **Sidebar Prioritization**: Refactor the sidebar to prioritize Chat History (Recent Chats) and basic Corpus toggles.
- **Responsive Navigation**: Adapt the header persona switcher for mobile using a collapsible/expandable UI.

## Capabilities

### New Capabilities
- `responsive-navigation`: Requirements for the updated header navigation and mobile-specific persona switcher.

### Modified Capabilities
- `web-interface`: Update layout requirements to reflect the persona relocation and contextual filter behavior.
- `chat-persistence`: Refine titling logic requirements to include local fallback and robust LLM synchronization.

## Impact

- **Frontend Components**: `portal.ts`, `portal.html` (if applicable), and associated styling.
- **UX Flow**: General users (Parishioners/Priests) will see a cleaner sidebar; Researchers will maintain access to granular filters.
