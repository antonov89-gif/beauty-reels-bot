#!/usr/bin/env bash
# C04 v2 (owner 29.10 "Делай сразу 1080"): draft -> automatic word check -> 1080p final only if every word is there.
set -e
cd "$(dirname "$0")"
python3 seedance25_c04.py draft 2>&1 | grep -v "^ " | tail -3
python3 - <<'PY'
import sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
s, _ = m.transcribe("frames/seedance25_c04v2_draft.mp4", language="en")
t = " ".join(g.text for g in s).lower(); print("draft says:", t)
need = ["wig", "hair", "falling", "seventeen|17", "took", "personally", "so i got"]
miss = [w for w in need if not any(x in t for x in w.split("|"))]
print("missing:", miss)
sys.exit(1 if miss else 0)
PY
python3 seedance25_c04.py final "$(cat frames/seedance25_c04v2_draft.task_id)" 2>&1 | grep -v "^ " | tail -3
