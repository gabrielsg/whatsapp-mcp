package main

// Local filenames for downloaded media.
//
// Downloaded files are always saved under a generated name
// ({type}_{timestamp}_{messageID}) rather than the sender-supplied
// document filename, so a hostile filename cannot influence the path.
// Only a strictly sanitized extension is carried over from the stored
// filename, so documents (PDF, DOCX, …) keep a usable file type.

import (
	"fmt"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

// safeExtPattern matches a plain extension like ".pdf" or ".docx":
// a dot followed by 1-9 alphanumerics, nothing else.
var safeExtPattern = regexp.MustCompile(`^\.[A-Za-z0-9]{1,9}$`)

// safeExt extracts a sanitized, lowercased extension from a stored
// (sender-supplied) filename. Returns "" when there is no extension or
// it contains anything beyond short alphanumerics.
func safeExt(storedFilename string) string {
	ext := filepath.Ext(filepath.Base(storedFilename))
	if !safeExtPattern.MatchString(ext) {
		return ""
	}
	return strings.ToLower(ext)
}

// downloadFilename rebuilds the local filename for a media download.
// For image/video/audio the extension is fixed (matching extractMediaInfo);
// for documents it is derived from the stored original filename.
func downloadFilename(mediaType string, timestamp time.Time, messageID, storedFilename string) string {
	var ext string
	switch mediaType {
	case "image":
		ext = ".jpg"
	case "video":
		ext = ".mp4"
	case "audio":
		ext = ".ogg"
	case "document":
		ext = safeExt(storedFilename)
	}
	return fmt.Sprintf("%s_%s_%s%s", mediaType, timestamp.Format("20060102_150405"), messageID, ext)
}
