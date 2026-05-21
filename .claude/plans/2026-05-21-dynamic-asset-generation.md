# Dynamic Asset Generation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the four hand-authored printable assets with files
generated from `nato_phonetic.core`, while preserving the existing
visual style (Source Code Pro, two-column zebra-striped table, CC
BY-SA footer) and keeping the CLI's user-visible behavior unchanged.

**Architecture:** Pure-Python generators live in `scripts/build_assets/`
(outside the installable package) with `[project.optional-dependencies]
build` deps. They write the four committed asset files in the repo
root. A local pre-push hook and a CI step verify the committed files
match the generator output, so the generator is the source of truth.

**Tech Stack:** ReportLab (PDF), python-docx (DOCX), ebooklib (EPub),
Source Code Pro TTF (SIL OFL), pytest, GitHub Actions, Git hooks.

**Spec:** `docs/superpowers/specs/2026-05-21-dynamic-asset-generation-design.md`

---

## File Structure

**New files:**
- `scripts/__init__.py` — empty, makes `scripts` importable
- `scripts/build_assets/__init__.py` — re-exports public functions
- `scripts/build_assets/__main__.py` — CLI entry; `python -m scripts.build_assets`
- `scripts/build_assets/config.py` — title text, fonts, colors, footer copy
- `scripts/build_assets/pdf.py` — `build_pdf(landscape: bool, dest: Path)`
- `scripts/build_assets/docx.py` — `build_docx(dest: Path)`
- `scripts/build_assets/epub.py` — `build_epub(dest: Path)`
- `scripts/build_assets/fonts/SourceCodePro-Regular.ttf` — bundled font
- `scripts/build_assets/assets/cc-by-sa.png` — bundled license badge
- `tests/test_build_assets.py` — generator smoke + format-valid tests
- `.githooks/pre-push` — runs build, aborts push if asset diff

**Modified files:**
- `pyproject.toml` — add `[project.optional-dependencies] build`
- `Makefile` — add `build-assets` target
- `.github/workflows/publish.yml:11-23` — build job adds asset
  regeneration + drift check
- `src/nato_phonetic/assets.py:39-46` — drop `pages`, `pages-landscape`,
  `odt` from `ASSETS`
- `tests/test_assets.py` — drop assertions about removed slugs
- `README.md` — slug list shrinks; Development subsection on
  regenerating assets

**Deleted files:**
- `Nato Phonetic Alphabet.pages`
- `Nato Phonetic Alphabet Landscape.pages`
- `Nato Phonetic Alphabet - Open Doc Format.odt`

**Regenerated (still committed) files:**
- `Nato Phonetic Alphabet - PDF.pdf`
- `Nato Phonetic Alphabet (Landscape) - PDF.pdf`
- `Nato Phonetic Alphabet - EPub.epub`
- `Nato Phonetic Alphabet - Microsoft Word.docx`

---

## Task 1: Scaffold module + add build extra

**Files:**
- Modify: `pyproject.toml`
- Create: `scripts/__init__.py`, `scripts/build_assets/__init__.py`,
  `scripts/build_assets/__main__.py`, `scripts/build_assets/config.py`,
  `scripts/build_assets/pdf.py`, `scripts/build_assets/docx.py`,
  `scripts/build_assets/epub.py`

- [ ] **Step 1: Add the build extra to pyproject.toml**

Append to the `[project.optional-dependencies]` block at lines 29-36 of
`pyproject.toml` (the section currently containing `dev = [...]`). The
final block should read:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]
build = [
    "reportlab>=4.0.0",
    "python-docx>=1.0.0",
    "ebooklib>=0.18",
]
```

- [ ] **Step 2: Create empty `scripts/__init__.py`**

Write a single-line file:

```python
"""Build-time scripts (not part of the installable package)."""
```

- [ ] **Step 3: Create `scripts/build_assets/__init__.py`**

```python
"""Generators for the printable NATO phonetic alphabet assets."""

from .docx import build_docx
from .epub import build_epub
from .pdf import build_pdf

__all__ = ["build_pdf", "build_docx", "build_epub"]
```

- [ ] **Step 4: Create stub modules for each generator**

For each of `pdf.py`, `docx.py`, `epub.py`, create:

```python
"""<format> generator (stub — implemented in a later task)."""

from pathlib import Path


def build_pdf(landscape: bool, dest: Path) -> None:  # rename per file
    raise NotImplementedError
