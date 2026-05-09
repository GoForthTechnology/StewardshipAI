## Context

The current Stewardship AI Portal is built with a desktop-first design using Tailwind CSS. The layout uses a fixed-width sidebar (`w-72`) and a flexible main chat area. On small screens, this sidebar consumes most of the horizontal space, making the chat interface unusable. The discovery grid also uses a two-column layout that becomes cramped on narrow viewports.

## Goals / Non-Goals

**Goals:**
- Implement a responsive layout that adapts to mobile (sm/md) and desktop (lg/xl) screen sizes.
- Transition the fixed sidebar to a collapsible side drawer on mobile.
- Create a mobile header with branding and menu controls.
- Ensure the chat interface and discovery grid are fully functional and readable on mobile.

**Non-Goals:**
- Completely redesigning the visual style or color palette.
- Implementing native mobile apps (iOS/Android)—this is a web optimization.
- Changing the backend API or RAG logic.

## Decisions

### Decision 1: Mobile-First CSS Strategy
- **Rationale**: While the current app is desktop-first, we will use Tailwind's responsive prefixes (`md:`, `lg:`) to "layer on" desktop styles, making the default (mobile) view clean and full-width.
- **Implementation**: Set the sidebar to `hidden` by default and use `lg:flex` to show it on larger screens.

### Decision 2: State-Managed Side Drawer
- **Rationale**: To handle the drawer visibility on mobile, we need a simple boolean state in `PortalComponent`.
- **Implementation**: Add an `isMenuOpen` signal and toggle it via a hamburger menu in the new mobile header.

### Decision 3: "Sticky" and Compact Mobile Header
- **Rationale**: On small screens, users need a persistent reference for where they are and how to access the menu, without losing valuable chat vertical space.
- **Implementation**: A height-constrained (`h-14`) header that is only visible below the `lg` breakpoint.

## Risks / Trade-offs

- **[Risk] Touch Target Size** → **Mitigation**: Use larger padding and standard touch heights (min 44px) for all mobile-visible buttons.
- **[Risk] Keyboard Overlap** → **Mitigation**: Use `flex-col` with `h-screen` and `overflow-hidden` to ensure the chat input remains at the bottom of the viewport.
