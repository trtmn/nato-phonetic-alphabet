const input = document.getElementById("input");
const output = document.getElementById("output");
const hint = document.getElementById("hint");
const swapBtn = document.getElementById("swap");
const viewBtn = document.getElementById("view");
const copyBtn = document.getElementById("copy");

const BITS_PER_BYTE = 8;

let circleView = false;
// What the last render produced, so swap/copy act on the conversion
// rather than on whatever happens to be on screen.
let lastBinary = null; // raw 0/1 output when converting text -> binary
let lastText = null; // decoded text when converting binary -> text
let lastVisible = "";

function isBinaryInput(value) {
  return /[01]/.test(value) && /^[01\s]+$/.test(value);
}

function textToBinary(text) {
  const encoder = new TextEncoder();
  return text
    .split("\n")
    .map((line) =>
      Array.from(encoder.encode(line))
        .map((byte) => byte.toString(2).padStart(BITS_PER_BYTE, "0"))
        .join(" "),
    )
    .join("\n");
}

function binaryToText(bits) {
  const clean = bits.replace(/\s+/g, "");
  const completeLength = clean.length - (clean.length % BITS_PER_BYTE);
  const bytes = new Uint8Array(completeLength / BITS_PER_BYTE);

  for (let i = 0; i < completeLength; i += BITS_PER_BYTE) {
    bytes[i / BITS_PER_BYTE] = parseInt(clean.slice(i, i + BITS_PER_BYTE), 2);
  }

  return {
    text: new TextDecoder().decode(bytes),
    leftoverBits: clean.length - completeLength,
  };
}

function isNearBottom() {
  return output.scrollHeight - output.scrollTop - output.clientHeight < 40;
}

function renderBinaryLines(binaryText, circles) {
  for (const line of binaryText.split("\n")) {
    const lineEl = document.createElement("div");
    lineEl.className = circles ? "line circles" : "line text";

    if (!circles) {
      lineEl.textContent = line;
    } else {
      for (const bit of line) {
        if (bit === "1" || bit === "0") {
          const bitEl = document.createElement("span");
          bitEl.className = bit === "1" ? "one" : "zero";
          bitEl.textContent = bit === "1" ? "●" : "○";
          lineEl.appendChild(bitEl);
        } else {
          lineEl.appendChild(document.createTextNode(bit));
        }
      }
    }

    output.appendChild(lineEl);
  }
}

function renderTextLines(text) {
  for (const line of text.split("\n")) {
    const lineEl = document.createElement("div");
    lineEl.className = "line text";
    lineEl.textContent = line;
    output.appendChild(lineEl);
  }
}

function render() {
  const follow = isNearBottom();
  const value = input.value;
  output.textContent = "";
  hint.hidden = true;
  lastBinary = null;
  lastText = null;
  lastVisible = "";

  if (value.length === 0) {
    viewBtn.disabled = true;
    return;
  }

  if (isBinaryInput(value)) {
    const { text, leftoverBits } = binaryToText(value);
    lastText = text;
    lastVisible = text;
    viewBtn.disabled = true;
    renderTextLines(text);

    if (leftoverBits > 0) {
      hint.textContent = `${leftoverBits} trailing bit${leftoverBits === 1 ? "" : "s"} ignored — a byte needs ${BITS_PER_BYTE} bits.`;
      hint.hidden = false;
    }
  } else {
    lastBinary = textToBinary(value);
    viewBtn.disabled = false;
    lastVisible = circleView ? lastBinary.replace(/1/g, "●").replace(/0/g, "○") : lastBinary;
    renderBinaryLines(lastBinary, circleView);
  }

  if (follow) {
    output.scrollTop = output.scrollHeight;
  }
}

input.addEventListener("input", render);

swapBtn.addEventListener("click", () => {
  const next = lastBinary ?? lastText;
  if (next === null) return;
  input.value = next;
  render();
  input.focus();
});

viewBtn.addEventListener("click", () => {
  circleView = !circleView;
  viewBtn.setAttribute("aria-pressed", String(circleView));
  viewBtn.textContent = circleView ? "●○ / 01" : "01 / ●○";
  render();
});

copyBtn.addEventListener("click", async () => {
  if (!lastVisible) return;
  const label = copyBtn.textContent;
  try {
    await navigator.clipboard.writeText(lastVisible);
    copyBtn.textContent = "copied";
  } catch {
    copyBtn.textContent = "copy failed";
  }
  setTimeout(() => {
    copyBtn.textContent = label;
  }, 1200);
});

render();
