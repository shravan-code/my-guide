document.addEventListener('DOMContentLoaded', function() {
  const sidebar = document.getElementById("sidebar");
  const sidebarOverlay = document.getElementById("sidebar-overlay");

  const closeSidebar = () => {
    if (sidebar) sidebar.classList.remove("open");
    if (sidebarOverlay) sidebarOverlay.classList.remove("active");
  };

  const navItems = Array.from(document.querySelectorAll(".nav-item"));

  const setActiveNav = (id) => {
    navItems.forEach((item) => {
      const isActive = item.getAttribute("href") === "#" + id;
      item.classList.toggle("active", isActive);
      if (isActive) {
        item.setAttribute("aria-current", "location");
        item.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "nearest" });
      } else {
        item.removeAttribute("aria-current");
      }
    });
  };

  navItems.forEach((item) => {
    item.addEventListener("click", function (e) {
      const href = this.getAttribute("href");
      if (!href || !href.startsWith("#")) return;
      e.preventDefault();
      const targetId = href.substring(1);
      const target = document.getElementById(targetId);
      if (!target) return;
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      history.replaceState(null, "", "#" + targetId);
      setActiveNav(targetId);
      closeSidebar();
    });
  });

  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && entry.intersectionRatio > 0) {
        const id = entry.target.getAttribute("id");
        if (id) setActiveNav(id);
      }
    });
  }, { root: null, rootMargin: "-15% 0px -60% 0px", threshold: 0 });

  document.querySelectorAll(".topic[id], .concept[id]").forEach((el) => sectionObserver.observe(el));

  const initialId = (window.location.hash || "").substring(1);
  if (initialId) {
    setActiveNav(initialId);
  } else {
    const firstSection = document.querySelector(".topic[id], .concept[id]");
    if (firstSection) {
      const id = firstSection.getAttribute("id");
      if (id) setActiveNav(id);
    }
  }

  let scrollTimeout;
  const handleScroll = () => {
    if (scrollTimeout) return;
    scrollTimeout = setTimeout(() => {
      const sections = document.querySelectorAll(".topic[id], .concept[id]");
      const scrollY = window.scrollY + 150;
      let currentSection = null;
      sections.forEach((section) => {
        if (section.offsetTop <= scrollY) {
          currentSection = section;
        }
      });
      if (currentSection) {
        const id = currentSection.getAttribute("id");
        if (id) setActiveNav(id);
      }
      scrollTimeout = null;
    }, 50);
  };

  window.addEventListener("scroll", handleScroll, { passive: true });

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in");
      }
    });
  }, { root: null, rootMargin: "0px 0px -50px 0px", threshold: 0.1 });

  document.querySelectorAll(".topic, .concept, .hero").forEach((el) => {
    revealObserver.observe(el);
  });
});