```

(Replace `build_pdf(landscape: bool, dest: Path)` with
`build_docx(dest: Path)` for `docx.py` and `build_epub(dest: Path)` for
`epub.py`.)

- [ ] **Step 5: Create `scripts/build_assets/config.py`**

```python
"""Shared layout and content constants for the asset generators."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
FONT_PATH = PROJECT_ROOT / "fonts" / "SourceCodePro-Regular.ttf"
CC_ICON_PATH = PROJECT_ROOT / "assets" / "cc-by-sa.png"

TITLE = "Nato Phonetic Alphabet"

# Visual constants — match the existing PDF style
HEADER_FONT_NAME = "SourceCodePro"
HEADER_FONT_SIZE = 32
BODY_FONT_SIZE = 14
ROW_HEIGHT = 28
GRID_COLOR = "#cccccc"
ZEBRA_COLOR = "#f4f4f4"
LINK_COLOR = "#1f88c5"

# License footer
LICENSE_TEXT = "© 2024 by Matt Troutman is licensed under CC BY-SA 4.0"
PROJECT_URL = "https://trtmn.io/nato-phonetic-alphabet"
AUTHOR_URL = "https://trtmn.io"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"

# Default filenames written into the repo root
PDF_PORTRAIT_NAME = "Nato Phonetic Alphabet - PDF.pdf"
PDF_LANDSCAPE_NAME = "Nato Phonetic Alphabet (Landscape) - PDF.pdf"
DOCX_NAME = "Nato Phonetic Alphabet - Microsoft Word.docx"
EPUB_NAME = "Nato Phonetic Alphabet - EPub.epub"
```

- [ ] **Step 6: Create stub `__main__.py`**

```python
"""CLI entry: `python -m scripts.build_assets`."""

import argparse
from pathlib import Path

from . import config


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate printable NATO alphabet assets.")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path.cwd(),
        help="Destination directory (default: current working directory).",
    )
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    raise NotImplementedError("generators wired up in a later task")


if __name__ == "__main__":
    main()
```

- [ ] **Step 7: Sync deps and verify import**

Run: `uv sync --extra build`
Expected: installs reportlab, python-docx, ebooklib.

Run: `uv run python -c "from scripts.build_assets import build_pdf, build_docx, build_epub; print('ok')"`
Expected: prints `ok`.

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml scripts/
git commit -m "Scaffold scripts/build_assets module + add build extra"
```

---

## Task 2: Bundle Source Code Pro font and CC badge

**Files:**
- Create: `scripts/build_assets/fonts/SourceCodePro-Regular.ttf`
- Create: `scripts/build_assets/assets/cc-by-sa.png`

- [ ] **Step 1: Create the directories**

```bash
mkdir -p scripts/build_assets/fonts scripts/build_assets/assets
```

- [ ] **Step 2: Download Source Code Pro Regular (SIL OFL)**

```bash
curl -sLo scripts/build_assets/fonts/SourceCodePro-Regular.ttf \
  https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Regular.ttf
```

Verify with: `ls -la scripts/build_assets/fonts/SourceCodePro-Regular.ttf`
Expected: file size between 80,000 and 150,000 bytes.

Sanity-check it's a TrueType file:

```bash
file scripts/build_assets/fonts/SourceCodePro-Regular.ttf
```

Expected: contains `TrueType font` or `OpenType font`.

- [ ] **Step 3: Download the CC BY-SA 4.0 badge**

```bash
curl -sLo scripts/build_assets/assets/cc-by-sa.png \
  https://licensebuttons.net/l/by-sa/4.0/88x31.png
```

Verify:

```bash
file scripts/build_assets/assets/cc-by-sa.png
```

Expected: `PNG image data, 88 x 31`.

- [ ] **Step 4: Commit**

```bash
git add scripts/build_assets/fonts/ scripts/build_assets/assets/
git commit -m "Bundle Source Code Pro Regular + CC BY-SA badge"
```

---

## Task 3: TDD the PDF generator

**Files:**
- Create: `tests/test_build_assets.py`
- Modify: `scripts/build_assets/pdf.py`

- [ ] **Step 1: Write the failing PDF test**

Create `tests/test_build_assets.py`:

```python
"""Tests for the printable-asset generators."""

import zipfile
from pathlib import Path

import pytest

from scripts.build_assets import build_docx, build_epub, build_pdf


def test_build_pdf_portrait_writes_valid_pdf(tmp_path: Path) -> None:
    dest = tmp_path / "out.pdf"
    build_pdf(landscape=False, dest=dest)
    assert dest.exists()
    assert dest.stat().st_size > 5000, "PDF should be non-trivially sized"
    assert dest.read_bytes()[:5] == b"%PDF-"


def test_build_pdf_landscape_writes_valid_pdf(tmp_path: Path) -> None:
    dest = tmp_path / "out-landscape.pdf"
    build_pdf(landscape=True, dest=dest)
    assert dest.exists()
    assert dest.read_bytes()[:5] == b"%PDF-"
```

- [ ] **Step 2: Run and verify it fails**

Run: `uv run --extra build pytest tests/test_build_assets.py::test_build_pdf_portrait_writes_valid_pdf -v --no-cov`
Expected: FAIL with `NotImplementedError` from the stub `build_pdf`.

- [ ] **Step 3: Implement `build_pdf`**

Replace the contents of `scripts/build_assets/pdf.py`:

```python
"""PDF generator: portrait or landscape, two-column zebra-striped table."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER, landscape as _landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from nato_phonetic.core import NATO_PHONETIC_ALPHABET

