# nato-phonetic-alphabet
Printable / Remixable Nato Phonetic Alphabet page with a beautiful command-line interface.
![Social Image](https://github.com/trtmn/nato-phonetic-alphabet/raw/main/Social%20Image.png)

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

#### Option 2: Homebrew (macOS)

```bash
# Install from local formula (development)
brew install Formula/phonetic-nato.rb

# Or install from tap (when published)
brew tap trtmn/phonetic-nato
brew install phonetic-nato
```

#### Option 3: pip

```bash
pip install phonetic-nato
```

#### From source (development)

```bash
git clone https://github.com/trtmn/nato-phonetic-alphabet.git
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

### Development

#### Project Structure
```
nato-phonetic-alphabet/
├── .venv/                 # Virtual environment
├── src/                   # Source code
│   └── nato_phonetic/     # Main package
├── tests/                 # Test files
├── pyproject.toml         # Project configuration & dependencies
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

