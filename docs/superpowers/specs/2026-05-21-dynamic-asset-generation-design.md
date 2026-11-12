# Dynamic Asset Generation — Design (v0.4.1)

**Status:** approved
**Date:** 2026-05-21
**Target release:** v0.4.1

## Problem

The repo currently ships seven static, hand-authored printable assets
(`Nato Phonetic Alphabet*.{pdf,docx,epub,odt,pages}`). Changes to the
visual design — fonts, colors, spacing — require opening Apple Pages,
manually re-exporting four files, and committing all of them. Two file
types (`.pages`, `.odt`) are no longer wanted.

We want a single source of truth that produces every printable artifact,
so design changes are a config edit instead of a Pages session.

## Goals

- Generate the printable assets from code, sharing the existing
  alphabet data in `src/nato_phonetic/core.py`.
- Output four files: PDF (portrait), PDF (landscape), DOCX, EPub.
- Generated PDFs **match the current visual style** (Source Code Pro
  monospace, two-column table, gray zebra striping, CC BY-SA footer).
- Drop `.pages` and `.odt` formats entirely.
- Enforce freshness so committed assets cannot drift from the generator.
- End-user `phonetic open` / `phonetic download` keep working with no
  URL or behavior changes.
- End-user install footprint is unchanged (generation deps are
  build-time only).

## Non-goals

- Pixel-perfect parity between PDF and DOCX/EPub. DOCX and EPub will
  approximate the PDF's look using their native styling.
- Letting end users regenerate or restyle the assets at runtime. The
  "more options" requirement is a project-maintainer concern.
- Replacing `Social Image.png` / `Social Image.pxd` (separate concern,
  not part of the printable set).
- Migrating older CLI versions. v0.4.0 will keep working because the
  Codeberg raw URL paths don't change (only the catalog shrinks).

## Architecture

```
repo root/
├── Nato Phonetic Alphabet - PDF.pdf              ← generated, committed
├── Nato Phonetic Alphabet (Landscape) - PDF.pdf  ← generated, committed
├── Nato Phonetic Alphabet - EPub.epub            ← generated, committed
├── Nato Phonetic Alphabet - Microsoft Word.docx  ← generated, committed
│
├── scripts/build_assets/
│   ├── __init__.py
│   ├── __main__.py     # entry: python -m scripts.build_assets
│   ├── config.py       # title text, fonts, colors, page margins
│   ├── pdf.py          # build_pdf(landscape: bool, dest: Path)
│   ├── docx.py         # build_docx(dest: Path)
│   ├── epub.py         # build_epub(dest: Path)
│   ├── fonts/
│   │   └── SourceCodePro-Regular.ttf
│   └── assets/
│       └── cc-by-sa.png
│
├── .githooks/
│   └── pre-push        # runs `make build-assets`; aborts if diff
│
├── src/nato_phonetic/
│   └── assets.py       # catalog shrinks; URL pattern unchanged
│
└── tests/
    └── test_build_assets.py    # smoke + format-valid checks
```

### Source of truth

The alphabet lives in `nato_phonetic.core.NATO_PHONETIC_ALPHABET`. Each
generator imports it directly. No duplication, no separate template
data file.

### Generators

Each generator module exports one pure function that writes one file.

| Module | Function | Library |
|---|---|---|
| `pdf.py` | `build_pdf(landscape: bool, dest: Path) -> None` | reportlab |
| `docx.py` | `build_docx(dest: Path) -> None` | python-docx |
| `epub.py` | `build_epub(dest: Path) -> None` | ebooklib |

`config.py` exports shared constants — title text, body/header font
filename, accent color, page margins, license text and URLs.

### Visual fidelity (PDF)

The current portrait PDF was rendered for inspection:

- Page size: US Letter portrait (612 × 792 pt).
- Font: Source Code Pro, regular weight, throughout.
- Title: large centered "Nato Phonetic Alphabet" near top.
- Table: 13 rows × 4 columns (letter | word | letter | word). Letters
  A–M run down the left half, N–Z down the right.
- Cell borders: thin gray (`#cccccc`).
- Row backgrounds: alternating white and `#f4f4f4`.
- Footer: CC BY-SA attribution with hyperlinks, followed by the CC icon.

Source Code Pro ships under the SIL Open Font License and is freely
redistributable. We bundle `SourceCodePro-Regular.ttf` in
`scripts/build_assets/fonts/`. The CC icon is downloaded once from
creativecommons.org and bundled as a small PNG in
`scripts/build_assets/assets/`.

The landscape PDF mirrors the portrait layout on a rotated page.

### Build dependencies

```toml
[project.optional-dependencies]
build = ["reportlab", "python-docx", "ebooklib"]
```

End-user installs (`uv tool install phonetic-nato`, `pipx install
phonetic-nato`, etc.) do not pull these in. The CLI runtime keeps its
slim click + rich dependency set.

### Dev UX

```bash
make build-assets
```

Implementation:

```make
build-assets: ## Generate printable assets in the repo root
	uv sync --extra build
	uv run python -m scripts.build_assets
```

`python -m scripts.build_assets` writes the four files in the current
working directory by default. A `--out` flag overrides the destination.

### Freshness enforcement

The committed assets and the generator must never disagree. Two layers
of protection:

**Layer 1 — local pre-push hook (recommended).**

`.githooks/pre-push` is committed to the repo. It runs `make
build-assets`, then `git diff --exit-status` against the four asset
files. If diff is non-empty, the hook aborts the push with a message:

```
Generated assets are stale. Inspect with `git diff`, stage with
`git add`, commit, and retry your push.
```

Contributors enable the hook once per clone:

```bash
git config core.hooksPath .githooks
```

This setup line goes in the README's Development section.

**Layer 2 — CI verification (the actual gate).**

`publish.yml` `build` job gets a new step after `setup-uv`:

```yaml
- run: uv sync --extra build
- run: uv run python -m scripts.build_assets
- run: git diff --exit-status -- 'Nato Phonetic Alphabet*'
```

CI fails the workflow if the generator's output disagrees with what's
committed. Hooks are best-effort; CI is the gate.

Other documented options (not the default but supported):

- **pre-commit framework.** A `.pre-commit-config.yaml` snippet in the
  README for contributors who prefer it.
- **`make check`.** Existing `check` target adds an `assets-fresh`
  step that runs the same diff check locally.

### CLI changes

`src/nato_phonetic/assets.py`:

- `ASSETS` catalog drops the `pages`, `pages-landscape`, and `odt`
  entries. Remaining: `pdf`, `pdf-landscape`, `epub`, `docx`.
- `RAW_BASE` is unchanged — Codeberg raw URLs, same path scheme,
  because the four target files still live in the repo root.

No URL or behavior change at the CLI surface. `phonetic open`,
`phonetic download`, and `phonetic download --list` continue to work as
they do in v0.4.0.

### Tests

- `tests/test_assets.py`: drop assertions about the removed slugs; add
  assertion that the catalog has exactly the four expected entries.
- `tests/test_build_assets.py` (new):
  - `test_pdf_portrait_writes_valid_pdf` — calls `build_pdf(False,
    tmp_path / "out.pdf")`, asserts file starts with `%PDF-` and is
    larger than 5KB.
  - `test_pdf_landscape_writes_valid_pdf` — same for landscape.
  - `test_docx_writes_valid_docx` — `build_docx(...)`, asserts file is
    a valid zip with `word/document.xml` member.
  - `test_epub_writes_valid_epub` — `build_epub(...)`, asserts file is
    a valid zip with `mimetype` member containing `application/epub+zip`.

Tests run under the existing `pytest` invocation. They require the
`build` extra; CI's existing `uv sync --extra dev --extra build` covers
both. Local-only contributors can run `uv run --extra build pytest`.

### Cleanup

Delete from the repo on this branch:

- `Nato Phonetic Alphabet.pages`
- `Nato Phonetic Alphabet Landscape.pages`
- `Nato Phonetic Alphabet - Open Doc Format.odt`

Kept and regenerated by the build:

- `Nato Phonetic Alphabet - PDF.pdf`
- `Nato Phonetic Alphabet (Landscape) - PDF.pdf`
- `Nato Phonetic Alphabet - EPub.epub`
- `Nato Phonetic Alphabet - Microsoft Word.docx`

Kept untouched (not part of the printable set):

- `Social Image.png`
- `Social Image.pxd`

### Documentation

README gets:

- The "Available slugs" list shrinks to `pdf, pdf-landscape, epub, docx`.
- A new Development subsection: "Regenerating printable assets" —
  covers the `make build-assets` command, the
  `git config core.hooksPath .githooks` setup, and a note that CI will
  fail the build if committed assets drift.

## Error handling

- Missing font / icon file in `scripts/build_assets/` → generator
  raises `FileNotFoundError` with the absolute path it tried. Caller
  (Makefile, CI, hook) surfaces the error and exits non-zero.
- Build extra not installed when running `python -m scripts.build_assets`
  → standard `ModuleNotFoundError` for reportlab/python-docx/ebooklib.
  Documented in the README; Makefile target runs `uv sync --extra build`
  first so it self-heals.
- Pre-push hook can't find `make` → hook is portable shell; if `make`
  isn't on PATH, it falls back to running the python module directly.

## Risks & open questions

- **Font rendering parity.** ReportLab's Source Code Pro rendering may
  differ subtly from Pages' rendering of the same font. Acceptable for
  this design — the goal is "visually consistent", not "byte identical".
- **CC icon source.** The icon is small (~3KB) but adds a binary blob
  to the repo. Acceptable; alternative is to skip the icon and use the
  text "CC BY-SA 4.0" alone, which costs visual fidelity.
- **DOCX / EPub fidelity.** Both formats have intentionally limited
  layout control compared to PDF. The generated versions will use
  format-native styling and may visibly differ from a Pages-exported
  reference. Called out in non-goals.

## Implementation order

1. Add the `build` optional extra to `pyproject.toml`.
2. Scaffold `scripts/build_assets/` with `__init__.py`, `__main__.py`,
   `config.py`, `pdf.py`, `docx.py`, `epub.py`.
3. Bundle `SourceCodePro-Regular.ttf` and `cc-by-sa.png`.
4. Implement PDF generator first (the visually load-bearing format).
5. Implement DOCX, then EPub.
6. Wire the Makefile target.
7. Add tests under `tests/test_build_assets.py`.
8. Add the pre-push hook in `.githooks/pre-push`.
9. Update `publish.yml` build job with the freshness check.
10. Update `src/nato_phonetic/assets.py` catalog.
11. Delete `.pages` and `.odt` files; regenerate the four committed
    assets via `make build-assets`.
12. Update the README.
13. Bump version, tag, release.
