# Ep.1 sound bed C01-C08: room tone + foley, 30.10.2026 (owner: "сделай сразу шум как в референсе")
Script: build_bed.py (own synthesis, no samples, no library, no music; free). Reference: Vlog 1 LjfGP7wpjVs, measured on the owner's mp4 (voice_source.md, 28.10) and its audio kept in the session: pause floor -57...-45 dB RMS (10th percentile -49.5, 25th -45.5), low-heavy spectrum, an ambience per shot, no silence > 1 s at -50 dB, -15.4 LUFS.

## What the bed is
- Room tone: pink noise 30-7000 Hz, low-heavy, slow level drift, decorrelated stereo. One continuous tone per scene (A bedroom C01-C03, B wig table C04-C06, C court C07-C08); a different tone at each hard cut, as in the reference ("an ambience per shot").
- People in the room: faint band-passed murmur (200-1800 Hz, syllable-rate envelope), a little in scene A (C02 "a hundred people"), almost none at the wig table, clearly in the court scene C07-C08.
- Foley on the real motion of each clip (frame-difference peaks): fabric/wig rustles, rings clinks (C02, C04-C06, short, inharmonic), C07 courtiers' soft footsteps in the first 4 s and a wig tap at "wig", C08 cloth swishes of the bowing court. Louder with bigger motion.
- The voice is unchanged (lowered 2.6 dB: dual-mono stereo reads 3 dB louder than the mono finals). The video models' own audio stays muted.

## Measured (frames/<clip>_bed.mp4, frames/EP1_C01-C08_bed.mp4, 67.4 s; videos not committed)
| Item | Reference | Ours | Verdict |
|--|--|--|--|
| Silences >= 0.5 s at -50 dB | none > 1 s | none in any clip or in the episode (before: 1.5-5.2 s of dead silence per clip) | PASS |
| Pause floor, 10th / 25th percentile | -49.5 / -45.5 dB | -48.6 / -48.0 dB (episode) | PASS (a little more even than the reference) |
| Loudness | -15.4 LUFS | -14.8 LUFS (clips -13.8...-15.5), LRA 6.9 | PASS |
| True peak | -1.1 | -4.2 | PASS |
| Narrow-band peaks in quiet frames (tonal content / music) | median 9.4, max 11.9 dB | median 8.7, max 11.1 dB: same as the reference noise, no tone | PASS: no music, no tune |
| ASR of every clip before / after the bed | - | identical words in all 8 clips (voice still clear) | PASS |

Defect found and fixed during the check: AAC at 192 kbps overshot to +0.7 dBFS in the right channel (mix peak was -4.4); 320 kbps gives -4.2 true peak.

## NOT VERIFIED
- The bed is judged by measurements, not by ear: the owner listens. Foley timing follows the picture's motion peaks, not a frame-by-frame look at each action (it can rustle at a head turn rather than a hand move).
- The reference's ambience per shot is a hypothesis from the noise floors (-57...-49 dB per take), not a proven method.
- C09-C15 are not built yet; the same script runs on them (add the clips to CLIPS and the scenes: D = Hall of Mirrors with a longer reverb).
