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


def test_build_docx_writes_valid_docx(tmp_path: Path) -> None:
    dest = tmp_path / "out.docx"
    build_docx(dest)
    assert dest.exists()
    with zipfile.ZipFile(dest) as zf:
        names = zf.namelist()
    assert "word/document.xml" in names
    assert "[Content_Types].xml" in names
