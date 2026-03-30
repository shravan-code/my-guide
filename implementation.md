# Data Guide — UI implementation plan

This document tracks phased work to stabilize layout, navigation, theming, motion, and responsive media across the static site. Update the **Progress log** at the bottom as phases complete.

## Current architecture (audit summary)

| Area | What exists today |
|------|-------------------|
| **Entry points** | Root `index.html` with large inline `<style>` overrides; inner pages use `source/styles/base.css` + `mobile.css` / `desktop.css`, or `source/styles/styles.css`, plus section bundles (`python/`, `cloud/`, `portfolios/`, `cheatsheets/`, `libraries/spark/`, `roadmaps/`, etc.). |
| **Scripts** | `source/scripts/app.js` — theme (`localStorage` + `prefers-color-scheme`), mobile menu builder, sidebar open/collapse + overlay, **`initScrollToTop()`** (DOMContentLoaded-safe), resize handlers. |
| **Sidebar** | `source/styles/sidebar.css` + `body.with-sidebar` on long-form library pages; grid layout with `.main-content`, `.sidebar-toggle`, `#sidebar-overlay`. |
| **Cheatsheets** | `../scripts/app.js` then `scripts/cheatsheets.js` (reveal + pill nav only). |
| **Portfolio projects** | `#hamburger-btn` pages skip global mobile menu init; `portfolio.js` only toggles the project drawer. |

## Goals

1. **Shell (mobile + desktop):** Sidebar, sidebar toggle, breadcrumb, topbar, navbar, theme toggle, scroll-to-top behave consistently and accessibly.
2. **Visual quality:** Shared motion, card surfaces, hover/focus states, alignment, spacing scale, and button styles across hubs and content pages.
3. **Responsive media:** Images, embeds, and card thumbnails use fluid sizing without overflow on small viewports.
4. **Stability:** Repeat pass over all HTML pages and nested routes until behavior and visuals are consistent.

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

- [x] **`applyTheme`** sets **`aria-label`** (“Switch to light/dark mode”) on `#theme-toggle`.

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

- [ ] Optional: dedupe home **`index.html`** inline shell styles into shared CSS (large file; defer if not blocking).

---

## Phase 3 — Responsive aspect ratios and media

- [x] **`img, video, iframe`** defaults and **`.table-wrap`** in **`base.css`** (pages that load `base.css`).

---

## Phase 4 — Recursive QA and regression passes

- [ ] Full inventory pass: viewport, broken links, contrast (see checklist in original plan).
- [x] **SQL hub**: stylesheet paths → `styles/styles.css`, `styles/hub.css`, `python/styles/python.css`, `python/scripts/python.js`; nav slugs → `sql-queries-joins.html`, etc.; hub → `sql-hub.html`.
- [x] **Libraries**: `href="index.html"` → correct `*-hub.html` per section.

### Regression strategy

- **P0 set:** `index.html`, `libraries-hub.html`, `spark-theory.html` (sidebar), `sql-hub.html`, `python-hub.html`, `cloud-index.html`, `portfolio.html`, `cheatsheet-index.html`.

---

## File touch map (expected)

| Files | Likely changes |
|-------|----------------|
| `source/scripts/app.js` | Scroll-to-top, theme aria-label, mobile aria-expanded |
| `source/styles/design-tokens.css` | Z-index + spacing scale |
| `source/styles/base.css` | Breadcrumb, media, scroll z-index, tracks a11y |
| `source/styles/mobile.css` | 44px touch targets |
| `source/styles/hub.css` | Track cards, motion |
| `source/styles/styles.css` | Topbar/mobile z-index tokens, scroll z-index |
| `source/styles/sidebar.css` | Overlay/toggle z-index tokens |
| `source/cheatsheets/scripts/cheatsheets.js` | Cheatsheet-only behaviors |
| `source/portfolios/scripts/portfolio.js` | Project hamburger only |
| `index.html` | Correct section URLs |
| Section `*.html` | Script paths, removed inline scroll |

---

## Progress log

| Date | Phase | Notes |
|------|-------|-------|
| 2026-03-31 | Plan | Initial `implementation.md` created. |
| 2026-03-31 | 1–3 | Centralized scroll + theme aria; tokens; breadcrumb + media utilities; hub/base tracks; fixed SQL + library + `index.html` links; corrected all `app.js` paths; cheatsheets use `app.js` + slim `cheatsheets.js`; portfolio.js deduped. |
| 2026-03-31 | 4 | UI asset stabilization: fixed Cloud/Python/Library/Spark/Roadmaps/Big-Data/Cheatsheets CSS+JS paths; removed missing AWS `aws.css/aws.js` refs; centralized scroll-to-top by removing remaining inline handlers in `cloud-architecture.html` + AWS `interview.html`. |
| 2026-03-31 | 4 | Breadcrumb spacing fix: added `--breadcrumb-height` alias in `design-tokens.css` to remove overlap on cloud pages. |
| 2026-03-31 | 2 | Visual polish: reduced-motion handling for `.reveal` (styles.css) + consistent focus ring for `.toc a` plus hover de-motion. |

---

## How to update this document

- After completing a subsection, change `[ ]` to `[x]` and add a dated row to **Progress log**.
- If scope changes (e.g. new section added to site), append a row under **Page inventory** and extend the P0 set.
