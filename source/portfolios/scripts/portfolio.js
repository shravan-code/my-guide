/* ========================================
   Portfolio Page JavaScript
   ======================================== */

// NEW Hamburger Menu JavaScript
(function() {
  const hamburger = document.getElementById('hamburger-btn');
  const mobileMenu = document.getElementById('new-mobile-menu');
  
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function(e) {
      e.preventDefault();
      hamburger.classList.toggle('active');
      mobileMenu.classList.toggle('show');
    });
  }
})();

// NEW Theme Toggle with animation
(function() {
  const toggleButton = document.getElementById('theme-toggle');
  const body = document.body;
  
  if (toggleButton) {
    toggleButton.addEventListener('click', function() {
      // Add animation class to button
      toggleButton.classList.add('animating');
      setTimeout(() => toggleButton.classList.remove('animating'), 500);
      
      // Add flash overlay effect - full page animation
      const overlay = document.getElementById('theme-overlay');
      const isDark = body.classList.contains('dark');
      const nextTheme = isDark ? 'light' : 'dark';
      
      if (overlay) {
        overlay.classList.remove('flash-light', 'flash-dark');
        // Trigger reflow
        void overlay.offsetWidth;
        overlay.classList.add(nextTheme === 'dark' ? 'flash-dark' : 'flash-light');
        setTimeout(() => overlay.classList.remove('flash-light', 'flash-dark'), 600);
      }
      
      // Animate orbs on theme change
      document.querySelectorAll('.bg-orb').forEach((orb, i) => {
        orb.style.transform = 'scale(1.5)';
        orb.style.opacity = '0';
        setTimeout(() => {
          orb.style.transform = '';
          orb.style.opacity = '';
        }, 400);
      });
    });
  }
})();

// Scroll to top functionality
(function() {
  const scrollToTopBtn = document.getElementById('scrollToTop');
  
  if (scrollToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.pageYOffset > 300) {
        scrollToTopBtn.classList.add('visible');
      } else {
        scrollToTopBtn.classList.remove('visible');
      }
    });

    scrollToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
})();
