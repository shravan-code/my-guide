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

  const topbar = document.querySelector(".topbar");
  let headerActions = topbar?.querySelector(".header-actions");

  if (!headerActions && topbar) {
    headerActions = document.createElement("div");
    headerActions.className = "header-actions";

    const themeBtn = topbar.querySelector("#theme-toggle");
    const portfolioBtn = topbar.querySelector(".portfolio-link");

    if (themeBtn) {
      headerActions.appendChild(themeBtn);
    }
    if (portfolioBtn) {
      headerActions.appendChild(portfolioBtn);
    }

    topbar.appendChild(headerActions);
  }

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
      if (!group.label) {
        return group.items.join("");
      }

      return `
        <div class="mobile-dropdown">
          <button class="mobile-dropdown-trigger" type="button" aria-expanded="false">${group.label}</button>
          <div class="mobile-dropdown-content">${group.items.join("")}</div>
        </div>
      `;
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

function initializeMobileDropdowns() {
  const mobileDropdowns = document.querySelectorAll(".mobile-dropdown");

  mobileDropdowns.forEach((dropdown) => {
    const trigger = dropdown.querySelector(".mobile-dropdown-trigger");
    const content = dropdown.querySelector(".mobile-dropdown-content");
    if (!trigger || !content) return;

    trigger.setAttribute("aria-expanded", "false");

    const close = () => {
      dropdown.classList.remove("open");
      trigger.setAttribute("aria-expanded", "false");
      content.style.maxHeight = "0";
    };

    const open = () => {
      dropdown.classList.add("open");
      trigger.setAttribute("aria-expanded", "true");
      content.style.maxHeight = `${content.scrollHeight}px`;
    };

    trigger.addEventListener("click", (event) => {
      event.stopPropagation();
      if (dropdown.classList.contains("open")) {
        close();
      } else {
        mobileDropdowns.forEach((other) => {
          if (other !== dropdown) {
            other.classList.remove("open");
            const otherTrigger = other.querySelector(".mobile-dropdown-trigger");
            const otherContent = other.querySelector(".mobile-dropdown-content");
            if (otherTrigger) otherTrigger.setAttribute("aria-expanded", "false");
            if (otherContent) otherContent.style.maxHeight = "0";
          }
        });
        open();
      }
    });

    document.addEventListener("click", (event) => {
      if (!dropdown.contains(event.target)) {
        close();
      }
    });

    content.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", close);
    });
  });
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
  // Don't add click handlers to links - let them navigate naturally

  window.addEventListener("resize", () => {
    if (window.innerWidth > 920) {
      closeMobileMenu();
    }
  });
}

function initializeMobileMenu() {
  // Skip if new hamburger exists (index.html handles it)
  if (document.getElementById("hamburger-btn")) {
    return;
  }
  
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
      initializeMobileDropdowns();
    }
    return;
  }

  attachMobileHandlers(mobileMenuToggle, mobileMenu, mobileMenuOverlay);
  initializeMobileDropdowns();
}

initializeMobileMenu();

// Sidebar toggle for mobile
function initializeSidebarToggle() {
  const sidebar = document.getElementById("sidebar");
  const sidebarOverlay = document.getElementById("sidebar-overlay");
  const sidebarToggle = document.getElementById("sidebar-toggle");

  if (!sidebar || !sidebarToggle) {
    return;
  }

  const mainContent = document.querySelector(".main-content");

  const setCollapsedState = (collapsed) => {
    if (!mainContent) return;
    mainContent.classList.toggle("sidebar-collapsed", collapsed);
  };

  const closeSidebar = () => {
    sidebar?.classList.remove("open");
    sidebar?.classList.remove("collapsed");
    sidebarOverlay?.classList.remove("active");
    sidebarToggle?.classList.remove("active");
    setCollapsedState(false);
    document.body.style.overflow = "";
  };

  const openSidebar = () => {
    sidebar?.classList.add("open");
    sidebar?.classList.remove("collapsed");
    sidebarOverlay?.classList.add("active");
    sidebarToggle?.classList.add("active");
    setCollapsedState(false);
    document.body.style.overflow = "hidden";
  };

  const toggleSidebar = () => {
    const isDesktop = window.innerWidth > 920;

    if (isDesktop) {
      // On desktop, toggle collapsed class
      const collapsed = !sidebar?.classList.contains("collapsed");
      if (collapsed) {
        sidebar?.classList.add("collapsed");
        sidebarToggle?.classList.add("active");
      } else {
        sidebar?.classList.remove("collapsed");
        sidebarToggle?.classList.remove("active");
      }
      setCollapsedState(collapsed);
    } else {
      // On mobile, use open/close
      if (sidebar?.classList.contains("open")) {
        closeSidebar();
      } else {
        openSidebar();
      }
    }
  };

  sidebarToggle?.addEventListener("click", toggleSidebar);

  sidebarOverlay?.addEventListener("click", closeSidebar);

  sidebar?.querySelectorAll(".nav-item").forEach((link) => {
    link.addEventListener("click", closeSidebar);
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 920) {
      closeSidebar();
    }
  });
}

initializeSidebarToggle();
