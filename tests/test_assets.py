"""Tests for the downloadable-assets module."""

from pathlib import Path
from unittest.mock import patch

import pytest

from nato_phonetic import assets


def test_catalog_is_non_empty_and_has_default():
    assert assets.ASSETS, "catalog must not be empty"
    assert assets.DEFAULT_SLUG in assets.ASSETS, "default slug must be in catalog"


def test_every_asset_has_filename_and_description():
    for slug, asset in assets.ASSETS.items():
        assert asset.slug == slug
        assert asset.filename, f"{slug} missing filename"
        assert asset.description, f"{slug} missing description"


def test_default_downloads_dir_is_under_home():
    dest = assets.default_downloads_dir()
    assert dest == Path.home() / "Downloads"


def test_asset_url_uses_codeberg_raw_and_encodes_spaces():
    url = assets.asset_url("pdf")
    assert url.startswith(assets.RAW_BASE)
    assert "%20" in url, "spaces must be URL-encoded"
    assert " " not in url


def test_asset_url_handles_parentheses():
    url = assets.asset_url("pdf-landscape")
    assert "%28" in url and "%29" in url, "parens must be URL-encoded"


def test_unknown_slug_raises():
    with pytest.raises(assets.AssetError, match="Unknown asset slug"):
        assets.asset_url("does-not-exist")


def test_download_reuses_existing_file_by_default(tmp_path):
    target = tmp_path / assets.ASSETS["pdf"].filename
    target.write_bytes(b"stub")

    with patch("nato_phonetic.assets.urllib.request.urlopen") as fake:
        result = assets.download_asset("pdf", tmp_path)

    fake.assert_not_called()
    assert result == target
    assert target.read_bytes() == b"stub"


def test_download_force_redownloads_existing_file(tmp_path):
    target = tmp_path / assets.ASSETS["pdf"].filename
    target.write_bytes(b"stale")

    fake_response = _fake_http_response(b"fresh")
    with patch("nato_phonetic.assets.urllib.request.urlopen", return_value=fake_response):
        assets.download_asset("pdf", tmp_path, force=True)

    assert target.read_bytes() == b"fresh"


def _fake_http_response(payload: bytes):
    from io import BytesIO

    class _Resp(BytesIO):
        headers = {"Content-Length": str(len(payload))}

        def __enter__(self):
            return self

        def __exit__(self, *_):
            self.close()
            return False

    return _Resp(payload)
