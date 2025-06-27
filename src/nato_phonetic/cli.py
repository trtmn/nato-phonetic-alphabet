"""Command-line interface for the NATO phonetic alphabet."""

import sys
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED
from rich.panel import Panel
from rich.prompt import Prompt

from .core import lookup_letter, spell_word, get_full_alphabet

console = Console()


@click.group(invoke_without_command=True)
@click.argument("word", required=False)
@click.version_option(version="0.1.0", prog_name="nato-phonetic")
@click.pass_context
def main(ctx: click.Context, word: Optional[str]) -> None:
    """NATO Phonetic Alphabet CLI - Beautiful terminal interface.
    
    If a word is provided without a command, it will be spelled out using 
    the NATO phonetic alphabet.
    
    Examples:
        nato-phonetic "HELLO"     # Spell out HELLO
        nato-phonetic spell "HELLO"  # Same as above
        nato-phonetic lookup A    # Look up letter A
        nato-phonetic list        # Show full alphabet
    """
    if ctx.invoked_subcommand is None:
        if word:
            # If no subcommand was invoked but a word was provided, spell it
            spell_word_command(word)
        else:
            # Show help if no arguments provided
            click.echo(ctx.get_help())


@main.command()
@click.argument("letter", type=str)
def lookup(letter: str) -> None:
    """Look up the NATO phonetic equivalent for a single letter."""
    if len(letter) != 1:
        console.print(
            f"[red]Error:[/red] Please provide a single letter, got '{letter}'"
        )
        sys.exit(1)

    phonetic = lookup_letter(letter)
    if phonetic:
        console.print(f"[green]{letter.upper()} - {phonetic}[/green]")
    else:
        console.print(
            f"[red]Error:[/red] No NATO phonetic equivalent found for '{letter}'"
        )
        sys.exit(1)


@main.command()
@click.argument("word", type=str)
def spell(word: str) -> None:
    """Spell out a word using the NATO phonetic alphabet."""
    if not word:
        console.print("[red]Error:[/red] Please provide a word to spell")
        sys.exit(1)

    spell_word_command(word)


@main.command()
def interactive() -> None:
    """Enter interactive mode for spelling words."""
    console.print(
        Panel.fit(
            "[bold blue]NATO Phonetic Alphabet - Interactive Mode[/bold blue]\n"
            "Enter words to spell them out. Type 'quit' or 'exit' to leave.",
            border_style="blue",
        )
    )

    while True:
        try:
            word = Prompt.ask("\n[cyan]Enter a word to spell[/cyan]")

            if word.lower() in ["quit", "exit", "q"]:
                console.print("[yellow]Goodbye![/yellow]")
                break

            if not word.strip():
                continue

            spell_word_command(word)

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break


@main.command()
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def print_alphabet(output: Optional[str]) -> None:
    """Display the complete NATO phonetic alphabet."""
    alphabet = get_full_alphabet()

    # Create a table for beautiful output with rounded corners
    table = Table(
        title="NATO Phonetic Alphabet", 
        box=ROUNDED
    )
    table.add_column("Letter", style="cyan", justify="center")
    table.add_column("Phonetic", style="green", justify="left")

    # Sort alphabetically
    for letter in sorted(alphabet.keys()):
        table.add_row(letter, alphabet[letter])

    if output:
        # Save to file
        with open(output, "w") as f:
            f.write("NATO Phonetic Alphabet\n")
            f.write("=" * 25 + "\n\n")
            for letter in sorted(alphabet.keys()):
                f.write(f"{letter} - {alphabet[letter]}\n")
        console.print(f"[green]Alphabet saved to {output}[/green]")
    else:
        console.print(table)


@main.command()
def list() -> None:
    """Display the complete NATO phonetic alphabet (alias for print)."""
    print_alphabet_command()


# Alias functions for internal use
def spell_word_command(word: str) -> None:
    """Internal function to spell a word (used by interactive mode)."""
    result = spell_word(word)

    # Create a table for beautiful output with rounded corners
    table = Table(
        title=f"NATO Phonetic Spelling: {word.upper()}", 
        box=ROUNDED
    )
    table.add_column("Letter", style="cyan", justify="center")
    table.add_column("Phonetic", style="green", justify="left")

    for letter, phonetic in result:
        if letter.isspace():
            table.add_row(letter, "[dim]Space[/dim]")
        elif not letter.isalnum():
            table.add_row(letter, "[dim]Special Character[/dim]")
        else:
            table.add_row(letter, phonetic)

    console.print(table)


def print_alphabet_command() -> None:
    """Internal function to print the alphabet (used by list command)."""
    alphabet = get_full_alphabet()

    # Create a table for beautiful output with rounded corners
    table = Table(
        title="NATO Phonetic Alphabet", 
        box=ROUNDED
    )
    table.add_column("Letter", style="cyan", justify="center")
    table.add_column("Phonetic", style="green", justify="left")

    # Sort alphabetically
    for letter in sorted(alphabet.keys()):
        table.add_row(letter, alphabet[letter])

    console.print(table)


if __name__ == "__main__":
    main()
