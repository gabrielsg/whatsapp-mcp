"""Tests for the read_file MCP tool."""
from unittest.mock import MagicMock

import pytest

import main as mcp_main
from mcp.types import EmbeddedResource, ImageContent, TextContent


@pytest.fixture(autouse=True)
def _allow_tmp_reads(tmp_path, monkeypatch):
    """read_file only serves files under allowed roots; let tests use tmp_path."""
    monkeypatch.setenv("WHATSAPP_READ_ROOTS", str(tmp_path))


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------

def test_read_file_not_found(tmp_path):
    result = mcp_main.read_file(str(tmp_path / "missing.jpg"))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "File not found" in result[0].text


def test_read_file_directory_rejected(tmp_path):
    result = mcp_main.read_file(str(tmp_path))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "Not a file" in result[0].text


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------

def test_read_file_jpeg(tmp_path):
    img = tmp_path / "photo.jpg"
    img.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 10)
    result = mcp_main.read_file(str(img))
    assert len(result) == 1
    assert isinstance(result[0], ImageContent)
    assert result[0].mimeType == "image/jpeg"
    assert len(result[0].data) > 0


def test_read_file_png(tmp_path):
    img = tmp_path / "photo.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 10)
    result = mcp_main.read_file(str(img))
    assert len(result) == 1
    assert isinstance(result[0], ImageContent)
    assert result[0].mimeType == "image/png"


def test_read_file_image_too_large(tmp_path, monkeypatch):
    img = tmp_path / "big.jpg"
    img.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 10)
    monkeypatch.setattr(mcp_main, "MAX_FILE_BYTES", 5)
    result = mcp_main.read_file(str(img))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "too large" in result[0].text


# ---------------------------------------------------------------------------
# PDFs
# ---------------------------------------------------------------------------

def test_read_file_pdf(tmp_path):
    pdf = tmp_path / "invoice.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake pdf content here")
    result = mcp_main.read_file(str(pdf))
    assert len(result) == 1
    assert isinstance(result[0], EmbeddedResource)
    assert result[0].resource.mimeType == "application/pdf"
    assert len(result[0].resource.blob) > 0


def test_read_file_pdf_too_large(tmp_path, monkeypatch):
    pdf = tmp_path / "big.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake content")
    monkeypatch.setattr(mcp_main, "MAX_FILE_BYTES", 5)
    result = mcp_main.read_file(str(pdf))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "too large" in result[0].text


# ---------------------------------------------------------------------------
# Audio / voice notes
# ---------------------------------------------------------------------------

def test_read_file_audio_returns_transcript(tmp_path, monkeypatch):
    ogg = tmp_path / "voice.ogg"
    ogg.write_bytes(b"OggS" + b"\x00" * 20)
    monkeypatch.setattr(mcp_main, "transcribe_audio", lambda path: "I'll be there at 3pm")
    result = mcp_main.read_file(str(ogg))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "[Transcript]" in result[0].text
    assert "I'll be there at 3pm" in result[0].text


def test_read_file_audio_faster_whisper_not_installed(tmp_path, monkeypatch):
    ogg = tmp_path / "voice.ogg"
    ogg.write_bytes(b"fake ogg")
    monkeypatch.setattr(
        mcp_main,
        "transcribe_audio",
        MagicMock(side_effect=ImportError("faster-whisper is not installed. Run: uv add faster-whisper")),
    )
    result = mcp_main.read_file(str(ogg))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "faster-whisper" in result[0].text


def test_read_file_audio_transcription_failed(tmp_path, monkeypatch):
    ogg = tmp_path / "voice.ogg"
    ogg.write_bytes(b"corrupt audio")
    monkeypatch.setattr(
        mcp_main,
        "transcribe_audio",
        MagicMock(side_effect=RuntimeError("ffmpeg not found")),
    )
    result = mcp_main.read_file(str(ogg))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "Transcription failed" in result[0].text
    assert "ffmpeg not found" in result[0].text


# ---------------------------------------------------------------------------
# Text files
# ---------------------------------------------------------------------------

def test_read_file_txt(tmp_path):
    txt = tmp_path / "message.txt"
    txt.write_text("Please review the attached document.", encoding="utf-8")
    result = mcp_main.read_file(str(txt))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert result[0].text == "Please review the attached document."


