# Ep.1 voice check, 30.10.2026 (owner: "Проверяй озвучку")
Files: voice/tts_ep1/C01-C15.mp3 (14 lines, locked voice v3 The Young Heir, French accent) and the built finals C01-C08 (frames/*_final*.mp4). All checks free: faster_whisper small (beam 5, word times), f0 by autocorrelation, EBU R128, silencedetect -50 dB.

## Text vs ASR (words of lines_ep1_emotion.json without tags)
| Clip | TTS line | Final clip | Note |
|--|--|--|--|
| C01 | PASS | PASS | "handsome" only here (rule: once, in the opener) |
| C02 | PASS | PASS | |
| C03 | PASS | PASS | |
| C04 | PASS ("17" = seventeen) | PASS | |
| C05 | PASS | PASS | fastest line, 3.8 words/s in TTS, 3.2 in the clip: still clear |
| C06 | PASS | PASS | |
| C07 | PASS | **FAIL -> FIXED**: heard "Take note." The final "s" of "notes" (TTS 5.04-5.30 s) fell after the end of the clip (7.91 s). Fix (free): L-cut, the 0.25 s tail is mixed into the silent start of C08 (C08 voice starts at 1.10 s). Re-check by ASR on the join: "Take notes!" PASS. Files: frames/C08_final_lcut.mp4 (use it in the edit instead of C08_final.mp4), frames/C07_C08_lcut_check.mp4. | |
| C08 | PASS | PASS | the 0.3 s pause before "To myself" is there (ASR joins it into one sentence, the joke still lands by ear) |
| C09 | FIXED 30.10: re-voiced with plain "the" (0.23 RUB), ASR hears "there goes the hat" | not built yet | see voice/qc.md |
| C10 | PASS | not built | |
| C12 | PASS ("357") | not built | |
| C13 | PASS | not built | |
| C14 | PASS | not built | |
| C15 | PASS; the haughty laugh sits between "do what you like" (ends 3.04 s) and "I'm off" (5.68 s): 2.6 s, no silence | not built | |

No tag or bracket is spoken aloud in any line (ASR finds only the script words). No music. No subtitles.

## Consistency of the voice
- Median pitch, C02-C10: 139-195 Hz, mean about 165 Hz. C12-C15 (voiced in a separate order): 186-230 Hz, mean about 211 Hz = about 4 semitones higher (the tags there are "snapping", "gleeful", "imperious"). Same voice ID, so the timbre is the same; the risk is that the king sounds more excited in the finale than in the morning. SOFT: decide by ear on the built C12-C15; free option then: pitch -1...-2 semitones on those lines; paid option: re-voice C12-C15 with calmer tags (about 0.23 RUB).
- Loudness of finals C01-C08: -14.2...-15.9 LUFS, true peak -1.9 dBFS on all: PASS (the episode master will be normalised once more).
- Pace: 1.9-3.1 words/s on all lines except C05 (above): PASS.

## Still open (known, not voice errors)
- Dead silence in the finals: 1.5-5.2 s per clip (pauses between phrases with muted model audio): the room tone + foley layer (free) fills it.
- Page and courtier lines ("The court, Sire." / "Pardon, Sire!" / "Sire, I only..."): the page voice is not chosen yet (shortlist 1-6).
