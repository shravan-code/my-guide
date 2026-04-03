# Complete UI Redesign Implementation Plan

## Transform Your Website to Architectural Scholar Design System

This plan provides exact specifications for every UI element, with separate instructions for Desktop (≥768px) and Mobile (<768px) implementations.

---

## Phase 1: Foundation Setup

### 1.1 Design Tokens - Color System

Define these exact color variables in your CSS/Tailwind config:

```javascript
// Primary Palette
primary: "#006882"           // Main action color (buttons, links, active states)
primary-dim: "#005b72"       // Hover/dimmed primary
primary-container: "#8fdfff" // Background for primary elements
primary-fixed: "#8fdfff"     // Fixed variant for badges
primary-fixed-dim: "#81d1f0" // Dimmed fixed variant
on-primary: "#f2faff"        // Text on primary background
on-primary-container: "#005065" // Text on primary container
on-primary-fixed: "#003b4c"  // Text on primary fixed
on-primary-fixed-variant: "#005a71"

// Secondary Palette
secondary: "#526074"
secondary-container: "#d5e3fc"
secondary-fixed: "#d5e3fc"
secondary-fixed-dim: "#c7d5ed"
on-secondary: "#f8f8ff"
on-secondary-container: "#455367"
on-secondary-fixed: "#324053"
on-secondary-fixed-variant: "#4e5c71"
secondary-dim: "#465468"

// Tertiary Palette
tertiary: "#4d5f84"
tertiary-container: "#bfd2fd"
tertiary-fixed: "#bfd2fd"
tertiary-fixed-dim: "#b1c4ee"
on-tertiary: "#f9f8ff"
on-tertiary-container: "#35476b"
on-tertiary-fixed: "#213456"
on-tertiary-fixed-variant: "#3e5175"
tertiary-dim: "#415377"

// Surface Colors (Backgrounds)
surface: "#f7f9fb"
surface-bright: "#f7f9fb"
surface-dim: "#d4dbdf"
surface-container-lowest: "#ffffff"
surface-container-low: "#f0f4f7"
surface-container: "#eaeff2"
surface-container-high: "#e3e9ed"
surface-container-highest: "#dce4e8"
background: "#f7f9fb"

// Text Colors
on-surface: "#2c3437"
on-surface-variant: "#596064"
inverse-on-surface: "#9a9d9f"
inverse-surface: "#0b0f10"

// Outlines
outline: "#747c80"
outline-variant: "#acb3b7"

// Error States
error: "#a83836"
error-container: "#fa746f"
error-dim: "#67040d"
on-error: "#fff7f6"
on-error-container: "#6e0a12"

// Special
surface-tint: "#006882"
inverse-primary: "#8fdfff"
```

### 1.2 Typography System

```css
/* Font Families */
--font-headline: 'Manrope', sans-serif;  /* For h1, h2, h3, brand text */
--font-body: 'Inter', sans-serif;        /* For body text, paragraphs */
--font-label: 'Inter', sans-serif;       /* For small labels, breadcrumbs */

/* Font Weights */
headline-extrabold: 800    /* Page titles */
headline-bold: 700         /* Section headers */
headline-semibold: 600     /* Card titles */
body-regular: 400          /* Paragraph text */
body-medium: 500           /* Links, secondary text */
body-semibold: 600         /* Emphasized text */
label-medium: 500          /* Small labels */

/* Font Sizes by Element */
h1-page-title: 5xl (48px) desktop, 3xl (30px) mobile
h2-section: 2xl (24px) desktop, xl (20px) mobile
h3-card-title: xl (20px) desktop, lg (18px) mobile
h4-subsection: lg (18px)
body-large: lg (18px) line-height: 1.75
body-default: sm (14px) line-height: 1.5
body-small: xs (12px)
label-tiny: 10px
label-micro: 11px
```

### 1.3 Border Radius System

```css
--radius-sm: 0.125rem (2px)
--radius-md: 0.25rem (4px)
--radius-lg: 0.5rem (8px)    /* Cards, buttons */
--radius-xl: 0.75rem (12px)  /* Large cards, containers */
--radius-full: 9999px        /* Avatar circles, pills */
```

### 1.4 Spacing Scale

```css
--space-1: 0.25rem (4px)
--space-2: 0.5rem (8px)
--space-3: 0.75rem (12px)
--space-4: 1rem (16px)
--space-6: 1.5rem (24px)
--space-8: 2rem (32px)
--space-10: 2.5rem (40px)
--space-12: 3rem (48px)
--space-16: 4rem (64px)
--space-20: 5rem (80px)
```

### 1.5 Breakpoints

```css
mobile: < 768px
tablet: 768px - 1024px
desktop: ≥ 768px (md:)
large-desktop: ≥ 1024px (lg:)
xl-desktop: ≥ 1280px (xl:)
```

---

## Phase 2: Layout Architecture

### 2.1 Overall Page Shell

#### DESKTOP (≥768px)

```
┌─────────────────────────────────────────────────────────────┐
│                    TOP NAV BAR (fixed, z-50)                │
│  height: 64px | bg: slate-50/80 backdrop-blur-xl           │
│  padding: px-6 py-3                                        │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│   SIDEBAR    │           MAIN CONTENT AREA                  │
│   (fixed)    │           margin-left: 288px (ml-72)         │
│   width:     │           padding: px-12 py-10               │
│   288px      │           max-width: 7xl (1280px)            │
│   (w-72)     │                                              │
│   height:    │   ┌──────────────────────────────────────┐   │
│   100vh      │   │  Breadcrumbs                          │   │
│              │   ├──────────────────────────────────────┤   │
│   bg:        │   │  Page Header (h1 + description)       │   │
│   slate-100  │   ├──────────────────────────────────────┤   │
│              │   │  Content Grid (Bento Layout)          │   │
│   z-index:   │   │  - Cards with hover effects           │   │
│   40         │   │  - Asymmetric grid columns            │   │
│              │   └──────────────────────────────────────┘   │
│              │                                              │
│              ├──────────────────────────────────────────────┤
│              │                    FOOTER                    │
│              │  margin-top: 80px | padding: py-12           │
└──────────────┴──────────────────────────────────────────────┘
```

**Desktop Layout CSS:**
```html
<body class="bg-background text-on-background min-h-screen">
  <!-- Top Nav: fixed top-0 w-full z-50 -->
  <header class="fixed top-0 w-full z-50 bg-slate-50/80 backdrop-blur-xl shadow-sm">
  
  <!-- Sidebar: hidden on mobile, flex on desktop -->
  <aside class="hidden md:flex flex-col h-screen w-72 fixed left-0 top-0 overflow-y-auto bg-slate-100 z-40">
  
  <!-- Main: margin-left on desktop only -->
  <main class="pt-24 md:ml-72 min-h-screen">
    <div class="max-w-7xl mx-auto px-6 md:px-12 py-8">
      <!-- Content here -->
    </div>
  </main>
  
  <!-- Footer -->
  <footer class="mt-24 w-full py-12 border-t border-slate-200/20">
</body>
```

#### MOBILE (<768px)

