# Data Guide — UI implementation plan

This document tracks phased work to stabilize layout, navigation, theming, motion, and responsive media across the static site. Update the **Progress log** at the bottom as phases complete.

## Current architecture (audit summary)

| Area | What exists today |
|------|-------------------|
| **Entry points** | Root `index.html` uses `source/styles/homepage.css` for layout; inner pages use `source/styles/base.css` + `mobile.css` / `desktop.css`, or `source/styles/styles.css`, plus section bundles (`python/`, `cloud/`, `portfolios/`, `cheatsheets/`, `libraries/spark/`, `roadmaps/`, etc.). |
| **Scripts** | `source/scripts/app.js` — theme (`localStorage` + `prefers-color-scheme`), mobile menu builder, sidebar open/collapse + overlay, **`initScrollToTop()`** (DOMContentLoaded-safe), resize handlers. |
| **Sidebar** | `source/styles/sidebar.css` + `body.with-sidebar` on long-form library pages; grid layout with `.main-content`, `.sidebar-toggle`, `#sidebar-overlay`. |
| **Cheatsheets** | `../scripts/app.js` then `scripts/cheatsheets.js` (reveal + pill nav only). |
| **Portfolio projects** | `#hamburger-btn` pages skip global mobile menu init; `portfolio.js` only toggles the project drawer. |

## Goals

1. **Shell (mobile + desktop):** Sidebar, sidebar toggle, breadcrumb, topbar, navbar, theme toggle, scroll-to-top behave consistently and accessibly.
2. **Visual quality:** Shared motion, card surfaces, hover/focus states, alignment, spacing scale, and button styles across hubs and content pages.
3. **Responsive media:** Images, embeds, and card thumbnails use fluid sizing without overflow on small viewports.
4. **Stability:** Repeat pass over all HTML pages and nested routes until behavior and visuals are consistent.
5. **Links and navigation:** All links (buttons, logos, paths, topbar menu links, breadcrumb links, sidebar links, sidebar toggle) are correct, consistent, and accessible.
6. **Spacing and padding:** Consistent gaps, spacing, and padding across all pages using design tokens.
7. **UI interactions:** Consistent hover, focus, active, and mobile interactions across all pages and sub-pages.

## Phase 1 — Layout shell and behavior (priority)

### 1.1 Topbar and navbar

- [x] Normalize **DOM order** where batch-fixed; root **`index.html`** home nav targets real files (`cloud-index.html`, `sql-hub.html`, library hubs, `cheatsheet-index.html`, `roadmaps-data-engineer.html`, `big-data-index.html`, `python-hub.html`).
- [x] **`app.js`** mobile menu: initial **`aria-expanded="false"`** on hamburger attach; portfolio project pages still skip duplicate `#mobile-menu` when `#hamburger-btn` exists.
- [x] **`app.js`** paths: all pages under `source/` now reference **`scripts/app.js`** with correct `../` depth (incl. AWS nested pages).

### 1.2 Sidebar and toggle

- [x] Sticky sidebar **z-index** on desktop reset to `1`; overlay/toggle use **stacking tokens** (`--z-sidebar-*`, `--z-sidebar-fab`).

### 1.3 Breadcrumb

- [x] Shared **`.breadcrumb`** block in **`base.css`** (wrap, padding, separators, current).

### 1.4 Theme toggling

- [x] **`applyTheme`** sets **`aria-label`** ("Switch to light/dark mode") on `#theme-toggle`.

### 1.5 Scroll-to-top

- [x] **`initScrollToTop()`** in **`app.js`**: passive scroll listener, **`prefers-reduced-motion`**, runs on **`DOMContentLoaded`** so `#scrollToTop` can live after the script tag.
- [x] Removed **duplicate inline scroll** from ~56 HTML files; trimmed **`cheatsheets.js`** and **`portfolio.js`** so **`app.js`** owns scroll/theme/mobile globally.
- [x] **`--z-scroll-top`** on **`.scroll-to-top`** in `base.css` and `styles.css`.

**Phase 1 exit criteria:** Spot-check home, `sql-hub.html`, one sidebar library page, `cheatsheet-index.html`, and `portfolio.html` at mobile/desktop widths.

---

