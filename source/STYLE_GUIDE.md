# Website Style Guide

Use `source/design-tokens.css` as the single customization layer for the site.

Recommended developer workflow:

- Colors: change accent and surface tokens in `source/design-tokens.css`
- Typography: change `--font-family-*` and `--font-size-*` tokens in `source/design-tokens.css`
- Layout: change `--layout-topbar-height` and `--layout-sidebar-width`
- Motion/radius: change `--transition-standard`, `--radius-*`

Core token groups:

- `--font-family-body`, `--font-family-display`, `--font-family-mono`
- `--font-size-root`, `--font-size-body`, `--font-size-brand`, `--font-size-h1`, `--font-size-h2`, `--font-size-h3`
- `--color-bg-light`, `--color-bg-dark`, `--color-text-light`, `--color-text-dark`
- `--color-accent`, `--color-accent-pink`, `--color-accent-cyan`
- `--shadow-*`, `--radius-*`, `--glass-blur-default`

Recommended rules:

- Change tokens first; avoid editing component colors directly unless a page needs a deliberate override.
- Keep semantic aliases in shared CSS (`source/styles.css`, `source/cheatsheets/cheatsheets.css`, `source/sidebar.css`, etc.) so component code stays stable.
- For section-specific themes, override only tokens in the page or section wrapper instead of rewriting component CSS.

Quick examples:

```css
:root {
  --font-size-brand: 1.2rem;
  --color-accent: #2563eb;
  --color-accent-pink: #db2777;
  --color-accent-cyan: #0891b2;
}
```

```css
body.theme-forest {
  --color-accent: #0f766e;
  --color-accent-pink: #65a30d;
}
```

Shared styles already wired to these tokens:

- `source/styles.css`
- `source/cheatsheets/cheatsheets.css`
- `source/sidebar.css`
- `source/hub.css`
- `source/python/python.css`
- `source/spark/styles.css`
- `source/spark/spark.css`
