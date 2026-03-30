(() => {
  const pillLinks = Array.from(document.querySelectorAll('.pill-nav a[href^="#"]'));

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
