"""Shared layout and content constants for the asset generators."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
FONT_PATH = PROJECT_ROOT / "fonts" / "SourceCodePro-Regular.ttf"
CC_ICON_PATH = PROJECT_ROOT / "assets" / "cc-by-sa.png"

TITLE = "Nato Phonetic Alphabet"

HEADER_FONT_NAME = "SourceCodePro"
HEADER_FONT_SIZE = 32
BODY_FONT_SIZE = 14
ROW_HEIGHT = 28
GRID_COLOR = "#cccccc"
ZEBRA_COLOR = "#f4f4f4"
LINK_COLOR = "#1f88c5"

LICENSE_TEXT = "© 2024 by Matt Troutman is licensed under CC BY-SA 4.0"
PROJECT_URL = "https://trtmn.io/nato-phonetic-alphabet"
AUTHOR_URL = "https://trtmn.io"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"

PDF_PORTRAIT_NAME = "Nato Phonetic Alphabet - PDF.pdf"
PDF_LANDSCAPE_NAME = "Nato Phonetic Alphabet (Landscape) - PDF.pdf"
DOCX_NAME = "Nato Phonetic Alphabet - Microsoft Word.docx"
EPUB_NAME = "Nato Phonetic Alphabet - EPub.epub"
