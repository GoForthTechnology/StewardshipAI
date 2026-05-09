## 1. Backend Refactor

- [x] 1.1 Update `config.py` default `diocese_name` to "Stewardship AI Portal".
- [x] 1.2 Update `deploy_manual.sh` to remove Wichita-specific variable defaults.

## 2. Frontend Style Normalization

- [x] 2.1 Rename CSS variables in `frontend/src/styles.css` from `diocese-*` to `brand-*`.
- [x] 2.2 Update all component templates and CSS files to use the new `brand-*` classes.
- [x] 2.3 Verify `frontend/src/styles.compiled.css` is updated or regeneratable.

## 3. UI Text & Component Updates

- [x] 3.1 Remove "Catholic Diocese of Wichita" from `login.ts`.
- [x] 3.2 Remove "Catholic Diocese of Wichita" from `portal.ts`.
- [x] 3.3 Review and generalize labels in `discovery-grid.ts`.

## 4. Testing & Validation

- [x] 4.1 Update Playwright tests in `frontend/verify-styles.spec.ts` to reflect the name and style changes.
- [x] 4.2 Run frontend tests to ensure no regressions in layout or branding.
- [x] 4.3 Manually verify the app identity in the local UI.