```
┌──────────────────────────────┐
│  ☰  Brand Name    🔔 👤     │  TOP NAV (fixed, z-50)
│  height: 64px                │
├──────────────────────────────┤
│                              │
│   MAIN CONTENT AREA          │
│   full width, no sidebar     │
│   padding: px-6 py-8         │
│   padding-top: 80px          │
│                              │
│   ┌──────────────────────┐   │
│   │ Breadcrumbs          │   │
│   ├──────────────────────┤   │
│   │ Page Header          │   │
│   ├──────────────────────┤   │
│   │ Content Cards        │   │
│   │ (single column)      │   │
│   └──────────────────────┘   │
│                              │
├──────────────────────────────┤
│ 🏠    🔍    📚    ⚙️        │  BOTTOM NAV (fixed, z-40)
│ Home  Explore Lib  Settings  │
│ height: 64px                 │
└──────────────────────────────┘
```

**Mobile Layout CSS:**
```html
<body class="bg-surface text-on-surface min-h-screen relative">
  <!-- Top Nav with hamburger -->
  <header class="fixed top-0 w-full z-50 bg-slate-50/80 backdrop-blur-xl shadow-sm flex items-center justify-between px-6 py-3">
    <div class="flex items-center gap-4">
      <button class="text-cyan-700">
        <span class="material-symbols-outlined">menu</span>
      </button>
      <span class="text-lg font-bold text-cyan-800">Brand</span>
    </div>
  </header>
  
  <!-- Main: full width, no sidebar margin -->
  <main class="pt-20 px-6 pb-24">
    <!-- Content here -->
  </main>
  
  <!-- Bottom Navigation -->
  <nav class="fixed bottom-0 w-full z-40 bg-slate-50/80 backdrop-blur-xl flex justify-around py-4 md:hidden">
    <button class="flex flex-col items-center gap-1 text-cyan-700">
      <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">home</span>
      <span class="text-[10px] font-bold">Home</span>
    </button>
    <!-- More nav items... -->
  </nav>
</body>
```

---

## Phase 3: Component Implementation

### 3.1 Top Navigation Bar

#### DESKTOP Version

```html
<header class="fixed top-0 w-full z-50 bg-slate-50/80 dark:bg-slate-900/80 backdrop-blur-xl shadow-sm">
  <div class="flex items-center justify-between px-6 py-3 w-full md:pl-80">
    <!-- Left: Brand -->
    <div class="flex items-center">
      <span class="text-lg font-bold text-cyan-800 dark:text-cyan-300 font-manrope">Architectural Scholar</span>
    </div>
    
    <!-- Center: Search Bar (hidden on small screens) -->
    <div class="flex-1 max-w-md mx-8 hidden lg:block">
      <div class="relative group">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-primary text-lg">search</span>
        <input 
          class="w-full bg-surface-container-low border-none rounded-full py-1.5 pl-10 pr-4 text-sm focus:ring-1 focus:ring-primary/20 transition-all placeholder:text-slate-400" 
          type="text" 
          placeholder="Search architecture, patterns, or cloud..."
        />
      </div>
    </div>
    
    <!-- Right: Notifications + Avatar -->
    <div class="flex items-center space-x-4">
      <button class="p-2 text-slate-500 hover:text-cyan-700 transition-colors">
        <span class="material-symbols-outlined">notifications</span>
      </button>
      <div class="w-8 h-8 rounded-full overflow-hidden bg-surface-container-highest border border-outline-variant/20">
        <img src="avatar.jpg" alt="User profile" class="w-full h-full object-cover" />
      </div>
    </div>
  </div>
</header>
```

**Desktop Specifications:**
- Position: `fixed top-0` with `z-50`
- Background: `bg-slate-50/80` with `backdrop-blur-xl`
- Shadow: `shadow-sm`
- Height: implicit ~64px (py-3 + content)
- Left padding on desktop: `md:pl-80` (accounts for 288px sidebar)
- Search bar: visible on `lg:` screens only, hidden otherwise
- Brand text: `text-lg font-bold text-cyan-800 font-manrope`
- Avatar: 32x32px, rounded-full, with border

#### MOBILE Version

```html
<header class="fixed top-0 w-full z-50 bg-slate-50/80 backdrop-blur-xl shadow-sm flex items-center justify-between px-6 py-3">
  <!-- Left: Hamburger + Brand -->
  <div class="flex items-center gap-4">
    <button class="text-cyan-700 active:opacity-80 transition-opacity" onclick="toggleDrawer()">
      <span class="material-symbols-outlined">menu</span>
    </button>
    <span class="text-lg font-bold text-cyan-800 font-manrope">Architectural Scholar</span>
  </div>
  
  <!-- Right: Notifications + Avatar (no search bar on mobile top) -->
  <div class="flex items-center gap-3">
    <span class="material-symbols-outlined text-slate-500">notifications</span>
    <div class="w-8 h-8 rounded-full bg-surface-container-highest overflow-hidden">
      <img src="avatar.jpg" alt="User profile" class="w-full h-full object-cover" />
    </div>
  </div>
</header>
```

**Mobile Specifications:**
- Same fixed positioning and styling as desktop
- NO search bar in top nav (search moves elsewhere or is accessed differently)
- Hamburger menu button on left: `text-cyan-700`
- Active state: `active:opacity-80`
- Gap between hamburger and brand: `gap-4`
- Smaller gap for right icons: `gap-3`

### 3.2 Desktop Sidebar Navigation

