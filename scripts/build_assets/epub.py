"""EPub generator using ebooklib."""

import re
import zipfile
from pathlib import Path

from ebooklib import epub

from nato_phonetic.core import NATO_PHONETIC_ALPHABET

from . import config
from ._zip_util import normalize_zip

_FIXED_MODIFIED = b"2024-01-01T00:00:00Z"
_MODIFIED_RE = re.compile(
    rb'(<meta property="dcterms:modified">)[^<]+(</meta>)'
)


def _row_html(letter: str) -> str:
    return f"<tr><td><b>{letter}</b></td><td>{NATO_PHONETIC_ALPHABET[letter]}</td></tr>"


def build_epub(dest: Path) -> None:
    book = epub.EpubBook()
    book.set_identifier("trtmn.nato-phonetic-alphabet")
    book.set_title(config.TITLE)
    book.set_language("en")
    book.add_author("Matt Troutman")
    book.add_metadata(None, "meta", "2024-01-01T00:00:00Z", {"property": "dcterms:modified"})

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
    _force_fixed_modified(dest)
    normalize_zip(dest)


def _force_fixed_modified(epub_path: Path) -> None:
    """Override the dcterms:modified value ebooklib injects with our fixed epoch."""
    with zipfile.ZipFile(epub_path, "r") as src:
        members = [
            (info, src.read(info.filename))
            for info in src.infolist()
        ]
    rewritten = []
    for info, data in members:
        if info.filename.endswith(".opf"):
            data = _MODIFIED_RE.sub(
                rb"\g<1>" + _FIXED_MODIFIED + rb"\g<2>",
                data,
            )
        rewritten.append((info, data))
    with zipfile.ZipFile(epub_path, "w") as dst:
        for info, data in rewritten:
            dst.writestr(info, data)
