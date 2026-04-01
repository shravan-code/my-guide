// Site Configuration - Generated from links.yaml
// This file is the single source of truth for site navigation

const SITE_CONFIG = {
  site: {
    name: "*d@ta#",
    brandHover: "Data.id.name",
    url: "index.html"
  },

  topbar: {
    brand: {
      text: "*d@ta#",
      hoverText: "Data.id.name",
      url: "index.html"
    },
    themeToggle: true,
    portfolioLink: {
      text: "Portfolio",
      url: "source/portfolios/portfolio.html"
    }
  },

  sections: [
    { name: "cloud", title: "Cloud", url: "source/cloud/index.html" },
    { name: "data", title: "Big Data", url: "source/data/index.html" },
    { name: "python", title: "Python", url: "source/python/index.html" },
    { name: "sql", title: "SQL", url: "source/sql/index.html" },
    { name: "cheatsheets", title: "Cheatsheet", url: "source/cheatsheets/cheatsheet.html" },
    { name: "roadmaps", title: "Roadmap", url: "source/roadmaps/roadmap.html" }
  ],

  libraries: [
    { name: "pandas", title: "Pandas", description: "DataFrames and analysis", url: "source/pandas/index.html" },
    { name: "numpy", title: "NumPy", description: "Numerical computing", url: "source/numpy/index.html" },
    { name: "spark", title: "Spark", description: "Distributed processing", url: "source/spark/index.html" }
  ],

  roadmaps: {
    hub: { title: "Hub", url: "source/roadmaps/roadmap.html" },
    items: [
      { name: "data-engineer", title: "Data Engineering", url: "source/roadmaps/data-engineer-roadmap.html" },
      { name: "python", title: "Python", url: "source/roadmaps/python-roadmap.html" },
      { name: "sql", title: "SQL", url: "source/roadmaps/sql-roadmap.html" },
      { name: "spark", title: "Spark", url: "source/roadmaps/spark-roadmap.html" },
      { name: "ml-engineer", title: "ML Engineer", url: "source/roadmaps/ml-engineer-roadmap.html" },
      { name: "ai-engineer", title: "AI Engineer", url: "source/roadmaps/ai-engineer-roadmap.html" }
    ]
  },

  cheatsheets: {
    hub: { title: "Hub", url: "source/cheatsheets/cheatsheet.html" },
    items: [
      { name: "python", title: "Python", url: "source/cheatsheets/python-cheatsheet.html" },
      { name: "numpy", title: "NumPy", url: "source/cheatsheets/numpy-cheatsheet.html" },
      { name: "pandas", title: "Pandas", url: "source/cheatsheets/pandas-cheatsheet.html" },
      { name: "spark", title: "PySpark", url: "source/cheatsheets/spark-cheatsheet.html" },
      { name: "postgresql", title: "PostgreSQL", url: "source/cheatsheets/postgresql-cheatsheet.html" },
      { name: "compare", title: "Comparison", url: "source/cheatsheets/compare.html" }
    ]
  },

  portfolio: {
    url: "source/portfolios/portfolio.html",
    projects: {
      experienced: { title: "Experienced", url: "source/portfolios/projects/projects-experienced.html" },
      self: { title: "Self", url: "source/portfolios/projects/projects-self.html" }
    }
  },

  career: {
    startDate: "2021-11-02"
  }
};

// Helper: resolve URL relative to site root
function resolveUrl(url) {
  if (url.startsWith("http") || url.startsWith("/")) return url;
  const depth = (window.location.pathname.match(/\//g) || []).length - 1;
  const prefix = depth > 1 ? "../".repeat(depth - 1) : "";
  return prefix + url;
}

// Helper: build brand HTML
function buildBrand() {
  return `<a class="brand" href="${resolveUrl(SITE_CONFIG.topbar.brand.url)}">
    <span class="brand-default">${SITE_CONFIG.topbar.brand.text}</span>
    <span class="brand-hover">${SITE_CONFIG.topbar.brand.hoverText}</span>
  </a>`;
}

// Helper: build topbar menu HTML
function buildMenu(activePage) {
  return `<nav class="menu" aria-label="Main menu">${
    SITE_CONFIG.sections.map(s =>
      `<a href="${resolveUrl(s.url)}" class="${s.name === activePage ? 'active' : ''}">${s.title}</a>`
    ).join("")
  }</nav>`;
}

// Helper: build roadmap menu HTML
function buildRoadmapMenu(activePage) {
  const items = [SITE_CONFIG.roadmaps.hub, ...SITE_CONFIG.roadmaps.items];
  return `<nav class="menu" aria-label="Roadmap menu">${
    items.map(r =>
      `<a href="${resolveUrl(r.url)}" class="${r.url.includes(activePage) ? 'active' : ''}">${r.title}</a>`
    ).join("")
  }</nav>`;
}

// Helper: build cheatsheet menu HTML
function buildCheatsheetMenu(activePage) {
  const items = [SITE_CONFIG.cheatsheets.hub, ...SITE_CONFIG.cheatsheets.items];
  return `<nav class="menu" aria-label="Cheatsheet menu">${
    items.map(c =>
      `<a href="${resolveUrl(c.url)}" class="${c.url.includes(activePage) ? 'active' : ''}">${c.title}</a>`
    ).join("")
  }</nav>`;
}

// Helper: build header actions HTML
function buildHeaderActions() {
  return `<div class="header-actions">
    <button id="theme-toggle" class="theme-toggle" type="button" aria-label="Toggle light and dark mode">
      <span class="theme-icon-wrapper">
        <svg class="theme-sun" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="4"/>
          <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
        </svg>
        <svg class="theme-moon" viewBox="0 0 24 24" fill="none">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </span>
    </button>
  </div>`;
}

// Helper: build full topbar HTML
function buildTopbar(activePage, menuType) {
  let menuHtml;
  switch (menuType) {
    case "roadmaps": menuHtml = buildRoadmapMenu(activePage); break;
    case "cheatsheets": menuHtml = buildCheatsheetMenu(activePage); break;
    default: menuHtml = buildMenu(activePage);
  }
  return `<header class="topbar glass reveal in">
    ${buildBrand()}
    ${menuHtml}
    ${buildHeaderActions()}
  </header>`;
}

// Helper: build bottom bar HTML
function buildBottomBar() {
  return `<footer class="bottom-bar">
    <span class="current-page-path" id="current-path"></span>
    <span class="experience-years">Experience: <strong id="career-timer"></strong></span>
  </footer>`;
}

// Helper: initialize career timer
function initCareerTimer() {
  const careerTimer = document.getElementById("career-timer");
  if (!careerTimer) return;
  const startDate = new Date(SITE_CONFIG.career.startDate);
  function update() {
    const now = new Date();
    let years = now.getFullYear() - startDate.getFullYear();
    let months = now.getMonth() - startDate.getMonth();
    let days = now.getDate() - startDate.getDate();
    if (days < 0) { months--; days += new Date(now.getFullYear(), now.getMonth(), 0).getDate(); }
    if (months < 0) { years--; months += 12; }
    careerTimer.textContent = `${years} years ${months} months ${days} days`;
  }
  update();
  setInterval(update, 86400000);
}

// Helper: initialize current path pills
function initCurrentPath() {
  const el = document.getElementById("current-path");
  if (!el) return;
  const filename = window.location.pathname.split("/").pop().replace(".html", "");
  const label = filename.replace("-roadmap", "").replace("-cheatsheet", "").replace(/[-_]/g, " ");
  const words = ["home", label];
  el.innerHTML = words.map(w => `<span class="path-pill">${w}</span>`).join("");
}
