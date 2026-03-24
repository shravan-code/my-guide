# Skills

## Navigation and UI Enhancement Skill

### Description
Add and maintain consistent navigation experience:
- `Hamburger menu` at right side in mobile view
- `Data Guide` brand on left
- `theme toggle` in header-actions
- `menu` visibility toggle
- closing menu on outside click

### Implementation
- JavaScript: `assets/js/app.js`
- CSS: `assets/css/styles.css`

### Testing
- Confirm upon screen resize below 980px: hamburger appears, menu hidden, click opens/closes menu.
- Confirm above 980px: menu always shown and hamburger hidden.
- Confirm theme toggles and persists via localStorage.

## Troubleshooting
- If hamburger doesn’t appear: verify `initNavToggle` in `source/app.js` runs and attaches button.
- If menu does not close: verify `.mobile-open` class is toggled and click outside event is not blocked.
