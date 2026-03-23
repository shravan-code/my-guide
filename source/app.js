console.log("App.js loading...");
const body = document.body;
const storageKey = "data-guide-theme";
const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

function applyTheme(mode) {
  const isDark = mode === "dark";
  body.classList.toggle("dark", isDark);
  document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
  console.log("Applied theme:", mode, "dark class:", body.classList.contains("dark"));

  const toggleButton = document.getElementById("theme-toggle");
  const toggleText = toggleButton?.querySelector(".toggle-text");
  const toggleIcon = toggleButton?.querySelector(".toggle-icon");

  if (toggleText) {
    toggleText.textContent = isDark ? "Light" : "Dark";
  }

  if (toggleIcon) {
    toggleIcon.textContent = isDark ? "☀" : "☾";
  }
}

function initTheme() {
  try {
    const toggleButton = document.getElementById("theme-toggle");
    console.log("Theme toggle button found:", toggleButton);
    const storedTheme = localStorage.getItem(storageKey);
    const prefersDark = mediaQuery.matches;
    const initialTheme = storedTheme || (prefersDark ? "dark" : "light");
    applyTheme(initialTheme);

    toggleButton?.addEventListener("click", () => {
      const nextTheme = body.classList.contains("dark") ? "light" : "dark";
      console.log("Toggle clicked, switching to:", nextTheme);
      localStorage.setItem(storageKey, nextTheme);
      applyTheme(nextTheme);
    });

    mediaQuery.addEventListener("change", (event) => {
      const saved = localStorage.getItem(storageKey);
      if (!saved) {
        applyTheme(event.matches ? "dark" : "light");
      }
    });
  } catch (error) {
    console.error("Error in initTheme:", error);
  }
}

// Apply theme immediately to avoid flash of wrong theme
try {
  const storedTheme = localStorage.getItem(storageKey);
  const prefersDark = mediaQuery.matches;
  const initialTheme = storedTheme || (prefersDark ? "dark" : "light");
  applyTheme(initialTheme);
} catch (error) {
  console.error("Error applying initial theme:", error);
}

// Attach event listeners after DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initTheme);
} else {
  initTheme();
}
