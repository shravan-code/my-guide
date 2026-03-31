# Project Notes - UI/UX Polish

## Goal

Polish and unify the website UI/UX across all pages (main, Python, Spark, Roadmaps, Cheatsheets, etc.) with consistent topbar/navbar behavior, theming, and mobile responsiveness.

## Instructions

Key persistent directives from user:
- Logo should be gradient across the site
- Menu hover style should be rounded cards (not underline)
- Mobile topbar/navbar: left hamburger, centered logo, right theme toggle
- No close button on mobile navbar (toggle button only)
- Mobile overlay should start **below** topbar, not cover it (prevents blur issue)
- Sidebar pages should have a floating toggle button on mobile
- Logo links must redirect to home page on click (z-index fix needed)

## Discoveries

- Project has **multiple style systems** causing inconsistency:
  - `source/styles.css` (main unified styles)
  - `source/styles/base.css`, `source/styles/mobile.css`, `source/styles/desktop.css` (split legacy styles)
  - Section-specific CSS: `source/python/python.css`, `source/spark/spark.css`, `source/spark/styles.css`, `source/roadmaps/roadmap.css`, `source/cheatsheets/cheatsheet-base.css`, `source/cheatsheets/cheatsheets.css`
- Cheatsheet pages were loading `base.css + mobile.css + desktop.css` separately which had incomplete topbar styles → changed all 7 cheatsheet pages to load `styles.css` directly
- **Z-index stacking issue**: `.header-actions` had `z-index: 2` while `.brand` had `z-index: 1`, causing header-actions grid to intercept logo clicks on mobile → fixed by setting brand to z-index: 10, header-actions to z-index: 5 across all CSS files
- **Overlay blur issue**: `.mobile-menu-overlay` and `.sidebar-overlay` had `backdrop-filter: blur()` covering the topbar area → removed blur and made overlays start below topbar (`top: var(--topbar-height)`)
- **Sidebar toggle button z-index**: Button needs z-index higher than overlay (2001) to remain clickable

## Accomplished

### Topbar/Navbar Mobile Fixes
- Unified mobile topbar grid pattern (left toggle / centered logo / right theme) across all page families
- Fixed z-index stacking so logo clicks work on mobile
- Fixed overlay to start below topbar (no blur over topbar)
- Fixed responsive breakpoints: changed `@media (max-width: 900px)` to `@media (max-width: 920px)` on index.html
- Applied mobile topbar CSS to: `source/styles.css`, `source/styles/mobile.css`, `source/python/python.css`, `source/roadmaps/roadmap.css`, `source/spark/spark.css`, `source/cheatsheets/cheatsheet-base.css`, `source/cheatsheets/cheatsheets.css`, `index.html`, `source/portfolios/portfolio.html`

### Cheatsheet Pages
- Changed all 7 cheatsheet HTML pages to load `styles.css` instead of `base.css + mobile.css + desktop.css`
- Fixed navbar visibility (was missing full topbar styling)
- Added comprehensive mobile content styles (hero, sections, code blocks, tables, scroll behavior)
- Added sidebar overlay + floating toggle button (top-right corner)
- Added @media breakpoints at 920px, 700px, 480px for content

### Sidebar Toggle Button (Mobile)
- Added floating sidebar toggle button to all pages with sidebars (top-right, below topbar)
- Added sidebar overlay (below topbar, no blur)
- Added sidebar slide-in behavior (transform: translateX)
- Added `initializeSidebarToggle()` to `source/app.js` (centralized, works for all pages)

### Cheatsheet JS
- Added sidebar toggle functionality to `source/cheatsheets/cheatsheets.js`
- Removed legacy `mobile-menu-close` references

### Portfolio Page
- Added mobile topbar/navbar CSS matching main site pattern
- Added z-index fix for logo click
- Added profile image with faded/feathered border and glow effect

### Main Page (index.html)
- Fixed mobile menu to open below topbar
- Added hamburger-icon class (3-line style)
- Applied consistent z-index fixes
- Changed `@media (max-width: 900px)` to `@media (max-width: 920px)`

### JS Consolidation (this session)
- **`app.js` mobile menu refactor**: Refactored `initializeMobileMenu` into `attachMobileHandlers` + factory pattern. Now handles both pages with inline mobile menu HTML (Python, Roadmaps) and pages that build it dynamically (pandas, numpy, sql, cloud, data, etc.). Previously had `hasCustomMobileMenu` early-return that skipped handler attachment.
- **`spark.js`**: Removed duplicate `sidebarToggle` click handler — was conflicting with `app.js`'s handler, causing sidebar not to open.
- **Removed duplicate inline JS from 13 files**:
  - `python-fundamentals.html`, `python-oops.html`, `methods.html`, `memory-performance.html`, `python/index.html` — removed sidebar + mobile menu JS (kept navItems/setActiveNav)
  - `pandas-series.html`, `pandas-dataframes.html`, `pandas-methods.html` — removed sidebar JS (kept navItems/setActiveNav)
  - `roadmap.html`, `sql-roadmap.html`, `spark-roadmap.html`, `python-roadmap.html`, `ml-engineer-roadmap.html`, `ai-engineer-roadmap.html` — removed duplicate mobile menu JS
  - `index.html` — removed duplicate mobile menu + dropdown JS (kept scroll-to-top)