```html
<aside class="hidden md:flex flex-col h-screen w-72 fixed left-0 top-0 overflow-y-auto bg-slate-100 dark:bg-slate-800/50 z-40">
  <div class="flex flex-col h-full py-8 space-y-2">
    
    <!-- Sidebar Header -->
    <div class="px-8 mb-8">
      <div class="flex items-center space-x-3 mb-2">
        <div class="w-10 h-10 rounded-lg bg-primary flex items-center justify-center text-on-primary">
          <span class="material-symbols-outlined">architecture</span>
        </div>
        <div>
          <h2 class="font-manrope font-extrabold text-cyan-800 dark:text-cyan-200 text-lg leading-tight">Curricula</h2>
          <p class="text-[10px] uppercase tracking-widest text-on-surface-variant font-semibold">Technical Hierarchy</p>
        </div>
      </div>
    </div>
    
    <!-- Navigation Items -->
    <nav class="flex-1 space-y-1">
      
      <!-- Simple Nav Item -->
      <a class="flex items-center px-4 py-2.5 text-slate-600 dark:text-slate-400 pl-4 hover:bg-slate-200/50 dark:hover:bg-slate-700/50 transition-all duration-200 group" href="#">
        <span class="material-symbols-outlined mr-3 text-lg">analytics</span>
        <span class="font-inter text-sm font-medium">Big-Data</span>
      </a>
      
      <!-- ACTIVE Section with Expanded Sub-items -->
      <div class="space-y-1">
        <!-- Active parent item -->
        <a class="flex items-center px-4 py-2.5 text-cyan-700 dark:text-cyan-400 border-l-2 border-cyan-700 dark:border-cyan-400 pl-4 hover:bg-slate-200/50 transition-all duration-200 group active:scale-95" href="#">
          <span class="material-symbols-outlined mr-3 text-lg">cloud</span>
          <span class="font-inter text-sm font-medium">Cloud</span>
        </a>
        
        <!-- Sub-categories (indented) -->
        <div class="ml-12 space-y-2 py-2 border-l border-outline-variant/20">
          <div class="pl-4">
            <span class="text-[11px] font-bold text-on-surface-variant/60 uppercase tracking-tighter">Architecture</span>
          </div>
          <div class="pl-4">
            <span class="text-[11px] font-bold text-on-surface-variant/60 uppercase tracking-tighter mb-1 block">Providers</span>
            <ul class="space-y-1 ml-1">
              <li class="text-xs text-on-surface-variant hover:text-primary cursor-pointer py-1">AWS</li>
              <li class="text-xs text-on-surface-variant hover:text-primary cursor-pointer py-1">Azure</li>
              <li class="text-xs text-on-surface-variant hover:text-primary cursor-pointer py-1">GCP</li>
            </ul>
          </div>
          <div class="pl-4">
            <span class="text-[11px] font-bold text-on-surface-variant/60 uppercase tracking-tighter mb-1 block">Fundamentals</span>
            <ul class="space-y-1 ml-1">
              <li class="text-xs text-on-surface-variant hover:text-primary cursor-pointer py-1">Basics</li>
              <li class="text-xs text-on-surface-variant hover:text-primary cursor-pointer py-1">Compute</li>
              <li class="text-xs text-on-surface-variant hover:text-primary cursor-pointer py-1">Serverless</li>
              <li class="text-xs text-on-surface-variant hover:text-primary cursor-pointer py-1">Services</li>
              <li class="text-xs text-on-surface-variant hover:text-primary cursor-pointer py-1">Storage</li>
            </ul>
          </div>
        </div>
      </div>
      
      <!-- More simple nav items... -->
      <a class="flex items-center px-4 py-2.5 text-slate-600 dark:text-slate-400 pl-4 hover:bg-slate-200/50 dark:hover:bg-slate-700/50 transition-all duration-200 group" href="#">
        <span class="material-symbols-outlined mr-3 text-lg">terminal</span>
        <span class="font-inter text-sm font-medium">Languages</span>
      </a>
      
    </nav>
    
    <!-- CTA Section (bottom of sidebar) -->
    <div class="px-6 mt-auto">
      <div class="bg-surface-container-highest/50 p-4 rounded-xl text-center">
        <p class="text-xs text-on-surface-variant mb-3">Master the Architecture</p>
        <button class="w-full py-2 bg-primary text-on-primary text-xs font-bold rounded-lg hover:bg-primary-dim transition-colors">
          Upgrade to Pro
        </button>
      </div>
    </div>
    
  </div>
</aside>
```

**Desktop Sidebar Specifications:**
- Width: 288px (`w-72`)
- Position: `fixed left-0 top-0`
- Height: `h-screen` (full viewport height)
- Background: `bg-slate-100` (light) / `dark:bg-slate-800/50` (dark)
- Hidden on mobile: `hidden md:flex`
- Overflow: `overflow-y-auto` for scrolling
- Z-index: `z-40`
- Padding: `py-8` top/bottom
- Header icon: 40x40px, rounded-lg, primary bg
- Header title: `text-lg font-extrabold text-cyan-800`
- Header subtitle: `text-[10px] uppercase tracking-widest`
- Nav items: `px-4 py-2.5` padding
- Icon size: `text-lg` (20px) with `mr-3` margin
- Text: `text-sm font-medium`
- Hover: `hover:bg-slate-200/50`
- Active item: `text-cyan-700 border-l-2 border-cyan-700`
- Sub-items indentation: `ml-12` with left border
- Sub-item labels: `text-[11px] uppercase tracking-tighter`
- Sub-item links: `text-xs hover:text-primary`
- CTA card: `bg-surface-container-highest/50 p-4 rounded-xl`
- CTA button: full width, `bg-primary text-on-primary text-xs font-bold rounded-lg`

### 3.3 Mobile Navigation Drawer

```html
<!-- Overlay Background (shown when drawer is open) -->
<div class="fixed inset-0 bg-inverse-surface/40 z-[60] backdrop-blur-[2px]" onclick="closeDrawer()"></div>

<!-- Drawer -->
<aside class="h-screen w-[80%] max-w-[320px] fixed left-0 top-0 overflow-y-auto z-[70] bg-slate-100 font-inter text-sm font-medium flex flex-col py-8 space-y-2">
  
  <!-- Drawer Header -->
  <div class="px-6 mb-8 flex flex-col">
    <div class="flex items-center justify-between mb-4">
      <span class="font-manrope font-extrabold text-cyan-800 text-xl">Curricula</span>
      <span class="material-symbols-outlined text-cyan-700 cursor-pointer" onclick="closeDrawer()">close</span>
    </div>
    <span class="text-xs font-bold uppercase tracking-widest text-cyan-700/60 mb-1">Technical Hierarchy</span>
  </div>
  
  <!-- Navigation Categories -->
  <nav class="flex-1 px-2 space-y-1">
    
    <!-- Simple Category Item -->
    <div class="flex items-center gap-3 text-slate-600 pl-4 py-3 hover:bg-slate-200/50 transition-all duration-200 rounded-lg">
      <span class="material-symbols-outlined">analytics</span>
      <span>Big-Data</span>
    </div>
    
    <!-- ACTIVE Category with Expanded Sub-sections -->
    <div class="space-y-1">
      <!-- Active parent -->
      <div class="flex items-center justify-between text-cyan-700 border-l-2 border-cyan-700 pl-4 py-3 bg-surface-container-low transition-all duration-200 rounded-r-lg">
        <div class="flex items-center gap-3">
          <span class="material-symbols-outlined">terminal</span>
          <span class="font-bold">Languages</span>
        </div>
        <span class="material-symbols-outlined pr-2">expand_more</span>
      </div>
      
      <!-- Expanded Sub-sections -->
      <div class="ml-10 mt-2 space-y-4 border-l border-outline-variant/20 pl-4 py-2">
        
        <!-- Sub-category: Python -->
        <div>
          <span class="text-[10px] uppercase tracking-tighter text-on-surface-variant/60 font-bold">Python</span>
          <ul class="mt-2 space-y-2">
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Oops</li>
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Methods</li>
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Memory</li>
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Practice</li>
          </ul>
        </div>
        
        <!-- Sub-category: Libraries -->
        <div>
          <span class="text-[10px] uppercase tracking-tighter text-on-surface-variant/60 font-bold">Libraries</span>
          <ul class="mt-2 space-y-2">
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Pandas</li>
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Numpy</li>
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Spark</li>
          </ul>
        </div>
        
        <!-- Sub-category: Framework (2-column grid) -->
        <div>
          <span class="text-[10px] uppercase tracking-tighter text-on-surface-variant/60 font-bold">Framework</span>
          <ul class="mt-2 space-y-2 grid grid-cols-2 gap-x-2">
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">DBT</li>
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Airflow</li>
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Kafka</li>
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Flask</li>
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">Django</li>
            <li class="text-slate-600 hover:text-cyan-700 transition-colors">FastAPI</li>
          </ul>
        </div>
        
      </div>
    </div>
    
    <!-- More categories... -->
    <div class="flex items-center gap-3 text-slate-600 pl-4 py-3 hover:bg-slate-200/50 transition-all duration-200 rounded-lg">
      <span class="material-symbols-outlined">database</span>
      <span>Database</span>
    </div>
    
  </nav>
  
  <!-- Footer CTA -->
  <div class="px-6 pt-4 mt-auto border-t border-outline-variant/10">
    <button class="w-full bg-primary text-on-primary py-3 rounded-lg font-bold flex items-center justify-center gap-2 active:scale-95 transition-transform">
      <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">bolt</span>
      Upgrade to Pro
    </button>
  </div>
  
</aside>
```

