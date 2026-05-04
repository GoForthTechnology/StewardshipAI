## 1. Configuration & Persona Refinement

- [x] 1.1 Add `DIOCESE_NAME` to `GCPConfig` in `config.py` with default "Catholic Diocese of Wichita".
- [x] 1.2 Refactor `SYSTEM_INSTRUCTION` in `rag_agent.py` to support "Stewardship Guide" persona and role-based templates.
- [x] 1.3 Update `GCPRagAgent.generate_response` to accept a `persona` argument.

## 2. UI Rebranding & Theming

- [x] 2.1 Update `app.py` page configuration and title for the "Stewardship Portal".
- [x] 2.2 Inject custom CSS into `app.py` for branding (Diocese colors/styles).
- [x] 2.3 Implement the persona selection toggle (Parishioner vs. Priest) in the sidebar.

## 3. Discovery Elements

- [x] 3.1 Implement the "Quick-Start" button grid on the main page.
- [x] 3.2 Wire up "Quick-Start" buttons to trigger agent queries automatically.
- [x] 3.3 Ensure the assistant response incorporates the selected persona context.

## 4. Verification

- [x] 4.1 Update `verify_rag.py` with test cases for pastoral refusal messages.
- [x] 4.2 Verify persona-specific tone shifts (Priest vs. Parishioner) manually or with sample prompts.

## 5. UI Polish & Contrast Fixes

- [x] 5.1 Fix title contrast by explicitly setting title color to deep blue.
- [x] 5.2 Improve sidebar readability by ensuring all labels and radio button text are white.
- [x] 5.3 Polish "Quick-Start" buttons with better contrast and hover states.
