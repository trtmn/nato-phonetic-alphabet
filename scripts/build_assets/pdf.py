"""PDF generator: portrait or landscape, two-column zebra-striped table."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER, landscape as _landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
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
        rows.append(
            (left, NATO_PHONETIC_ALPHABET[left], right, NATO_PHONETIC_ALPHABET[right])
        )
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
        alignment=1,
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

    letter_style = ParagraphStyle(
        "LetterCell",
        parent=styles["Normal"],
        fontName=config.HEADER_FONT_NAME,
        fontSize=config.BODY_FONT_SIZE,
        alignment=0,  # left
        leftIndent=4,
    )
    word_style = ParagraphStyle(
        "WordCell",
        parent=styles["Normal"],
        fontName=config.HEADER_FONT_NAME,
        fontSize=config.BODY_FONT_SIZE,
        alignment=1,  # center
    )

    table_data = _alphabet_pairs()
    table_rows = [
        [
            Paragraph(left, letter_style),
            Paragraph(left_word, word_style),
            Paragraph(right, letter_style),
            Paragraph(right_word, word_style),
        ]
        for left, left_word, right, right_word in table_data
    ]

    col_widths = [0.6 * inch, 2.4 * inch, 0.6 * inch, 2.4 * inch]
    row_height = config.ROW_HEIGHT
    if landscape:
        col_widths = [0.7 * inch, 3.5 * inch, 0.7 * inch, 3.5 * inch]
        row_height = config.ROW_HEIGHT - 6

    table = Table(table_rows, colWidths=col_widths, rowHeights=row_height)
    style_cmds: list[tuple] = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(config.GRID_COLOR)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for row_idx in range(len(table_rows)):
        if row_idx % 2 == 1:
            style_cmds.append(
                (
                    "BACKGROUND",
                    (0, row_idx),
                    (-1, row_idx),
                    colors.HexColor(config.ZEBRA_COLOR),
                )
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
    doc.build(story, canvasmaker=_invariant_canvas)


def _invariant_canvas(filename, *args, **kwargs):
    kwargs["invariant"] = 1
    return Canvas(filename, *args, **kwargs)