from . import config

_FONT_REGISTERED = False


def _ensure_font_registered() -> None:
    global _FONT_REGISTERED
    if _FONT_REGISTERED:
        return
    pdfmetrics.registerFont(TTFont(config.HEADER_FONT_NAME, str(config.FONT_PATH)))
    _FONT_REGISTERED = True


def _alphabet_pairs() -> list[tuple[str, str, str, str]]:
    """Return 13 rows of (letter, word, letter, word) for the A-M / N-Z split."""
    letters = [chr(c) for c in range(ord("A"), ord("Z") + 1)]
    rows: list[tuple[str, str, str, str]] = []
    for i in range(13):
        left = letters[i]
        right = letters[i + 13]
        rows.append((left, NATO_PHONETIC_ALPHABET[left], right, NATO_PHONETIC_ALPHABET[right]))
    return rows


def build_pdf(landscape: bool, dest: Path) -> None:
    """Generate a printable PDF of the NATO phonetic alphabet."""
    _ensure_font_registered()

    page_size = _landscape(LETTER) if landscape else LETTER
    doc = SimpleDocTemplate(
        str(dest),
        pagesize=page_size,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title=config.TITLE,
        author="Matt Troutman",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName=config.HEADER_FONT_NAME,
        fontSize=config.HEADER_FONT_SIZE,
        leading=config.HEADER_FONT_SIZE * 1.2,
        alignment=1,  # center
        spaceAfter=0.5 * inch,
    )

    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontName=config.HEADER_FONT_NAME,
        fontSize=10,
        alignment=1,
        leading=14,
    )

    table_data = _alphabet_pairs()
    cell_style = ParagraphStyle(
        "Cell",
        parent=styles["Normal"],
        fontName=config.HEADER_FONT_NAME,
        fontSize=config.BODY_FONT_SIZE,
        alignment=1,
    )
    table_rows = [
        [
            Paragraph(left, cell_style),
            Paragraph(left_word, cell_style),
            Paragraph(right, cell_style),
            Paragraph(right_word, cell_style),
        ]
        for left, left_word, right, right_word in table_data
    ]

    col_widths = [0.6 * inch, 2.4 * inch, 0.6 * inch, 2.4 * inch]
    if landscape:
        col_widths = [0.7 * inch, 3.5 * inch, 0.7 * inch, 3.5 * inch]

    table = Table(table_rows, colWidths=col_widths, rowHeights=config.ROW_HEIGHT)
    style_cmds: list[tuple] = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(config.GRID_COLOR)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for row_idx in range(len(table_rows)):
        if row_idx % 2 == 1:
            style_cmds.append(
                ("BACKGROUND", (0, row_idx), (-1, row_idx), colors.HexColor(config.ZEBRA_COLOR))
            )
    table.setStyle(TableStyle(style_cmds))

    footer_html = (
        f'<a href="{config.PROJECT_URL}" color="{config.LINK_COLOR}"><u>{config.TITLE}</u></a> '
        f'© 2024 by <a href="{config.AUTHOR_URL}" color="{config.LINK_COLOR}"><u>Matt Troutman</u></a> '
        f'is licensed under <a href="{config.LICENSE_URL}" color="{config.LINK_COLOR}"><u>CC BY-SA 4.0</u></a>'
    )

    story = [
        Paragraph(config.TITLE, title_style),
        table,
        Spacer(1, 0.4 * inch),
        Paragraph(footer_html, footer_style),
        Spacer(1, 0.1 * inch),
        Image(str(config.CC_ICON_PATH), width=88, height=31, hAlign="CENTER"),
    ]
    doc.build(story)
