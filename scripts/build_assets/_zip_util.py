"""Make zip-based outputs (DOCX, EPub) byte-deterministic."""

import zipfile
from pathlib import Path

_FIXED_DATETIME = (2024, 1, 1, 0, 0, 0)


def normalize_zip(path: Path) -> None:
    """Rewrite ``path`` so every member has the same fixed mtime.

    DOCX and EPub files are zip archives. python-docx and ebooklib write
    members with the current timestamp, which makes byte-deterministic
    output impossible. This rewrites the archive in place with a fixed
    epoch on every member so subsequent builds produce identical bytes.
    """
    with zipfile.ZipFile(path, "r") as src:
        members = [
            (info.filename, src.read(info.filename), info.compress_type, info.external_attr)
            for info in src.infolist()
        ]
    with zipfile.ZipFile(path, "w") as dst:
        for filename, data, compress_type, external_attr in members:
            zi = zipfile.ZipInfo(filename, date_time=_FIXED_DATETIME)
            zi.compress_type = compress_type
            zi.external_attr = external_attr
            dst.writestr(zi, data)
