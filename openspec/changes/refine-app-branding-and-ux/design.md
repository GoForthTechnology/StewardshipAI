## Context

The application is transitioning to a more refined identity as the "Stewardship Portal." While the core functionality is established, the visual presentation needs alignment with this new brand and general UX improvements to feel like a modern, responsive web application.

## Goals / Non-Goals

**Goals:**
- Update all instances of the application name to "Stewardship Portal."
- Implement the Dove icon as the favicon.
- Add smooth animations for sidebar transitions.
- Enhance interactivity with hover states for key components.
- Standardize spacing and alignment in the main portal layout.

**Non-Goals:**
- Changing the underlying RAG logic or persona behaviors.
- Re-architecting the component structure.
- Introducing a complex theme switching system (beyond the existing palette).

## Decisions

### Decision 1: Centralized Branding Variable
- **Rationale**: Update the `diocese_name` variable in Terraform to "Stewardship Portal" and ensure the frontend dynamically reflects this.
- **Alternatives**: Hardcoding the name in multiple Angular components (Rejected for maintainability).

### Decision 2: CSS Transition for Sidebar
- **Rationale**: Use CSS transitions on the `width` or `transform` property of the sidebar to provide a smooth expansion/collapse effect. This is lightweight and high-impact.
- **Alternatives**: JavaScript-based animations (Rejected as unnecessary for simple layout shifts).

### Decision 3: Standardizing "Lift" Hover Effect
- **Rationale**: Interactive cards (Discovery Grid) and navigation items will use a consistent `translateY(-2px)` and subtle box-shadow increase on hover to provide clear tactile feedback.

### Decision 4: Global Layout Variables
- **Rationale**: Define CSS variables for `--portal-gutter` and `--portal-padding` in `styles.css` to ensure perfectly aligned vertical gutters between the header and chat content.

## Risks / Trade-offs

- **[Risk] Layout Jitter during Animation** → **Mitigation**: Use `will-change: transform` or ensure layout shifts are calculated correctly by the browser during transition.
- **[Risk] Favicon Caching** → **Mitigation**: Update the favicon filename or add a query string (e.g., `favicon.ico?v=2`) to force browser refresh.