```

- [ ] **Step 4: Run both PDF tests, expect pass**

Run: `uv run --extra build pytest tests/test_build_assets.py::test_build_pdf_portrait_writes_valid_pdf tests/test_build_assets.py::test_build_pdf_landscape_writes_valid_pdf -v --no-cov`
Expected: 2 passed.

- [ ] **Step 5: Eyeball the rendered output**

```bash
uv run --extra build python -c "
from pathlib import Path
from scripts.build_assets import build_pdf
build_pdf(False, Path('/tmp/preview.pdf'))
"
open /tmp/preview.pdf
```

Visually confirm: Source Code Pro is used, two-column table with A-M
and N-Z, zebra-striped rows, centered title, footer with hyperlinks
and CC badge. If anything is wrong, fix and re-run. Don't proceed
until the portrait PDF looks right.

- [ ] **Step 6: Commit**

```bash
git add tests/test_build_assets.py scripts/build_assets/pdf.py
git commit -m "Implement PDF generator (portrait + landscape)"
```

---

## Task 4: TDD the DOCX generator

**Files:**
- Modify: `tests/test_build_assets.py`
- Modify: `scripts/build_assets/docx.py`

- [ ] **Step 1: Append the failing DOCX test**

Add to `tests/test_build_assets.py`:

```python
def test_build_docx_writes_valid_docx(tmp_path: Path) -> None:
    dest = tmp_path / "out.docx"
    build_docx(dest)
    assert dest.exists()
    with zipfile.ZipFile(dest) as zf:
        names = zf.namelist()
    assert "word/document.xml" in names
    assert "[Content_Types].xml" in names
```

- [ ] **Step 2: Run the test, verify fail**

Run: `uv run --extra build pytest tests/test_build_assets.py::test_build_docx_writes_valid_docx -v --no-cov`
Expected: FAIL with `NotImplementedError`.

- [ ] **Step 3: Implement `build_docx`**

Replace `scripts/build_assets/docx.py`:

```python
"""DOCX generator: matches the PDF's two-column layout where DOCX allows."""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor

from nato_phonetic.core import NATO_PHONETIC_ALPHABET

from . import config


