# Ep.1 0-42 s (C01-C05) vs the reference "Elizabeth I - vlog 1" (LjfGP7wpjVs), 29.10.2026
Reference numbers: map_shorts/ref_tudor_vlog_2026_10_28/frames_vlog1_LjfGP7wpjVs.md (measured on the owner's mp4 on 28.10; the mp4 itself is not on disk now, so no new side-by-side frames).
Ours: frames/EP1_0-42_check.mp4 (C01 v4 + C02 + C03 + C04 + C05 jump-cut), measured with the same methods (mean frame difference per second, hard-cut scan at diff > 15, global camera shift by phase correlation, silences >= 1 s below -50 dB, EBU R128).

| Item | Reference | Ours | Verdict |
|--|--|--|--|
| Take 1 | 23.6 s: selfie from the ceiling, tilt to level 2.5-4.5 s, then calm | 28 s (C01-C03), tilt 1.7-3.7 s, joins invisible | MATCH |
| Take 2 camera | 28.8 s, table height, rolled (dutch), VERY close, hand-held sway, a thumb in the lower right, tilt up to the face, pan to a jar | 14.4 s, propped and locked (camera path 0 px), level, medium-wide, no sway, no foreground "mistake"; a jump cut at 37 s | GAP: too static, too wide, too tidy |
| Movement inside takes | the camera always moves (roll, drift, pan, push-in, a hand re-aims) | C02-C03 only micro-shake (1-8 px total), C04-C05 none | GAP |
| Calm-segment motion | 2-4 mean diff per second | C02-C03 1.4-2.0, C04 1.0-2.0, C05 0.3-0.6 (almost still) | GAP (C05 reads near frozen at the end) |
| Foreground "phone mistakes" | 5 in 128 s (thumb, hand, fingers, toothpick, lens cover) | 1 (the plume on the ceiling in C01) | GAP: add the planned ones (wig filling the lens C06, hand re-aims C07, heel in the foreground C10, mirror flash C15) |
| Lens look | ultra-wide front camera, nose distortion at close range | yes in C01-C03 (selfie), weak in C04-C05 (subject far) | PARTIAL |
| Light | soft overcast window light, warm oak, pale face | soft window light, warm gilding and oak | MATCH |
| Face consistency | (AI, small drifts between shots) | Seedance face stable C01-C05 | MATCH |
| Sound bed | no silence longer than 1 s (room tone always there), LRA 11.1 LU | 5 dead-silent gaps of 1-2.8 s (1.8-4.6, 10.8-12.8, 19.2-21.7, 27.2-28.2, 29.4-31.0 s), LRA 6.2 LU: voice only, no room tone, no foley yet | GAP: the bible asks for voice + room tone + foley; silence reads as "AI video" |
| Loudness | -15.4 LUFS, TP -1.1 | -15.0 LUFS, TP -1.9 | MATCH |
| Captions | burned-in | none (owner: no subtitles, platform SRT) | deliberate difference |
| Picture | 360x640 30 fps (upload copy) | 1080x1920 24 fps | ours sharper |

## What to change from C06 on (prompts, free)
1. Camera: a phone in his hand or propped with a gentle hand-held sway and slow drift, a slight dutch roll (10-20 degrees) in take 2, closer framing (face and hands fill the frame), one motivated move per clip (tilt up to the face, push-in, pan to the object, a hand re-aiming).
2. One foreground "mistake" per take: the white wig filling the lens in C06 (planned), a hand re-aiming the phone in C07, the heel in the foreground in C10.
3. Seedance draft route only (keeps the exact first frame); no direct i2v.

## Edit layer (free or almost free, before the final export)
1. Room tone under the whole episode (quiet palace room: distant voices, footsteps on parquet, fabric), no gap of dead silence; foley on actions (wig rustle, powder puff, door, boots). Source: own synthesis or a licensed library; the video models' audio stays muted (channel rule).
2. Stereo export.
3. AI mark, title chip, authenticity audit.
