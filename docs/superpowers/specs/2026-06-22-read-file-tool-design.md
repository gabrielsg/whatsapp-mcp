# Design: `read_file` MCP Tool

**Date:** 2026-06-22  
**Status:** Approved

## Problem

`download_media` returns a local file path after downloading a WhatsApp media file, but Claude Desktop has no tool to actually read or view that file. The path is useless on its own — Claude cannot see images, read PDFs, or hear voice messages.

## Solution

Add a single `read_file` MCP tool to `whatsapp-mcp-server` that accepts a file path and returns content Claude can process, using the appropriate MCP content type for each file class.

## Behaviour by File Type

| File class | Extensions | Return type | What Claude gets |
|---|---|---|---|
| Images | jpg, jpeg, png, gif, webp | `ImageContent` (base64) | Sees the image via vision |
| PDFs | pdf | `EmbeddedResource` (base64 blob, `application/pdf`) | Reads the full document natively — formatting, tables, embedded images preserved |
| Audio / voice notes | ogg, mp3, wav, m4a, opus | `TextContent` | Transcript of what was said |
| Text files | txt, csv, json, md, xml, html | `TextContent` | Raw file content |
| Video / other binary | mp4, avi, mov, … | `TextContent` | Metadata only: type, size, path |

## Architecture

### New tool — `main.py`

```python
@mcp.tool()
def read_file(file_path: str) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Read a downloaded WhatsApp media file and return its contents.

    Use after download_media to view images, read PDFs, or transcribe voice notes.

    Args:
        file_path: Absolute path to the file (as returned by download_media).
    """
```

Dispatch logic (pure stdlib except for the Whisper call):
- Detect MIME type via `mimetypes.guess_type`
- Route to the appropriate handler
- Size guard: reject images and PDFs over 20 MB with a clear error message

### Transcription helper — `audio.py`

New function `transcribe_audio(file_path: str) -> str` added alongside existing `convert_to_opus_ogg`. Uses `faster-whisper` with the `base` model by default. Model overridable via `WHISPER_MODEL` environment variable (e.g. `small`, `medium`). Returns the joined transcript text. Raises `RuntimeError` on failure (model load error, file unreadable) so `read_file` can catch and return a descriptive error message.

### New dependency — `pyproject.toml`

```
faster-whisper>=1.0.0
```

No other new dependencies. `base64`, `mimetypes`, and `pathlib` are stdlib. ffmpeg is already required by the existing audio conversion code.

## Error Handling

| Scenario | Response |
|---|---|
| File not found | `TextContent`: "File not found: \<path\>" |
| File is a directory | `TextContent`: "Not a file: \<path\>" |
| Image / PDF over 20 MB | `TextContent`: "File too large to read (X MB). Max 20 MB." |
| Whisper not installed | `TextContent`: "Audio transcription unavailable: faster-whisper is not installed. Run `uv add faster-whisper`." |
| ffmpeg missing | `TextContent`: "Audio transcription failed: ffmpeg not found. Install ffmpeg and retry." |
| Transcription error | `TextContent`: "Transcription failed: \<error message\>" |
| PDF / image unreadable | `TextContent`: "Could not read file: \<error message\>" |

## Security

No path restriction. File paths passed to `read_file` will always originate from `download_media`, which only ever returns paths within the bridge's `store/` directory. Adding a path allowlist would add complexity without meaningful security benefit in this deployment.

## Out of Scope

- Word (.docx) and Excel (.xlsx) extraction — not commonly received; can be added later with `python-docx` / `openpyxl`
- Video transcription — too large and complex for this iteration
- Automatic `read_file` call after `download_media` — kept as separate tool calls so Claude can decide whether to read the content