**Mobile Drawer Specifications:**
- Width: 80% of screen, max 320px (`w-[80%] max-w-[320px]`)
- Position: `fixed left-0 top-0`
- Z-index: `z-[70]` (above overlay)
- Background: `bg-slate-100`
- Overlay: `fixed inset-0 bg-inverse-surface/40 z-[60] backdrop-blur-[2px]`
- Close button: `material-symbols-outlined` with `close` icon
- Category items: `pl-4 py-3` padding, `gap-3` between icon and text
- Active item: `text-cyan-700 border-l-2 border-cyan-700 bg-surface-container-low rounded-r-lg`
- Expand indicator: `expand_more` icon on right
- Sub-section indentation: `ml-10` with left border
- Sub-section labels: `text-[10px] uppercase tracking-tighter`
- Sub-section items: `text-slate-600 hover:text-cyan-700`
- Multi-column grid for many items: `grid grid-cols-2 gap-x-2`
- CTA button: full width, `py-3`, with icon, `active:scale-95`

**JavaScript for Drawer Toggle:**
```javascript
function toggleDrawer() {
  const drawer = document.querySelector('aside.z-\\[70\\]');
  const overlay = document.querySelector('.z-\\[60\\]');
  drawer.classList.toggle('translate-x-[-100%]');
  overlay.classList.toggle('hidden');
}

function closeDrawer() {
  const drawer = document.querySelector('aside.z-\\[70\\]');
  const overlay = document.querySelector('.z-\\[60\\]');
  drawer.classList.add('translate-x-[-100%]');
  overlay.classList.add('hidden');
}
```

### 3.4 Mobile Bottom Navigation Bar

```html
<nav class="fixed bottom-0 w-full z-40 bg-slate-50/80 backdrop-blur-xl flex justify-around py-4 shadow-[0_-2px_10px_rgba(0,0,0,0.02)] md:hidden">
  <!-- Active Item -->
  <button class="flex flex-col items-center gap-1 text-cyan-700">
    <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">home</span>
    <span class="text-[10px] font-bold">Home</span>
  </button>
  
  <!-- Inactive Items -->
  <button class="flex flex-col items-center gap-1 text-slate-400">
    <span class="material-symbols-outlined">explore</span>
    <span class="text-[10px] font-medium">Explore</span>
  </button>
  <button class="flex flex-col items-center gap-1 text-slate-400">
    <span class="material-symbols-outlined">book</span>
    <span class="text-[10px] font-medium">Library</span>
  </button>
  <button class="flex flex-col items-center gap-1 text-slate-400">
    <span class="material-symbols-outlined">settings</span>
    <span class="text-[10px] font-medium">Settings</span>
  </button>
</nav>
```

**Bottom Nav Specifications:**
- Position: `fixed bottom-0 w-full`
- Z-index: `z-40`
- Background: `bg-slate-50/80 backdrop-blur-xl`
- Hidden on desktop: `md:hidden`
- Layout: `flex justify-around py-4`
- Top shadow: `shadow-[0_-2px_10px_rgba(0,0,0,0.02)]`
- Items: `flex flex-col items-center gap-1`
- Icon: default material symbols
- Active icon: `style="font-variation-settings: 'FILL' 1;"` (filled icon)
- Active text: `text-[10px] font-bold text-cyan-700`
- Inactive text: `text-[10px] font-medium text-slate-400`

### 3.5 Breadcrumbs

#### DESKTOP Breadcrumbs

```html
<nav class="flex items-center gap-2 mb-10 text-xs font-medium text-on-surface-variant font-label">
  <a class="hover:text-primary transition-colors" href="#">Home</a>
  <span class="material-symbols-outlined text-[14px] opacity-40">chevron_right</span>
  <a class="hover:text-primary transition-colors" href="#">Cloud</a>
  <span class="material-symbols-outlined text-[14px] opacity-40">chevron_right</span>
  <a class="hover:text-primary transition-colors" href="#">Providers</a>
  <span class="material-symbols-outlined text-[14px] opacity-40">chevron_right</span>
  <a class="hover:text-primary transition-colors" href="#">AWS</a>
  <span class="material-symbols-outlined text-[14px] opacity-40">chevron_right</span>
  <span class="text-primary font-semibold">Services</span>
</nav>
```

#### MOBILE Breadcrumbs

```html
<nav class="flex items-center space-x-2 text-xs font-medium text-on-surface-variant/60 mb-8">
  <a class="hover:text-primary transition-colors" href="#">Home</a>
  <span class="material-symbols-outlined text-[10px]">chevron_right</span>
  <span class="text-on-surface font-semibold">Cloud</span>
</nav>
```

**Breadcrumb Specifications:**
- Spacing between items: `gap-2` (desktop) / `space-x-2` (mobile)
- Separator icon: `chevron_right` at `text-[14px]` (desktop) / `text-[10px]` (mobile)
- Separator opacity: `opacity-40`
- Link text: `text-xs font-medium text-on-surface-variant`
- Link hover: `hover:text-primary transition-colors`
- Current page: `text-primary font-semibold` (desktop) / `text-on-surface font-semibold` (mobile)
- Bottom margin: `mb-10` (desktop) / `mb-8` (mobile)

### 3.6 Page Header (Title + Description)

#### DESKTOP Page Header

```html
<header class="mb-16">
  <h1 class="text-5xl font-extrabold text-on-surface font-headline tracking-tighter mb-4">AWS Services</h1>
  <p class="text-lg text-on-surface-variant font-body leading-relaxed max-w-2xl">
    Navigate the extensive ecosystem of Amazon Web Services. Each module represents a foundational block for cloud-native architectural patterns.
  </p>
</header>
```

#### MOBILE Page Header

```html
<div class="mb-8">
  <h1 class="text-3xl font-extrabold tracking-tight text-on-surface mb-2">Systems Design & Logic</h1>
  <p class="text-on-surface-variant leading-relaxed">Modern architectural principles for technical hierarchies and distributed systems.</p>
</div>
```

**Page Header Specifications:**
- Desktop h1: `text-5xl font-extrabold tracking-tighter mb-4`
- Mobile h1: `text-3xl font-extrabold tracking-tight mb-2`
- Font: Manrope (`font-headline` / `font-manrope`)
- Desktop description: `text-lg text-on-surface-variant leading-relaxed max-w-2xl`
- Mobile description: `text-on-surface-variant leading-relaxed`
- Bottom margin: `mb-16` (desktop) / `mb-8` (mobile)

