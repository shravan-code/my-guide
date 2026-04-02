# Content Architecture Rules

## Goals

- Keep `index.html` as the only custom home page.
- Make every non-home page use one shared shell.
- Keep navigation, breadcrumb, and content section controls consistent.
- Make future content additions require minimal new layout code.

## Canonical Navigation Rules

- Top-level sidebar items should land on hub pages, not random leaf pages.
- Current canonical hubs:
  - `data/index.html`
  - `cloud/index.html`
  - `languages/index.html`
  - `libraries/libraries-hub.html`
  - `tools/index.html`
  - `sql/index.html`
  - `cheatsheets/cheatsheet.html`
  - `roadmaps/roadmap.html`
  - `portfolios/portfolio.html`
- Update `source/hierarchy.js` first when adding or moving visible pages.

## Shared Layout Ownership

- `source/sidebar-nav.js`
  - owns global sidebar injection
  - owns breadcrumb generation
  - owns content section navigation generation
  - removes legacy page-local sidebar controls
- `source/sidebar-nav.css`
  - owns global sidebar visuals
  - imports shared non-home shell styles
  - imports shared content navigation styles
- `source/components/page-shell.css`
  - owns non-home page width, padding, and shell spacing
- `source/components/content-nav.css`
  - owns the right-side section navigation panel and mobile section toggle

## Body Classes

- `home-with-sidebar`
  - marks pages that use the shared global sidebar system
- `non-home-shell`
  - marks all pages under `source/`
  - shared non-home layout rules must target this class
- `has-content-nav`
  - added when a page has section navigation
- `content-nav-collapsed`
  - desktop content navigation collapsed state
- `content-nav-open`
  - mobile content navigation open state

## Mobile Rules

- Main sidebar hamburger stays on the right.
- Breadcrumb stays centered at the top.
- Content section toggle stays bottom-right above the scroll-to-top button.
- Legacy page-local sidebar toggles must not appear.

## Laptop/Desktop Rules

- Main sidebar is visible on the left.
- Breadcrumb stays centered at the top middle.
- Content section navigation is visible by default.
- Content section navigation can be collapsed.

## Adding a New Page

1. Put the page in the correct section folder under `source/`.
2. Link shared styles:
   - `../styles.css`
   - `../hub.css` or page-type stylesheet if needed
   - `../sidebar-nav.css`
3. Keep page content inside `main > .page-wrap`.
4. If the page has section anchors, keep stable heading ids.
5. If the page uses a legacy in-page `.sidebar`, the shared shell can harvest it, but new pages should not add a new one.
6. Register the page in `source/hierarchy.js` if it should appear in visible navigation.

## Adding a New Hub

1. Create `index.html` or a named hub page in the target section.
2. Add it as the canonical `href` for the visible sidebar node in `source/hierarchy.js`.
3. Keep hub pages free of page-local sidebar toggles.
4. Use shared breadcrumb and shared sidebar only.

## What Not To Add Anymore

- New `#sidebar-toggle` buttons
- New `#sidebar-overlay` elements
- New page-local mobile menu systems
- New page-local breadcrumb systems with custom positioning logic
- New duplicated layout shell rules inside section-specific CSS files

## Preferred Content Structure

```html
<main>
  <div class="page-wrap">
    <section class="hero">...</section>
    <section class="topic-section" id="...">...</section>
  </div>
</main>
```

## Migration Principle

- Shared shell handles layout chrome.
- Section-specific CSS should only style content patterns.
- Navigation structure belongs in `source/hierarchy.js`.
- If a page breaks layout, fix the shared shell first unless the page has truly unique content needs.
