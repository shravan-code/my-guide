# Data Guide

A comprehensive, modern educational website covering Python, NumPy, Pandas, Spark, and SQL fundamentals. Built with a beautiful glass morphism design and fully responsive layout.

## Features

- **Glass Morphism Design** - Modern, frosted glass UI with floating orb backgrounds
- **Dark/Light Mode** - Toggle between themes with persistent preference
- **Responsive Layout** - Works seamlessly on desktop, tablet, and mobile
- **Sidebar Navigation** - Easy navigation for in-depth content pages
- **Syntax Highlighted Code** - Python and SQL code blocks with proper styling

## Project Structure

```
my-guide/
├── index.html                          # Homepage with all sections
├── README.md                           # This file
├── source/
│   ├── styles.css                      # Main styles and CSS variables
│   ├── hub.css                         # Hub page styles
│   ├── app.js                          # Theme toggle and global scripts
│   │
│   ├── python/                         # Python section
│   │   ├── python.css                  # Sidebar styles (reusable)
│   │   ├── python.js                   # Sidebar functionality
│   │   ├── index.html                  # Python Hub
│   │   ├── python-fundamentals.html    # Fundamentals page
│   │   ├── python-oops.html           # OOPs concepts page
│   │   ├── methods.html               # Comprehensive methods reference
│   │   └── memory-performance.html     # Memory & performance tips
│   │
│   ├── pandas/                         # Pandas section
│   │   ├── index.html                  # Pandas Hub
│   │   ├── pandas-series.html          # Series documentation
│   │   ├── pandas-dataframes.html      # DataFrames documentation
│   │   └── methods.html               # Comprehensive methods reference
│   │
│   ├── numpy/                          # NumPy section
│   │   ├── index.html                  # NumPy Hub
│   │   ├── numpy-arrays.html           # Arrays fundamentals
│   │   ├── numpy-operations.html       # Mathematical operations
│   │   └── methods.html               # Comprehensive methods reference
│   │
│   ├── sql/                            # SQL section
│   │   ├── index.html                  # SQL Hub
│   │   ├── sql-queries.html            # SELECT queries
│   │   ├── sql-joins.html              # JOIN operations
│   │   └── sql-subqueries.html         # Subqueries and CTEs
│   │
│   └── spark/                          # Spark section
│       ├── spark.css                   # Spark-specific styles
│       ├── spark.js                    # Spark functionality
│       ├── index.html                  # Spark Hub
│       ├── spark-theory.html           # Spark theory
│       ├── spark-code.html             # Spark code examples
│       └── spark-architecture.html     # Architecture diagrams
```

## Sections

### Python
- **Hub** - Introduction and learning path overview
- **Fundamentals** - Variables, data types, operators, control flow
- **OOPs** - Classes, inheritance, polymorphism, encapsulation
- **Methods** - Built-in methods, magic methods, decorators (15 sections)
- **Memory** - Memory management, optimization, performance tips

### Pandas
- **Hub** - Introduction to data analysis
- **Series** - 1D labeled arrays, indexing, operations
- **DataFrames** - 2D data structures, manipulation, grouping
- **Methods** - Complete API reference (17 sections)

### NumPy
- **Hub** - Numerical computing foundation
- **Arrays** - Array creation, attributes, dtypes
- **Operations** - Mathematical and statistical functions
- **Methods** - Complete API reference (14 sections)

### SQL
- **Hub** - Database fundamentals
- **Queries** - SELECT, WHERE, GROUP BY, ORDER BY
- **Joins** - INNER, LEFT, RIGHT, FULL joins
- **Subqueries** - Nested queries, CTEs, window functions

### Spark
- **Hub** - Big data processing introduction
- **Theory** - Core concepts and RDDs
- **Code** - Practical examples
- **Architecture** - Cluster architecture diagrams

## CSS Architecture

- **`styles.css`** - Main styles with CSS variables for theming
- **`hub.css`** - Styles for hub/landing pages (`.inspire`, `.tracks`, `.track-grid`)
- **`python.css`** - Sidebar navigation styles (reused by Pandas and NumPy)

### CSS Variables

```css
:root {
  --bg: #0a0a12;           /* Background */
  --text: #e6edf3;         /* Text color */
  --accent: #58a6ff;       /* Primary accent */
  --accent2: #3fb950;      /* Secondary accent */
  --accent3: #bc8cff;      /* Tertiary accent */
  --glass: rgba(255,255,255,0.05);  /* Glass effect */
  --border: rgba(255,255,255,0.08); /* Border */
}
```

## Getting Started

1. Clone the repository
2. Open `index.html` in your browser, or use a local server:
   ```bash
   # Python
   python -m http.server 8000
   
   # Node.js
   npx serve .
   ```
3. Navigate to `http://localhost:8000`

## Design System

### Typography
- **Headings** - Space Grotesk (400-700)
- **Body** - Sora (500-700)

### Color Palette
- Dark theme with glass morphism effects
- Gradient accents for visual interest
- High contrast for readability

### Components
- `.glass` - Frosted glass effect
- `.bg-orb` - Floating background orbs
- `.track` - Feature cards on hub pages
- `.topic-section` - Content sections with badges
- `.split-grid` - Two-column code examples
- `.code-block` - Syntax-highlighted code
- `.sidebar` - Navigation sidebar for content pages

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## License

MIT
