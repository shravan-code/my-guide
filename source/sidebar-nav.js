/**
 * sidebar-nav.js - Shared navigation shell for all non-home pages.
 * Uses hierarchy.js for the global sidebar and breadcrumb structure.
 */
(function () {
  var scriptEl = document.currentScript;
  var scriptSrc = scriptEl ? scriptEl.getAttribute('src') : '';
  var sourcePath = scriptSrc.replace('sidebar-nav.js', '');
  var rootPath = sourcePath + '../';

  function normalizeHref(href) {
    if (!href) return '';

    var normalized = href
      .replace(/\\/g, '/')
      .replace(/[?#].*$/, '')
      .replace(/^\.?\/?source\//, '')
      .replace(/^\//, '');

    if (normalized.slice(-1) === '/') {
      normalized += 'index.html';
    }

    if (normalized.slice(-11) === '/index.html') {
      normalized = normalized.slice(0, -11);
    } else if (normalized === 'index.html') {
      normalized = '';
    }

    return normalized;
  }

  function getCurrentSourcePath() {
    var path = window.location.pathname.replace(/\\/g, '/');
    var marker = '/source/';
    var index = path.indexOf(marker);
    if (index === -1) return '';
    return normalizeHref(path.substring(index + marker.length));
  }

  function titleCase(str) {
    var s = str.replace(/\.html$/, '').replace(/-/g, ' ');
    return s.replace(/\b\w/g, function (letter) {
      return letter.toUpperCase();
    });
  }

  function getCrumbLabel(item) {
    if (!item) return '';
    if (item.section === 'bigdata') return 'Big Data';
    return item.label;
  }

  function buildPageRegistry(items, trail, registry) {
    (items || []).forEach(function (item) {
      var nextTrail = trail.concat([{ label: getCrumbLabel(item), href: item.href || '' }]);
      if (item.href) {
        registry[normalizeHref(item.href)] = nextTrail.slice();
      }
      if (item.children && item.children.length) {
        buildPageRegistry(item.children, nextTrail, registry);
      }
    });
    return registry;
  }

  function findTrailForCurrentPage(relativePath, registry) {
    if (registry[relativePath]) return registry[relativePath];

    var matches = Object.keys(registry).filter(function (key) {
      return key && relativePath.indexOf(key) !== -1;
    }).sort(function (a, b) {
      return b.length - a.length;
    });

    return matches.length ? registry[matches[0]] : null;
  }

  function extractLegacyContentNav(sidebar) {
    var items = [];
    if (sidebar) {
      var currentGroup = '';
      Array.prototype.forEach.call(sidebar.children, function (node) {
        if (node.classList && node.classList.contains('nav-title')) {
          currentGroup = node.textContent.trim();
          return;
        }

        if (node.classList && node.classList.contains('nav-item')) {
          var href = node.getAttribute('href') || '';
          if (!href || href.charAt(0) !== '#') return;

          var clone = node.cloneNode(true);
          Array.prototype.forEach.call(clone.querySelectorAll('span'), function (span) {
            span.remove();
          });

          items.push({
            href: href,
            label: clone.textContent.replace(/\s+/g, ' ').trim(),
            group: currentGroup,
            depth: 0
          });
        }
      });
    }

    if (items.length) return items;

    var headings = document.querySelectorAll('main .page-wrap h2[id], main .page-wrap h3[id]');
    Array.prototype.forEach.call(headings, function (heading) {
      items.push({
        href: '#' + heading.id,
        label: heading.textContent.replace(/\s+/g, ' ').trim(),
        group: '',
        depth: heading.tagName === 'H3' ? 1 : 0
      });
    });

    return items;
  }

  function init() {
    var storageKey = 'data-guide-theme';
    var savedTheme = localStorage.getItem(storageKey);
    if (savedTheme === 'dark') {
      document.body.classList.add('dark');
      document.documentElement.setAttribute('data-theme', 'dark');
    }

    var relativePath = getCurrentSourcePath();
    var isSubPage = relativePath !== '';

    var legacySidebar = document.getElementById('sidebar');
    var contentNavData = extractLegacyContentNav(legacySidebar);

    var sidebar = document.querySelector('.sidebar-nav');
    if (sidebar) {
      var existingContent = sidebar.querySelector('.sidebar-brand, .sidebar-menu');
      if (existingContent) {
        setupSubmenu();
        highlightActiveLink();
        setupMobileMenu();
        setupContentNav(contentNavData);
        return;
      }
      sidebar.remove();
    }

    var topbar = document.querySelector('header.topbar');
    if (topbar) topbar.remove();

    [
      document.getElementById('mobile-menu'),
      document.getElementById('mobile-menu-overlay'),
      document.getElementById('mobile-menu-toggle'),
      document.getElementById('sidebar-toggle'),
      document.getElementById('sidebar-overlay'),
      document.getElementById('sidebar')
    ].forEach(function (node) {
      if (node) node.remove();
    });

    document.body.classList.add('home-with-sidebar');

    document.body.insertAdjacentHTML('afterbegin', buildSidebarHTML());
    injectMobileControls();
    injectBottomBar();
    setupThemeToggle();
    highlightActiveLink();
    setupSubmenu();
    setupMobileMenu();
    implementBreadcrumb();
    setupContentNav(contentNavData);
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
      var href = item.href || '#';
      if (href !== '#' && !href.startsWith('http') && !href.startsWith('/')) {
        href = rootPath + 'source/' + href;
      }

      var itemClass = 'sidebar-item' + (hasChildren ? ' has-submenu' : '');
      var linkClass = isChild ? 'sidebar-link submenu-link' : 'sidebar-link';
      var dataSection = item.section ? ' data-section="' + item.section + '"' : '';
      var iconSVG = item.icon ? '<svg viewBox="0 0 24 24" fill="currentColor" title="' + item.label + '">' + item.icon + '</svg>' : '';
      var labelHTML = isChild
        ? '<span class="submenu-link-text">' + item.label + '</span>'
        : '<span class="sidebar-link-text">' + item.label + '</span>';
      var childrenHTML = '';

      if (hasChildren) {
        childrenHTML = '<ul class="submenu">' + item.children.map(function (child) {
          return '<li>' + buildMenuItem(child, true) + '</li>';
        }).join('') + '</ul>';
      }

      return '<div class="' + itemClass + '">' +
        '<a href="' + href + '" class="' + linkClass + '"' + dataSection + ' aria-label="' + item.label + '" title="' + item.label + '">' +
        iconSVG + labelHTML + (hasChildren ? arrowIcon : '') +
        '</a>' +
        childrenHTML +
        '</div>';
    }

    var linksHTML = sidebarHierarchy.slice(0, -1).map(function (item) {
      return buildMenuItem(item, false);
    }).join('\n');

    // Add portfolio as a regular menu item after Roadmaps (with children)
    var portfolioItem = sidebarHierarchy[sidebarHierarchy.length - 1];
    var portfolioHTML = buildMenuItem(portfolioItem, false);

    return '<aside class="sidebar-nav">' +
      '<a class="sidebar-brand" href="' + rootPath + 'index.html" title="Home">' +
      '<img src="' + rootPath + 'assets/images/logo.png" alt="Data Sheets" class="sidebar-logo" />' +
      '<span class="sidebar-brand-text">Data Sheets</span>' +
      '</a>' +
      '<nav class="sidebar-menu" aria-label="Main navigation">' + linksHTML + '\n' + portfolioHTML + '</nav>' +
      '</aside>';
  }

  function injectMobileControls() {
    var hamburgerBtn = '<button class="sidebar-mobile-toggle" type="button" aria-label="Open navigation">' +
      '<svg viewBox="0 0 24 24"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>' +
      '</button>';
    var overlay = '<div class="sidebar-mobile-overlay"></div>';
    document.body.insertAdjacentHTML('beforeend', hamburgerBtn + overlay);
  }

  function injectBottomBar() {
    var isDark = document.body.classList.contains('dark');
    // Sunrise for light mode, crescent moon for dark mode
    var toggleIconChar = isDark
      ? '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>'
      : '<path d="M17 18a5 5 0 0 0-10 0"/><line x1="12" y1="2" x2="12" y2="9"/><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"/><line x1="1" y1="18" x2="3" y2="18"/><line x1="21" y1="18" x2="23" y2="18"/><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"/><line x1="23" y1="22" x2="1" y2="22"/><polyline points="8 6 12 2 16 6"/>';

    var bar = '<footer class="bottom-bar">' +
      '<span class="bottom-bar-right">' +
      '<a class="bottom-bar-home" href="' + rootPath + 'index.html" title="Home">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>' +
      '</a>' +
      '<a class="bottom-bar-portfolio" href="' + rootPath + 'source/portfolios/portfolio.html" title="Portfolio">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>' +
      '</a>' +
      '<button class="bottom-bar-theme-toggle" type="button" aria-label="Toggle theme" title="Toggle Theme">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + toggleIconChar + '</svg>' +
      '</button>' +
      '</span>' +
      '</footer>';
    document.body.insertAdjacentHTML('beforeend', bar);
  }

  function setupThemeToggle() {
    var storageKey = 'data-guide-theme';
    var sunriseIcon = '<path d="M17 18a5 5 0 0 0-10 0"/><line x1="12" y1="2" x2="12" y2="9"/><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"/><line x1="1" y1="18" x2="3" y2="18"/><line x1="21" y1="18" x2="23" y2="18"/><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"/><line x1="23" y1="22" x2="1" y2="22"/><polyline points="8 6 12 2 16 6"/>';
    var moonIcon = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';

    function toggleTheme() {
      var isDark = document.body.classList.contains('dark');
      var nextTheme = isDark ? 'light' : 'dark';
      var newIcon = isDark ? sunriseIcon : moonIcon;

      document.body.classList.toggle('dark', !isDark);
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem(storageKey, nextTheme);

      // Update bottom bar theme toggle icon
      document.querySelectorAll('.bottom-bar-theme-toggle svg').forEach(function (el) {
        el.innerHTML = newIcon;
      });
    }

    // Attach sidebar theme toggle (if exists)
    var sidebarToggle = document.querySelector('.sidebar-theme-toggle');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', toggleTheme);
    }

    // Attach bottom bar theme toggle (always)
    var bottomBarThemeToggle = document.querySelector('.bottom-bar-theme-toggle');
    if (bottomBarThemeToggle) {
      bottomBarThemeToggle.addEventListener('click', toggleTheme);
    }
  }

  function setupSubmenu() {
    var sidebarMenu = document.querySelector('.sidebar-nav');
    if (!sidebarMenu) return;

    sidebarMenu.addEventListener('mouseenter', function () {
      document.body.classList.add('sidebar-expanded');
    });

    sidebarMenu.addEventListener('mouseleave', function () {
      document.body.classList.remove('sidebar-expanded');
      // Close all open submenus when sidebar collapses
      sidebarMenu.querySelectorAll('.sidebar-item.has-submenu.open').forEach(function (item) {
        item.classList.remove('open');
        syncExpandedState(item);
      });
    });

    function syncExpandedState(item) {
      var trigger = item.querySelector(':scope > .sidebar-link');
      if (!trigger) return;
      trigger.setAttribute('aria-expanded', item.classList.contains('open') ? 'true' : 'false');
    }

    sidebarMenu.querySelectorAll('.sidebar-item.has-submenu').forEach(function (item) {
      syncExpandedState(item);
    });

    sidebarMenu.addEventListener('click', function (e) {
      var link = e.target.closest('.sidebar-item.has-submenu > .sidebar-link');
      if (!link || !sidebarMenu.contains(link)) return;

      var parent = link.parentElement;
      var submenu = parent ? parent.querySelector(':scope > .submenu') : null;
      if (!parent || !submenu) return;

      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();

      var isOpen = parent.classList.contains('open');
      var siblings = parent.parentElement ? parent.parentElement.children : [];
      Array.prototype.forEach.call(siblings, function (sibling) {
        if (sibling !== parent && sibling.classList && sibling.classList.contains('has-submenu')) {
          sibling.classList.remove('open');
          syncExpandedState(sibling);
        }
      });

      parent.classList.toggle('open', !isOpen);
      syncExpandedState(parent);
    });
  }

  function highlightActiveLink() {
    var currentPath = getCurrentSourcePath();
    document.querySelectorAll('.sidebar-nav .sidebar-link').forEach(function (link) {
      var href = link.getAttribute('href') || '';
      if (href.indexOf('/source/') !== -1) {
        href = href.substring(href.indexOf('/source/') + 8);
      }
      href = normalizeHref(href);
      if (href && currentPath === href) {
        link.classList.add('active');
        var parentItem = link.closest('.sidebar-item.has-submenu');
        while (parentItem) {
          parentItem.classList.add('open');
          parentItem = parentItem.parentElement.closest('.sidebar-item.has-submenu');
        }
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
      if (!document.body.classList.contains('content-nav-open')) {
        document.body.style.overflow = '';
      }
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
      link.addEventListener('click', function () {
        if (!link.parentElement.classList.contains('has-submenu')) {
          closeMenu();
        }
      });
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 1024) {
        closeMenu();
      }
    });
  }

  function implementBreadcrumb() {
    var relativePath = getCurrentSourcePath();
    if (!relativePath || typeof sidebarHierarchy === 'undefined') return;

    if (relativePath.indexOf('cheatsheet') !== -1) return;

    var main = document.querySelector('main');
    if (!main) return;

    var existing = main.querySelector('.breadcrumb, .breadcrumb-pill');
    if (existing) existing.remove();

    var registry = buildPageRegistry(sidebarHierarchy, [], {});
    var trail = findTrailForCurrentPage(relativePath, registry);

    if (!trail || !trail.length) {
      trail = [{ label: titleCase(relativePath), href: relativePath }];
    }

    var html = '<nav class="breadcrumb" aria-label="Breadcrumb">';
    html += '<a href="' + rootPath + 'index.html" class="breadcrumb-home">Home</a>';

    trail.forEach(function (crumb, index) {
      var isLast = index === trail.length - 1;
      var href = crumb.href ? rootPath + 'source/' + crumb.href : '';
      html += '<span class="separator">/</span>';
      if (isLast) {
        html += '<span class="current">' + crumb.label + '</span>';
      } else {
        html += '<a href="' + href + '">' + crumb.label + '</a>';
      }
    });

    html += '</nav>';
    main.insertAdjacentHTML('afterbegin', html);
  }

  function setupContentNav(items) {
    if (!document.body.classList.contains('home-with-sidebar')) return;
    if (!items || !items.length) return;

    document.body.classList.add('has-content-nav');

    var linksHTML = items.map(function (item) {
      return '<a class="content-nav-link" data-depth="' + item.depth + '" href="' + item.href + '">' + item.label + '</a>';
    }).join('');

    var html = '<aside class="content-nav" aria-label="On this page">' +
      '<div class="content-nav-header">' +
      '<span class="content-nav-title">On This Page</span>' +
      '<button class="content-nav-collapse" type="button" aria-label="Collapse section navigation">' +
      '<svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>' +
      '</button>' +
      '</div>' +
      '<nav class="content-nav-list">' + linksHTML + '</nav>' +
      '</aside>' +
      '<button class="content-nav-toggle" type="button" aria-label="Open section navigation">' +
      '<svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></svg>' +
      '</button>' +
      '<div class="content-nav-overlay"></div>';

    document.body.insertAdjacentHTML('beforeend', html);

    var collapseBtn = document.querySelector('.content-nav-collapse');
    var toggleBtn = document.querySelector('.content-nav-toggle');
    var overlay = document.querySelector('.content-nav-overlay');
    var links = document.querySelectorAll('.content-nav-link');

    collapseBtn.addEventListener('click', function () {
      document.body.classList.toggle('content-nav-collapsed');
    });

    toggleBtn.addEventListener('click', function () {
      document.body.classList.toggle('content-nav-open');
      document.body.style.overflow = document.body.classList.contains('content-nav-open') ? 'hidden' : '';
    });

    overlay.addEventListener('click', function () {
      document.body.classList.remove('content-nav-open');
      document.body.style.overflow = '';
    });

    links.forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.innerWidth <= 1024) {
          document.body.classList.remove('content-nav-open');
          document.body.style.overflow = '';
        }
      });
    });

    var targets = Array.prototype.map.call(links, function (link) {
      var id = link.getAttribute('href').replace('#', '');
      return document.getElementById(id);
    }).filter(Boolean);

    function setActiveByHash(hash) {
      if (!hash) return;
      links.forEach(function (link) {
        link.classList.toggle('active', link.getAttribute('href') === hash);
      });
    }

    if (targets.length && 'IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        var visible = entries.filter(function (entry) {
          return entry.isIntersecting;
        }).sort(function (a, b) {
          return a.boundingClientRect.top - b.boundingClientRect.top;
        });

        if (visible.length) {
          setActiveByHash('#' + visible[0].target.id);
        }
      }, {
        rootMargin: '-20% 0px -60% 0px',
        threshold: [0, 0.1, 0.25]
      });

      targets.forEach(function (target) {
        observer.observe(target);
      });
    }

    setActiveByHash(window.location.hash || (links[0] ? links[0].getAttribute('href') : ''));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