def test_read_file_csv(tmp_path):
    csv = tmp_path / "data.csv"
    csv.write_text("name,age\nAlice,30", encoding="utf-8")
    result = mcp_main.read_file(str(csv))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "Alice" in result[0].text


def test_read_file_json(tmp_path):
    j = tmp_path / "config.json"
    j.write_text('{"key": "value"}', encoding="utf-8")
    result = mcp_main.read_file(str(j))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert '"key"' in result[0].text


# ---------------------------------------------------------------------------
# Extensionless files — type detected from magic bytes
# ---------------------------------------------------------------------------

def test_read_file_pdf_without_extension(tmp_path):
    # Documents downloaded by older bridge versions have no extension,
    # e.g. document_20260703_172709_AC0957499B276E221B982D08FFC76F1D
    doc = tmp_path / "document_20260703_172709_AC0957499B276E221B982D08FFC76F1D"
    doc.write_bytes(b"%PDF-1.4 fake pdf content here")
    result = mcp_main.read_file(str(doc))
    assert len(result) == 1
    assert isinstance(result[0], EmbeddedResource)
    assert result[0].resource.mimeType == "application/pdf"


def test_read_file_jpeg_without_extension(tmp_path):
    img = tmp_path / "image_20260703_172709_ABC123"
    img.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 10)
    result = mcp_main.read_file(str(img))
    assert len(result) == 1
    assert isinstance(result[0], ImageContent)
    assert result[0].mimeType == "image/jpeg"


def test_read_file_ogg_without_extension(tmp_path, monkeypatch):
    aud = tmp_path / "audio_20260703_172709_DEF456"
    aud.write_bytes(b"OggS" + b"\x00" * 20)
    monkeypatch.setattr(mcp_main, "transcribe_audio", lambda path: "see you at 3pm")
    result = mcp_main.read_file(str(aud))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "[Transcript]" in result[0].text


def test_read_file_unknown_binary_without_extension(tmp_path):
    blob = tmp_path / "document_20260703_172709_GHI789"
    blob.write_bytes(b"\x00\x01\x02\x03unknown format")
    result = mcp_main.read_file(str(blob))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "Binary file" in result[0].text


# ---------------------------------------------------------------------------
# Path restriction — only files under allowed roots may be read
# ---------------------------------------------------------------------------

def test_read_file_outside_roots_rejected(tmp_path_factory):
    # A real, readable file that is NOT under any allowed root
    outside = tmp_path_factory.mktemp("outside") / "secret.txt"
    outside.write_text("s3cr3t", encoding="utf-8")
    result = mcp_main.read_file(str(outside))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "outside the allowed" in result[0].text
    assert "s3cr3t" not in result[0].text


def test_read_file_symlink_escaping_root_rejected(tmp_path, tmp_path_factory):
    # A symlink inside an allowed root must not read a target outside it
    target = tmp_path_factory.mktemp("outside") / "id_rsa"
    target.write_text("PRIVATE KEY", encoding="utf-8")
    link = tmp_path / "innocent.txt"
    link.symlink_to(target)
    result = mcp_main.read_file(str(link))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "outside the allowed" in result[0].text
    assert "PRIVATE KEY" not in result[0].text


def test_read_file_store_dir_allowed_by_default(tmp_path, monkeypatch):
    # Without WHATSAPP_READ_ROOTS, the bridge store dir (derived from
    # MESSAGES_DB_PATH) is the allowed root
    monkeypatch.delenv("WHATSAPP_READ_ROOTS", raising=False)
    store = tmp_path / "store"
    store.mkdir()
    monkeypatch.setattr(mcp_main, "MESSAGES_DB_PATH", str(store / "messages.db"))
    chat_dir = store / "chat"
    chat_dir.mkdir()
    pdf = chat_dir / "document_20260703_172709_ABC.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake pdf content here")
    result = mcp_main.read_file(str(pdf))
    assert len(result) == 1
    assert isinstance(result[0], EmbeddedResource)
    assert result[0].resource.mimeType == "application/pdf"


# ---------------------------------------------------------------------------
# Binary / unknown fallback
# ---------------------------------------------------------------------------

def test_read_file_video_returns_metadata(tmp_path):
    mp4 = tmp_path / "clip.mp4"
    mp4.write_bytes(b"\x00\x00\x00\x18ftyp" + b"\x00" * 20)
    result = mcp_main.read_file(str(mp4))
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "clip.mp4" in result[0].text
    assert "bytes" in result[0].text
