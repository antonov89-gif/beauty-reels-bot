# Ep.1 reference check (statuses: GENERATED != INSPECTED != APPROVED)

## C01 start frame, frames/C01_ceiling.jpg (29.10, $0.04)
Status: GENERATED, INSPECTED (by us), not APPROVED by the owner.
Check: painted gilded baroque ceiling, gold canopy top at the lower right, a black hat with a white plume at the lower left (our phone-mistake device, not the reference thumb), no people, no faces, no modern objects. Soft defect: a skylight at the top edge (the real state bedchamber has none); accepted because the camera leaves the ceiling in 1.3 s. Kling character refs switched to night-wig images only (D2_morning, C01, C02, C03).

## C01 clip, Kling 4.0 r2v, 12 s 1080p (owner said yes, about $2.55)
Attempt 1 (task 940f34aa): FAILED by the provider: "Not enough speech in the voice audio. Please use a 5-30 second clip with clear speech and no long pauses." (voice ref heir_fr_sample.mp3, 12.8 s with pauses).
Attempt 2 (task dda11367): FAILED with the same message, voice ref heir_fr_ref_speech.mp3 = 23.7 s of continuous speech (no pause >= 0.3 s at -40 dB, mp3 48 kHz mono, URL checked: 200, audio/mpeg).
No cost field in either failed status; APIpod has no balance endpoint, so "not charged" is NOT VERIFIED. Two corrective attempts used: method reassessment goes to the owner (no third attempt without a decision).
Attempt 3 (task 7bf475e6, owner chose "C": same 23.7 s reference as WAV 44.1 kHz 16-bit mono): FAILED, same message. Kling r2v does not accept our synthetic French-accent voice as a voice reference (3 of 3). Also found in the official spec (docs.apipod.ai, kling-4.0-r2v.yaml): r2v `image_urls` are REFERENCE images (@image_N), not a first frame, so the ceiling would not have been the opening frame anyway.
Method reassessment (to the owner): kling-4.0-i2v takes a real first frame, up to 8 keyframes and a last frame (3-30 s, about $0.145/s at 720p from the estimator; 1080p rate NOT VERIFIED). seedance-2.0-r2v takes `audio_urls` (needs an image) but no first frame; its lip-sync to a given audio is undocumented.

## C01 part 1 (0-3 s), Kling 4.0 i2v, 1080p (owner said yes 29.10)
File: frames/kling_i2v_part1.mp4 (1076x1924, 24 fps, 3.04 s, task 8440d148). ACTUAL COST $0.6525 (status usage.cost) = $0.2175/s at 1080p, so the 9-s part 2 is about $1.96 and the 12-s total about $2.61.
Status: GENERATED, INSPECTED (contact sheet 6 fps + 3 full-res frames + motion curve + audio), not APPROVED by the owner.
| Check | Result |
|--|--|
| Starts on the ceiling, one continuous tilt, no cut | PASS: no cut; ceiling hold 0-0.6 s, tilt 0.6-2.2 s, settle 2.2-3.0 s |
| Lands on the C01 frame | PASS: last frame matches the storyboard frame (wig, moustache, gown, courtiers, window) |
| Natural motion blur, focus hunt, exposure change | PASS: heavy blur 0.7-2.0 s, face sharpens at ~1.9 s, exposure drops to the warm bed |
| Hand-held shake in the ceiling hold | SOFT FAIL: frames 0-0.4 s almost static (mean diff 5-6 vs 30 in the tilt); the plume moves a little. Add a measured micro-shake in the edit |
| Ceiling hold length | SOFT FAIL: 0.6 s instead of the planned 1.3 s (3-s clip). Fix: stretch the first 0.4 s (frames 0-9 are near static) by a slow-down or a freeze-and-shake in the edit, or add silence before the tilt |
| Camera is a pure tilt | SOFT: the camera also moves toward the bed (the king grows from small to large between 1.0 and 1.9 s), like a page stepping forward while tilting; acceptable for a phone move |
| Face identity during the move | SOFT: at ~1.5 s the face is smeared by motion blur and the moustache looks thicker (blur); sharp and on-model from ~1.9 s and in the last frame |
| Overshoot and settle | PASS: a rolled frame at ~2.0 s, then a settled landing |
| Hands, props, modern objects | PASS: no hands in the first 2 s, no modern objects |
| Last 0.8 s | HOLD: almost frozen (diff 2-3), no breathing or blink; part 2 starts from this frame, so trim the hold when joining |
| Audio | A generated track exists (no speech, transcription empty): a swoosh at 0.75-1.75 s peaking about -9 dB, room tone about -46 dB. Keep as a base for our own foley or replace |

