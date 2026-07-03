package main

import (
	"testing"
	"time"
)

func TestSafeExt(t *testing.T) {
	tests := []struct {
		name           string
		storedFilename string
		want           string
	}{
		{"pdf document", "IPA_Rashid.pdf", ".pdf"},
		{"uppercase extension lowered", "Report.PDF", ".pdf"},
		{"docx", "contract.docx", ".docx"},
		{"no extension", "document_20260703_172709_ABC123", ""},
		{"empty filename", "", ""},
		{"path traversal stripped to ext", "../../../etc/evil.pdf", ".pdf"},
		{"path traversal without ext", "../../../etc/passwd", ""},
		{"multiple dots keeps last", "archive.tar.gz", ".gz"},
		{"dot only", "file.", ""},
		{"whitespace in ext rejected", "file.p df", ""},
		{"overlong ext rejected", "file.aaaaaaaaaaaaaaa", ""},
		{"separator smuggled into ext", "file.p/df", ""},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := safeExt(tt.storedFilename); got != tt.want {
				t.Errorf("safeExt(%q) = %q, want %q", tt.storedFilename, got, tt.want)
			}
		})
	}
}

func TestDownloadFilename(t *testing.T) {
	ts := time.Date(2026, 7, 3, 17, 27, 9, 0, time.UTC)

	tests := []struct {
		name           string
		mediaType      string
		messageID      string
		storedFilename string
		want           string
	}{
		{
			"image keeps fixed jpg ext",
			"image", "MSGID1", "image_20260703_172709_MSGID1.jpg",
			"image_20260703_172709_MSGID1.jpg",
		},
		{
			"video keeps fixed mp4 ext",
			"video", "MSGID2", "video_20260703_172709_MSGID2.mp4",
			"video_20260703_172709_MSGID2.mp4",
		},
		{
			"audio keeps fixed ogg ext",
			"audio", "MSGID3", "audio_20260703_172709_MSGID3.ogg",
			"audio_20260703_172709_MSGID3.ogg",
		},
		{
			"document gets ext from stored filename",
			"document", "AC0957", "IPA_Rashid.pdf",
			"document_20260703_172709_AC0957.pdf",
		},
		{
			"document without stored ext stays extensionless",
			"document", "AC0957", "document_20260703_172709_AC0957",
			"document_20260703_172709_AC0957",
		},
		{
			"document with hostile stored filename only keeps ext",
			"document", "AC0957", "../../../home/user/.ssh/evil.docx",
			"document_20260703_172709_AC0957.docx",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := downloadFilename(tt.mediaType, ts, tt.messageID, tt.storedFilename)
			if got != tt.want {
				t.Errorf("downloadFilename(%q, ts, %q, %q) = %q, want %q",
					tt.mediaType, tt.messageID, tt.storedFilename, got, tt.want)
			}
		})
	}
}
