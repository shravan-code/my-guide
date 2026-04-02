// ---- Theme Toggle ----
const body = document.body;
const toggleButton = document.getElementById("theme-toggle");
const toggleText = toggleButton?.querySelector(".toggle-text");
const toggleIcon = toggleButton?.querySelector(".toggle-icon");
const storageKey = "data-guide-theme";
const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
const topMenu = document.querySelector(".menu");
const portfolioLink = document.querySelector(".portfolio-link");

function applyTheme(mode) {
  const isDark = mode === "dark";
  body.classList.toggle("dark", isDark);
  document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");

  if (toggleText) {
    toggleText.textContent = isDark ? "Light" : "Dark";
  }

  if (toggleIcon) {
    toggleIcon.textContent = isDark ? "☀" : "☾";
  }

  const sun = toggleButton?.querySelector(".theme-sun");
  const moon = toggleButton?.querySelector(".theme-moon");
  if (sun && moon) {
    if (isDark) {
      sun.style.opacity = "0";
      moon.style.opacity = "1";
    } else {
      sun.style.opacity = "1";
      moon.style.opacity = "0";
    }
  }
}

const storedTheme = localStorage.getItem(storageKey);
const prefersDark = mediaQuery.matches;
const initialTheme = storedTheme || (prefersDark ? "dark" : "light");

applyTheme(initialTheme);

toggleButton?.addEventListener("click", () => {
  const nextTheme = body.classList.contains("dark") ? "light" : "dark";
  localStorage.setItem(storageKey, nextTheme);
  applyTheme(nextTheme);
});

mediaQuery.addEventListener("change", (event) => {
  const saved = localStorage.getItem(storageKey);
  if (!saved) {
    applyTheme(event.matches ? "dark" : "light");
  }
});

function buildMobileMenuFromDesktop() {
  if (!topMenu || document.getElementById("mobile-menu-toggle")) {
    return;
  }

  const headerActions = document.querySelector(".header-actions") || toggleButton?.parentElement;
  const toggleMarkup = `
    <button id="mobile-menu-toggle" class="mobile-menu-toggle" type="button" aria-label="Toggle mobile menu" aria-expanded="false">
      <span class="hamburger-icon" aria-hidden="true">
        <span></span>
        <span></span>
        <span></span>
      </span>
    </button>
  `;

  if (headerActions) {
    headerActions.insertAdjacentHTML("afterbegin", toggleMarkup);
  } else if (toggleButton) {
    toggleButton.insertAdjacentHTML("beforebegin", toggleMarkup);
  } else {
    topMenu.insertAdjacentHTML("afterend", toggleMarkup);
  }

  const groups = [];
  let currentGroup = { label: null, items: [] };
  for (const child of Array.from(topMenu.children)) {
    if (child.matches("a")) {
      currentGroup.items.push(child.outerHTML);
      continue;
    }

    if (child.matches(".menu-dropdown")) {
      if (currentGroup.items.length) {
        groups.push(currentGroup);
        currentGroup = { label: null, items: [] };
      }

      const triggerText = child.querySelector(".menu-trigger")?.textContent?.trim() || "More";
      const links = Array.from(child.querySelectorAll(".dropdown-panel a")).map((link) => link.outerHTML);
      groups.push({ label: triggerText, items: links });
    }
  }

  if (currentGroup.items.length) {
    groups.push(currentGroup);
  }

  if (portfolioLink) {
    groups.push({ label: null, items: [portfolioLink.outerHTML] });
  }

  const navMarkup = groups
    .map((group) => {
      const label = group.label ? `<div class="mobile-nav-label">${group.label}</div>` : "";
      return `<div class="mobile-nav-group">${label}${group.items.join("")}</div>`;
    })
    .join("");

  const mobileMenu = `
    <div id="mobile-menu" class="mobile-menu">
      <nav class="mobile-nav" aria-label="Mobile navigation">
        ${navMarkup}
      </nav>
    </div>
    <div id="mobile-menu-overlay" class="mobile-menu-overlay"></div>
  `;

  document.body.insertAdjacentHTML("beforeend", mobileMenu);
}

