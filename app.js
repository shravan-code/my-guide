const body = document.body;
const toggleButton = document.getElementById("theme-toggle");
const toggleText = toggleButton?.querySelector(".toggle-text");
const toggleIcon = toggleButton?.querySelector(".toggle-icon");
const storageKey = "data-guide-theme";

function applyTheme(mode) {
  const isDark = mode === "dark";
  body.classList.toggle("dark", isDark);

  if (toggleText) {
    toggleText.textContent = isDark ? "Light" : "Dark";
  }

  if (toggleIcon) {
    toggleIcon.textContent = isDark ? "☀️" : "🌙";
  }
}

const storedTheme = localStorage.getItem(storageKey);
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
const initialTheme = storedTheme || (prefersDark ? "dark" : "light");

applyTheme(initialTheme);

toggleButton?.addEventListener("click", () => {
  const nextTheme = body.classList.contains("dark") ? "light" : "dark";
  localStorage.setItem(storageKey, nextTheme);
  applyTheme(nextTheme);
});
