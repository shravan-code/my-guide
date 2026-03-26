(() => {
  const body = document.body;
  const themeToggle = document.getElementById("theme-toggle");
  const toggleIcon = themeToggle?.querySelector(".toggle-icon");
  const mobileToggle = document.getElementById("mobile-menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  const mobileOverlay = document.getElementById("mobile-menu-overlay");
  const scrollToTop = document.getElementById("scrollToTop");
  const pillLinks = Array.from(document.querySelectorAll('.pill-nav a[href^="#"]'));

  const setTheme = (isDark) => {
    body.classList.toggle("dark", isDark);
    if (toggleIcon) {
      toggleIcon.textContent = isDark ? "\u2600\ufe0f" : "\u263e\ufe0f";
    }
    localStorage.setItem("theme", isDark ? "dark" : "light");
  };

  const savedTheme = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  setTheme(savedTheme === "dark" || (savedTheme === null && prefersDark));

  themeToggle?.addEventListener("click", () => {
    setTheme(!body.classList.contains("dark"));
  });

  const closeMobileMenu = () => {
    mobileMenu?.classList.remove("open");
    mobileOverlay?.classList.remove("active");
    mobileToggle?.setAttribute("aria-expanded", "false");
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
  });

  mobileOverlay?.addEventListener("click", closeMobileMenu);
  document.querySelectorAll(".mobile-nav a").forEach((link) => {
    link.addEventListener("click", closeMobileMenu);
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 640) {
      closeMobileMenu();
    }
  });

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
