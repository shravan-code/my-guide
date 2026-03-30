/* Portfolio project pages: separate drawer menu (not global #mobile-menu). */
(function () {
  const hamburger = document.getElementById("hamburger-btn");
  const mobileMenu = document.getElementById("new-mobile-menu");

  if (hamburger && mobileMenu) {
    hamburger.addEventListener("click", function (e) {
      e.preventDefault();
      hamburger.classList.toggle("active");
      mobileMenu.classList.toggle("show");
    });
  }
})();
