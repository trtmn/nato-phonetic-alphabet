const THEMES = ["red", "orange", "yellow", "green", "blue", "purple", "slate"];
const DEFAULT_THEME = "blue";
const STORAGE_KEY = "nato-theme";

const input = document.getElementById("input");
const output = document.getElementById("output");
const swatches = document.querySelectorAll(".swatch");

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  swatches.forEach((swatch) => {
    swatch.classList.toggle("active", swatch.dataset.theme === theme);
  });
}

function setTheme(theme) {
  applyTheme(theme);
  localStorage.setItem(STORAGE_KEY, theme);
}

swatches.forEach((swatch) => {
  swatch.addEventListener("click", () => setTheme(swatch.dataset.theme));
});

const savedTheme = localStorage.getItem(STORAGE_KEY);
applyTheme(THEMES.includes(savedTheme) ? savedTheme : DEFAULT_THEME);

function makeRow(charText, wordText, extraClass) {
  const row = document.createElement("div");
  row.className = extraClass ? `row ${extraClass}` : "row";

  const charSpan = document.createElement("span");
  charSpan.className = "char";
  charSpan.textContent = charText;

  const wordSpan = document.createElement("span");
  wordSpan.className = "word";
  wordSpan.textContent = wordText;

  row.append(charSpan, wordSpan);
  return row;
}

// Follow new output only when the reader is already at (or near) the
// bottom, so scrolling up to re-read something doesn't get yanked away.
function isNearBottom() {
  return output.scrollHeight - output.scrollTop - output.clientHeight < 40;
}

function render() {
  const follow = isNearBottom();
  output.textContent = "";
  for (const char of input.value) {
    const upper = char.toUpperCase();

    if (/\s/.test(char)) {
      output.appendChild(makeRow("·", "Space", "space"));
    } else if (NATO_ALPHABET[upper]) {
      output.appendChild(makeRow(upper, NATO_ALPHABET[upper]));
    } else {
      output.appendChild(makeRow(char, char));
    }
  }
  if (follow) {
    output.scrollTop = output.scrollHeight;
  }
}

input.addEventListener("input", render);
