## Why

The current web interface of the Stewardship AI Portal is built with a desktop-first layout, featuring a fixed-width sidebar and a multi-column discovery grid. This design results in a suboptimal user experience on mobile and small-screen devices, where the sidebar consumes a significant portion of the screen real estate and the layout becomes cramped. To improve accessibility and usability for mobile users, the application needs a responsive refactor.

## What Changes

- **Navigation**: Transition the fixed sidebar into a collapsible side-drawer accessible via a hamburger menu on small screens.
- **Layout**: Implement responsive breakpoints to adjust padding, margins, and component widths for mobile devices.
- **Discovery Grid**: Refactor the discovery grid to stack vertically or use a more mobile-friendly presentation on small screens.
- **Chat Input**: Optimize the chat input bar for mobile touch targets and ensure it remains visible and usable when the on-screen keyboard is active.
- **Header**: Add a mobile-specific header that includes the branding and navigation trigger.

## Capabilities

### New Capabilities
- `responsive-navigation`: A capability providing a collapsible navigation drawer and mobile-optimized header.
- `mobile-layout-adaptation`: Automated layout adjustments based on screen size, including optimized spacing and component stacking.

### Modified Capabilities
- `web-interface`: Update the layout requirements to include responsive behavior and mobile-first design principles.

## Impact

- **UI Components**: `PortalComponent` and `DiscoveryGridComponent` will require template and CSS updates.
- **Global Styles**: `styles.css` will be updated with global responsive utility classes and breakpoints.
- **User Experience**: Mobile users will have a full-screen chat experience with easy access to navigation and personas.
