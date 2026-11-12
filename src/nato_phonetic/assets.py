"""Downloadable assets hosted alongside the source on Codeberg."""

from __future__ import annotations

import os
import platform
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.table import Table
from rich.box import ROUNDED


RAW_BASE = "https://codeberg.org/trtmn/nato-phonetic-alphabet/raw/branch/main/"
DEFAULT_SLUG = "pdf"


@dataclass(frozen=True)
class Asset:
    slug: str
    filename: str
    description: str


ASSETS: dict[str, Asset] = {
    a.slug: a
    for a in (
        Asset("pdf", "Nato Phonetic Alphabet - PDF.pdf", "Printable PDF (portrait)"),
        Asset("pdf-landscape", "Nato Phonetic Alphabet (Landscape) - PDF.pdf", "Printable PDF (landscape)"),
        Asset("epub", "Nato Phonetic Alphabet - EPub.epub", "EPub for e-readers"),
        Asset("docx", "Nato Phonetic Alphabet - Microsoft Word.docx", "Microsoft Word"),
    )
}


class AssetError(Exception):
    """Raised for asset-related errors (unknown slug, download failure, etc.)."""


def default_downloads_dir() -> Path:
    """Return the user's Downloads directory — works on macOS, Linux, and Windows."""
    return Path.home() / "Downloads"


def asset_url(slug: str) -> str:
    asset = _resolve(slug)
    return RAW_BASE + urllib.parse.quote(asset.filename)


def list_assets(console: Console) -> None:
    table = Table(title="Available Assets", box=ROUNDED)
    table.add_column("Slug", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Filename", style="dim")
    for asset in ASSETS.values():
        table.add_row(asset.slug, asset.description, asset.filename)
    console.print(table)


def download_asset(
    slug: str,
    dest_dir: Optional[Path] = None,
    *,
    force: bool = False,
    console: Optional[Console] = None,
) -> Path:
    """Download an asset to ``dest_dir`` (defaults to ~/Downloads). Returns the file path.

    Reuses an existing file at the destination unless ``force`` is True.
    """
    asset = _resolve(slug)
    console = console or Console()
    dest_dir = (dest_dir or default_downloads_dir()).expanduser()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / asset.filename

    if dest.exists() and not force:
        console.print(f"[green]Reusing[/green] [dim]{dest}[/dim] (pass [cyan]--force[/cyan] to re-download)")
        return dest

    url = asset_url(slug)
    try:
        with urllib.request.urlopen(url) as response:  # noqa: S310 - controlled URL
            total = int(response.headers.get("Content-Length") or 0) or None
            with Progress(
                TextColumn("[cyan]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
                console=console,
            ) as progress:
                task_id = progress.add_task(asset.filename, total=total)
                with dest.open("wb") as fh:
                    while chunk := response.read(64 * 1024):
                        fh.write(chunk)
                        progress.update(task_id, advance=len(chunk))
    except urllib.error.URLError as exc:
        if dest.exists():
            dest.unlink(missing_ok=True)
        raise AssetError(f"Failed to download {asset.filename}: {exc}") from exc

    console.print(f"[green]Saved[/green] [dim]{dest}[/dim]")
    return dest


def open_asset(
    slug: str,
    dest_dir: Optional[Path] = None,
    *,
    force: bool = False,
    console: Optional[Console] = None,
) -> Path:
    """Download (or reuse) the asset, then open it with the OS default handler."""
    path = download_asset(slug, dest_dir, force=force, console=console)
    open_file(path)
    return path


def open_file(path: Path) -> None:
    """Open ``path`` with the operating-system default handler."""
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["open", str(path)], check=False)
    elif system == "Windows":
        os.startfile(str(path))  # type: ignore[attr-defined] # noqa: SCS108 - Windows only
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


def _resolve(slug: str) -> Asset:
    asset = ASSETS.get(slug)
    if asset is None:
        valid = ", ".join(ASSETS)
        raise AssetError(f"Unknown asset slug: {slug!r}. Valid slugs: {valid}")
    return asset
