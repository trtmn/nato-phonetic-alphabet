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
