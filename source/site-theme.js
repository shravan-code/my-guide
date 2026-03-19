(function () {
  const storageKey = "data-guide-theme";
  const body = document.body;

  function applyTheme(mode) {
    const isDark = mode === "dark";
    body.classList.toggle("dg-dark", isDark);
    body.classList.toggle("dark", isDark);
  }

  const saved = localStorage.getItem(storageKey);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(saved || (prefersDark ? "dark" : "light"));

  const wrap = document.createElement("div");
  wrap.className = "dg-actions";

  const home = document.createElement("a");
  home.href = "../index.html";
  home.textContent = "Home";
  home.setAttribute("aria-label", "Go to Data-Guide home");

  const themeButton = document.createElement("button");
  themeButton.type = "button";

  function syncLabel() {
    themeButton.textContent = body.classList.contains("dg-dark") ? "Light" : "Dark";
  }

  syncLabel();

  themeButton.addEventListener("click", function () {
    const next = body.classList.contains("dg-dark") ? "light" : "dark";
    localStorage.setItem(storageKey, next);
    applyTheme(next);
    syncLabel();
  });

  wrap.append(home, themeButton);
  body.appendChild(wrap);
})();
