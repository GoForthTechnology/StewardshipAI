## 1. Global Style Refactor

- [x] 1.1 Add responsive utility classes and breakpoints to `frontend/src/styles.css`.
- [x] 1.2 Implement a "mobile-only" hidden state for the main sidebar.

## 2. Portal Component Enhancements

- [x] 2.1 Add `isMenuOpen` signal to `PortalComponent` in `portal.ts`.
- [x] 2.2 Create the mobile header with hamburger menu icon and "🕊️ Portal" branding.
- [x] 2.3 Refactor the sidebar template to support absolute positioning (drawer mode) on mobile.
- [x] 2.4 Add click-outside or "Close" button logic to the mobile drawer.

## 3. Discovery Grid & Content Optimization

- [x] 3.1 Refactor `discovery-grid.ts` to stack cards vertically on small screens.
- [x] 3.2 Adjust chat bubble max-width and padding for better mobile readability.
- [x] 3.3 Optimize the chat input bar and send button for mobile touch targets.

## 4. Final Validation

- [x] 4.1 Verify mobile layout using Chrome DevTools (Responsive mode).
- [x] 4.2 Verify desktop layout remains unaffected.
- [x] 4.3 Ensure the side drawer correctly handles persona selection and sign-out on mobile.
