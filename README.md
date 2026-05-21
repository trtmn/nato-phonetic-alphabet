# nato-phonetic-alphabet
Printable / Remixable Nato Phonetic Alphabet page with a beautiful command-line interface.
![Social Image](https://codeberg.org/trtmn/nato-phonetic-alphabet/raw/branch/main/Social%20Image.png)

Project page is hosted at https://trtmn.io/nato-phonetic-alphabet

## Command Line Interface

A beautiful and easy-to-use CLI built with Python 3.11, Click, and Rich for displaying and working with the NATO phonetic alphabet.

### Features

- 🎨 **Beautiful Output**: Rich terminal formatting with colors and styling
- 🔍 **Search & Lookup**: Find phonetic equivalents for letters and words
- 📝 **Interactive Mode**: Spell out words interactively
- 🖨️ **Printable Output**: Generate formatted output for printing
- 🚀 **Fast & Lightweight**: Built with modern Python libraries

### Installation

#### Option 1: uv / uvx (Recommended)

Try it once without installing:

```bash
uvx phonetic-nato
```

Install it as a persistent CLI:

```bash
uv tool install phonetic-nato
```

Don't have `uv` yet? See the [uv install guide](https://docs.astral.sh/uv/getting-started/installation/) (one-line installer for macOS, Linux, and Windows).

#### Option 2: pip

```bash
pip install phonetic-nato
```

#### From source (development)

```bash
git clone https://codeberg.org/trtmn/nato-phonetic-alphabet.git
cd nato-phonetic-alphabet
uv sync --dev
uv run phonetic --help
```

### Usage

#### Basic Commands

**Display the full NATO phonetic alphabet:**
```bash
phonetic
```

**Look up a specific letter:**
```bash
phonetic lookup A
```

**Spell out a word:**
```bash
phonetic spell "HELLO"
```

**Interactive spelling mode:**
```bash
phonetic interactive
```

**Generate printable output:**
```bash
phonetic print --output nato-alphabet.txt
```

#### Command Options

```bash
phonetic --help
```

Available commands:
- `lookup <letter>` - Find phonetic equivalent for a single letter
- `spell <word>` - Spell out a word using NATO phonetic alphabet
- `interactive` - Enter interactive mode for spelling words
- `print` - Generate formatted output for printing
- `list` - Display the complete NATO phonetic alphabet
- `open [slug]` - Download (or reuse) a printable asset and open it with the OS default handler. Default slug is the portrait PDF.
- `download [slug]` - Download a printable asset to `~/Downloads` (use `--list` to see slugs, `-o` for a custom directory, `--force` to re-download)

#### Examples

```bash
# Look up a letter
phonetic lookup X
# Output: X - X-ray

# Spell a word
phonetic spell "WORLD"
# Output: W - Whiskey, O - Oscar, R - Romeo, L - Lima, D - Delta

# Interactive mode
phonetic interactive
# Enter words to spell them out interactively
```

#### Printable assets

The project ships printable PDFs, an EPub, Word/ODT documents, and Apple Pages
sources alongside the source on Codeberg. The CLI can grab any of them
straight to your Downloads folder.

```bash
# Open the portrait PDF (downloads to ~/Downloads, then opens in your default viewer)
phonetic open

# Other printable variants
phonetic open pdf-landscape
phonetic open epub

# Download without opening
phonetic download docx
phonetic download odt -o ~/Documents/nato/

# See every available asset
phonetic download --list

# Re-download a stale copy
phonetic open --force
```

Available slugs: `pdf`, `pdf-landscape`, `epub`, `docx`, `odt`, `pages`, `pages-landscape`.

### Development

#### Project Structure
```
nato-phonetic-alphabet/
├── .venv/                 # Virtual environment
├── src/                   # Source code
│   └── nato_phonetic/     # Main package
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

#### Running Tests
```bash
pytest tests/
```

#### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Dependencies

- **Click**: Command-line interface creation kit
- **Rich**: Rich text and beautiful formatting in the terminal
- **Python 3.11+**: Modern Python features and performance

### License

This project is open source. See the LICENSE file for details.

