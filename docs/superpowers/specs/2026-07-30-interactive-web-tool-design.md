# Interactive NATO Phonetic Web Tool — Design

**Status:** approved
**Date:** 2026-07-30

## Problem

The project currently offers two ways to use the NATO phonetic alphabet:
a Click-based CLI (`phonetic spell "WORD"`) and a set of static printable
assets (PDF/EPub/DOCX). There is no way to interactively spell out text
in a browser without installing anything.

## Goals

- Add a static, dependency-free web page: type text, see the NATO
  phonetic breakdown update live, letter by letter.
- Style it with Matt's trtmn brand (dark background, Martian Mono +
  Inter typography, accent color), minus the sidebar — this is a
  utility tool, not a resume-shaped document.
- Let the user pick from 6 curated accent themes via a small color-swatch
  picker, persisted across reloads.
- Zero build step, zero JS dependencies — plain HTML/CSS/JS that opens
  directly in a browser or can be hosted as a static file later.

## Non-goals

- No changes to the existing Python CLI, `core.py`, or the
  PDF/EPub/DOCX asset generation pipeline — all of that stays as-is.
- No copy-to-clipboard, shareable links, audio playback, or other
  extras beyond the core conversion + theme picker.
- No automated JS test suite — this is a small vanilla script verified
  by hand in a browser.
- No CI/deploy wiring for hosting the page (out of scope for this spec).

## Design

### Files

New `web/` directory, entirely self-contained:

- `web/index.html` — page structure: input textarea, output list,
  theme-swatch picker.
- `web/style.css` — dark, sidebar-less layout using trtmn brand tokens
  (hand-copied color/typography values, not a dependency on the brand
  skill's `brand.css` file since this ships in the repo independently).
- `web/app.js` — all behavior: live conversion on input, theme
  switching + persistence.
- `web/nato-alphabet.js` — a hand-written `NATO_ALPHABET` object
  mirroring `src/nato_phonetic/core.py`'s `NATO_PHONETIC_ALPHABET`
  mapping. This is fixed, never-changing data, so duplicating it here
  (rather than generating it from Python at build time) carries
  negligible sync risk and keeps the page a zero-build static artifact.

### Behavior

- A `<textarea>` for free-text entry, focused on page load.
- On every `input` event, re-render the output live (no submit button).
- Conversion rules, one output line per character:
  - Letters (A-Z, case-insensitive) → NATO word (`Alpha`, `Bravo`, …).
  - Digits (0-9) → NATO word (`Zero`, `One`, …).
  - Whitespace → rendered as a blank/space marker line (not spelled out).
  - Any other character (punctuation, symbols) → shown as itself,
    unstyled, so unexpected input never breaks rendering.
- Empty input → empty output area, no placeholder copy.
- Output format: `H — Hotel` per line, matching the CLI's `spell`
  command output for familiarity.

### Styling & theme picker

- Full dark background (`--bg-dark` token from the chosen theme),
  centered single-column layout — no sidebar, no nav.
- Martian Mono (uppercase, wide tracking) for the title and labels;
  Inter 300 for the output list, matching the brand's two-face system.
- A small row of 6 color swatches (buttons) lets the user switch
  accent theme instantly by setting `data-theme` on `<html>`:
  **teal (default), blue, green, purple, red, slate** — a representative
  spread across cool/warm/neutral rather than all 17 brand themes, to
  keep the picker small and scannable.
- Selected theme is saved to `localStorage` and restored on page load.
- Color values for these 6 themes are hand-copied from the trtmn-brand
  skill's `references/tokens.md` into `style.css` as CSS custom
  properties per `[data-theme="..."]` selector — no external stylesheet
  dependency.
- Google Fonts (Martian Mono + Inter) loaded via `<link>` tags, same as
  other trtmn-branded surfaces.

### Error handling

None needed — the conversion is a pure function over displayable
characters; there's no invalid state, network call, or async operation
that can fail. Unrecognized characters fall through to "display as-is"
rather than raising or showing an error.

### Testing

Manual verification in a browser:
- Type a mixed-case word, confirm live per-letter output.
- Type digits, punctuation, and whitespace, confirm each renders per
  the rules above.
- Clear the input, confirm output clears.
- Switch themes, confirm the swatch picker updates colors instantly and
  the choice survives a page reload.

No automated test suite is added; existing Python tests are unaffected.
