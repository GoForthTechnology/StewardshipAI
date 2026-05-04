## Why

Currently, when a chat message is pending a response, a small static bubble is shown. This static visual does not clearly convey to the user that the system is actively processing their request. Animating the bubble with a moving ellipsis ("...") will provide better visual feedback that the request is still pending.

## What Changes

- Add a CSS animation for a moving ellipsis to the chat bubble component.
- Update the pending state in the UI to display the animated ellipsis instead of a static placeholder.

## Capabilities

### New Capabilities

### Modified Capabilities
- `web-interface`: Updating UI requirements to include an animated pending state for chat messages.

## Impact

- Frontend styles (`styles.css` or Tailwind config) to define the animation.
- Frontend chat component (`frontend/src/app/components/portal/portal.ts`) to implement the animated display.