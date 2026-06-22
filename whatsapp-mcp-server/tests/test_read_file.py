"""Tests for the read_file MCP tool."""
from unittest.mock import MagicMock

import pytest

import main as mcp_main
from mcp.types import EmbeddedResource, ImageContent, TextContent


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