## Phase 2 — Visual system (cards, motion, spacing, buttons)

- [x] **Spacing + z-index tokens** in **`design-tokens.css`** (`--space-*`, `--z-*`).
- [x] **Hub `.track`** cards in **`hub.css`**: `display: block`, `min-height`, transitions, **`focus-visible`**, dark hover shadows, **`prefers-reduced-motion`**.
- [x] **`.track`** in **`base.css`**: focus-visible + reduced-motion for pages using base tracks.
- [x] **Touch targets** (44px) for **`.mobile-menu-toggle`**, **`.theme-toggle`**, **`.portfolio-link`** in **`mobile.css`**.

### 2.4 Alignment and rhythm

- [x] Optional: dedupe home **`index.html`** inline shell styles into shared CSS — extracted to **`source/styles/homepage.css`**.

---

## Phase 3 — Responsive aspect ratios and media

- [x] **`img, video, iframe`** defaults and **`.table-wrap`** in **`base.css`** (pages that load `base.css`).

---

## Phase 4 — Recursive QA and regression passes

- [x] Full inventory pass: viewport, broken links, contrast — fixed critical broken links in `index.html`, `big-data-index.html`, `aws-index.html`, `numpy-hub.html`, `pandas-hub.html`.
- [x] **SQL hub**: stylesheet paths → `styles/styles.css`, `styles/hub.css`, `python/styles/python.css`, `python/scripts/python.js`; nav slugs → `sql-queries-joins.html`, etc.; hub → `sql-hub.html`.
- [x] **Libraries**: `href="index.html"` → correct `*-hub.html` per section.

### Regression strategy

- **P0 set:** `index.html`, `libraries-hub.html`, `spark-theory.html` (sidebar), `sql-hub.html`, `python-hub.html`, `cloud-index.html`, `portfolio.html`, `cheatsheet-index.html`.

---

## Phase 5 — Links and navigation consistency

### 5.1 Topbar menu links

- [x] Verify all topbar navigation links (`<a>` elements in `.topbar`, `.navbar`, `.nav`) point to correct file paths (`*-hub.html`, `index.html`, section landing pages).
- [x] Ensure relative path depth (`../`) is correct for all pages at different directory levels.
- [x] Check logo links (site logo, brand images) point to root `index.html`.
- [x] Ensure topbar links have consistent hover/focus states (colors, underline, background).

### 5.2 Breadcrumb links

- [x] Verify breadcrumb links use correct relative paths for all nested pages.
- [x] Ensure current page is non-link (`.breadcrumb .current` or `aria-current="page"`).
- [x] Check breadcrumb separator consistency (character, spacing, icon).
- [x] Verify breadcrumb styling matches across all pages using `.breadcrumb`.

### 5.3 Sidebar links

- [x] Verify all sidebar navigation links point to correct section pages.
- [x] Ensure active/current page is highlighted (`.active`, `aria-current="page"`).
- [x] Check sidebar toggle button (`#sidebar-toggle`, `.sidebar-toggle`) works on all sidebar pages.
- [x] Ensure sidebar links have consistent hover/focus states.

### 5.4 Button links

- [x] Verify all `<a class="btn">`, `<button>` elements styled as links have correct `href` targets.
- [x] Ensure button styles are consistent: padding, border-radius, background, text color, hover states.
- [x] Check CTA buttons on hub pages link to correct destinations.
- [x] Verify "back to hub" / "back to top" buttons point to correct pages.

### 5.5 Path validation

- [x] Validate all internal links across all HTML pages (P0 set minimum).
- [x] Fix any broken links to sections, hubs, or resources.
- [x] Ensure external links (if any) open in new tab with `rel="noopener noreferrer"`.

---

## Phase 6 — Spacing, gaps, and padding fixes

### 6.1 Spacing scale validation

- [x] Verify spacing tokens (`--space-*`) in `design-tokens.css` are consistently applied.
- [x] Check for hardcoded pixel values that should use spacing tokens.
- [x] Ensure consistent margin/padding on container elements.

### 6.2 Component spacing

- [x] Audit cards (`.track`, `.card`) for consistent internal padding.
- [x] Verify button padding matches design spec (horizontal, vertical).
- [x] Check list items, table cells, and form elements for consistent spacing.

