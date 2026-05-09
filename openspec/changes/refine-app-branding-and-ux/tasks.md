## 1. Branding & Application Identity

- [x] 1.1 Update `diocese_name` default value in `terraform/variables.tf` to "Stewardship Portal".
- [x] 1.2 Update the site favicon to the Dove icon in `frontend/src/index.html` (verify icon availability or convert from existing SVG).
- [x] 1.3 Ensure the application title in `frontend/src/app/components/portal/portal.ts` and `app.html` uses the centralized `diocese_name`.

## 2. UX Polish & Animations

- [x] 2.1 Add CSS transition for sidebar expansion/collapse in `frontend/src/app/app.css`.
- [x] 2.2 Implement "lift" hover effect for discovery grid cards in `frontend/src/app/components/discovery-grid/discovery-grid.css`.
- [x] 2.3 Implement hover visual feedback for sidebar navigation items.

## 3. Layout & Alignment

- [x] 3.1 Define global layout CSS variables for gutters and padding in `frontend/src/styles.css`.
- [x] 3.2 Refactor header and main content container padding to ensure consistent vertical alignment.
- [x] 3.3 Verify responsive alignment for mobile view (collapsible drawer).

## 4. Verification

- [x] 4.1 Verify "Stewardship Portal" name appears correctly in header and login.
- [x] 4.2 Verify Dove favicon is displayed in browser tabs.
- [x] 4.3 Verify smooth sidebar animations and card hover effects.