def _set_cell_shading(cell, hex_color: str) -> None:
    """Apply a background fill to a docx table cell (no native API for this)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:color"), "auto")
    shading.set(qn("w:fill"), hex_color.lstrip("#"))
    tc_pr.append(shading)


def build_docx(dest: Path) -> None:
    """Generate a printable DOCX of the NATO phonetic alphabet."""
    doc = Document()

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(config.TITLE)
    run.font.name = "Source Code Pro"
    run.font.size = Pt(config.HEADER_FONT_SIZE)
    run.bold = False

    doc.add_paragraph()  # spacer

    letters = [chr(c) for c in range(ord("A"), ord("Z") + 1)]
    table = doc.add_table(rows=13, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    for i in range(13):
        left, right = letters[i], letters[i + 13]
        row = table.rows[i]
        cells = row.cells
        values = [left, NATO_PHONETIC_ALPHABET[left], right, NATO_PHONETIC_ALPHABET[right]]
        for col_idx, value in enumerate(values):
            cell = cells[col_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            cell.text = ""  # clear default empty paragraph
            paragraph = cell.paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = paragraph.add_run(value)
            run.font.name = "Source Code Pro"
            run.font.size = Pt(config.BODY_FONT_SIZE)
            if i % 2 == 1:
                _set_cell_shading(cell, config.ZEBRA_COLOR)

    doc.add_paragraph()  # spacer

    footer = doc.add_paragraph()
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer.add_run(f"{config.TITLE} {config.LICENSE_TEXT}")
    footer_run.font.name = "Source Code Pro"
    footer_run.font.size = Pt(10)
    footer_run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    doc.save(str(dest))
```

- [ ] **Step 4: Run the test, expect pass**

Run: `uv run --extra build pytest tests/test_build_assets.py::test_build_docx_writes_valid_docx -v --no-cov`
Expected: 1 passed.

- [ ] **Step 5: Visual sanity-check**

```bash
uv run --extra build python -c "
from pathlib import Path
from scripts.build_assets import build_docx
build_docx(Path('/tmp/preview.docx'))
"
open /tmp/preview.docx
```

Confirm: title at top, 13×4 table with the alphabet, zebra rows,
footer with attribution.

- [ ] **Step 6: Commit**

```bash
git add tests/test_build_assets.py scripts/build_assets/docx.py
git commit -m "Implement DOCX generator"
```

---

## Task 5: TDD the EPub generator

**Files:**
- Modify: `tests/test_build_assets.py`
- Modify: `scripts/build_assets/epub.py`

- [ ] **Step 1: Append the failing EPub test**

Add to `tests/test_build_assets.py`:

```python
def test_build_epub_writes_valid_epub(tmp_path: Path) -> None:
    dest = tmp_path / "out.epub"
    build_epub(dest)
    assert dest.exists()
    with zipfile.ZipFile(dest) as zf:
        names = zf.namelist()
    assert "mimetype" in names
    with zipfile.ZipFile(dest) as zf:
        assert zf.read("mimetype").strip() == b"application/epub+zip"
```

- [ ] **Step 2: Run the test, verify fail**

Run: `uv run --extra build pytest tests/test_build_assets.py::test_build_epub_writes_valid_epub -v --no-cov`
Expected: FAIL with `NotImplementedError`.

- [ ] **Step 3: Implement `build_epub`**

Replace `scripts/build_assets/epub.py`:

```python
"""EPub generator using ebooklib."""

from pathlib import Path

from ebooklib import epub

from nato_phonetic.core import NATO_PHONETIC_ALPHABET

from . import config


def _row_html(letter: str) -> str:
    return f"<tr><td><b>{letter}</b></td><td>{NATO_PHONETIC_ALPHABET[letter]}</td></tr>"


def build_epub(dest: Path) -> None:
    book = epub.EpubBook()
    book.set_identifier("trtmn.nato-phonetic-alphabet")
    book.set_title(config.TITLE)
    book.set_language("en")
    book.add_author("Matt Troutman")

    rows = "\n".join(_row_html(chr(c)) for c in range(ord("A"), ord("Z") + 1))
    body = f"""
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head><title>{config.TITLE}</title>
    <style>
        body {{ font-family: 'Source Code Pro', monospace; padding: 1em; }}
        h1 {{ text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin: 0 auto; }}
        td {{ border: 1px solid {config.GRID_COLOR}; padding: 0.4em 0.8em; text-align: center; }}
        tr:nth-child(even) td {{ background-color: {config.ZEBRA_COLOR}; }}
        footer {{ text-align: center; margin-top: 2em; font-size: 0.9em; }}
        footer a {{ color: {config.LINK_COLOR}; }}
    </style></head>
    <body>
        <h1>{config.TITLE}</h1>
        <table>
            {rows}
        </table>
        <footer>
            <a href="{config.PROJECT_URL}">{config.TITLE}</a> © 2024 by
            <a href="{config.AUTHOR_URL}">Matt Troutman</a> is licensed under
            <a href="{config.LICENSE_URL}">CC BY-SA 4.0</a>.
        </footer>
    </body></html>
    """
    chapter = epub.EpubHtml(title=config.TITLE, file_name="alphabet.xhtml", lang="en")
    chapter.content = body
    book.add_item(chapter)
    book.toc = (chapter,)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", chapter]

    epub.write_epub(str(dest), book)
```

- [ ] **Step 4: Run the test, expect pass**

Run: `uv run --extra build pytest tests/test_build_assets.py -v --no-cov`
Expected: 4 passed (all PDF, DOCX, and EPub tests).

- [ ] **Step 5: Commit**

```bash
git add tests/test_build_assets.py scripts/build_assets/epub.py
git commit -m "Implement EPub generator"
```

---

## Task 6: Wire `__main__.py` entry point

**Files:**
- Modify: `scripts/build_assets/__main__.py`

- [ ] **Step 1: Replace the stub `__main__.py`**

```python
"""CLI entry: `python -m scripts.build_assets [--out DIR]`."""

import argparse
from pathlib import Path

from . import build_docx, build_epub, build_pdf, config


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate printable NATO alphabet assets.")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path.cwd(),
        help="Destination directory (default: current working directory).",
    )
    args = parser.parse_args()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    targets = [
        (out / config.PDF_PORTRAIT_NAME, lambda d: build_pdf(False, d)),
        (out / config.PDF_LANDSCAPE_NAME, lambda d: build_pdf(True, d)),
        (out / config.DOCX_NAME, build_docx),
        (out / config.EPUB_NAME, build_epub),
    ]
    for dest, builder in targets:
        builder(dest)
        print(f"wrote {dest.relative_to(out.parent) if out.parent in dest.parents else dest}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke-test it**

```bash
rm -rf /tmp/asset-build-test
uv run --extra build python -m scripts.build_assets --out /tmp/asset-build-test
ls -la /tmp/asset-build-test/
```

Expected: four files printed by the script, all present in
`/tmp/asset-build-test`, all non-empty.

- [ ] **Step 3: Commit**

```bash
git add scripts/build_assets/__main__.py
git commit -m "Wire __main__ entry point for asset generation"
```

---

## Task 7: Makefile target

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: Add the `build-assets` target**

Append to `Makefile` (before the existing `hatch-build` target on line
59 — keeping `.PHONY` tidy):

Change the `.PHONY` line at top of Makefile:

```make
.PHONY: help install install-dev test format lint clean build hatch-build hatch-clean bump-patch bump-minor bump-major build-assets
```

Add this target near the bottom, after the version-bump targets:

```make
build-assets: ## Regenerate printable assets (PDF, DOCX, EPub) in repo root
	uv sync --extra build
	uv run python -m scripts.build_assets
```

- [ ] **Step 2: Verify it works**

```bash
make build-assets
ls -la "Nato Phonetic Alphabet - PDF.pdf" "Nato Phonetic Alphabet (Landscape) - PDF.pdf" "Nato Phonetic Alphabet - EPub.epub" "Nato Phonetic Alphabet - Microsoft Word.docx"
```

Expected: all four files exist with recent timestamps.

- [ ] **Step 3: Commit the Makefile only (not the regenerated assets — that's Task 11)**

```bash
git add Makefile
git commit -m "Add make build-assets target"
```

Leave the regenerated asset files in the working tree — they'll be
committed in Task 11 alongside the deletion of the dropped formats.

---

## Task 8: Update CLI catalog (drop pages/odt slugs)

**Files:**
- Modify: `src/nato_phonetic/assets.py:39-46`
- Modify: `tests/test_assets.py`

- [ ] **Step 1: Update `ASSETS` in `src/nato_phonetic/assets.py`**

Replace the `ASSETS` block (currently lines 39-49):

```python
ASSETS: dict[str, Asset] = {
    a.slug: a
    for a in (
        Asset("pdf", "Nato Phonetic Alphabet - PDF.pdf", "Printable PDF (portrait)"),
        Asset("pdf-landscape", "Nato Phonetic Alphabet (Landscape) - PDF.pdf", "Printable PDF (landscape)"),
        Asset("epub", "Nato Phonetic Alphabet - EPub.epub", "EPub for e-readers"),
        Asset("docx", "Nato Phonetic Alphabet - Microsoft Word.docx", "Microsoft Word"),
    )
}
```

- [ ] **Step 2: Update `tests/test_assets.py`**

Add a new test that locks the expected slug set, and update any
existing test that assumed the dropped slugs. Append:

```python
def test_catalog_contains_exactly_four_slugs():
    assert set(assets.ASSETS) == {"pdf", "pdf-landscape", "epub", "docx"}
```

- [ ] **Step 3: Run all CLI-side tests**

Run: `uv run pytest tests/test_assets.py tests/test_core.py -v --no-cov`
Expected: all tests pass (no test currently asserts the presence of
`pages`/`odt`, but verify).

- [ ] **Step 4: Smoke-test the CLI**

```bash
uv run phonetic download --list 2>&1 | tail -20
```

Expected: table shows only `pdf`, `pdf-landscape`, `epub`, `docx`. No
`pages`/`pages-landscape`/`odt`.

- [ ] **Step 5: Commit**

```bash
git add src/nato_phonetic/assets.py tests/test_assets.py
git commit -m "Drop pages/odt slugs from CLI asset catalog"
```

---

## Task 9: Pre-push hook

**Files:**
- Create: `.githooks/pre-push`

- [ ] **Step 1: Write the hook script**

Create `.githooks/pre-push`:

```bash
#!/usr/bin/env bash
# Pre-push hook: regenerate printable assets and fail if they're stale.
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
    echo "pre-push: uv not on PATH; skipping asset freshness check." >&2
    exit 0
fi

echo "pre-push: regenerating printable assets..."
uv sync --extra build >/dev/null
uv run python -m scripts.build_assets >/dev/null

ASSETS=(
    "Nato Phonetic Alphabet - PDF.pdf"
    "Nato Phonetic Alphabet (Landscape) - PDF.pdf"
    "Nato Phonetic Alphabet - Microsoft Word.docx"
    "Nato Phonetic Alphabet - EPub.epub"
)

if ! git diff --quiet -- "${ASSETS[@]}"; then
    echo
    echo "pre-push: generated assets are stale. Inspect with:" >&2
    echo "  git diff -- \"Nato Phonetic Alphabet\"*" >&2
    echo "Stage the changes, commit, and retry the push." >&2
    exit 1
fi

echo "pre-push: assets fresh, proceeding."
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x .githooks/pre-push
ls -la .githooks/pre-push
```

Expected: `-rwxr-xr-x` permissions.

- [ ] **Step 3: Enable in this clone**

```bash
git config core.hooksPath .githooks
git config --get core.hooksPath
```

Expected output: `.githooks`.

- [ ] **Step 4: Commit**

```bash
git add .githooks/pre-push
git commit -m "Add pre-push hook to regenerate + verify printable assets"
```

---

## Task 10: CI freshness check

**Files:**
- Modify: `.github/workflows/publish.yml:11-23` (the `build` job)

- [ ] **Step 1: Read the current `build` job**

```bash
sed -n '11,25p' .github/workflows/publish.yml
```

Expected: shows the current four-step build job (checkout, setup-uv,
uv build, upload-artifact).

- [ ] **Step 2: Insert the freshness-check steps**

Edit `.github/workflows/publish.yml`. Replace the `build` job body:

```yaml
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --extra build
      - name: Regenerate printable assets
        run: uv run python -m scripts.build_assets
      - name: Verify committed assets match generator output
        run: |
          git diff --exit-status -- \
            "Nato Phonetic Alphabet - PDF.pdf" \
            "Nato Phonetic Alphabet (Landscape) - PDF.pdf" \
            "Nato Phonetic Alphabet - Microsoft Word.docx" \
            "Nato Phonetic Alphabet - EPub.epub"
      - run: uv build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/publish.yml
git commit -m "CI: verify committed printable assets match generator output"
```

---

## Task 11: Delete obsolete files and commit regenerated assets

**Files:**
- Delete: `Nato Phonetic Alphabet.pages`, `Nato Phonetic Alphabet Landscape.pages`, `Nato Phonetic Alphabet - Open Doc Format.odt`
- Replace: the four kept asset files (in working tree from Task 7, now committed)

- [ ] **Step 1: Regenerate to make sure working tree is current**

```bash
make build-assets
```

- [ ] **Step 2: Delete the obsolete formats**

```bash
git rm "Nato Phonetic Alphabet.pages" \
       "Nato Phonetic Alphabet Landscape.pages" \
       "Nato Phonetic Alphabet - Open Doc Format.odt"
```

- [ ] **Step 3: Stage the regenerated assets and review**

```bash
git add "Nato Phonetic Alphabet - PDF.pdf" \
        "Nato Phonetic Alphabet (Landscape) - PDF.pdf" \
        "Nato Phonetic Alphabet - Microsoft Word.docx" \
        "Nato Phonetic Alphabet - EPub.epub"
git status --short
```

Expected: deletions of the three obsolete files + modifications of the
four kept files.

- [ ] **Step 4: Eyeball the regenerated PDFs vs old ones for surprises**

```bash
open "Nato Phonetic Alphabet - PDF.pdf"
open "Nato Phonetic Alphabet (Landscape) - PDF.pdf"
```

Confirm both look right.

- [ ] **Step 5: Commit**

```bash
git commit -m "Replace static assets with generator output; drop pages/odt"
```

---

## Task 12: README updates

**Files:**
- Modify: `README.md` (slug list around line 92 + new Development subsection)

- [ ] **Step 1: Update the slug list**

Find the line in `README.md` that ends with `Apple Pages (portrait)`
and the surrounding asset bullet/list mentioning slugs. Update the
"Available slugs" line near the bottom of the "Printable assets"
section so it reads:

```
Available slugs: `pdf`, `pdf-landscape`, `epub`, `docx`.
```

(If the old line listed `pages` and `pages-landscape`, remove them.)

Also update the `Available commands` list in the same file — the
download line should say:

```
- `download [slug]` - Download a printable asset to `~/Downloads` (use `--list` to see slugs, `-o` for a custom directory, `--force` to re-download)
```

(no change needed if it already reads this way).

- [ ] **Step 2: Add a "Regenerating printable assets" Development subsection**

Insert after the existing `#### Running Tests` subsection in the
Development section:

```markdown
#### Regenerating printable assets

The printable PDFs, DOCX, and EPub files in the repo root are generated
from `scripts/build_assets/`. They must stay in sync with the
generator — CI fails the build otherwise.

```bash
make build-assets
```

**Recommended:** enable the pre-push hook so a stale-asset push is
caught locally before CI rejects it:

```bash
git config core.hooksPath .githooks
```

**Alternative:** integrate with the `pre-commit` framework by adding to
your `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: build-assets
      name: regenerate printable assets
      entry: make build-assets
      language: system
      pass_filenames: false
      stages: [pre-push]
```

If you only edit the alphabet data or the layout config in
`scripts/build_assets/config.py`, run `make build-assets` before
committing.
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "README: document asset regeneration and hook setup"
```

---

## Task 13: Bump to v0.4.1 and release

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Bump the version**

```bash
uv version 0.4.1
```

Expected: pyproject.toml shows `version = "0.4.1"`.

- [ ] **Step 2: Confirm full test suite still passes**

```bash
uv run --extra build pytest --no-cov
```

Expected: all tests pass (existing + the 4 new ones in
test_build_assets.py).

- [ ] **Step 3: Commit the bump**

```bash
git add pyproject.toml
git commit -m "Bump to v0.4.1"
```

- [ ] **Step 4: Merge the branch into main**

```bash
git switch main
git pull origin main
git merge --no-ff release/v0.4.1 -m "Merge release/v0.4.1: dynamic asset generation"
```

- [ ] **Step 5: Tag and push to both remotes**

```bash
git tag v0.4.1
git push origin main
git push origin v0.4.1
# Codeberg mirror pushes to github, but push direct tag for redundancy:
git push github v0.4.1 || true
```

- [ ] **Step 6: Watch the workflow**

```bash
sleep 6
rid=$(gh run list -R trtmn/nato-phonetic-alphabet --event push --limit 1 --json databaseId | jq -r '.[0].databaseId')
gh run watch "$rid" -R trtmn/nato-phonetic-alphabet --exit-status --interval 10
gh run view "$rid" -R trtmn/nato-phonetic-alphabet --json conclusion,jobs | jq -r '"conclusion=\(.conclusion)", (.jobs[] | "  \(.name): \(.conclusion)")'
```

Expected: all three jobs (build, publish-pypi, release) succeed.

- [ ] **Step 7: Verify on PyPI**

```bash
curl -s https://pypi.org/pypi/phonetic-nato/json | jq -r '"latest=\(.info.version)"'
uvx phonetic-nato@latest --version
```

Expected: `latest=0.4.1`, CLI reports `phonetic v0.4.1`.

- [ ] **Step 8: Verify the new `phonetic download --list` is correct**

```bash
uvx phonetic-nato@latest download --list
```

Expected: table shows exactly `pdf`, `pdf-landscape`, `epub`, `docx`.

---

## Self-review

**Spec coverage:**
- §1 Source of truth → Task 4 (PDF), Task 5 (DOCX), Task 6 (EPub) all
  import `NATO_PHONETIC_ALPHABET`. ✅
- §2 Generators (file layout) → Task 1 scaffolds, Tasks 4-6 fill in,
  Task 7 wires entry. ✅
- §3 Output location (repo root) → Task 7 `__main__` defaults to cwd;
  Task 11 commits the regenerated files at repo root. ✅
- §4 Build deps & dev UX → Task 1 adds extras, Task 8 adds Makefile
  target. (NOTE: in the plan above this is Task 7, renamed.) Wait —
  let me re-check task numbering.

Looking at the plan: Task 7 is the Makefile target. Task 8 is the CLI
catalog update. The internal references inside Task 8 say `Task 11`
for the asset commit; that's correct (deletion + regen is Task 11).
✅

- §5 Freshness enforcement → Task 9 (hook) + Task 10 (CI verify). ✅
- §6 CLI catalog → Task 8. ✅
- §7 Cleanup → Task 11. ✅
- §8 Tests → Tasks 3/4/5 add `tests/test_build_assets.py`. ✅
- §9 Documentation → Task 12. ✅

**Placeholder scan:** no "TBD" / "TODO" / "implement later". Every
code block is complete; every command has expected output.

**Type consistency:** `build_pdf(landscape: bool, dest: Path)`,
`build_docx(dest: Path)`, `build_epub(dest: Path)` consistent across
scaffold, tests, implementations, and `__main__.py`. Config names
(`PDF_PORTRAIT_NAME`, `PDF_LANDSCAPE_NAME`, `DOCX_NAME`, `EPUB_NAME`)
consistent between `config.py` definition and `__main__.py` usage.

**Ambiguity:** none I can spot.