### 3.7 Bento Grid Card System

#### DESKTOP Bento Grid Layout

```html
<div class="grid grid-cols-1 md:grid-cols-12 gap-6">
  
  <!-- Large Feature Card (spans 8 columns) -->
  <div class="md:col-span-8 bg-surface-container-lowest rounded-xl overflow-hidden group hover:shadow-lg transition-all duration-500 flex flex-col md:flex-row min-h-[320px]">
    <div class="md:w-1/2 p-8 flex flex-col justify-between">
      <div>
        <!-- Icon Container -->
        <div class="w-12 h-12 rounded-lg bg-primary-container text-on-primary-container flex items-center justify-center mb-6">
          <span class="material-symbols-outlined text-2xl">architecture</span>
        </div>
        <h3 class="text-2xl font-bold mb-3 text-on-surface">Architecture</h3>
        <p class="text-on-surface-variant text-sm leading-relaxed mb-6">
          Master high-availability, fault-tolerance, and scalable patterns.
        </p>
      </div>
      <a class="inline-flex items-center text-primary font-bold text-sm group-hover:translate-x-1 transition-transform" href="#">
        Explore Frameworks <span class="material-symbols-outlined ml-2 text-sm">arrow_forward</span>
      </a>
    </div>
    <!-- Image Side -->
    <div class="md:w-1/2 relative bg-slate-900 overflow-hidden">
      <img src="image.jpg" alt="Description" class="w-full h-full object-cover opacity-80 group-hover:scale-110 transition-transform duration-700" />
      <div class="absolute inset-0 bg-gradient-to-r from-surface-container-lowest to-transparent"></div>
    </div>
  </div>
  
  <!-- Medium Card (spans 4 columns) -->
  <div class="md:col-span-4 bg-surface-container-lowest p-8 rounded-xl group hover:shadow-lg transition-all duration-500 border-none flex flex-col justify-between min-h-[320px]">
    <div>
      <div class="w-12 h-12 rounded-lg bg-secondary-container text-on-secondary-container flex items-center justify-center mb-6">
        <span class="material-symbols-outlined text-2xl">hub</span>
      </div>
      <h3 class="text-2xl font-bold mb-3 text-on-surface">Providers</h3>
      <p class="text-on-surface-variant text-sm leading-relaxed mb-6">
        Deep-dives into AWS, Azure, and GCP.
      </p>
      <!-- Tags -->
      <div class="flex flex-wrap gap-2">
        <span class="px-3 py-1 bg-surface-container text-on-surface-variant text-[10px] font-bold rounded-full uppercase tracking-wider">AWS</span>
        <span class="px-3 py-1 bg-surface-container text-on-surface-variant text-[10px] font-bold rounded-full uppercase tracking-wider">Azure</span>
        <span class="px-3 py-1 bg-surface-container text-on-surface-variant text-[10px] font-bold rounded-full uppercase tracking-wider">GCP</span>
      </div>
    </div>
    <a class="inline-flex items-center text-primary font-bold text-sm mt-8 group-hover:translate-x-1 transition-transform" href="#">
      View Ecosystems <span class="material-symbols-outlined ml-2 text-sm">arrow_forward</span>
    </a>
  </div>
  
  <!-- List Card (spans 5 columns) -->
  <div class="md:col-span-5 bg-surface-container-highest/30 backdrop-blur-sm p-8 rounded-xl group hover:shadow-lg transition-all duration-500 flex flex-col justify-between min-h-[280px]">
    <div>
      <h3 class="text-xl font-bold mb-3 text-on-surface">Fundamentals</h3>
      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-surface-container-lowest rounded-lg group/item cursor-pointer">
          <span class="text-sm font-medium">Compute (EC2, Lambda)</span>
          <span class="material-symbols-outlined text-sm opacity-0 group-hover/item:opacity-100 transition-opacity">chevron_right</span>
        </div>
        <div class="flex items-center justify-between p-3 bg-surface-container-lowest rounded-lg group/item cursor-pointer">
          <span class="text-sm font-medium">Storage (S3, Blob)</span>
          <span class="material-symbols-outlined text-sm opacity-0 group-hover/item:opacity-100 transition-opacity">chevron_right</span>
        </div>
        <div class="flex items-center justify-between p-3 bg-surface-container-lowest rounded-lg group/item cursor-pointer">
          <span class="text-sm font-medium">Networking & VPC</span>
          <span class="material-symbols-outlined text-sm opacity-0 group-hover/item:opacity-100 transition-opacity">chevron_right</span>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Featured Dark Card (spans 7 columns) -->
  <div class="md:col-span-7 relative bg-slate-900 rounded-xl overflow-hidden min-h-[280px] group">
    <img src="image.jpg" alt="Description" class="w-full h-full object-cover opacity-50 group-hover:scale-105 transition-transform duration-1000" />
    <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent p-8 flex flex-col justify-end">
      <span class="text-[10px] font-bold text-primary-fixed uppercase tracking-[0.2em] mb-2">Featured Guide</span>
      <h3 class="text-2xl font-bold text-white mb-2">Serverless Mastery</h3>
      <p class="text-slate-300 text-sm max-w-sm mb-4">The definitive architect's guide to event-driven serverless systems.</p>
      <button class="bg-white/10 backdrop-blur-md border border-white/20 text-white px-6 py-2 rounded-lg text-sm font-bold hover:bg-white/20 transition-colors self-start">
        Read Now
      </button>
    </div>
  </div>
  
</div>
```

**Desktop Bento Grid Specifications:**
- Grid: `grid grid-cols-1 md:grid-cols-12 gap-6`
- Card backgrounds: `bg-surface-container-lowest` (white) / `bg-surface-container-highest/30` (tinted)
- Card border radius: `rounded-xl`
- Card padding: `p-8`
- Card hover: `hover:shadow-lg transition-all duration-500`
- Icon container: `w-12 h-12 rounded-lg` with color variant backgrounds
- Icon size: `text-2xl` (24px)
- Card title: `text-2xl font-bold mb-3`
- Card description: `text-sm text-on-surface-variant leading-relaxed mb-6`
- CTA link: `text-primary font-bold text-sm` with `arrow_forward` icon
- CTA hover: `group-hover:translate-x-1 transition-transform`
- Tags: `px-3 py-1 bg-surface-container text-[10px] font-bold rounded-full uppercase tracking-wider`
- List items: `p-3 bg-surface-container-lowest rounded-lg` with hover-reveal chevron
- Dark card: `bg-slate-900` with overlay gradient and white text
- Dark card label: `text-[10px] font-bold text-primary-fixed uppercase tracking-[0.2em]`
- Dark card button: `bg-white/10 backdrop-blur-md border border-white/20`

#### MOBILE Card Layout

