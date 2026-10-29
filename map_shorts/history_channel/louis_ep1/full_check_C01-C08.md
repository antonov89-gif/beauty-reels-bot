# Full check C01-C08 (owner: "Проверяй все"), 29.10.2026, frames/EP1_C01-C08_check.mp4 (67.4 s, 1080x1920, 24 fps, mono AAC; not committed)
Measured on the assembled file (same methods as the reference comparison): mean frame difference, global camera path (phase correlation), hard-cut scan, silences below -50 dB, EBU R128.

## Joins
| Join | Frame diff at the cut | Verdict |
|--|--|--|
| C01->C02 11.0 s | 1.7 | PASS invisible |
| C02->C03 20.0 s | 1.7 | PASS invisible |
| C03->C04 28.0 s | 70.9 | planned hard cut (wig table) |
| C04->C05 37.0 s | 24.3 | accepted jump cut (owner "Нормально") |
| C05->C06 42.4 s | 2.2 | PASS |
| C06->C07 51.4 s | 63.7 | planned hard cut (court enters) |
| C07->C08 59.4 s | 8.2 | PASS (neighbours 6.7 / 9.0) |

## Camera per clip (rule from 29.10: the king cannot hold a phone, the camera must visibly walk like the reference)
| Clip | Mean motion | Camera path px (x,y) | Calm seconds (<1.0) | Verdict |
|--|--|--|--|--|
| C01 | 8.1 | 33 / 159 | 0 | PASS (the planned tilt) |
| C02 | 2.6 | 1 / 1 | 0 | FAIL: tripod-like, no sway |
| C03 | 2.5 | 8 / 0 | 0 | FAIL: tripod-like |
| C04 | 1.9 | 0 / 0 | 2 | FAIL: locked, propped phone |
| C05 | 0.5 | 0 / 0 | 5 | FAIL: frozen (5 of 5.4 s) |
| C06 | 7.6 | 69 / 117 | 0 | PASS (pick-up, sway, wig in the lens) |
| C07 | 10.0 | 72 / 23 | 0 | PASS (swing to the court, too close) |
| C08 | 7.2 | 81 / 56 | 0 | PASS (creeping push-in) |
Reference calm stretches are 2-4 mean difference with constant drift; C02-C05 were made BEFORE the camera rule and are the weakest part of the opening (22 of 67 s).

## Sound
- Loudness 67.4 s: -15.1 LUFS, TP -1.9, LRA 6.1 LU (reference -15.4 / 11.1 LU); per clip -14.5 ... -16.0: PASS (within 1.5 LU).
- Dead silence: 10 stretches of 1-2.8 s below -50 dB, 18.3 s in total = 27 % of the runtime (1.8-4.6, 10.8-12.8, 19.2-21.7, 27.2-28.2, 29.4-31.0, 41.2-44.0, 50.6-53.1, 55.3-56.4, 58.9-59.9, 64.1-65.1 s). The reference has none longer than 1 s (room tone always present). FAIL until the room-tone/foley layer is added in the edit (planned, free, synthesised).
- Voice only, no music, no subtitles: PASS.

## Picture continuity (one frame per clip, looked at)
Face: one man in all 8 clips (long straight nose, upturned moustache, light eyes): PASS. Morning take C01-C06: brown curled night wig, gold gown, natural face: PASS. Take 3 (C07-C08): the tall powdered wig, white powdered face with rouge, jabot: consistent between C07 and C08; the make-up step from C06 to C07 is explained by the hard cut and "this is the new wig". C08 close-up: rouge and smile a bit strong (soft).

## Script vs actual timeline
Actual lengths: C01 11, C02 9, C03 8, C04 9, C05 5.4 (jump cut, planned 8), C06 9, C07 8, C08 8 = 67.4 s; planned remainder C09 8, C10 8, burst 8, C12 8, C13 8, C14 8, C15 10 = 58 s: runtime about 2:05 (script says the same, but C05 is 2.6 s shorter than planned: C06 starts at 42.4 s, not 43).

## Open
1. C02-C05 camera is static: remake with the hand-held plan? C02 (draft+1080p about $5.1), C03 (about $5.1), C04 (about $5.1), C05 (about $5.1) = about $20, each a separate yes; or accept the calm opening as the "composed" part of the episode (the reference's calm stretches are 19 s long too, but still drift).
2. Room tone and foley (free): to do.
3. APIpod balance: "insufficient quota" on 29.10 after C08; C09-C15 (about $12-15) wait for a top-up.
4. Authenticity audit, AI mark, title chip, stereo export, platform package: at the end.
