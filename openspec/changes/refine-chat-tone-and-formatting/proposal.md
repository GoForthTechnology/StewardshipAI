## Why

The current agent responses are perceived as "pandering" and contain technical artifacts like raw email addresses in greetings, which detracts from a professional and pastoral user experience. Additionally, the formatting of long responses often results in dense blocks of text or inconsistent markdown usage that is difficult to read in the portal interface.

## What Changes

- **MODIFICATION**: Update system instructions to remove the requirement to greet users by their email address.
- **MODIFICATION**: Refine the "Pastoral Tone" to be more direct and concise, avoiding overly flowery or repetitive language.
- **MODIFICATION**: Improve markdown output formatting to ensure consistent spacing, readable lists, and appropriate use of headers for better clarity in the Angular UI.
- **MODIFICATION**: Remove unnecessary preamble and postamble text that adds "fluff" to the response.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `gcp-rag-agent`: Refine system instructions for tone, user identity handling, and formatting.
- `web-interface`: Ensure the Angular component handles the refined markdown output cleanly (e.g., proper spacing for lists).

## Impact

- `rag_agent.py`: `SYSTEM_INSTRUCTION` and persona-specific instructions will be updated.
- `frontend/`: `PortalComponent` CSS or template might need minor adjustments for improved markdown rendering (e.g., list indentation).
