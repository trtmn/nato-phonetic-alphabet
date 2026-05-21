"""NATO Phonetic Alphabet CLI package."""

from importlib.metadata import PackageNotFoundError, version as _pkg_version

try:
    __version__ = _pkg_version("phonetic-nato")
except PackageNotFoundError:
    __version__ = "0.0.0+local"

__author__ = "trtmn"
__email__ = "trtmn@trtmn.io"

from .core import NATO_PHONETIC_ALPHABET, lookup_letter, spell_word

__all__ = [
    "NATO_PHONETIC_ALPHABET",
    "lookup_letter",
    "spell_word",
]
