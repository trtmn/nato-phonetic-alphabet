// Shared accent-theme picker for every tool on apps.trtmn.io.
// The storage key predates the shared file; keeping it preserves the
// color people already picked on the NATO page.
(function () {
  const THEMES = ["red", "orange", "yellow", "green", "blue", "purple", "slate"];
  const DEFAULT_THEME = "blue";
  const STORAGE_KEY = "nato-theme";

  const swatches = document.querySelectorAll(".swatch");

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    swatches.forEach((swatch) => {
      swatch.classList.toggle("active", swatch.dataset.theme === theme);
    });
  }

  swatches.forEach((swatch) => {
    swatch.addEventListener("click", () => {
      applyTheme(swatch.dataset.theme);
      localStorage.setItem(STORAGE_KEY, swatch.dataset.theme);
    });
  });

  const savedTheme = localStorage.getItem(STORAGE_KEY);
  applyTheme(THEMES.includes(savedTheme) ? savedTheme : DEFAULT_THEME);
})();
