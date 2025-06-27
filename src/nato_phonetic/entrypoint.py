import sys
from .cli import main, spell_word_command

# List of known subcommands
SUBCOMMANDS = {"lookup", "spell", "interactive", "print-alphabet", "list", "--help", "-h", "--version", "-V"}

def entrypoint():
    argv = sys.argv[1:]
    if argv and not argv[0].startswith('-') and argv[0] not in SUBCOMMANDS:
        # If the first argument is not a subcommand or option, treat it as a word
        spell_word_command(argv[0])
        sys.exit(0)
    else:
        # Otherwise, invoke the CLI as normal
        main(args=argv)

if __name__ == "__main__":
    entrypoint() 