function attachMobileHandlers(mobileMenuToggle, mobileMenu, mobileMenuOverlay) {
  const closeMobileMenu = () => {
    mobileMenu.classList.remove("open");
    mobileMenuOverlay.classList.remove("active");
    mobileMenuToggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  };

  const openMobileMenu = () => {
    mobileMenu.classList.add("open");
    mobileMenuOverlay.classList.add("active");
    mobileMenuToggle.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  };

  mobileMenuToggle.addEventListener("click", () => {
    if (mobileMenu.classList.contains("open")) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
  });

  mobileMenuOverlay.addEventListener("click", closeMobileMenu);
  mobileMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMobileMenu);
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 920) {
      closeMobileMenu();
    }
  });
}

function initializeMobileMenu() {
  const mobileMenuToggle = document.getElementById("mobile-menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  const mobileMenuOverlay = document.getElementById("mobile-menu-overlay");

  if (!mobileMenuToggle || !mobileMenu || !mobileMenuOverlay) {
    buildMobileMenuFromDesktop();
    const retryToggle = document.getElementById("mobile-menu-toggle");
    const retryMenu = document.getElementById("mobile-menu");
    const retryOverlay = document.getElementById("mobile-menu-overlay");
    if (retryToggle && retryMenu && retryOverlay) {
      attachMobileHandlers(retryToggle, retryMenu, retryOverlay);
    }
    return;
  }

  attachMobileHandlers(mobileMenuToggle, mobileMenu, mobileMenuOverlay);
}

initializeMobileMenu();

// Sidebar toggle for all devices
function initializeSidebarToggle() {
  const sidebar = document.getElementById("sidebar");
  const sidebarOverlay = document.getElementById("sidebar-overlay");
  const sidebarToggle = document.getElementById("sidebar-toggle");
  const mainContent = document.querySelector(".main-content");

  if (!sidebar || !sidebarToggle) {
    return;
  }

  const toggleSidebar = () => {
    const isMobile = window.innerWidth <= 920;
    if (isMobile) {
      sidebar.classList.toggle("open");
      sidebarOverlay?.classList.toggle("active");
      sidebarToggle.classList.toggle("active");
      document.body.style.overflow = sidebar.classList.contains("open") ? "hidden" : "";
    } else {
      sidebar.classList.toggle("collapsed");
      sidebarToggle.classList.toggle("active");
      mainContent?.classList.toggle("sidebar-collapsed");
    }
  };

  const closeSidebar = () => {
    sidebar.classList.remove("open");
    sidebar.classList.remove("collapsed");
    sidebarOverlay?.classList.remove("active");
    sidebarToggle.classList.remove("active");
    mainContent?.classList.remove("sidebar-collapsed");
    document.body.style.overflow = "";
  };

  sidebarToggle.addEventListener("click", toggleSidebar);
  sidebarOverlay?.addEventListener("click", closeSidebar);

  sidebar.querySelectorAll(".nav-item").forEach((link) => {
    link.addEventListener("click", () => {
      if (window.innerWidth <= 920) {
        closeSidebar();
      }
    });
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 920) {
      sidebar.classList.remove("open");
      sidebarOverlay?.classList.remove("active");
      document.body.style.overflow = "";
    }
  });
}

initializeSidebarToggle();

// Smooth scroll behavior
document.documentElement.style.scrollBehavior = 'smooth';

// Breadcrumbs should be removed at runtime across all pages.
document.addEventListener('DOMContentLoaded', function() {
  // Remove any existing breadcrumb elements on load
  try {
    var crumbs = document.querySelectorAll('nav.breadcrumb, [aria-label="Breadcrumb"]');
    crumbs.forEach(function(el) {
      if (el && el.parentNode) el.parentNode.removeChild(el);
    });
  } catch (e) {
    // ignore if elements not present
  }

  // Also remove breadcrumbs injected later by scripts (MutationObserver)
  try {
    var observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mut) {
        mut.addedNodes.forEach(function(node) {
          if (!node || node.nodeType !== 1) return;
          if (node.matches && (node.classList.contains('breadcrumb') || node.hasAttribute('aria-label') && node.getAttribute('aria-label') === 'Breadcrumb')) {
            if (node.parentNode) node.parentNode.removeChild(node);
          }
          if (node.querySelectorAll) {
            var nested = node.querySelectorAll('nav.breadcrumb, [aria-label="Breadcrumb"]');
            nested.forEach(function(n) { if (n.parentNode) n.parentNode.removeChild(n); });
          }
        });
      });
    });
    observer.observe(document.body, { childList: true, subtree: true });
  } catch (e) {
    // ignore if MutationObserver unsupported
  }
});
