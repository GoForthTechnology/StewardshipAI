## Why

The current StewardshipAI agent is configured as a "Strict Research Assistant," which results in a cold, robotic user experience. To better serve the priests and parishioners of the Catholic Diocese of Wichita, the system needs to transition into a "Stewardship Portal" with a warm, pastoral persona while maintaining its rigorous grounding in official sources.

## What Changes

- **Persona Shift**: Transition the system prompt from a robotic research assistant to a "Stewardship Guide" that is encouraging and pastoral.
- **Diocesan Branding**: Update the UI with "Catholic Diocese of Wichita" branding and traditional stewardship colors.
- **Persona Toggle**: Add a "I am a... [Parishioner / Priest]" selector to the UI to tailor the response tone and surface relevant quick-start questions.
- **Quick-Start Actions**: Implement buttons for common stewardship topics (Time, Talent, Treasure, Homily Inspiration) to aid discovery.
- **Pastoral Refusals**: Soften "out-of-scope" responses to be helpful redirects rather than cold denials.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `gcp-rag-agent`: Refine the system instruction to implement the "Stewardship Guide" persona and handle role-based (Priest/Parishioner) nuances.
- `web-interface`: Update the UI layout to include diocesan branding, a persona toggle, and quick-start action buttons.

## Impact

- `rag_agent.py`: Modification of the `SYSTEM_INSTRUCTION` and response logic to support dynamic role-based prompting.
- `app.py`: Significant UI refactor to support the new layout, branding, and interactive discovery elements.
- `config.py`: Addition of branding-related configuration (e.g., Diocese name).