```html
<div class="grid grid-cols-1 gap-4">
  
  <!-- Feature Card -->
  <div class="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4">
    <div class="w-12 h-12 bg-primary-container rounded-full flex items-center justify-center text-on-primary-container">
      <span class="material-symbols-outlined">architecture</span>
    </div>
    <h3 class="text-lg font-bold">Distributed Architectures</h3>
    <p class="text-on-surface-variant text-sm">Deep dive into microservices patterns and event-driven data flow.</p>
  </div>
  
  <!-- Image Card -->
  <div class="bg-surface-container rounded-xl overflow-hidden relative min-h-[200px]">
    <img src="image.jpg" alt="Description" class="absolute inset-0 w-full h-full object-cover opacity-20" />
    <div class="relative z-10 p-6 flex flex-col h-full justify-end">
      <h3 class="text-lg font-bold text-primary">Core Modules</h3>
      <p class="text-on-surface-variant text-sm">Access 45+ technical modules designed for senior developers.</p>
    </div>
  </div>
  
</div>
```

**Mobile Card Specifications:**
- Grid: `grid grid-cols-1 gap-4` (single column)
- Card padding: `p-6` (smaller than desktop `p-8`)
- Card background: `bg-surface-container-lowest`
- Card radius: `rounded-xl`
- Card shadow: `shadow-sm`
- Icon: `w-12 h-12 bg-primary-container rounded-full` (circular on mobile)
- Title: `text-lg font-bold` (smaller than desktop `text-2xl`)
- Description: `text-sm text-on-surface-variant`
- Image card: `min-h-[200px]` with `opacity-20` overlay
- Content overlay: `relative z-10 p-6 flex flex-col h-full justify-end`

### 3.8 Asymmetric Content Grid (Deep Content Pages)

```html
<div class="asymmetric-grid">
  <!-- Left Column (wider - 1.5fr) -->
  <section class="bg-surface-container-lowest rounded-xl p-8 transition-all hover:bg-surface-container-low">
    <div class="flex items-center justify-between mb-8">
      <h2 class="text-2xl font-bold font-headline text-cyan-800">Compute Ecosystem</h2>
      <span class="material-symbols-outlined text-primary">bolt</span>
    </div>
    
    <!-- Content Item -->
    <div class="group cursor-pointer">
      <div class="flex justify-between items-start mb-2">
        <h3 class="font-bold text-lg">EC2 <span class="text-xs font-normal text-slate-400 ml-2">Elastic Compute Cloud</span></h3>
        <span class="text-primary-dim text-xs font-bold uppercase tracking-widest px-2 py-0.5 bg-primary-container/30 rounded">Core</span>
      </div>
      <p class="text-sm text-on-surface-variant font-body mb-4">Virtual servers in the cloud with complete control.</p>
      <!-- Tags -->
      <div class="flex gap-2">
        <span class="bg-surface-container px-2 py-1 rounded text-[10px] font-bold text-slate-500">Auto-Scaling</span>
        <span class="bg-surface-container px-2 py-1 rounded text-[10px] font-bold text-slate-500">EBS-Backed</span>
      </div>
    </div>
    
    <!-- Divider -->
    <div class="h-px bg-outline-variant/10 my-6"></div>
    
    <!-- More items... -->
  </section>
  
  <!-- Right Column (narrower - 1fr) -->
  <div class="flex flex-col gap-8">
    <!-- Storage Card -->
    <section class="bg-surface-container rounded-xl p-8">
      <h2 class="text-xl font-bold font-headline text-cyan-800 mb-6">Storage Assets</h2>
      <div class="space-y-6">
        <div class="flex items-start gap-4">
          <div class="bg-surface-container-lowest p-2 rounded-lg">
            <span class="material-symbols-outlined text-primary">inventory_2</span>
          </div>
          <div>
            <h4 class="font-bold text-sm">S3 (Simple Storage Service)</h4>
            <p class="text-xs text-on-surface-variant mt-1">Object storage built to retrieve any amount of data.</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Database Card with left accent -->
    <section class="bg-surface-container-high rounded-xl p-8 border-l-4 border-primary">
      <h2 class="text-xl font-bold font-headline text-cyan-800 mb-6">Database Tier</h2>
      <div class="space-y-4">
        <div class="bg-surface-container-lowest p-4 rounded-lg flex justify-between items-center">
          <div>
            <h4 class="font-bold text-sm">RDS</h4>
            <p class="text-[10px] text-slate-500">Relational Database Service</p>
          </div>
          <span class="material-symbols-outlined text-slate-400 text-sm">open_in_new</span>
        </div>
      </div>
    </section>
  </div>
</div>
```

**Asymmetric Grid Specifications:**
- CSS: `grid-template-columns: 1.5fr 1fr; gap: 2rem;`
- Responsive: collapses to single column at `max-width: 1024px`
- Section headers: `text-2xl font-bold text-cyan-800` with icon on right
- Content items: separated by `h-px bg-outline-variant/10` dividers
- Badge/Tag: `text-xs font-bold uppercase tracking-widest px-2 py-0.5 bg-primary-container/30 rounded`
- Icon containers: `bg-surface-container-lowest p-2 rounded-lg`
- Left accent border: `border-l-4 border-primary`
- Nested items: `p-4 rounded-lg flex justify-between items-center`

### 3.9 Visualization/CTA Section

```html
<section class="mt-12">
  <div class="bg-surface-container-lowest rounded-xl overflow-hidden relative min-h-[400px] flex items-center justify-center p-12">
    <!-- Background Gradient -->
    <div class="absolute inset-0 opacity-10 bg-gradient-to-br from-primary to-transparent"></div>
    
    <!-- Centered Content -->
    <div class="relative z-10 text-center">
      <div class="mb-6 inline-flex p-4 bg-primary-container rounded-full">
        <span class="material-symbols-outlined text-on-primary-container text-4xl">hub</span>
      </div>
      <h2 class="text-3xl font-bold font-headline mb-4">Architecture Visualization</h2>
      <p class="text-on-surface-variant font-body max-w-xl mx-auto mb-8">
        Interactive infrastructure diagrams coming soon.
      </p>
      <div class="flex justify-center gap-4">
        <button class="bg-primary text-on-primary px-6 py-2.5 rounded-lg text-sm font-bold">Join Waitlist</button>
        <button class="bg-surface-container-highest text-primary px-6 py-2.5 rounded-lg text-sm font-bold">View Samples</button>
      </div>
    </div>
    
    <!-- Decorative Graphic -->
    <div class="absolute bottom-0 right-0 w-64 h-64 opacity-20">
      <img src="graphic.png" alt="Technical graphic" class="w-full h-full object-contain" />
    </div>
  </div>
</section>
```

**Visualization Section Specifications:**
- Top margin: `mt-12`
- Container: `min-h-[400px] p-12` with centered content
- Background gradient: `opacity-10 bg-gradient-to-br from-primary to-transparent`
- Icon container: `p-4 bg-primary-container rounded-full`
- Icon: `text-4xl`
- Title: `text-3xl font-bold mb-4`
- Description: `max-w-xl mx-auto mb-8`
- Primary button: `bg-primary text-on-primary px-6 py-2.5 rounded-lg text-sm font-bold`
- Secondary button: `bg-surface-container-highest text-primary px-6 py-2.5 rounded-lg text-sm font-bold`
- Buttons gap: `gap-4`
- Decorative image: `absolute bottom-0 right-0 w-64 h-64 opacity-20`

### 3.10 Footer

#### DESKTOP Footer

