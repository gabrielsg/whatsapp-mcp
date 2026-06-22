"""Tests for the transcribe_audio helper."""
from unittest.mock import MagicMock, patch

import pytest


def test_transcribe_audio_success(tmp_path):
    audio_file = tmp_path / "voice.ogg"
    audio_file.write_bytes(b"fake ogg audio data")

    seg1, seg2 = MagicMock(), MagicMock()
    seg1.text = " Hello "
    seg2.text = " world. "

    mock_model = MagicMock()
    mock_model.transcribe.return_value = ([seg1, seg2], MagicMock())

    mock_fw = MagicMock()
    mock_fw.WhisperModel.return_value = mock_model

    with patch.dict("sys.modules", {"faster_whisper": mock_fw}):
        import audio
        result = audio.transcribe_audio(str(audio_file))

    assert result == "Hello world."
    mock_fw.WhisperModel.assert_called_once_with("base", device="cpu", compute_type="int8")
    mock_model.transcribe.assert_called_once_with(str(audio_file))


def test_transcribe_audio_respects_whisper_model_env(tmp_path, monkeypatch):
    audio_file = tmp_path / "voice.ogg"
    audio_file.write_bytes(b"fake audio")

    monkeypatch.setenv("WHISPER_MODEL", "small")

    seg = MagicMock()
    seg.text = " Test "
    mock_model = MagicMock()
    mock_model.transcribe.return_value = ([seg], MagicMock())

    mock_fw = MagicMock()
    mock_fw.WhisperModel.return_value = mock_model

    with patch.dict("sys.modules", {"faster_whisper": mock_fw}):
        import audio
        result = audio.transcribe_audio(str(audio_file))

    assert result == "Test"
    mock_fw.WhisperModel.assert_called_once_with("small", device="cpu", compute_type="int8")


def test_transcribe_audio_explicit_model_overrides_env(tmp_path, monkeypatch):
    audio_file = tmp_path / "voice.ogg"
    audio_file.write_bytes(b"fake audio")

    monkeypatch.setenv("WHISPER_MODEL", "small")

    seg = MagicMock()
    seg.text = " explicit "
    mock_model = MagicMock()
    mock_model.transcribe.return_value = ([seg], MagicMock())

    mock_fw = MagicMock()
    mock_fw.WhisperModel.return_value = mock_model

    with patch.dict("sys.modules", {"faster_whisper": mock_fw}):
        import audio
        result = audio.transcribe_audio(str(audio_file), model_name="medium")

    assert result == "explicit"
    mock_fw.WhisperModel.assert_called_once_with("medium", device="cpu", compute_type="int8")


def test_transcribe_audio_raises_import_error_when_not_installed(tmp_path):
    audio_file = tmp_path / "voice.ogg"
    audio_file.write_bytes(b"fake audio")

    with patch.dict("sys.modules", {"faster_whisper": None}):
        import audio
        with pytest.raises(ImportError, match="faster-whisper is not installed"):
            audio.transcribe_audio(str(audio_file))


def test_transcribe_audio_raises_runtime_error_on_failure(tmp_path):
    audio_file = tmp_path / "voice.ogg"
    audio_file.write_bytes(b"corrupt audio")

    mock_model = MagicMock()
    mock_model.transcribe.side_effect = ValueError("invalid audio format")

    mock_fw = MagicMock()
    mock_fw.WhisperModel.return_value = mock_model

    with patch.dict("sys.modules", {"faster_whisper": mock_fw}):
        import audio
        with pytest.raises(RuntimeError, match="invalid audio format"):
            audio.transcribe_audio(str(audio_file))
