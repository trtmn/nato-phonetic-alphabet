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

_CSS = f"""
@font-face {{
    font-family: 'Source Code Pro';
    src: url('fonts/SourceCodePro-Regular.ttf') format('truetype');
}}
body {{
    font-family: 'Source Code Pro', monospace;
    padding: 1em;
    color: #111;
}}
h1 {{ text-align: center; font-size: 1.8em; margin-bottom: 1em; }}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0 auto 1.5em auto;
}}
td {{
    border: 1px solid {config.GRID_COLOR};
    padding: 0.4em 0.8em;
    text-align: center;
}}
td.letter {{ text-align: left; width: 2em; padding-left: 0.8em; }}
tr:nth-child(even) td {{ background-color: {config.ZEBRA_COLOR}; }}
footer {{
    text-align: center;
    margin-top: 2em;
    font-size: 0.9em;
}}
footer a {{ color: {config.LINK_COLOR}; }}
footer .badge {{
    display: block;
    margin: 1em auto 0 auto;
}}
"""


def _row_html(letter: str) -> str:
    return (
        f'<tr><td class="letter"><b>{letter}</b></td>'
        f"<td>{NATO_PHONETIC_ALPHABET[letter]}</td></tr>"
    )


def build_epub(dest: Path) -> None:
    book = epub.EpubBook()
    book.set_identifier("trtmn.nato-phonetic-alphabet")
    book.set_title(config.TITLE)
    book.set_language("en")
    book.add_author("Matt Troutman")
    book.add_metadata(None, "meta", "2024-01-01T00:00:00Z", {"property": "dcterms:modified"})

    font_bytes = config.FONT_PATH.read_bytes()
    book.add_item(
        epub.EpubItem(
            uid="font_scp",
            file_name="fonts/SourceCodePro-Regular.ttf",
            media_type="font/ttf",
            content=font_bytes,
        )
    )

    icon_bytes = config.CC_ICON_PATH.read_bytes()
    book.add_item(
        epub.EpubItem(
            uid="cc_icon",
            file_name="images/cc-by-sa.png",
            media_type="image/png",
            content=icon_bytes,
        )
    )

    style = epub.EpubItem(
        uid="style",
        file_name="css/style.css",
        media_type="text/css",
        content=_CSS,
    )
    book.add_item(style)

    rows = "\n".join(_row_html(chr(c)) for c in range(ord("A"), ord("Z") + 1))
    body = f"""<h1>{config.TITLE}</h1>
<table>
{rows}
</table>
<footer>
    <a href="{config.PROJECT_URL}">{config.TITLE}</a> © 2024 by
    <a href="{config.AUTHOR_URL}">Matt Troutman</a> is licensed under
    <a href="{config.LICENSE_URL}">CC BY-SA 4.0</a>.
    <img class="badge" src="images/cc-by-sa.png" alt="CC BY-SA 4.0" width="88" height="31" />
</footer>
"""
    chapter = epub.EpubHtml(title=config.TITLE, file_name="alphabet.xhtml", lang="en")
    chapter.content = body
    chapter.add_link(href="css/style.css", rel="stylesheet", type="text/css")
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