### CSS Fixes (this session)
- **`styles.css`**: Un-nested `.topbar` from `.glass {}` block (was accidentally nested, making selector `.glass .topbar` instead of `.topbar`)
- **`python.css`**: Fixed `.sidebar-overlay` to `top: var(--topbar-height)` with no blur
- **`spark.css`**: Added `background: var(--glass)`, `backdrop-filter: blur(16px)`, `border-right` to mobile sidebar (was transparent)
- **`index.html` inline styles**: Moved hamburger/mobile menu base styles out of `@media (max-width: 600px)` into un-nested block so they apply at correct `≤920px` breakpoint
- **`index.html`**: Removed `display: none` for `.portfolio-link` on mobile — now visible on mobile topbar
- **`index.html`**: Fixed `header-actions` grid to 4 columns (hamburger | spacer | portfolio | theme toggle)

## Relevant files / directories

### Core shared styles and scripts
- `source/styles.css` — main unified styles; has topbar, mobile menu, hamburger-icon; z-index fixed at line 1137-1153
- `source/styles/base.css` — code theme variables; has topbar base styles; overlay fixed to start below topbar
- `source/styles/mobile.css` — mobile-specific overrides; z-index fixed at lines 20, 31
- `source/styles/desktop.css` — desktop overrides
- `source/app.js` — theme toggle + mobile menu + sidebar toggle (centralized, handles all page families)
- `source/design-tokens.css` — CSS custom properties

### Main page
- `index.html` — inline CSS with mobile topbar/navbar; hamburger-icon added; z-index fixed inline

### Python pages (use `source/python/python.css`)
- `source/python/index.html`
- `source/python/python-fundamentals.html`
- `source/python/python-oops.html`
- `source/python/methods.html`
- `source/python/memory-performance.html`
- `source/python/python.css` — mobile topbar/navbar; sidebar toggle CSS
- `source/python/python.js` (accordion only)

### Spark pages (use `source/spark/spark.css`)
- `source/spark/index.html`
- `source/spark/spark-theory.html`
- `source/spark/spark-code.html`
- `source/spark/spark-architecture.html`
- `source/spark/spark.css` — sidebar toggle CSS; overlay fixed to start below topbar; mobile sidebar now has glass background
- `source/spark/spark.js` — sidebar nav/intersection/scroll handlers only (toggle handled by app.js)

### Roadmap pages (use `source/roadmaps/roadmap.css`)
- `source/roadmaps/roadmap.html`
- `source/roadmaps/python-roadmap.html`
- `source/roadmaps/sql-roadmap.html`
- `source/roadmaps/spark-roadmap.html`
- `source/roadmaps/ml-engineer-roadmap.html`
- `source/roadmaps/ai-engineer-roadmap.html`
- `source/roadmaps/roadmap.css` — mobile topbar CSS; z-index fixed

### Cheatsheet pages
- `source/cheatsheets/cheatsheet.html` — overview page (no sidebar)
- `source/cheatsheets/compare.html` — comparison page (no sidebar)
- `source/cheatsheets/python-cheatsheet.html` — has sidebar + toggle button
- `source/cheatsheets/numpy-cheatsheet.html` — has sidebar + toggle button
- `source/cheatsheets/pandas-cheatsheet.html` — has sidebar + toggle button
- `source/cheatsheets/spark-cheatsheet.html` — has sidebar + toggle button
- `source/cheatsheets/postgresql-cheatsheet.html` — has sidebar + toggle button
- `source/cheatsheets/cheatsheet-base.css` — shared cheatsheet styles; sidebar toggle CSS; comprehensive mobile content styles
- `source/cheatsheets/cheatsheets.css` — comparison page styles; mobile content styles
- `source/cheatsheets/cheatsheets.js` — theme + mobile menu + sidebar toggle (standalone)

### Other content pages (use `source/python/python.css`)
- `source/portfolios/portfolio.html` — profile image with faded border and glow
- `source/sql/*.html` (6 files) — all have sidebar + toggle button
- `source/pandas/*.html` (3 files) — all have sidebar + toggle button
- `source/numpy/*.html` (4 files) — all have sidebar + toggle button
- `source/data/*.html` (4 files) — all have sidebar + toggle button
- `source/cloud/*.html` (8 files) — all have sidebar + toggle button
