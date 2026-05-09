## Context

The application was originally developed with a specific branding and affiliation for the "Catholic Diocese of Wichita". As it transitions to a generic private prototype, these hardcoded references create unnecessary friction and lack of neutrality. The goal is to decouple the UI and backend from this specific organization.

## Goals / Non-Goals

**Goals:**
- Remove all explicit text references to "Diocese of Wichita".
- Renameorganizzazione-specific CSS tokens (e.g., `diocese-blue`) to generic ones (e.g., `brand-primary`).
- Update configuration defaults in the backend to be neutral.
- Maintain the same professional visual style and functionality.

**Non-Goals:**
- Changing the underlying color palette (the actual hex codes will likely remain the same for now).
- Implementing a full multi-tenancy system (this is a simplification, not an expansion).
- Removing the RAG corpus or stewardship theme entirely—just the specific organizational affiliation.

## Decisions

### Decision 1: Rename CSS Variables in `styles.css`
- **Rationale**: Using `brand-*` instead of `diocese-*` makes the codebase more professional and easier to rebrand in the future.
- **Implementation**: Update `styles.css` and all component templates/CSS.

### Decision 2: Generalize `config.py` Defaults
- **Rationale**: The default `DIOCESE_NAME` should be something neutral like "Stewardship AI Portal".
- **Implementation**: Change the default value in `config.py` and ensure the prompt system handles it gracefully.

### Decision 3: Update Discovery Grid Cards
- **Rationale**: Some cards contain religious terminology that, while related to stewardship, can be presented more neutrally if desired.
- **Implementation**: Review and update the discovery grid labels to be descriptive rather than organizational.

## Risks / Trade-offs

- **[Risk] Broken Styles** → **Mitigation**: Perform a global search and replace for CSS class names and ensure the compiled CSS is updated.
- **[Risk] Test Failures** → **Mitigation**: Update Playwright/unit tests that expect specific "Wichita" strings.
