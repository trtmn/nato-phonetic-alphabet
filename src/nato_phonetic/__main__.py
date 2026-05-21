#!/usr/bin/env python3
"""Main entry point for the phonetic CLI."""

import sys
from .cli import spell_word_command, main as cli_main

def main() -> None:
    """Main entry point that handles direct word input."""
    argv = sys.argv[1:]

    if not argv:
        cli_main()
        return

    if argv[0].startswith('-') or argv[0] in cli_main.commands:
        cli_main()
        return

    # Otherwise, treat as a word to spell
    spell_word_command(argv[0])

if __name__ == "__main__":
    main() 