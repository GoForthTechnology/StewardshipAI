## Why

The application currently contains explicit branding and affiliation for the "Catholic Diocese of Wichita" in both the user interface and backend configuration. As the application is transitioning to a generic private prototype, this specific branding needs to be removed or generalized to allow for a broader or more neutral scope.

## What Changes

- **Backend Configuration**: Update default environment variables and configuration constants to remove "Diocese of Wichita".
- **Frontend UI**:
    - Update the Login screen to remove the diocese name.
    - Update the Portal sidebar and main content to remove the diocese name.
    - Rename CSS variables and classes from `diocese-*` (e.g., `diocese-blue`, `diocese-gold`) to more generic names (e.g., `brand-primary`, `brand-accent`).
- **Source Code**: Search and replace instances of "Wichita" and "Diocese" in component logic and templates.
- **Documentation/Scripts**: Update `deploy_manual.sh` and other supporting scripts to use generic defaults.

## Capabilities

### New Capabilities
- `generic-branding`: A capability ensuring the UI and backend use a customizable or neutral branding scheme instead of a hardcoded affiliation.

### Modified Capabilities
- `web-interface`: Update the visual requirements to remove specific religious/geographic branding.
- `api-backend`: Generalize the configuration for the stewardship guide persona.
- `gcp-rag-agent`: Neutralize system instructions and refusal messages.

## Impact

- **UI/UX**: All references to the Diocese of Wichita will be removed. The color scheme names in the code will change, but the actual colors will likely be preserved unless a new palette is requested.
- **Configuration**: `config.py` and `deploy_manual.sh` will have new default values.
- **Testing**: Frontend tests that check for specific branding strings will need to be updated.