```html
<footer class="mt-24 w-full py-12 border-t border-slate-200/20 dark:border-slate-800/20">
  <div class="flex flex-col md:flex-row justify-between items-center px-4 max-w-7xl mx-auto">
    <div class="mb-6 md:mb-0">
      <span class="font-manrope font-bold text-slate-800 dark:text-slate-200 text-lg">Architectural Scholar</span>
      <p class="font-inter text-xs tracking-wide text-slate-400 dark:text-slate-500 mt-1">© 2024 Architectural Scholar. All rights reserved.</p>
    </div>
    <div class="flex space-x-8">
      <a class="font-inter text-xs tracking-wide text-slate-400 dark:text-slate-500 hover:text-cyan-700 dark:hover:text-cyan-400 transition-colors" href="#">Documentation</a>
      <a class="font-inter text-xs tracking-wide text-slate-400 dark:text-slate-500 hover:text-cyan-700 dark:hover:text-cyan-400 transition-colors" href="#">Privacy</a>
      <a class="font-inter text-xs tracking-wide text-slate-400 dark:text-slate-500 hover:text-cyan-700 dark:hover:text-cyan-400 transition-colors" href="#">Terms</a>
      <a class="font-inter text-xs tracking-wide text-slate-400 dark:text-slate-500 hover:text-cyan-700 dark:hover:text-cyan-400 transition-colors" href="#">Support</a>
    </div>
  </div>
</footer>
```

**Footer Specifications:**
- Top margin: `mt-24`
- Padding: `py-12`
- Border: `border-t border-slate-200/20`
- Layout: `flex flex-col md:flex-row justify-between items-center`
- Max width: `max-w-7xl mx-auto`
- Brand: `font-manrope font-bold text-lg`
- Copyright: `text-xs tracking-wide text-slate-400 mt-1`
- Links: `text-xs tracking-wide text-slate-400 hover:text-cyan-700 transition-colors`
- Link spacing: `space-x-8`
- Mobile: stacks vertically (`flex-col`), desktop: horizontal (`md:flex-row`)
- Brand bottom margin on mobile: `mb-6 md:mb-0`

### 3.11 Search Component

#### DESKTOP Search (in Top Nav)

```html
<div class="relative group">
  <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-primary text-lg">search</span>
  <input 
    class="w-full bg-surface-container-low border-none rounded-full py-1.5 pl-10 pr-4 text-sm focus:ring-1 focus:ring-primary/20 transition-all placeholder:text-slate-400" 
    type="text" 
    placeholder="Search architecture, patterns, or cloud..."
  />
</div>
```

**Desktop Search Specifications:**
- Container: `relative`
- Icon: `absolute left-3 top-1/2 -translate-y-1/2`
- Icon color: `text-slate-400` changing to `text-primary` on focus (`group-focus-within:`)
- Input background: `bg-surface-container-low`
- Input shape: `rounded-full`
- Input padding: `py-1.5 pl-10 pr-4`
- Input text: `text-sm`
- Focus ring: `focus:ring-1 focus:ring-primary/20`
- Placeholder: `placeholder:text-slate-400`
- Width: `max-w-md` in nav context
- Hidden on mobile: `hidden lg:block`

#### Alternative Landing Page Search (Prominent)

```html
<div class="flex-1 max-w-2xl mx-12">
  <div class="relative flex items-center">
    <span class="material-symbols-outlined absolute left-4 text-on-surface-variant">search</span>
    <input 
      class="w-full bg-surface-container-low border-none rounded-full py-2.5 pl-12 pr-4 text-sm focus:ring-2 focus:ring-primary/20 transition-all placeholder:text-on-surface-variant/60" 
      type="text" 
      placeholder="Search architectural patterns, languages, or roadmaps..."
    />
  </div>
</div>
```

**Landing Search Specifications:**
- Wider: `max-w-2xl`
- Centered in nav: `mx-12`
- Taller input: `py-2.5 pl-12`
- Stronger focus ring: `focus:ring-2`
- Placeholder: `placeholder:text-on-surface-variant/60`

### 3.12 Pro Upgrade CTA Card

#### DESKTOP Sidebar CTA

```html
<div class="px-6 mt-auto">
  <div class="bg-surface-container-highest/50 p-4 rounded-xl text-center">
    <p class="text-xs text-on-surface-variant mb-3">Master the Architecture</p>
    <button class="w-full py-2 bg-primary text-on-primary text-xs font-bold rounded-lg hover:bg-primary-dim transition-colors">
      Upgrade to Pro
    </button>
  </div>
</div>
```

#### Alternative Gradient CTA

```html
<div class="p-6 mt-auto">
  <div class="bg-gradient-to-br from-primary to-primary-dim p-4 rounded-xl shadow-lg shadow-primary/20">
    <p class="text-on-primary text-xs font-bold mb-2">Upgrade to Pro</p>
    <p class="text-on-primary/80 text-[10px] leading-relaxed mb-3">Get advanced architecture diagrams and expert review.</p>
    <button class="w-full bg-white text-primary text-[11px] font-bold py-2 rounded-lg hover:bg-on-primary transition-colors">
      Learn More
    </button>
  </div>
</div>
```

**CTA Specifications:**
- Position: `mt-auto` (pushed to bottom of sidebar)
- Card background option 1: `bg-surface-container-highest/50`
- Card background option 2: `bg-gradient-to-br from-primary to-primary-dim`
- Card padding: `p-4`
- Card radius: `rounded-xl`
- Shadow for gradient version: `shadow-lg shadow-primary/20`
- Title: `text-xs font-bold`
- Description: `text-[10px] leading-relaxed mb-3`
- Button: `w-full py-2 text-xs font-bold rounded-lg`
- Button hover: `hover:bg-primary-dim` (primary bg) / `hover:bg-on-primary` (white bg)

#### MOBILE Drawer CTA

```html
<div class="px-6 pt-4 mt-auto border-t border-outline-variant/10">
  <button class="w-full bg-primary text-on-primary py-3 rounded-lg font-bold flex items-center justify-center gap-2 active:scale-95 transition-transform">
    <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">bolt</span>
    Upgrade to Pro
  </button>
</div>
```

**Mobile CTA Specifications:**
- Top border separator: `border-t border-outline-variant/10`
- Top padding: `pt-4`
- Button: taller `py-3` with icon
- Icon: filled bolt icon
- Active state: `active:scale-95`

---

## Phase 4: Responsive Behavior Matrix

