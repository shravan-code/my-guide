// AWS Section Navigation and Highlighting
document.addEventListener('DOMContentLoaded', () => {
  initSectionNav();
  initScrollSpy();
  highlightFromHash();
});

function initSectionNav() {
  const navBtns = document.querySelectorAll('.section-nav-btn');
  const sections = document.querySelectorAll('.service-card, .section-sub-heading');
  
  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.target;
      
      // Update active button
      navBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      // Show/hide sections
      sections.forEach(section => {
        if (section.classList.contains('section-sub-heading')) {
          section.style.display = section.id === target ? 'block' : 'none';
        } else {
          const parentHeading = section.previousElementSibling;
          if (parentHeading && parentHeading.id === target) {
            section.style.display = 'block';
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
          } else {
            section.style.display = 'none';
          }
        }
      });
    });
  });
}

function initScrollSpy() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        // Remove highlight from all cards
        document.querySelectorAll('.service-card').forEach(card => {
          card.classList.remove('highlight');
        });
        // Highlight the visible card
        entry.target.classList.add('highlight');
      }
    });
  }, { threshold: 0.5 });
  
  document.querySelectorAll('.service-card').forEach(card => {
    observer.observe(card);
  });
}

function highlightFromHash() {
  const hash = window.location.hash;
  if (hash) {
    const target = document.querySelector(hash);
    if (target) {
      setTimeout(() => {
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        target.classList.add('highlight');
      }, 100);
    }
  }
}

// Smooth scroll for sidebar links
document.querySelectorAll('.sidebar a[href^="#"], .nav-item[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const hash = link.getAttribute('href');
    if (hash.startsWith('#')) {
      e.preventDefault();
      const target = document.querySelector(hash);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Update URL without scrolling
        history.pushState(null, '', hash);
      }
    }
  });
});
