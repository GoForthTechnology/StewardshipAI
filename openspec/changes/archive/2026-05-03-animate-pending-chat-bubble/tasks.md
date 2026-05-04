## 1. Styles Implementation

- [x] 1.1 Add `@keyframes` for the ellipsis animation in `frontend/src/styles.css` or the component's CSS.
- [x] 1.2 Define the `.dot` and `.animation-container` classes with appropriate bounce/pulse timing.

## 2. Component Logic Update

- [x] 2.1 Update `frontend/src/app/components/portal/portal.ts` to include a `pendingResponse` boolean state.
- [x] 2.2 Set `pendingResponse = true` when a query is submitted.
- [x] 2.3 Set `pendingResponse = false` once the first response chunk is received or the stream finishes.

## 3. Template and Layout

- [x] 3.1 Modify the `portal.ts` inline template (or separate HTML) to conditionally render the animated bubble when `pendingResponse` is true.
- [x] 3.2 Ensure the animated bubble matches the assistant's message styling.

## 4. Verification

- [x] 4.1 Verify the animation appears immediately after clicking send.
- [x] 4.2 Verify the animation is replaced by the actual response text smoothly.