| Element | Desktop (≥768px) | Mobile (<768px) |
|---------|------------------|-----------------|
| **Top Nav** | Fixed, brand left, search center, icons right | Fixed, hamburger left, brand, icons right, NO search |
| **Sidebar** | Fixed 288px left sidebar, always visible | Hidden, replaced by slide-out drawer (80% width) |
| **Main Content** | `ml-72` offset, `px-12 py-10` padding | Full width, `px-6 py-8` padding, `pt-20` top |
| **Bottom Nav** | Hidden (`md:hidden`) | Fixed bottom, 4-5 items, `py-4` |
| **Breadcrumbs** | Full path, `mb-10`, `gap-2` | Shorter path, `mb-8`, smaller icons |
| **Page Title** | `text-5xl`, `mb-4`, `tracking-tighter` | `text-3xl`, `mb-2`, `tracking-tight` |
| **Description** | `text-lg`, `max-w-2xl`, `leading-relaxed` | Default text size, no max-width |
| **Card Grid** | 12-column grid, asymmetric spans | Single column, `gap-4` |
| **Cards** | `p-8`, `min-h-[280-320px]`, hover shadows | `p-6`, smaller heights, `shadow-sm` |
| **Card Icons** | `rounded-lg` (square) | `rounded-full` (circular) |
| **Card Titles** | `text-2xl` | `text-lg` |
| **CTA Buttons** | `px-6 py-2.5` | Full width, `py-3` |
| **Footer** | Horizontal layout, `space-x-8` | Vertical stack, `mb-6` for brand |
| **Search** | In top nav, `max-w-md` | Not in top nav (access via separate page/modal) |
| **Pro CTA** | In sidebar bottom | In drawer bottom, with border separator |

---

## Phase 5: Interactive States & Animations

### 5.1 Hover States

```css
/* Nav Items */
hover:bg-slate-200/50 transition-all duration-200

/* Cards */
hover:shadow-lg transition-all duration-500
hover:bg-surface-container

/* Links */
hover:text-cyan-700 transition-colors
hover:text-primary transition-colors

/* CTA Arrows */
group-hover:translate-x-1 transition-transform

/* Card Images */
group-hover:scale-110 transition-transform duration-700

/* List Item Chevrons */
opacity-0 group-hover/item:opacity-100 transition-opacity
```

### 5.2 Active/Press States

```css
/* Nav Items */
active:scale-95

/* Buttons */
active:scale-95 transition-transform

/* Mobile Hamburger */
active:opacity-80 transition-opacity
```

### 5.3 Focus States

```css
/* Search Input */
focus:ring-1 focus:ring-primary/20 transition-all
focus:ring-2 focus:ring-primary/20 (landing page)

/* Focus-within for search container */
group-focus-within:text-primary
```

### 5.4 Transitions

```css
/* Standard */
transition-all duration-200
transition-all duration-300
transition-all duration-500

/* Specific */
transition-colors
transition-colors duration-200
transition-transform
transition-transform duration-700
transition-transform duration-1000
transition-opacity
```

---

## Phase 6: Implementation Checklist

### 6.1 Setup Tasks
- [ ] Install/configure Tailwind CSS with custom config
- [ ] Add Google Fonts: Manrope (400, 600, 700, 800) + Inter (400, 500, 600)
- [ ] Add Material Symbols Outlined font
- [ ] Define all color tokens in Tailwind config
- [ ] Define border radius tokens
- [ ] Define font family utilities

### 6.2 Layout Tasks
- [ ] Create page shell with fixed top nav
- [ ] Implement desktop sidebar (hidden on mobile)
- [ ] Implement mobile drawer with overlay
- [ ] Implement mobile bottom navigation
- [ ] Set up responsive main content area
- [ ] Add footer component

### 6.3 Component Tasks
- [ ] Build top navigation bar (desktop + mobile variants)
- [ ] Build sidebar navigation with hierarchy
- [ ] Build mobile drawer navigation with expandable sections
- [ ] Build breadcrumb component
- [ ] Build page header (title + description)
- [ ] Build bento grid card system
- [ ] Build asymmetric content grid
- [ ] Build visualization/CTA section
- [ ] Build search component
- [ ] Build Pro upgrade CTA card
- [ ] Build footer

### 6.4 Interactive Tasks
- [ ] Add drawer open/close JavaScript
- [ ] Add hover states to all interactive elements
- [ ] Add active/press states to buttons
- [ ] Add focus states to inputs
- [ ] Add transition animations
- [ ] Add expandable sub-navigation toggle

### 6.5 Responsive Tasks
- [ ] Test all breakpoints (sm, md, lg, xl)
- [ ] Verify sidebar hides on mobile
- [ ] Verify bottom nav shows only on mobile
- [ ] Verify card grid collapses to single column
- [ ] Verify typography scales appropriately
- [ ] Verify touch targets are 44px minimum on mobile
- [ ] Verify drawer is accessible (trap focus, close on overlay click)

### 6.6 Dark Mode Tasks
- [ ] Add `dark:` variants to all components
- [ ] Test dark mode toggle
- [ ] Verify color contrast in dark mode
- [ ] Verify images/icons visibility in dark mode

---

## Phase 7: Quick Reference - Icon Mapping

| Category | Icon Name | Usage |
|----------|-----------|-------|
| Big Data | `analytics` | Sidebar nav item |
| Cloud | `cloud` | Sidebar nav item |
| Languages | `terminal` | Sidebar nav item |
| Database | `database` | Sidebar nav item |
| Cheatsheet | `description` | Sidebar nav item |
| Roadmap | `map` | Sidebar nav item |
| Portfolio | `account_circle` | Sidebar nav item |
| Architecture | `architecture` | Logo, feature cards |
| Search | `search` | Search input |
| Notifications | `notifications` | Top nav bell |
| Menu | `menu` | Mobile hamburger |
| Close | `close` | Drawer close button |
| Expand | `expand_more` | Expandable sections |
| Chevron Right | `chevron_right` | Breadcrumbs, list items |
| Forward Arrow | `arrow_forward` | Card CTAs |
| External Link | `open_in_new` | Database cards |
| Hub | `hub` | Providers card |
| Bolt | `bolt` | Pro CTA, compute |
| Code Blocks | `code_blocks` | Decorative element |
| Inventory | `inventory_2` | Storage card |
| Hard Drive | `hard_drive` | Storage card |

---

## Phase 8: File Structure Recommendation

```
your-project/
├── index.html                 # Landing page
├── pages/
│   ├── category.html          # Category detail page
│   ├── deep-content.html      # Deep content page
│   └── mobile-nav.html        # Mobile navigation (for testing)
├── assets/
│   ├── css/
│   │   └── main.css           # Custom styles + Tailwind imports
│   ├── js/
│   │   └── navigation.js      # Drawer toggle, interactions
│   └── images/
│       └── ...                # All images
├── components/ (if using framework)
│   ├── TopNav.html
│   ├── Sidebar.html
│   ├── MobileDrawer.html
│   ├── BottomNav.html
│   ├── Breadcrumbs.html
│   ├── PageHeader.html
│   ├── CardGrid.html
│   ├── Card.html
│   ├── Footer.html
│   └── SearchBar.html
└── tailwind.config.js
```

---

## Summary

This plan covers every element from the Architectural Scholar design system:

1. **Foundation**: Colors, typography, spacing, borders, breakpoints
2. **Layout**: Desktop sidebar + mobile responsive shell
3. **Components**: Top nav, sidebar, drawer, bottom nav, breadcrumbs, headers, cards, footer, search, CTA
4. **Responsive**: Exact specifications for desktop vs mobile for every element
5. **Interactions**: Hover, active, focus states with exact Tailwind classes
6. **Checklist**: Step-by-step implementation tasks
7. **Icons**: Complete icon mapping for all navigation items
8. **Structure**: Recommended file organization

Follow phases 1-8 sequentially for a complete transformation of your website to match this design system.
