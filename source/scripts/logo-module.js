/**
 * Logo Module
 * Reusable logo component for all pages
 * 
 * Usage:
 * 1. Include CSS: <link rel="stylesheet" href="../styles/logo-module.css" />
 * 2. Add container: <div class="brand-container" data-logo></div>
 * 3. Include script: <script src="../scripts/logo-module.js"></script>
 * 
 * To update logo text, change the CONFIG object below.
 * Changes will reflect across ALL pages automatically.
 */

const LogoModule = (function() {
  'use strict';

  /**
   * Logo Configuration
   * Update these values to change the logo across all pages
   */
  const CONFIG = {
    default: "*d@ta#",
    hover: "Data.id.name",
    homePath: "/index.html"
  };

  /**
   * Generate the logo HTML
   */
  function getHTML() {
    return `
      <a class="brand" href="${getHomePath()}">
        <span class="brand-default">${CONFIG.default}</span>
        <span class="brand-hover">${CONFIG.hover}</span>
      </a>
    `;
  }

  /**
   * Calculate the relative path to the home page
   * Works from any nested directory level
   */
  function getHomePath() {
    if (CONFIG.homePath.startsWith('/') || CONFIG.homePath.startsWith('http')) {
      return CONFIG.homePath;
    }

    const path = window.location.pathname;
    const depth = (path.match(/\//g) || []).length - 1;
    const prefix = path.startsWith('/') ? '' : './';
    const relative = '../..'.repeat(Math.max(0, depth - 2));
    return prefix + relative + (relative ? '/' : '') + 'index.html';
  }

  /**
   * Initialize the logo in the specified container
   * @param {string} containerSelector - CSS selector for the container element
   */
  function init(containerSelector) {
    const selector = containerSelector || '.brand-container';
    const containers = document.querySelectorAll(selector);
    
    containers.forEach(function(container) {
      container.innerHTML = getHTML();
    });
  }

  /**
   * Auto-initialize when DOM is ready
   * Looks for [data-logo] attribute or .brand-container class
   */
  function autoInit() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        init('[data-logo]');
      });
    } else {
      init('[data-logo]');
    }
  }

  /**
   * Update logo text dynamically
   * @param {string} defaultText - The default logo text
   * @param {string} hoverText - The hover logo text
   */
  function update(defaultText, hoverText) {
    if (defaultText !== undefined) CONFIG.default = defaultText;
    if (hoverText !== undefined) CONFIG.hover = hoverText;
    init('[data-logo]');
  }

  // Auto-initialize
  autoInit();

  // Public API
  return {
    init: init,
    update: update,
    getHTML: getHTML,
    config: CONFIG
  };

})();

// Legacy support
if (typeof module !== 'undefined' && module.exports) {
  module.exports = LogoModule;
}