## C01 part 1 v1: REJECTED by the owner (29.10): "we make everything realistic, but the camera flies"
My earlier verdict "camera also moves toward the bed, acceptable" was WRONG. Measured with phone_move_check.py (feature tracking, new): scale grows 2-10 % per frame between 0.8 and 1.4 s, cumulative +141 % = the camera flies in (the king becomes about 2.4x larger in 0.7 s). A real tilt is a rotation: the king keeps his size. Cause: the first frame (ceiling) was generated from a different camera position than the last frame (C01, close), so the model had to travel between them. Status: GENERATED, INSPECTED, REJECTED. Spent $0.65.
Fix plan: new first frame from the SAME camera position as C01, pitched up (gen_ceiling2.py), prompt "rotation only, the camera does not move forward"; gate = phone_move_check.py cumulative scale change below 12 % and the king's apparent size constant. Fallback if the model still flies: build the tilt in the edit from two plates (ceiling plate and C01 frame) with a measured rotation curve, motion blur and shake.

## C01 part 1 v2 (29.10, owner said yes): frames/C01_ceiling2.jpg ($0.04) + frames/kling_i2v_part1_v2.mp4 ($0.6525, task eaf8522e)
Method: first frame = the same camera position as C01 pitched up 60 degrees; prompt "rotation only, no dolly, no zoom, no flying, the king keeps his size". 1076x1924, 24 fps, 3.04 s.
Status: GENERATED, INSPECTED (contact sheet 6 fps, 4 full-res frames next to the C01 target, motion tool, audio), not APPROVED by the owner.
| Check | Result |
|--|--|
| Camera does not fly (owner rule) | PASS by eye and by manual measurement: the king's wig is 140 / 120 (blur) / 135 / 128 px wide at t=0.1 / 1.4 / 1.9 / 2.9 s on a 400-px-wide panel, the C01 target 130 px: within +/-10 %. The room slides through the frame, the king does not grow |
| phone_move_check.py | FLAG (cumulative -21 %, per-frame scale 0.984-0.999). In v1 it measured +141 % with a visible dolly-in. With an ultra-wide lens a 60-degree pitch changes the apparent size of the ceiling and canopy by perspective, so the global-scale metric over-flags large pitches; the tool needs a subject-based variant (track the face/wig). Decision rests on the manual measurement above, stated as such |
| One continuous tilt, no cut | PASS: hold 0-0.6 s, tilt 0.6-2.0 s, settle by 2.1 s |
| Lands on the C01 frame | PASS: last frames match the storyboard frame (wig, moustache, gown, canopy, window, courtiers) |
| Natural blur / exposure / focus hunt | PASS (blur 0.8-1.9 s, face smeared by blur and sharp at ~1.9 s) |
| Ceiling hold and shake | SOFT: hold is 0.6 s (needs >= 1.3 s) and almost static; fix in the edit |
| Last 1 s | HOLD frozen; trim when joining part 2 |
| Audio | A continuous bed at about -25 dB, no speech (transcription empty); its content is NOT identified (possibly generated music/ambience). NOT USED: our own room tone and foley are laid instead (no unlicensed audio) |
Cost of the camera-flight lesson: v1 $0.65 + v2 $0.04 + $0.65.

## C01 part 2 (speech), Kling 4.0 i2v 9 s 1080p (owner said yes; usage.cost 1.9575, task 2869894b)
Status: GENERATED, INSPECTED, NOT APPROVED (failed the lip-sync check with our voice; not shown to the owner).
| Check | Result |
|--|--|
| Camera does not fly | PASS: phone_move_check +0.1 %, framing steady, micro-shake only |
| Identity / wig / gown vs first frame | PASS (frames 0-9 s and 3 full-res crops) |
| Gesture "Me." finger to chest | PASS: hand at 1.7-2.0 s, five fingers, natural |
| Expressions | PASS: irritated, smug, a broad grin at ~4.7 s, smirk at the end |
| Lip sync with OUR voice (tts_ep1/C01.mp3) | FAIL: Kling speaks its own (faster) line. Phrase starts match within 0.1 s (Marcel 0.00/0.00, Me 1.68/1.68, Versailles 4.44/4.32, Yes 5.30/5.20, Try 7.20/7.12), but words inside phrases are early by 0.4-0.9 s (ceiling 0.84 vs 1.28, that 5.64 vs 6.28, handsome 5.78 vs 6.64, faint 7.72 vs 8.14). Our drawled voice would visibly lag the lips |
| Audio of the clip | model speech in a generic voice; muted by rule |
Fix route: Wan 2.7 i2v takes `audio_url` (official spec), so the lips are driven by OUR audio; first frame = the same frame (seamless join with part 1 v2). Prepared: wan_part2.py + voice/tts_ep1/C01_drive_10s.mp3 (0.15 s lead + C01 voice, padded to 10 s). Price not shown by the estimator (returns 0): NOT VERIFIED until the status reports usage.cost.
