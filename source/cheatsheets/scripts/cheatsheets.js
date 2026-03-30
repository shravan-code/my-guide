(() => {
  const body = document.body;
  const themeToggle = document.getElementById("theme-toggle");
  const toggleIcon = themeToggle?.querySelector(".toggle-icon");
  const mobileToggle = document.getElementById("mobile-menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  const mobileOverlay = document.getElementById("mobile-menu-overlay");
  const scrollToTop = document.getElementById("scrollToTop");
  const pillLinks = Array.from(document.querySelectorAll('.pill-nav a[href^="#"]'));

  const storageKey = "data-guide-theme";

  const setTheme = (isDark) => {
    body.classList.toggle("dark", isDark);
    document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
    if (toggleIcon) {
      toggleIcon.textContent = isDark ? "☀" : "☾";
    }
    localStorage.setItem(storageKey, isDark ? "dark" : "light");
  };

  const savedTheme = localStorage.getItem(storageKey);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  setTheme(savedTheme === "dark" || (savedTheme === null && prefersDark));

  themeToggle?.addEventListener("click", () => {
    setTheme(!body.classList.contains("dark"));
  });

  const closeMobileMenu = () => {
    mobileMenu?.classList.remove("open");
    mobileOverlay?.classList.remove("active");
    mobileToggle?.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  };

  mobileToggle?.setAttribute("aria-expanded", "false");
  mobileToggle?.addEventListener("click", () => {
    const isOpen = mobileMenu?.classList.contains("open");
    if (isOpen) {
      closeMobileMenu();
      return;
    }

    mobileMenu?.classList.add("open");
    mobileOverlay?.classList.add("active");
    mobileToggle?.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  });

  mobileOverlay?.addEventListener("click", closeMobileMenu);
  document.querySelectorAll(".mobile-nav a").forEach((link) => {
    link.addEventListener("click", closeMobileMenu);
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 920) {
      closeMobileMenu();
    }
  });

  // Sidebar toggle for mobile
  const sidebar = document.getElementById("sidebar");
  const sidebarOverlay = document.getElementById("sidebar-overlay");
  const sidebarToggle = document.getElementById("sidebar-toggle");

  if (sidebar && sidebarToggle) {
    const closeSidebar = () => {
      sidebar?.classList.remove("open");
      sidebarOverlay?.classList.remove("active");
      sidebarToggle?.classList.remove("active");
      document.body.style.overflow = "";
    };

    const openSidebar = () => {
      sidebar?.classList.add("open");
      sidebarOverlay?.classList.add("active");
      sidebarToggle?.classList.add("active");
      document.body.style.overflow = "hidden";
    };

    sidebarToggle?.addEventListener("click", () => {
      if (sidebar?.classList.contains("open")) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });

    sidebarOverlay?.addEventListener("click", closeSidebar);

    document.querySelectorAll(".sidebar .nav-item").forEach((link) => {
      link.addEventListener("click", closeSidebar);
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 920) {
        closeSidebar();
      }
    });
  }

  if (scrollToTop) {
    const toggleScrollButton = () => {
      scrollToTop.classList.toggle("visible", window.scrollY > 300);
    };

    window.addEventListener("scroll", toggleScrollButton, { passive: true });
    toggleScrollButton();
    scrollToTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  const revealItems = document.querySelectorAll(".reveal");
  if (revealItems.length && "IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });

    revealItems.forEach((item) => revealObserver.observe(item));
  }

  if (pillLinks.length && "IntersectionObserver" in window) {
    const sections = pillLinks
      .map((link) => {
        const section = document.querySelector(link.getAttribute("href"));
        return section ? { link, section } : null;
      })
      .filter(Boolean);

    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const match = sections.find((item) => item.section === entry.target);
        if (!match || !entry.isIntersecting) {
          return;
        }

        pillLinks.forEach((link) => link.classList.remove("active"));
        match.link.classList.add("active");
      });
    }, {
      rootMargin: "-35% 0px -55% 0px",
      threshold: 0.01
    });

    sections.forEach(({ section }) => sectionObserver.observe(section));
  }
})();
