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
        print(f"wrote {dest}")


if __name__ == "__main__":
    main()
