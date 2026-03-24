# Agents

## DataGuide UI Agent

### Purpose
- Manage navigation and theme behavior across the Data Guide static site.
- Keep topbar interaction consistent across pages and screen sizes.

### Capabilities
- responsive hamburger menu control
- desktop and mobile layout adaptation
- theme toggle state persistence (dark/light)

### Files
- `assets/js/app.js`: core behavior and DOM interaction logic
- `source/styles.css`: topbar, menu and mobile style rules

### Usage
- This is a static site that runs in browser; no server-side agent runtime required.
- For local development, simply open `index.html` or run with any static web server (e.g., VS Code Live Server).