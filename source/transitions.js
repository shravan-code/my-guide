// Page Transitions & Theme Switching Animations

(function() {
  'use strict';

  // ---- Page Transition: Fade In on Load ----
  document.documentElement.style.opacity = '0';
  document.documentElement.style.transition = 'opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1)';

  window.addEventListener('load', function() {
    requestAnimationFrame(function() {
      document.documentElement.style.opacity = '1';
    });
  });

  // ---- Page Transition: Fade Out on Navigation ----
  document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (!link || link.target === '_blank' || link.hash || link.href.startsWith('javascript')) return;

    const sameOrigin = new URL(link.href).origin === window.location.origin;
    if (!sameOrigin) return;

    e.preventDefault();
    document.documentElement.style.opacity = '0';

    setTimeout(function() {
      window.location.href = link.href;
    }, 300);
  });

  // ---- Theme Switching Animation ----
  function animateThemeChange(isDark) {
    const overlay = document.createElement('div');
    overlay.className = 'theme-transition-overlay';
    document.body.appendChild(overlay);

    requestAnimationFrame(function() {
      overlay.style.background = isDark
        ? 'radial-gradient(circle at center, rgba(20,20,20,0.8) 0%, rgba(20,20,20,0) 70%)'
        : 'radial-gradient(circle at center, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%)';
    });

    setTimeout(function() {
      overlay.remove();
    }, 500);
  }

  // Patch the theme toggle in app.js
  const originalToggle = document.getElementById('theme-toggle');
  if (originalToggle) {
    const existingHandler = originalToggle.onclick;
    originalToggle.addEventListener('click', function() {
      const willBeDark = !document.body.classList.contains('dark');
      animateThemeChange(willBeDark);
    }, { capture: true });
  }

  // ---- Smooth Scroll Behavior ----
  document.documentElement.style.scrollBehavior = 'smooth';

  // ---- View Transitions API (Chrome 111+) ----
  if (document.startViewTransition) {
    document.addEventListener('click', function(e) {
      const link = e.target.closest('a');
      if (!link || link.target === '_blank' || link.hash || link.href.startsWith('javascript')) return;
      if (new URL(link.href).origin !== window.location.origin) return;

      e.preventDefault();
      const href = link.href;

      document.startViewTransition(function() {
        window.location.href = href;
      });
    });
  }

})();
