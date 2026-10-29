#!/usr/bin/env bash
# Frees about 9.8 GB: deletes ONLY video/audio files (mp4 mov webm mkv avi mp3 wav m4a) inside /home/claude/v10 ... v49 (old drafts of already published Shorts, 5-17.10.2026).
# Keeps scripts, json, images, and every other folder (v50+, ext, keys). IRREVERSIBLE. Default = dry run; pass --delete to delete.
set -euo pipefail
cd /home/claude
FILES=$(find v1[0-9] v2[0-9] v3[0-9] v4[0-9] v25s -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.webm' -o -iname '*.mkv' -o -iname '*.avi' -o -iname '*.mp3' -o -iname '*.wav' -o -iname '*.m4a' \) 2>/dev/null)
echo "files: $(echo "$FILES" | grep -c . || true)"; echo "$FILES" | xargs -r du -ch 2>/dev/null | tail -1
if [ "${1:-}" = "--delete" ]; then echo "$FILES" | xargs -r rm -f; df -h / | tail -1; else echo "dry run only; add --delete to delete"; fi