### 6.3 Layout gaps

- [x] Fix gaps in flexbox/grid layouts (use `gap` property consistently).
- [x] Verify column/row gaps match design tokens.
- [x] Check for missing or extra gaps on responsive breakpoints.

### 6.4 Section spacing

- [x] Ensure consistent vertical spacing between sections (hero, content, footer).
- [x] Verify heading-to-content spacing (`margin-top` on headings or `margin-bottom` on preceding elements).
- [x] Check spacing between breadcrumbs and page content.

---

## Phase 7 — UI interactions consistency

### 7.1 Hover and focus states

- [x] Verify all interactive elements (links, buttons, inputs) have visible hover states.
- [x] Ensure focus states are visible and consistent (`focus-visible`, outline, background).
- [x] Check that `:focus-within` is applied appropriately on containers.

### 7.2 Active and selected states

- [x] Verify current/active page states in navigation (topbar, sidebar, breadcrumbs).
- [x] Ensure selected states on tabs, pills, or filter controls are consistent.
- [x] Check accordion/collapse active states.

### 7.3 Mobile interactions

- [x] Verify touch targets are minimum 44px on mobile.
- [x] Ensure mobile menu toggle works consistently across all pages.
- [x] Check scroll-to-top button visibility and behavior on mobile.
- [x] Verify sidebar toggle works on mobile for sidebar pages.

### 7.4 Animation and motion consistency

- [x] Verify `prefers-reduced-motion` is respected across all animated elements.
- [x] Ensure transition durations are consistent (use CSS custom properties if needed).
- [x] Check that hover/focus transitions are smooth and not jarring.

### 7.5 Theme consistency

- [x] Verify all pages respect theme toggle (light/dark).
- [x] Ensure color variables are consistently used (no hardcoded colors).
- [x] Check that theme toggle `aria-label` updates correctly.

---

## File touch map (updated)

| Files | Likely changes |
|-------|----------------|
| `source/scripts/app.js` | Scroll-to-top, theme aria-label, mobile aria-expanded |
| `source/styles/design-tokens.css` | Z-index + spacing scale |
| `source/styles/base.css` | Breadcrumb, media, scroll z-index, tracks a11y |
| `source/styles/mobile.css` | 44px touch targets |
| `source/styles/hub.css` | Track cards, motion |
| `source/styles/homepage.css` | Homepage layout, hero, marquee, panels (extracted from index.html) |
| `source/styles/styles.css` | Topbar/mobile z-index tokens, scroll z-index |
| `source/styles/sidebar.css` | Overlay/toggle z-index tokens |
| `source/cheatsheets/scripts/cheatsheets.js` | Cheatsheet-only behaviors |
| `source/portfolios/scripts/portfolio.js` | Project hamburger only |
| `index.html` | Correct section URLs |
| Section `*.html` | Script paths, removed inline scroll |
| All HTML files | Link paths, spacing fixes, interaction states |

---

## Progress log

| Date | Phase | Notes |
|------|-------|-------|
| 2026-03-31 | Plan | Initial `implementation.md` created. |
| 2026-03-31 | 1 | Layout shell complete - nav links verified, sidebar overlay z-index fixed |
| 2026-03-31 | 2 | Visual system verified - spacing, z-index, track cards, touch targets all implemented |
| 2026-03-31 | 3 | Responsive media verified - img, video, iframe, table-wrap in base.css |
| 2026-03-31 | 4 | QA passes verified - broken links fixed, SQL hub paths corrected, library links fixed |
| 2026-03-31 | 5 | Links fixed - corrected portfolio paths in 27+ HTML files (../../source/ -> ../../) |
| 2026-03-31 | 6 | Spacing verified - design tokens, gaps, component spacing all consistent |
| 2026-03-31 | 7 | UI interactions verified - hover/focus, active states, mobile, reduced-motion, theme |
| 2026-03-31 | 6 | Spacing, gaps, and padding fixes added. |
| 2026-03-31 | 7 | UI interactions consistency added. |

---

## How to update this document

- After completing a subsection, change `[ ]` to `[x]` and add a dated row to **Progress log**.
- If scope changes (e.g. new section added to site), append a row under **Page inventory** and extend the P0 set.
