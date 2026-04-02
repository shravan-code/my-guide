/**
 * sidebar-nav.js - Injects the icon sidebar into all subpages
 * Uses hierarchy.js for menu structure
 */
(function () {
  var scriptEl = document.currentScript;
  var scriptSrc = scriptEl ? scriptEl.getAttribute('src') : '';
  var sourcePath = scriptSrc.replace('sidebar-nav.js', '');
  var rootPath = sourcePath + '../';

  function init() {
    // Load saved theme
    var storageKey = 'data-guide-theme';
    var savedTheme = localStorage.getItem(storageKey);
    if (savedTheme === 'dark') {
      document.body.classList.add('dark');
      document.documentElement.setAttribute('data-theme', 'dark');
    }

    // Check if sidebar already has content (e.g., homepage with hardcoded sidebar)
    var sidebar = document.querySelector('.sidebar-nav');
    if (sidebar) {
      var existingContent = sidebar.querySelector('.sidebar-brand, .sidebar-menu');
      if (existingContent) return;
      // If sidebar exists but is empty (like index.html placeholder), remove it first
      sidebar.remove();
    }

    var topbar = document.querySelector('header.topbar');
    if (topbar) topbar.remove();

    var oldMobileMenu = document.getElementById('mobile-menu');
    var oldMobileOverlay = document.getElementById('mobile-menu-overlay');
    var oldMobileToggle = document.getElementById('mobile-menu-toggle');
    if (oldMobileMenu) oldMobileMenu.remove();
    if (oldMobileOverlay) oldMobileOverlay.remove();
    if (oldMobileToggle) oldMobileToggle.remove();

    document.body.classList.add('home-with-sidebar');

    var sidebarHTML = buildSidebarHTML();
    document.body.insertAdjacentHTML('afterbegin', sidebarHTML);

    injectMobileControls();
    setupThemeToggle();
    setupSidebarHover();
    highlightActiveLink();
    setupSubmenu();
    setupMobileMenu();
    implementBreadcrumb();
  }

  function buildSidebarHTML() {
    if (typeof sidebarHierarchy === 'undefined') {
      console.error('Hierarchy data not loaded');
      return '';
    }

    var isDark = document.body.classList.contains('dark');
    var toggleIconChar = isDark 
      ? '<path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41.39.39 1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41.39.39 1.03.39 1.41 0l1.06-1.06z"/>'
      : '<path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z" />';
    var toggleLabelTxt = isDark ? 'Light' : 'Dark';

    var arrowIcon = '<svg class="submenu-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>';

    function buildMenuItem(item, isChild) {
      var hasChildren = item.children && item.children.length > 0;
      var childrenHTML = '';
      
      if (hasChildren) {
        childrenHTML = '<ul class="submenu">' +
          item.children.map(function(child) {
            return '<li>' + buildMenuItem(child, true) + '</li>';
          }).join('') +
          '</ul>';
      }

      var itemClass = 'sidebar-item' + (hasChildren ? ' has-submenu' : '');
      var linkClass = 'sidebar-link' + (item.section ? ' data-section="' + item.section + '"' : '');
      
      var href = item.href || '#';
      // Add rootPath prefix for relative links (not http, not #, not already absolute)
      if (href !== '#' && !href.startsWith('http') && !href.startsWith('/')) {
        href = rootPath + 'source/' + href;
      }
      var label = item.label;
      var icon = item.icon || '';
      
      var arrow = hasChildren ? arrowIcon : '';
      var displayLabel = isChild ? '<span class="submenu-link-text">' + label + '</span>' : '<span class="sidebar-link-text">' + label + '</span>';
      
      var iconSVG = '';
      if (icon) {
        iconSVG = '<svg viewBox="0 0 24 24" fill="currentColor" title="' + label + '">' + icon + '</svg>';
      }

      return '<div class="' + itemClass + '">' +
        '<a href="' + href + '" class="' + linkClass + '" aria-label="' + label + '" title="' + label + '">' +
        iconSVG +
        displayLabel +
        arrow +
        '</a>' +
        childrenHTML +
        '</div>';
    }

    var linksHTML = sidebarHierarchy.slice(0, -1).map(function(item) {
      return buildMenuItem(item, false);
    }).join('\n      ');
    
    var portfolioItem = sidebarHierarchy[sidebarHierarchy.length - 1];
    var portfolioHTML = buildMenuItem(portfolioItem, false);

    return '<aside class="sidebar-nav">' +
      '<a class="sidebar-brand" href="' + rootPath + 'index.html" title="Home">' +
      '<img src="' + rootPath + 'assets/images/logo.png" alt="Data Sheets" class="sidebar-logo" />' +
      '<span class="sidebar-brand-text">Data Sheets</span>' +
      '</a>' +
      '<nav class="sidebar-menu" aria-label="Main navigation">' +
      linksHTML +
      '</nav>' +
      '<div class="sidebar-bottom">' +
      portfolioHTML +
      '<button class="sidebar-theme-toggle" type="button" aria-label="Toggle light and dark mode" title="Toggle Theme">' +
      '<span class="toggle-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" title="Toggle Theme">' + toggleIconChar + '</svg></span>' +
      '<span class="toggle-label">' + toggleLabelTxt + '</span>' +
      '</button>' +
      '</div>' +
      '</aside>';
  }

  function injectMobileControls() {
    var hamburgerBtn = '<button class="sidebar-mobile-toggle" type="button" aria-label="Open navigation">' +
      '<svg viewBox="0 0 24 24"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>' +
      '</button>';

    var isDark = document.body.classList.contains('dark');
    var mobileThemeBtn = '<button class="sidebar-mobile-theme-toggle" type="button" aria-label="Toggle theme">' +
      '<span class="toggle-icon" aria-hidden="true">' + (isDark ? '☀' : '☾') + '</span>' +
      '</button>';

    var overlay = '<div class="sidebar-mobile-overlay"></div>';

    document.body.insertAdjacentHTML('beforeend', hamburgerBtn + mobileThemeBtn + overlay);
  }

  function setupThemeToggle() {
    var storageKey = 'data-guide-theme';

    var sidebarToggle = document.querySelector('.sidebar-theme-toggle');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', function () {
        toggleTheme();
      });
    }

    var mobileToggle = document.querySelector('.sidebar-mobile-theme-toggle');
    if (mobileToggle) {
      mobileToggle.addEventListener('click', function () {
        toggleTheme();
      });
    }

    function toggleTheme() {
      var isDark = document.body.classList.contains('dark');
      var nextTheme = isDark ? 'light' : 'dark';

      document.body.classList.toggle('dark', !isDark);
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem(storageKey, nextTheme);

      var newIconLight = '<path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41.39.39 1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41.39.39 1.03.39 1.41 0l1.06-1.06z"/>';
      var newIconDark = '<path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z" />';
      var newIconHTML = isDark ? newIconDark : newIconLight;
      var newTxtStr = isDark ? 'Dark' : 'Light';

      document.querySelectorAll('.sidebar-theme-toggle .toggle-icon svg, .sidebar-mobile-theme-toggle .toggle-icon').forEach(function (el) {
        el.innerHTML = newIconHTML;
      });

      document.querySelectorAll('.sidebar-theme-toggle .toggle-text').forEach(function (el) {
        el.textContent = newTxtStr;
      });

      var appToggleIcon = document.querySelector('#theme-toggle .toggle-icon');
      if (appToggleIcon) appToggleIcon.innerHTML = newIconHTML;
      var appToggleText = document.querySelector('#theme-toggle .toggle-text');
      if (appToggleText) appToggleText.textContent = newTxtStr;
    }
  }

  function setupSidebarHover() {
    var sidebarNav = document.querySelector('.sidebar-nav');
    if (!sidebarNav) return;

    sidebarNav.addEventListener('mouseenter', function () {
      document.body.classList.add('sidebar-expanded');
    });
    sidebarNav.addEventListener('mouseleave', function () {
      document.body.classList.remove('sidebar-expanded');
      sidebarNav.querySelectorAll('.sidebar-item.has-submenu.open').forEach(function(item) {
        item.classList.remove('open');
      });
    });
  }

  function setupSubmenu() {
    document.querySelectorAll('.sidebar-item.has-submenu > .sidebar-link').forEach(function (link) {
      link.addEventListener('click', function (e) {
        var parent = this.parentElement;
        
        if (parent.querySelector('.submenu')) {
          e.preventDefault();
          e.stopPropagation();
          
          var isOpen = parent.classList.contains('open');
          var parentUl = parent.parentElement;
          
          if (parentUl && parentUl.classList.contains('submenu')) {
            Array.from(parentUl.children).forEach(function(sibling) {
              if (sibling !== parent && sibling.classList.contains('has-submenu') && sibling.classList.contains('open')) {
                sibling.classList.remove('open');
              }
            });
          } else {
            var siblings = parent.parentElement.children;
            Array.from(siblings).forEach(function(sibling) {
              if (sibling !== parent && sibling.classList.contains('has-submenu') && sibling.classList.contains('open')) {
                sibling.classList.remove('open');
              }
            });
          }
          
          parent.classList.toggle('open', !isOpen);
        }
        // If no submenu, allow default navigation (do nothing - let link work)
      });
    });

    // Handle active page highlighting and auto-open parent menus
    var currentPath = window.location.pathname.replace(/\\/g, '/');
    document.querySelectorAll('.submenu-link').forEach(function (link) {
      var href = link.getAttribute('href');
      if (href && href !== '#' && currentPath.indexOf(href) !== -1) {
        link.classList.add('active');
        var parentItem = link.closest('.sidebar-item.has-submenu');
        while (parentItem) {
          parentItem.classList.add('open');
          var parentUl = parentItem.parentElement;
          if (parentUl && parentUl.classList.contains('submenu')) {
            parentItem = parentUl.parentElement.closest('.sidebar-item.has-submenu');
          } else {
            break;
          }
        }
      }
    });
  }

  function highlightActiveLink() {
    var path = window.location.pathname.replace(/\\/g, '/');
    var links = document.querySelectorAll('.sidebar-nav .sidebar-link');

    links.forEach(function (link) {
      var section = link.getAttribute('data-section');
      if (section && path.indexOf('/' + section + '/') !== -1) {
        link.classList.add('active');
      }
    });
  }

  function setupMobileMenu() {
    var sidebar = document.querySelector('.sidebar-nav');
    var toggleBtn = document.querySelector('.sidebar-mobile-toggle');
    var overlay = document.querySelector('.sidebar-mobile-overlay');

    if (!sidebar || !toggleBtn || !overlay) return;

    function openMenu() {
      sidebar.classList.add('open');
      overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
      sidebar.classList.remove('open');
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }

    toggleBtn.addEventListener('click', function () {
      if (sidebar.classList.contains('open')) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    overlay.addEventListener('click', closeMenu);

    sidebar.querySelectorAll('.sidebar-link').forEach(function (link) {
      link.addEventListener('click', function(e) {
        // If this link has a submenu, let submenu toggle handle it
        var parentItem = link.closest('.sidebar-item.has-submenu');
        if (parentItem && link.querySelector('.submenu-arrow')) {
          // This is a parent link with submenu; don't close menu
          return;
        }
        closeMenu();
      });
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 920) {
        closeMenu();
      }
    });
  }

  function implementBreadcrumb() {
    var main = document.querySelector('main');
    if (!main) return;

    var existing = main.querySelector('.breadcrumb, .breadcrumb-pill');
    if (existing) {
       existing.className = 'breadcrumb';
       return; 
    }

    var siteMap = {
      'cloud': ['cloud-architecture.html', 'cloud-aws.html', 'cloud-azure.html', 'cloud-gcp.html', 'cloud-basics.html', 'cloud-compute.html', 'cloud-serverless.html', 'cloud-services.html', 'cloud-storage.html'],
      'data': ['data-formats.html', 'data-pipeline.html', 'data-quality.html', 'data-types.html'],
      'numpy': ['numpy-basics.html', 'numpy-arrays.html', 'numpy-operations.html', 'methods.html'],
      'pandas': ['pandas-series.html', 'pandas-dataframes.html', 'methods.html'],
      'python': ['python-oops.html', 'python-methods.html', 'memory-performance.html', 'python-fundamentals.html'],
      'roadmaps': ['roadmap.html', 'ai-engineer-roadmap.html', 'data-engineer-roadmap.html', 'ml-engineer-roadmap.html', 'python-roadmap.html', 'spark-roadmap.html', 'sql-roadmap.html'],
      'spark': ['spark-theory.html', 'spark-architecture.html', 'spark-code.html'],
      'sql': ['sql-modelling.html', 'sql-concepts.html', 'sql-queries.html', 'sql-methods.html', 'sql-joins.html', 'sql-subqueries.html', 'sql-windows.html'],
      'tools': ['airflow.html', 'dbt.html', 'kafka.html'],
      'portfolios': ['portfolio.html', 'projects-self.html', 'projects-experienced.html'],
      'cheatsheets': ['cheatsheet.html', 'compare.html', 'numpy-cheatsheet.html', 'pandas-cheatsheet.html', 'postgresql-cheatsheet.html', 'python-cheatsheet.html', 'spark-cheatsheet.html']
    };

    function titleCase(str) {
       var s = str.replace(/\.html$/, '').replace(/-/g, ' ');
       return s.replace(/\b\w/g, function(l) { return l.toUpperCase() });
    }

    var pathStr = window.location.pathname.replace(/\\/g, '/');
    var isSubPage = pathStr.indexOf('/source/') !== -1;
    if (!isSubPage) return; 

    var relativeSegmentsStr = pathStr.substring(pathStr.indexOf('/source/') + 8);
    var segments = relativeSegmentsStr.split('/');
    
    var html = '<nav class="breadcrumb" aria-label="Breadcrumb">';
    html += '<a href="' + rootPath + 'index.html" class="breadcrumb-home">Home</a>';

    var currentPath = rootPath + 'source/';
    for (var i = 0; i < segments.length; i++) {
        var seg = segments[i];
        if (seg.endsWith('.html') || seg === '') {
            if (seg !== 'index.html' && seg !== '') {
               var name = titleCase(seg);
               html += '<span class="separator">/</span><span class="current">' + name + '</span>';
            }
        } else {
            currentPath += seg + '/';
            var niceName = titleCase(seg);
            if (seg.toLowerCase() === 'data') niceName = 'Big Data';
            
            html += '<span class="separator">/</span>';
            if (siteMap[seg] && siteMap[seg].length > 1) {
               html += '<div class="bc-dropdown">';
               html += '<a href="' + currentPath + (siteMap[seg].indexOf('index.html') > -1 ? 'index.html' : siteMap[seg][0]) + '">' + niceName + '</a>';
               html += '<svg class="bc-dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 15 12 9 18 15"></polyline><polyline points="6 9 12 15 18 9"></polyline></svg>';
               html += '<div class="bc-dropdown-menu">';
               for (var j = 0; j < siteMap[seg].length; j++) {
                  var fp = siteMap[seg][j];
                  if (fp === 'index.html' || fp === seg + '.html') continue;
                  var pageTitle = titleCase(fp);
                  html += '<a href="' + currentPath + fp + '">' + pageTitle + '</a>';
               }
               html += '</div></div>';
            } else {
               html += '<a href="' + currentPath + 'index.html">' + niceName + '</a>';
            }
        }
    }
    html += '</nav>';
    main.insertAdjacentHTML('afterbegin', html);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();