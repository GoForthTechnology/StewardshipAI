## Context

Currently, when the user submits a message and the system is fetching a response, a static placeholder or bubble is shown. This design addresses the need for an animated visual indicator (moving ellipsis) to improve user feedback during this pending state.

## Goals / Non-Goals

**Goals:**
- Implement a CSS-based "bouncing ellipsis" animation.
- Integrate the animation into the existing Angular chat component.
- Ensure the animation is lightweight and follows the project's aesthetic.

**Non-Goals:**
- Replacing the entire loading state or introducing complex progress bars.
- Modifying backend streaming logic.

## Decisions

### 1. CSS Keyframes Animation
Use standard CSS `@keyframes` to animate the opacity or position of three dots.
- **Rationale**: CSS animations are performant and easily managed within the Angular component's styles.
- **Alternatives**: Using an external GIF or SVG animation (increases asset load) or JavaScript-driven animation (more overhead).

### 2. Integration into `portal.ts`
Add a `isPending` state to the chat messages or a separate placeholder message object that displays when `chatService.sendMessage` is called and before the stream starts.
- **Rationale**: Leverages existing component state logic.

## Risks / Trade-offs

- **[Risk]** Animation might be visually distracting if too fast. → **Mitigation**: Use subtle timing (e.g., 1.4s duration with ease-in-out).
- **[Risk]** Layout shift when dots appear/disappear. → **Mitigation**: Use fixed-width containers for the ellipsis bubble.