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

## C01 part 2 test: Seedance 2.0 r2v 720p with OUR audio in audio_urls (owner said yes; usage.cost 1.26, task a852fc92)
- The model RE-VOICED the line in its own voice (median f0 143 Hz vs ours 216 Hz; timbre distance to ours 40, same as Kling's voice, while two takes of our voice are 17 apart). The mouth follows that voice (mouth-open vs audio correlation 0.24 at lag 0) more than ours (0.07). So Seedance does NOT lip-sync to a given audio.
- But it used our audio as the pacing guide: word durations are close to ours; only the pauses differ. Phrase-level alignment of OUR voice to its word timing (rough_c01.py: phrases moved, "I'm that handsome" compressed 1.3x) leaves residuals 0.00-0.14 s on 16 of 17 words and 0.19 s on "handsome".
- Opening frame: NOT identical to the reference image (frame difference 22 vs about 2 between neighbouring frames; the plume is in frame). Hidden in the rough cut by cutting inside the landing motion (1.92 s of part 1) with a 4-frame dissolve: no spike at the seam (frame differences fall 26 -> 12 -> 3).
- Rough cut frames/C01_rough_seedance.mp4 (not committed): 1080x1920, 24 fps, 12.5 s, 0 duplicate frames after the fix (30 fps conversion produced duplicates, corrected), -15.5 LUFS, true peak -1.5 dBFS, last frame not black, audio = our locked voice only (no music, model audio muted). Ceiling hold extended to ~1.3 s with a cloned first frame and a measured hand-held shake (about 1 % amplitude, 1.8 Hz sway + small tremor). Lips at "Me" closed on the M, open on the vowel; "handsome" and "faint" open in time.
- Limits: part 2 is 720p upscaled (soft vs part 1); the voice starts ~0.15 s before the camera fully stops.
Status: rough GENERATED + INSPECTED, shown to the owner as a lip-sync check, NOT final.

## Owner feedback on the C01 rough cut (29.10): "when he starts speaking the splice is visible" and "he holds the camera himself"
Accepted: my seam fix (dissolve inside the landing motion) only reduced the join; at the moment he starts speaking the cut shows (Seedance first frame differs from part 1 last frame, 720p vs 1080p softness, colour/exposure shift). A real fix = ONE continuous generation (ceiling, tilt and speech in one clip), no join. He films himself (selfie arm in frame), so "Marcel" lines are wrong; he speaks only after the phone is pointed at him. Options and cost sent to the owner; nothing generated.
Candidates: (1) Seedance 2.0 r2v single 12 s clip, ceiling image as reference, our audio with a silent lead (720p test $1.51, 1080p $3.78; first-frame and no-flight NOT guaranteed); (2) Kling i2v single 12 s with ceiling first frame (tilt proven) but its lips follow its own faster speech (0.4-0.9 s off our voice).

## C01 single take, Seedance 2.5 DRAFT 480p, 12 s (owner "да"; usage.cost 1.176, task c13cddf7; first submit 3a34e802 failed with a generic error at progress 0, cost not shown)
Voice for the new line "Oops, the ceiling. There. Welcome to Versailles. Yes, I'm that handsome. Try not to faint." made (0.23 RUB, 8.3 s, all words heard).
| Check | Result |
|--|--|
| Opens on the ceiling (reference image 1) | PASS: the ceiling holds 0-2.0 s, plume at the right edge, small shake |
| One take, no splice | PASS (single generation) |
| Rotation only, no flight | FAIL: phone_move_check cumulative scale +73.8 %; the king grows from small (2.3 s) to face-filling (4.0 s): the camera flies in |
| Landing frame matches C01 (reference image 2) | FAIL: lands on a tight selfie against the carved headboard, not the C01 framing |
| Speech after the camera lands | PARTLY: first word at 3.6 s while the camera is still settling (settles at 4.4 s) |
| Words | FAIL: "Yes, I'm that" is lost ("Hands-ansom"); the rest is clear |
| Follows our audio timing | NO: speech starts 1.3 s later than our drive audio (3.62 vs 2.28 s) and drifts, so our voice would need phrase alignment again |
| Faces / hands | face stable on model; no hands visible |
Status: draft GENERATED + INSPECTED, REJECTED (not shown as good). The 1080p final from this draft is NOT ordered.
Lesson: the one-take-with-audio route makes Seedance both re-time the speech and move the camera; the image-only route keeps first/last frames.

## C01 opening, owner: "the camera must move over the ceiling like a phone in a hand" and "the final version in 1080p" (29.10)
Built ceiling_handheld.py -> frames/C01_open_handheld.mp4 (1080x1920, 24 fps, 4.75 s, not committed): 1.7 s of the 2K ceiling still animated with a measured hand-held motion (drift +-30/52 px, roll +-0.7 deg, tremor; eased to rest at the junction) + Kling part 1 v2 from frame 0 (its tilt onto the king). Same 1.08 crop on both layers (no zoom change). Junction: frame differences 1.2, 1.1, 0.2, 2.0 (smooth, no pop); the first attempt cut at 0.4 s of Kling and popped (30 vs 1-2), fixed.
Soft notes: the plate motion is a 2-D drift (a distant planar ceiling under a rotating phone), so it has no parallax; the plume stays fixed to the lens edge from the still (a plume would move with the hand: acceptable). phone_move_check flags -15.6 % on the whole clip because the tilt changes the ceiling's perspective scale (known false positive for large pitch; the king's size is the real test, see part 1 v2).
Final delivery must be 1080p (owner). Part 2 plan: Seedance 2.5 Draft, image only (first frame = last frame of part 1 v2), draft 480p first, then the 1080p final from the approved draft; our voice aligned to its speech by phrase.

## C01 part 2, Seedance 2.5 Draft 480p, IMAGE-ONLY, 9 s (owner "да"; usage.cost 0.882, task 1b3b4511)
First frame = the last frame of the approved hand-held opening. Status: draft GENERATED + INSPECTED, good enough to order the 1080p final; NOT final.
| Check | Result |
|--|--|
| First frame equals the end of the opening | PASS (frame diff 3.3 at 480p vs 1-3 between neighbours): no splice at the start of speech |
| Camera flight | PASS: cumulative scale +0.3 %, mean frame diff 2.0 (steady, micro-shake only) |
| All words | PASS: "Oops, the ceiling. There. Welcome to Versailles. Yes, I'm that handsome. Try not to faint." (the transcript hears "zad -ansom" in our voice because of the respelling, the model said "that handsome") |
| Speech after the camera has landed | PASS: first word at 0.56 s of part 2 (the opening already holds still about 1 s) |
| Lips vs our voice | our voice aligned phrase by phrase to the model's speech (rough_c01b.py): residual 0.00-0.06 s on 12 of 15 words, 0.15-0.28 s on "the ceiling" and 0.22 s on "handsome"; tempo 0.81x on "Oops the ceiling", 1.25-1.3x on "welcome to Versailles" and "I'm that handsome" (audible but mild) |
| Face / identity | stable; expressions follow the prompt (startled, smug, smirk) |
Rough cut frames/C01_rough_v2.mp4 (not committed): opening 4.75 s + draft part 2 (480p upscaled for the check), 24 fps. The 1080p final of part 2 is NOT ordered yet: price not shown by the service.

## C01 part 2 FINAL 1080p, Seedance 2.5 Draft -> final (owner "да", cap $5; usage.cost 4.87746, task 051aa580; the first final submit de1968ed failed with a generic error, cost not shown)
Cost note: $0.542 per second at 1080p (draft $0.098/s): the 1080p final is the expensive step. Spent on the C01 final line: draft 0.882 + final 4.877.
Inspection (1080x1920, 24 fps, 9.04 s): first frame vs the end of the hand-held opening 1.4 (neighbour frames 1-3) = NO splice; camera scale +0.3 % (steady); mean frame diff 1.7; same speech as the approved draft (onset 0.94 s by energy; "Oops, the ceiling. There. Welcome to Versailles. Yes, I'm that handsome. Try not to faint."); face, wig, gown stable on 4 full-res crops (startled, annoyed, grin, smirk); hands not in frame.
Assembled frames/C01_final_v1.mp4 (not committed) = hand-held opening 4.75 s + final part 2, OUR voice aligned phrase by phrase to the model's speech (build_c01_final.py): residual 0.00-0.08 s on 14 of 15 words, 0.24 s on "handsome"; tempo 1.25-1.3x on "Welcome to Versailles" and "I'm that handsome". 13.79 s, 24 fps, 0 duplicate frames, seam diffs 1.3-3.1, last frame luma 111 (not black), audio = our locked voice only (model audio dropped), no music; loudness -14.9 LUFS, true peak -1.5 dBFS (target -14 / -1.5).
FAIL to fix (no subtitles, must be clear by ear): the ASR hears "that's awesome" for "that handsome" (respelling "zad 'ansom" plus the 1.3x tempo). Respelling exceptions for C01 ("that", "handsome") added to voice_lock.json; re-voice C01 (0.23 RUB) and re-align, 0 video cost.
Status: C01 video GENERATED + INSPECTED; the voice line needs the re-voice before APPROVED. Authenticity audit runs on the finished episode, not per clip.

## C01 FINAL v2 (voice re-done, 29.10, 0.23 RUB): frames/C01_final_v2.mp4 (not committed)
Re-voice with respelling off for "that" and "handsome" (C01 exceptions). Our take is clear (ASR on the unstretched take: "Oops, the ceiling. There, welcome to Versailles. Yes, I'm that handsome. Try not to faint."). Tempo capped at 1.15x (was 1.3x) so words stay intelligible; residual lip offset max 0.19 s (on "handsome"), 0.00-0.07 s elsewhere. In the assembled file ASR hears every word except the short "I'm" (lost at 1.15x): FLAG, owner's ear decides. 1080x1920, 24 fps, 13.79 s, loudness -14.9 LUFS, true peak -1.9 dBFS, our voice only, no music, 0 duplicate frames, no splice at the speech start.
Status: GENERATED + INSPECTED, awaiting owner approval. Disk was full during the check (a larger recognition model could not be downloaded; small model used): the recognition is the weaker one.

## FULL CHECK 29.10 (owner: "проверь всё"), results
PASS: project validator VALID; no video files tracked in git; no secrets in committed history_channel files or CLAUDE.md (key files ignored); no music anywhere (grep); every line consistent between lines_ep1_emotion.json, script_full, script_ru, storyboard captions and recording_sheet (3 "misses" were formatting only: 357 vs spelled-out number, the laugh tag, the signature-opener marker); C01 final: 1080x1920, 24 fps, H.264 + AAC, one audio stream, no tags, -14.9 LUFS, TP -1.9, 0 duplicate frames, no seam, camera steady, face/wig/gown consistent on 6 full-res frames.
FIXED during the check: (1) the spend ledger said "about $13.0" and "nothing generated yet": recomputed = $12.4 confirmed (images 0.90 + video 11.46 + voice 4.79 RUB), plus NOT VERIFIED up to about $8 for 3 failed Kling r2v tasks and 2 failed Seedance 2.5 submits; (2) the timeline: C01 is 13.8 s, not 12, so all later clips +2 s, runtime about 2:08 (scripts, RU script, storyboard updated); (3) the stale C01 method text in script_full.
OPEN (not done, needs the owner or later steps):
1. C01 is a clip, not the episode: no AI mark in the corner, no title chip "VERSAILLES, FRANCE · 1685" yet (edit layer, done at the end).
2. Authenticity audit (authenticity-check) not run: mandatory on the FINAL episode before delivery/upload.
3. Soft: at 5.6 s the eyes roll up showing white (the startled "Oops" beat): acceptable, owner's call; "I'm" is faint at 1.15x tempo.
4. Soft: the voice is a designed AI voice with a French accent; disclosed in the description and platform flags (to do in the publication package).
5. Disk is full (166 MB free): large models/new clips need space; /home/claude holds about 21 GB of older projects (not touched, owner's decision).
6. Storyboard frames (22) and card v2 still NOT approved by the owner; C13 and C15 frames need regeneration (new prompts).
7. Cost of the remaining 13 clips with the fixed method about $65 (draft 0.8 + final 4.3 per 8 s): needs the owner's budget decision.

## C01 v3 attempt (owner 29.10: "упс он должен говорить когда камера смотрит на потолок"), free re-assembly: frames/C01_final_v3.mp4 (not committed)
Method (build_c01_v3.py, 0 cost): hand-held opening cut at Kling 2.3 s (opening 4.0 s), our "Oops, the ceiling." placed at 0.45 s over the ceiling; part 2 = the Seedance 1080p final from 2.6 s (skips the model's own "Oops"), xfade 0.15 s; the other phrases aligned to the model's lips (residual max 0.19 s). 10.25 s.
Check: "Oops" now over the ceiling = PASS. Join at about 3.9 s = FAIL: frame diffs 7.7-8.5 against the clip median 2.3, a dissolve ghost and a jump in expression (smirk -> mid-sentence) on frames 3.70/3.84/3.92/4.05 s. That breaks the owner's no-splice rule, so v3 is REJECTED and not shown.
Clean fix (needs the owner's "да"): new Seedance 2.5 Draft image-only part 2 from the exact last frame of the 4.0 s opening, speech only "There. Welcome to Versailles. Yes, I'm that handsome. Try not to faint.", 7 s: draft about $0.69 + 1080p final about $3.79 = about $4.5.

## C01 v4 DRAFT (owner "да" 29.10, about $4.5 total; draft usage.cost 0.686, task 8c3f3d4f): part 2 from the landed frame
seedance25_part2_v4.py: image-only Seedance 2.5 Draft 480p, 7 s, first frame = frame 95 of C01_open_handheld.mp4 (camera landed at 3.7 s), speech "There. Welcome to Versailles. Yes, I'm that handsome. Try not to faint." Rough cut frames/C01_rough_v4.mp4 (not committed, build_c01_v4.py): opening 4.0 s + draft (upscaled for the check), plain concat.
| Check | Result |
|--|--|
| "Oops, the ceiling" over the ceiling | PASS: our voice 0.53-1.8 s, camera still on the ceiling (tilt 1.7-3.7 s) |
| Splice at the join (4.0 s) | PASS: frame diff 3.3 vs neighbours 2.9-3.7, no dissolve, same expression |
| Speech starts after landing | PASS: the model's lips start at 0.58 s of part 2 (4.58 s), camera landed at 3.7 s |
| Lips vs our voice | PASS: residual 0.00-0.13 s, tempo max 1.15x |
| All words by ear (ASR on the cut) | PASS: every word incl. "I'm" |
| Camera | FLAG: in 0.3-1.2 s of part 2 the phone re-centres him (pans and comes about 12 % closer, smooth, then steady). Reads as the arm settling the selfie on "There"; not the +74/141 % flight of the rejected takes. Owner's eye decides |
| Face / wig / gown | stable on 8 frames |
| Loudness | -15.1 LUFS, TP -1.9 (final mix normalises again) |
| Format | 11.04 s, 24 fps, last frame luma 118 |
Status: GENERATED + INSPECTED (draft). 1080p final (about $3.79) waits for the owner's look at the draft.

## C01 FINAL v4 1080p (owner "да" after the draft; first final submit 4a37025a failed with a generic error, cost not shown; retry f94ba318 usage.cost 3.79358): frames/C01_final_v4.mp4 (not committed)
build_c01_v4.py: opening 4.0 s + Seedance 2.5 1080p final part 2 (frame 0 dropped: it repeated the opening's last frame), plain concat; our locked voice: "Oops, the ceiling" at 0.5-1.8 s over the ceiling, the rest aligned to the lips (residual max 0.13 s, tempo max 1.15x).
Checks: 1080x1920, 24 fps, H.264 + AAC, 11.00 s; join frame diff 4.1 vs neighbours 2.9-3.4 (no splice, no repeated frame); near-duplicate frames only at 1.67 s (opening ease), 9.3-9.5 s (he holds still between phrases) and the last frame; ASR hears every word ("Oops, the ceiling! There, welcome to Versailles. Yes, I'm that handsome! Try not to faint."); -15.1 LUFS, TP -1.9; our voice only, no music, no subtitles; face, wig, gown consistent on 6 frames + full-res face crop; camera: the same re-centring of the selfie on "There" as the approved draft (+12 %, smooth, then steady).
Status: GENERATED + INSPECTED, awaiting the owner's approval.

Owner 29.10 after C01 v4 final: "дальше" -> C01 v4 taken as accepted (APPROVED by the owner's go-ahead); timeline shifted -3 s (C01 0-11, ... C15 115-125, runtime about 2:05) in script_full, script_ru, make_storyboard (storyboards re-rendered). Rejected/rough C01 renders deleted locally to free disk (192 MB free).

## C02 DRAFT (owner "да" 29.10, about $5.8 total; draft usage.cost 0.882, task df6b6803)
seedance25_c02.py: image-only Seedance 2.5 Draft 480p, 9 s, first frame = the last frame of the approved C01 (frames/C02_first.jpg). build_clip.py (new, generic): our C02 voice placed by sentence on the model's phrases found by energy (Whisper word times drift on this clip), tempo max 1.15x, centred when still longer. Rough frames/C02_rough.mp4 and preview C01+C02 frames/C02_rough_with_prev.mp4 (not committed).
| Check | Result |
|--|--|
| Join C01 -> C02 | PASS: frame diff 2.7 vs neighbours 0.5-2.5, same framing, same expression |
| Camera | PASS: +4.1 %, rotation-like (selfie stays put; he leans in on the secret, as planned) |
| Action | PASS: touches a curl with the ringed hand (0.3-1.8 s), leans in, tiny head tilt, pleased smile at the end; the hand mirror is not shown (dropped, no loss) |
| Lips vs our voice | offset max 0.18 s at sentence edges (C01 accepted 0.19), "The ceremony is called the rising" 0.00 |
| Words by ear (ASR on the cut) | PASS: "Some mornings, a hundred people watch me wake up. The ceremony is called The Rising. I call it Opening Night." |
| Face / wig / gown | consistent with C01 on 7 frames (480p) |
| Loudness | -15.7 LUFS, TP -1.9 |
| Pace note | silent beat 0-2.1 s (the curl gesture) before the first word: owner's call (the edit can keep it, it is an action beat) |
Status: GENERATED + INSPECTED (draft). 1080p final about $4.88 after the owner's look.

## C02 FINAL 1080p (owner "да"; usage.cost 4.87746, task d3c9695c): frames/C02_final.mp4, preview C01+C02 frames/C02_final_with_prev.mp4 (not committed)
Checks: 1080x1920, 24 fps, 9.00 s, 0 duplicate frames; join C01 -> C02 frame diff 1.7 vs neighbours 0.5-1.7 (no cut visible); camera +4.5 % rotation-like (selfie steady, he leans in); lips offset max 0.18 s; ASR on C01+C02 hears every C02 word (and reads C01's "Oops, the ceiling" as "Oops, there's a ceiling": small-model slip, the single-file check heard "the ceiling"); -15.3 LUFS, TP -1.9; our voice only, no music, no subtitles; ringed hand on the curl, lean-in, pleased smile; face, wig, gown consistent with C01 (6 frames + full-res crop).
Status: GENERATED + INSPECTED, awaiting the owner's approval.

## C03 DRAFT (owner "Да" 29.10, about $5.1 total; draft usage.cost 0.784, task 9b1495d9)
First frame = last frame of C02 final. build_clip.py now aligns by word index when the model's and our word counts match (energy phrases, words assigned by midpoint).
| Check | Result |
|--|--|
| Join C02 -> C03 | PASS: frame diff 2.4 vs neighbours 0.9-2.3 |
| Camera | PASS: +2.9 %, rotation-like |
| Action | PASS: the doctor and the surgeon walk in from the door (0.5 s) and stand behind; he looks at them over his shoulder (0.5-2 s), turns back, smug at the lens, slow "Naturally" with a smile |
| FAIL (fact look) | the doctor wears a RED skullcap and red trim: reads as a CARDINAL, not a royal physician (black robe, black cap). Fix = re-draft with "black cap, no red" (about $0.78) or accept |
| Lips vs our voice | offset 0.24 s on the long first sentence (model speaks it without pauses), 0.13 and 0.00 on the rest: soft |
| Words by ear | PASS: every word |
| Loudness | -14.5 LUFS |
Status: GENERATED + INSPECTED (draft), not approved.
Owner 29.10: C03 "как есть" (red cap accepted as is); 4K: no paid upscale chosen yet. C03 1080p final ordered.
C03 final: the first submit died with RemoteDisconnected before a task id came back (a server-side task and charge are NOT VERIFIED); resubmitted once.

## C03 FINAL 1080p (owner "как есть"; usage.cost 4.33552, task 10e5805d): frames/C03_final.mp4, preview C02+C03 frames/C03_final_with_prev.mp4 (not committed)
Checks: 1080x1920, 24 fps, 8.00 s; join C02 -> C03 frame diff 1.7 vs neighbours 0.9-2.0; camera +4.3 % rotation-like; lips offset 0.22 / 0.11 / 0.00 s (the long first sentence has no pauses); ASR hears every word; -14.8 LUFS, TP -1.9; our voice only, no music, no subtitles; the doctor (red cap, accepted by the owner) and the surgeon walk in and stand behind; last 0.6 s is a slow settling smile (frame diff 0.2-0.5, not frozen; C04 is a hard cut anyway).
Status: GENERATED + INSPECTED, awaiting the owner's approval.

## CHECK 29.10 (owner: "Проверь"), C01+C02+C03 assembled = frames/EP1_0-27_check.mp4 (not committed), 28.0 s
PASS: 1080x1920, 24 fps, H.264 + AAC 48 kHz; joins at 11.0 s and 20.0 s invisible (frame diffs 1.3-1.7 vs clip median 2.1) and silent at the cut (no clicks); loudness -14.9 LUFS, TP -1.9, LRA 5.6 (per clip -15.1 / -15.7 / -14.5, within 1.2 LU); motion spikes only at 4.4-5.1 s (the selfie re-centring in C01, approved) and 12.6-12.9 s (hand at the curl in C02): frames inspected, no warping or glitches; face, wig and gown consistent C01 -> C03; one self-praise line only (C01 opener); no music, no subtitles.
FIXED: C02 is 9 s, not 8, so the timeline is +1 s from C03 on (C02 11-20, C03 20-28, ... C15 116-126, runtime about 2:06) in script_full, script_ru, make_storyboard (storyboards re-rendered).
CONFIRMED RISK for C04: the storyboard frame C04.jpg shows a different face (older, darker, a beauty mark, thinner moustache) than the generated king of C01-C03 (side-by-side crops checked). C04 needs a new first frame made from the C03 face before any video.
OPEN (edit layer at the end): the audio is mono (fine for Shorts; a stereo export is an option); the AI mark and the title chip are not on yet; authenticity audit on the finished episode.

## C04 frame + DRAFT (owner "Да" 29.10): frame 0.04 (C04_v2.jpg, the C01-C03 king at the wig table, face/wig/gown match), draft usage.cost 0.784 (task f152c2d2)
| Check | Result |
|--|--|
| Face / wig / gown vs C01-C03 | PASS (frame and 8 draft frames) |
| Camera | PASS: -1.2 %, phone propped, still |
| Action | PASS: lifts the dark wig, hand on chest, mock-tragic face |
| Words | FAIL: the model skipped "I took it personally" (it says "Now, the wig. My hair started falling out at seventeen ... so I got a wig."): our full line cannot be lip-synced (1.1 s of words over a 0.3 s mouth movement) |
Status: GENERATED + INSPECTED, REJECTED (missing phrase). Corrective attempt 1 of max 2: re-draft with the full line stressed (9 s, about $0.88) after the owner's yes.

## C04 v2 (owner "Делай сразу 1080"): draft 0.882 (task 0e8e6c3c) auto-checked (every word present) -> 1080p final 4.87746 (task b30ad807): frames/C04_final.mp4, preview C03+C04 frames/C04_final_with_prev.mp4 (not committed)
Checks: 1080x1920, 24 fps, 9.00 s; hard cut from C03 (planned scene change, frame diff 70.9 at the cut); camera -4.0 % (phone propped, still); every word by ASR ("Now the wig. My hair started falling out at 17. I took it personally so I got a wig"); lips offset max 0.09 s after a build_clip fix (word mode now spans the whole clip, so short phrases like "Now, the wig" are not dropped; C02/C03 offsets unchanged 0.18/0.22); -14.9 LUFS, TP -1.8; face, wig, gown match C01-C03; lifts the dark wig, hand on chest, mock-tragic brow; our voice only, no music, no subtitles.
Status: GENERATED + INSPECTED, awaiting the owner's approval.

## C05 on Veo 3.1 quality 1080p (owner 29.10: "сразу финальную" + "which model is cheaper"): APIpod live prices: Seedance 2.5 i2v 1080p $0.542/s (= our draft-route final), Kling 4.0 i2v $0.2175/s, Veo 3.1 quality about $0.8-1 per 8-s clip (charged 1.00), Veo 3.1 fast about $0.18+.
veo_clip.py (new). First frame = last frame of C04 final.
- try 1 (task 0ea5ad36, $1): REJECTED: the shirt turns into a ruffled jabot at 2.2-2.8 s and he laughs wide-mouthed (not "lofty, smug").
- try 2 (task 5636e638): blocked by the provider's content filter (no charge shown); wording softened.
- try 3 (task ad94e576, $1): KEPT, cut to 6.8 s (from 7.0 s he stands up and walks away). Lips offset 0.00 s; calm haughty half-smile; same face, wig, gown; the lace shirt front was already in C01-C04; camera +10 % = he leans in, phone still; -15.2 LUFS; ASR hears every word.
build_clip.py fix: our voice is cut at word borders (a 0.10-s tail had copied the start of the next word: ASR heard "It makes, it makes"). C02-C05 rebuilt; offsets unchanged (0.18 / 0.22 / 0.09 / 0.00), every word heard once.
Status C05: GENERATED + INSPECTED, awaiting the owner's approval. Note: Veo drifts wardrobe more than Seedance (2 of 2 takes changed the shirt); per clip cost about $1 vs $4.3-5.2.
Owner 29.10: "Перед генерации спрашивай всегда": every generation call needs its own yes (retries, re-takes, draft->final included). Rule added to CLAUDE.md. Earlier this day without a separate yes: C03 final resubmit after a network error, C04 v2 auto draft->final chain, C05 Veo re-takes (tries 2 and 3).

## CHECK C04+C05 (owner: "проверяй"), frames/C05_final_with_prev.mp4, 15.8 s
PASS: 1080x1920, 24 fps; join at 9.0 s invisible (3 frames around it inspected: same pose, wig, hand) and silent; no frozen frames; motion spikes only at 0.42 s and 7.96 s (fast gestures: wig lift, hand to chest; frames inspected, no glitches); -15.4 LUFS, TP -1.7, LRA 2.6; every word by ASR (the small model writes "looked down" for "look down"); lips: C04 0.09 s, C05 0.00 s.
SOFT (owner's eye): the Veo face in C05 is a little rounder, with thinner brows and a softer moustache than the Seedance face of C01-C04 (full-res crops side by side). Same wig, gown, room; at phone size it reads as the same man, but it is a model difference.
Not done yet (edit layer): mono audio (stereo export option), AI mark, title chip, authenticity audit on the full episode.

## C05 redo on Seedance 2.5 i2v DIRECT 1080p (owner "Да, 2"; usage.cost 4.33552, task c4e682fa): frames/seedance25_c05_1080.mp4
| Check | Result |
|--|--|
| Face vs C01-C04 | PASS: the Seedance face is back (full-res crops side by side) |
| Words, lips | PASS: every word, offset 0.00 s |
| Camera | PASS: +0.3 % |
| FIRST FRAME | FAIL: the direct i2v route did NOT start on the given frame: frame 0 is re-framed (closer, lower, stands shifted, eyes closed), so C04 -> C05 is a visible jump (frame diff 26 vs 2-3). The draft route (seedance-2.5-draft, image-only) kept the exact first frame in C01-C04; I assumed the direct route behaves the same and did not verify it: my error, $4.34 |
| Pace | 3.0 s of silence (eyes closed, sigh) before the first word; the clip is very still (median frame diff 0.5) |
Free variant built: frames/C05_final_jumpcut.mp4 = the same take from 2.6 s (5.4 s): it reads as a vlog jump cut into a closer shot, speech starts at once; the jump is still a visible edit.
Status: GENERATED + INSPECTED; join FAIL against the no-visible-splice rule. Options for the owner: (a) keep the jump cut (free), (b) draft route draft + final (about $0.78 + $4.34, exact first frame proven), (c) back to the Veo take (different face).
Owner 29.10: "Нормально дальше" -> C05 = the jump-cut variant (frames/C05_final.mp4, 5.4 s), accepted. C06 first frame = last frame of seedance25_c05_1080.mp4 (frames/C06_first.jpg).

## C06 DRAFT, reference manner (owner "Да"; usage.cost 0.882, task 18f5f0ab): rough frames/C06_rough_with_prev.mp4 (not committed)
| Gate | Result |
|--|--|
| Join C05 -> C06 | PASS: frame diff 2.7 vs neighbours 0.2-1.4 |
| Camera moves (reference) | PASS: he picks the phone up from the table (0-2 s), then hand-held selfie with sway; camera path 130/88 px; motion per second 2.5-14 (reference calm 2-4, action higher) |
| Flight check | FLAG: scale +46 % = the pick-up (the phone lifts from the table into his hand, the move is motivated and visible); owner's eye |
| Phone mistake | PASS: the white wig fills the lens (2.5-4 s) |
| Words | PASS: every word by ASR |
| Lips | offset 0.10-0.20 s, 0.30 s on "One day" (soft) |
| Face / wig / gown | face and brown wig match; the shirt front reads more ruffled than in C04 (lace already in C05): soft |
Status: GENERATED + INSPECTED (draft). 1080p final about $4.88 = separate yes.

## C06 FINAL 1080p (owner "Да"; usage.cost 4.87746, task 05e42d44): frames/C06_final.mp4, preview C05+C06 frames/C06_final_with_prev.mp4 (not committed)
Checks: 1080x1920, 24 fps, 9.00 s, 0 duplicate frames; join C05 -> C06 frame diff 2.2 vs neighbours 0.2-1.4; reference-manner gates PASS (pick-up of the phone, hand-held sway, the white wig covers the lens at 3.5 s, lively motion); lips 0.10-0.21 s, 0.30 s on "One day" (soft, same as the draft); every word by ASR; -15.6 LUFS, TP -1.9; face/brown wig consistent (full-res crop); our voice only, no music, no subtitles.
Status: GENERATED + INSPECTED, awaiting the owner's approval.

## C07 first frame (owner "Да", 0.04, task 27c95af6): frames/C07_v2.jpg, gen_c07_frame.py
Hard cut into take 3 (court enters): low floor angle, the generated king in the tall white-grey wig and gold gown, a hand sweeping in from the top, courtiers entering at the back. Face matches C06 (identity ref = frames/C06_last.jpg). Inspected at preview size, not yet at full res: GENERATED + INSPECTED (preview), not approved.
Page voice (line "The court, Sire."): free audition of 6 Lumean library voices built (voice/page_voices_audition.mp3, shortlist voice/page_voice_shortlist.json); no order placed, waiting for the owner's pick and a separate yes for the order (about 0.3 RUB).

## First frames v3 from the face master (owner "Да, запускай"; 7 x 0.04 = 0.28, nano-banana-2.1 2K, gen_frames_v3.py): frames/C07_v3 C09_v3 C10_v3 C12_v3 C13_v3 C14_v3 C15_v3.jpg
Refs: face_front_talking + face_three_quarter + the storyboard frame as composition; fixed descriptor block; "not older, no rouge". Side-by-side sheet: frames/first_frames_v3_vs_master.jpg.
Our inspection (full frames at 560 px, face crops not reliable): the features (narrow face, long straight nose, thin upturned moustache, light eyes) are closer to the video king than the old storyboard frames (no pink rouge, no beauty-spot-heavy older face); BUT with the tall white wig the face reads older and harder than the video king: closest C07 and C12; weaker C13, C14, C15 (stern, older). C09 face is hidden by the wig at the crop (frame check pending). NOT APPROVED by the owner; no video ordered from them.

## First frames v4 (owner "Да" after the expert review; 6 x 0.04 = 0.24; C09 refused at submit by the provider's content filter, no charge): frames/C07 C10 C12 C13 C14 C15 _v4.jpg, gen_frames_v4.py
Fixes vs v3: the white wig is the one from C06 (cropped from C06 5.2 s, louis_card/face_master_v3/white_wig_C06.jpg: smooth top, side rolls, black bow), no towering wig; faces larger (C12-C15 close selfies); smug half-smile.
Face check (crops at measured positions, frames/first_frames_v4_faces.jpg): C12, C13, C14 match the master (narrow face, long straight nose, upturned moustache, light eyes, beauty spot by the mouth), age reads a little older only because the master is laughing; C15 same man, nose and face stretched by the ultra-wide lens close-up (phone look, soft); C07, C10 small faces, same features. Wig continuity with C06: PASS. NOT APPROVED by the owner yet.

## First frames v5 (owner "Да"; wig = the tall powdered wig of the old C09, owner "На с09"; 7 x 0.04 = 0.28, gen_frames_v5.py): frames/C07 C09 C10 C12 C13 C14 C15 _v5.jpg; sheets frames/first_frames_v5.jpg, frames/first_frames_v5_faces.jpg
Wig: matches the C09 reference on all 7 (high wavy crown, side rolls, long curls to the chest). Face (crops at measured positions vs the master): same features on all 7 (narrow face, long straight nose, upturned waxed moustache, light eyes, beauty spot by the mouth); reads about 5 years older than the laughing master; a light pink flush on the cheeks in C09, C12, C13 despite "no rouge" (soft); C10 face small and a little broader (soft). NOT APPROVED by the owner yet; no video ordered.

## First frames v6, close hand-held selfies (owner 29.10 "делай как референс: камера близко к лицу и ходит в руке"; "Да"): C09_v6, C10_v6 (2 x 0.04); C07 refused at submit by the content filter (no charge), prompt reworded, resubmit needs a separate yes.
C09: close selfie, face and wig large, courtiers bowing behind, the plumed hat on the floor; C10: close face, the red heel and buckle in the foreground. Face matches the master, wig = C09 style. NOT APPROVED yet.
C07_v6 (resubmit after the owner's "Да", 0.04): close selfie, face matches, courtiers walking in behind: PASS (owner to approve).
C10_v6 leg check (owner: "проверь что за нога"): FAIL. The leg in white stocking enters from the RIGHT edge at chest height and runs off-frame to the right; it does not connect to his hips (he sits in the centre), so it reads as someone else's leg. Prompt rewritten (his own bent leg rising from his lap, from the bottom centre); redo needs a separate yes (about $0.04).

## Makeup standard v2 frames (owner "Да"; 5 x 0.04 = 0.20): C07_mk, C10_mk, C13_mk, C14_mk, C15_mk (+ C09_v6 and C12_v5 kept) = frames/first_frames_final_candidates.jpg, list in frames/FIRST_FRAMES_CURRENT.md
Powder: all 7 now white-powdered with pink rouge (C09, C12 slightly stronger rouge). Wig: C09 style on all. Face: master features on all. C10 leg: now his own bent leg (knee by the armrest, shin down to the shoe by the lens), attached to the body: PASS; note the whole sole looks red, not only the heel (soft). NOT APPROVED by the owner yet.

## CHECK of the 7 first frames vs each other and the reference (owner: "Проверь ещё раз и с референсом"), 29.10
Reference DNA used: close hand-held selfie MCU with the arm visible, ultra-wide distortion, soft daylight + warm interior, the white-lead court makeup (Elizabeth), the face about 1/3 of the frame width (frames_vlog1_LjfGP7wpjVs.md, one_link_studio_lBkoOcM-r5k.md).
PASS: framing (C07, C09, C12-C15 close selfies, the arm/hand visible in C07, C09, C10, C12; C10 a planned action shot); light and palette; makeup level; one face on all 7; one wig on all 7; hands (C07, C09, C13 ring hand cropped at full res: 5 fingers, rings sit on fingers); wardrobe logic (gold gown in take 3 before the dressing burst, scarlet sun coat in take 4 after it); background people without broken faces at preview size.
FAIL (continuity, must fix): C07 has an OPEN shirt with no cravat, while C09 and C10 (same take 3) have a lace jabot: the cravat would appear from nowhere between C08 and C09.
SOFT: C10 shows the whole sole red (a modern designer-shoe look); historically the red is on the heel; C13 and C14 are almost the same framing back to back (the reference changes the setup at every cut); rouge a little stronger in C09 and C12.
Proposed: redo C07 (jabot), C10 (red heel only, sole dark leather), C14 (a different setup: a wider shot at the gallery doors pointing at the lens): 3 x 0.04, needs a yes.

## First frames v7 (owner "Да"; 7 x 0.04 = 0.28, gen_frames_v7.py): frames/first_frames_v7.jpg
C07 jabot now present (continuity with C09/C10 PASS); C09 deliberately badly framed (half the face cut by the left edge), the hat gag fully visible: PASS; C10 red heel, sole dark leather, leg attached: PASS; C13 far too close, the wig cut at the top, courtier behind: PASS; C14 a new wider setup at the gallery doors, pointing at the lens: PASS (differs from C13); C15 the hand mirror covers the lower right, face off-centre: PASS. Face and makeup consistent on all 7.
SOFT: C12 the "courtiers already wear copies of his tall wig" payoff is NOT visible (background courtiers wear ordinary small wigs); options: accept, or redo C12 (about $0.04).
NOT APPROVED by the owner yet.
C12 redo (owner "Перерисуй C12", 0.04): two courtiers right behind his shoulders wear copies of his tall powdered wig, in focus: the spine payoff is now visible: PASS. Previous C12 kept as C12_v7a.jpg.
Owner 29.10: "у придворных должны быть простые парики, звезда тут один" -> C12_v7.jpg (copies) REJECTED, C12_v7a.jpg (simple wigs) is the C12 first frame; the copies payoff removed from both scripts. No new generation.

## C07 FINAL 720p (owner "Давай сразу чистовик на 720п"; Seedance 2.5 i2v direct 720p, usage.cost 1.764, task 7ae2a252): frames/C07_final.mp4 (upscaled to 1080x1920 for the edit), preview frames/C07_final_with_prev.mp4 (not committed)
Hard cut from C06 (planned). Camera (camera_plan_ep1.md): PASS: the phone wobbles, swings with his shoulder as he turns to the court (1.2-3.8 s, we see the back of the wig while he says "Bow. Lower. Good."), turns back and comes far too close while he taps the wig (5.5-8 s); motion 4.7-14 per second, path 71/23 px; the +38 % scale = the motivated too-close re-centre (arm), frames 0.4-6.0 s inspected: smooth, no morph. Face, wig, makeup, jabot as the v7 frame. Lips 0.00-0.14 s. Words by ASR: see below.
Status: GENERATED + INSPECTED, awaiting the owner's approval.

## C08 direct 720p (owner "Да, сразу чистовик 720п"; Seedance 2.5 i2v direct, usage.cost 1.764, task 1fe14524): frames/seedance25_c08_720.mp4, preview frames/C08_final_with_prev.mp4 (not committed)
| Check | Result |
|--|--|
| Camera push-in (camera plan C08) | PASS: from a medium shot to the face filling the frame, the tall wig cut by the top edge, a jolt on the snort (3-8 s) |
| Words | PASS by ASR: "All these people, and nobody may speak before me, I love listening to myself, mostly" |
| Lips vs our voice | 0.00-0.03 s on most phrases, 0.55 s on "to myself" (soft) |
| Join C07 -> C08 | FAIL: frame diff 60 vs 4-7 around it. C07 ends on a face close-up with the hand on the wig; C08 starts as a MEDIUM shot, standing back (the direct route did not keep the first frame, same as C05; my own warning, and the cause is the route, not the prompt) |
| Phone in his hand | FAIL: for the first 3 s the model draws a phone with a lit screen in his raised hand (0-3 s): he is filming with that phone, it cannot be seen |
| Face | same man; in the close-up (3-8 s) the rouge and the smile read a little stronger (soft) |
Status: GENERATED + INSPECTED, REJECTED for the join and the phone. Free partial rescue is NOT possible (the first 3 s carry "All these people, and nobody may speak before me"). Corrective attempt 1: draft route from the exact last frame of the C07 take (draft 480p about $0.78, final 720p about $1.76 if the draft route allows 720p, otherwise 1080p about $4.34): needs the owner's yes.

## C08 DRAFT via the draft route (owner "Да"; usage.cost 0.784, task 52a589db): frames/seedance25_c08d_draft.mp4, rough frames/C08_rough_with_prev.mp4 (not committed)
Join C07 -> C08: PASS (frame diff 7.7 vs neighbours 4-8; it starts from the exact last frame of the C07 take). No phone in his hand: PASS. Camera: PASS: he lets go of the wig, the room and the bowing court show behind him (1-2 s), then the phone creeps in until his face fills the frame and the wig is cut by the top edge (3-8 s), a jolt on the snort; scale +72 % = the push-in by his arm, motion 4-12 per second. Words PASS by ASR. Lips 0.00-0.04 s, 0.24 s on "to myself" (soft). Face same man; rouge and smile strong in the close-up (soft). 
Status: GENERATED + INSPECTED (draft 480p). Final: 720p about $1.76 if the draft route accepts 720p, else 1080p about $4.34: SEPARATE yes.
C08 final 720p from the draft (owner "Да 720п"): API refused ("final video from draft_task_id supports only 1080p"), validation error, no charge. Options for the owner: 1080p final about $4.34 (guaranteed join), or a new direct 720p take (about $1.76, join risk as in C05/C08).

## C08 FINAL 1080p via the draft route (owner "1"; usage.cost 4.33552, task a1e463b9): frames/C08_final.mp4, preview C07+C08 frames/C08_final_with_prev.mp4 (not committed); build_c08_manual.py (the automatic fit failed: the model speaks in 3 runs and our voice has a long laugh)
Checks: 1080x1920, 24 fps, 8.00 s, 0 duplicate frames; join C07 -> C08 frame diff 8.2 vs neighbours 4-9 (no jump, starts from the exact last frame of the C07 take); no phone in his hand; camera: he lets go of the wig, the court bows behind him (1-2 s), the phone creeps in until the face fills the frame and the wig is cut at the top (3-8 s), a jolt on the snort; every word by ASR; -15.2 LUFS, TP -1.9; our voice only, no music, no subtitles; face = the master, the court rouge and the smile a little strong in the close-up (soft).
Lips vs our voice: P1 1.10-3.39 vs 1.16-3.50, P2 4.45-5.22 vs 4.48-5.22 (PASS); P3 "to myself, mostly" 6.3-7.95 vs lips 6.73-8.03: our "to myself" starts about 0.3-0.4 s before the model's lips (soft: the model's own snort covers 6.3-6.7; tempo 1.22 on the last unit, the laugh pause shortened).
Status: GENERATED + INSPECTED, awaiting the owner's approval.

## C09 video: the submit was REFUSED by APIpod ("insufficient quota", HTTP 500) at 29.10 after the C08 final; no task created, no charge. Most likely the APIpod balance is used up (confirmed spend today about $56.7 + earlier days); the balance cannot be read through the API (no balance endpoint). Needs a top-up by the owner or a different provider/credits. seedance25_c09.py is ready (direct 720p, 8 s, about $1.76).

## Voice check 30.10 (voice_check_ep1.md)
C07 lost the final "s" of "notes" at the clip end: fixed free by an L-cut into the silent start of C08: frames/C08_final_lcut.mp4 replaces C08_final.mp4 in the edit; ASR on the join "Take notes!" PASS. C09 line heard as "a hat": re-voice proposed (0.23 RUB, needs a yes). C12-C15 pitch about 4 semitones above C02-C10: check by ear when built.

## Sound bed C01-C08, 30.10 (owner "сделай сразу шум как в референсе"; sound_bed_ep1.md, build_bed.py; free, own synthesis)
Room tone + people murmur + foley on motion peaks; no silence >= 0.5 s at -50 dB in any clip (was 1.5-5.2 s each), floor -48.6 dB (reference -49.5), -14.8 LUFS, TP -4.2, ASR identical before/after, no tonal content. Files: frames/C0x_bed.mp4 (C08 uses the L-cut version) and frames/EP1_C01-C08_bed.mp4 (not committed). Status: GENERATED + MEASURED; ear check by the owner pending.

## Sound bed v2, 30.10 (owner on v1: "звук постоянно один и тот же")
v1 was a stationary hiss: rebuilt (sound_bed_ep1.md): breathing air in 4 bands, a crowd of synthetic voices, 18 kinds of events on motion peaks, story moments and random times (not over speech), a different mix per clip. Measured: no silence >= 0.5 s at -50 dB, -14.8 LUFS, TP -4.4, words identical (ASR medium). Ear check by the owner pending.

## Sound v3 "phone sound", 30.10 (owner: "в референсе звуки от телефона и от всего, у нас этого нет")
Reference audio re-analysed (sound_reference_vlog1.md: measured + vidIQ hypothesis): handling thumps/rubs, low-frequency phone-mic floor, proximity changes of the voice, darker mic colour, no music. Added to build_bed.py: rumble following the measured camera speed, grips/knocks on jerks and hand-set moments, phone-mic voice chain with distance from keyframes + measured zoom. Checks: words identical (ASR medium) in all 8 clips, no silence, -15.0 LUFS, TP -1.0. Ear check by the owner pending. The C03 "and" issue is still open (owner to choose a word/tag).

## C03 pause before the punchline, 30.10 (owner: "24-25 секунда как будто нужна пауза")
build_c03_manual.py: sentence 1 at tempo 1.2 (ends with the model's "them"), "Everyone came to see me," starts later: pause "them." -> "Everyone" 0.62 s (was 0.26 s); cost: that sentence is about 0.2 s after the model's lips. ASR medium: every word. Bed rebuilt (EP1_C01-C08_bed.mp4).

## Owner idea 30.10: "generation with sound, the model makes the right sounds, we add our voice"
Tested free on C01-C08: htdemucs (MIT, local CPU) splits each clip's own model audio into the model's speech and the rest. Result: the rest is almost silent (-60...-80 dB) in 6 of 8 clips; only C03 0-1 s and C06 (the wig hitting the lens) have real sounds. Reason: our Seedance prompts never asked for sound (only "No music"), so the model made speech only. No music found in the rest (bass stem -75...-84 dB).
Plan: (1) C09-C15: add a SOUND block to every Seedance prompt (phone handling at the mic, the room, the court, footsteps, fabric; no music), then remove the model's speech with htdemucs and lay our locked voice on top; no extra cost (audio is already generated). (2) C01-C08: real-sounding SFX from ElevenLabs Sound Effects via Lumean (about 0.05 RUB per sound, each needs the owner's yes), placed by me on the measured motion; or a video-to-audio model (MMAudio, about $0.001/s on fal.ai/muapi; we have no account there, licence of the weights to check).

## Sound v4: real recordings, 30.10 (owner on v3: "эхо и будто музыка какая-то, сравни ещё раз с референсом")
Cause of "music": the synthetic crowd (pulse-train voices = a tonal hum) and synthetic birds/clinks; cause of the echo: room reverb added to the voice. v4 (build_sound_v4.py) drops all synthesis and the voice reverb; beds and foley are real CC0 recordings (BigSoundBank, sfx/SOURCES.md): Chambord castle interiors, fireplace, door, parquet steps and squeaks, cloth, coat rubs, microphone taps (on camera jerks), key on wood. The phone-mic colour is applied to the whole scene, proximity to the voice (no reverb).
Measured vs reference: tonal peaks in quiet frames v4 median 9.3 / max 12.7 dB, reference 9.4 / 13.8 (no music); word level range 12.4 dB (ref 13.8); voice tail drop -0.5 dB = no echo tail added (the bed continues); no silence >= 0.5 s; -15.0 LUFS (ref -15.4), LRA 8.6 (ref 11.1), TP -1.2; quiet-floor centre 824 Hz (ref 170-624, v2 hiss 1-4 kHz); words identical in all 8 clips (ASR medium). C04 (phone propped far) is quieter, -18.6 LUFS, on purpose. Files frames/<clip>_snd.mp4, frames/EP1_C01-C08_snd.mp4 (not committed). Ear check by the owner pending. Lumean SFX refused (no subscription, no charge).

## C04 remake pilot on Seedance 2.5 Lite i2v, 30.10 (owner "а"; usage.cost 1.35, task ba3f30a3)
720x1278, 24 fps, 9.06 s, own audio. The model says the short line exactly; pauses 0.7 s and 3.06 s (asked 1 s). First frame close to C04_first.jpg (diff 7.2), not exact (hard cut, OK). Camera moves and settles (motion 9.7 -> 1.8). Picture: texture 1969, grain 3.03, brightness 100 ungraded (old C04: 645-1594) = more phone-like; face = the master (beauty spot, rings). Model's own sounds after htdemucs: quiet room -55...-66 dB, a knock at 4.5 s, no music (tonal peaks 8.8-14.3 dB like noise).
Build (build_c04_lite.py): our short line on the lips by speech-energy onsets (medium ASR; small ASR put "My" inside the sigh): offsets My +0.06, 17 +0.12, took -0.1, personally -0.06 s. Model sounds kept (+3 dB) under the v4 bed; lighter grade for Lite (GRADE_LITE). Bug found and fixed during the check: a placement line had slipped into a comment (silent voice); caught by ASR before showing.
Variants: A as generated (3 s silent beat), B jump cut removes 1.75 s of the pause. C04 -16.9/-17.1 LUFS, episode -15.0. Files frames/ab/C04_lite_A.mp4, C04_lite_B.mp4, EP1_C01-C08_v5_liteA/B.mp4 (not committed). Owner to choose.

## C04 Lite lip sync + sigh, 30.10 (owner chose A: "на 5 секунде вздох не попадает")
Cause: our voice had no sigh where the model's mouth sighs/says "ugh" (4.82-5.3 s), and "Now, the wig." was one unit although the model has two lip phrases (0.58 and 1.39 s): "wig" was 0.3 s early.
Fix (build_c04_lite.py): units "Now," 0.58 | "the wig." 1.39 | "My hair... 17." 2.55 | sigh 4.82 | "I took it personally." 7.94, tempo never below 1.0 (no slow-down), the sigh of our TTS (1.20-1.60 s of C04.mp3) placed on the model's sigh. Check vs the model's speech stem (50-ms frames): lips active while we are silent 7.1 % (before 2.3 %), we active while lips are silent 6.0 % (before 22.7 %); the remaining disagreements are single frames at phrase edges (0.1, 0.85-0.95, 1.75, 2.2, 4.6, 7.95, 8.35, 8.9 s). Phrase onsets 0.58/1.38/2.52/7.94 vs lips 0.58/1.39/2.55/7.94. Words by ASR medium all present; episode -15.0 LUFS, TP -1.3.
Files: frames/C04L_final_A.mp4, frames/ab/C04_lite_A2.mp4, EP1_C01-C08_v5_liteA.mp4 (not committed). Variant B dropped (its jump cut cuts through the sigh).

## C05 remake on Seedance 2.5 Lite, 30.10 (owner "да"; usage.cost 0.90, task 09a95ce2)
720x1278, 24 fps, 6.05 s. QC: first frame vs C05_first.jpg diff 5.8 (C04 pilot 7.2: close, not exact; C05 is now a jump cut after C04 anyway, so the old invisible C05 -> C06 join is no longer needed... see below); motion 8.5 -> 1.7 -> 4.6 per s (moves, settles, moves), no jumps (max 14.8, median 3.4); picture texture 1790, grain 2.75, brightness 99 (more phone-like than the old C05: texture about 1300). Model speech: "They say it makes me taller" 0.9-2.3 s, a silent beat with eyes closed 2.3-4.6 s, "I never look down" 4.7-5.85 s: exactly the pause I asked for. Own sounds: quiet room -46...-65 dB, no music.
Build (build_c05_lite.py): our short line on the model's two lip phrases by speech-energy onsets (30 % threshold; a breath at 0.3-0.8 s was fooling the 10 % one); our TTS sigh ("sighs contentedly") placed at 3.0 s into the closed-mouth beat (eyes closed). Lips vs voice (50-ms frames, each relative to its own peak): disagreements are single frames at phrase edges (0.35, 0.5, 1.55-1.8, 2.0-2.15, 5.3-5.75 s) and the sigh itself (3.0-3.15 s, mouth closed on purpose). Words all present (ASR medium). C05 -16.9 LUFS, episode -15.0 LUFS, TP -1.3, 68.1 s, no silence.
NOT VERIFIED: the join C04 -> C05 and C05 -> C06 by eye: C05 now ends on a different frame than C06's first frame (C06 was generated from the old C05's last frame): check as a hard cut; if it jars, regenerate C06 or keep the old C05. Files: frames/seedance25lite_c05.mp4, frames/C05L_final_A.mp4, EP1_C01-C08_v5_liteA.mp4, frames/ab/C04C05_lite.mp4 (not committed).

## C02 remake on Seedance 2.5 Lite, 30.10 (owner "да"; usage.cost 1.35, task 85fe89ed)
720x1278, 24 fps, 9.06 s. JOIN C01 -> C02: first frame vs the last frame of C01: numeric diff 6.4 (the old draft-route join was 1.7), but side by side the frames are the same picture (same pose, wig, gown, canopy, background people); the difference is the sharper Lite grain. Judged invisible by frames (the owner decides by eye).
Model: adjusts the curl with the ringed hand (0.5-2 s), a fast lean-in to the lens at 2.1-2.5 s (motion 13.5, max jump 22.2: the "sharing a secret" move), speaks "A hundred people watch me wake up" 2.7-4.5 s, a silent beat 4.5-5.9 s, "I call it" 6.0-6.8, "opening night" 7.4-8.2 s with a laugh. Texture 2001 (old C02 887), grain 2.97. Own sounds: room -48...-75 dB, a bump at 0-0.5 s and 2-3 s, no music.
Build (build_c02_lite.py): our short line on the three lip phrases by speech onsets. Lips vs voice by 50-ms frames (each vs its own peak): 11.6 % lips only / 29.6 % ours only, all single frames at phrase edges (ours runs about 0.2 s past the lips at 4.05-4.3 s and 7.95-8.2 s: the tempo clamp is 1.12). Words all present (ASR medium). C02 -14.1 LUFS, episode -15.0, TP -1.2, 68.2 s, no silence >= 0.5 s.
Files: frames/seedance25lite_c02.mp4, frames/C02L_final_A.mp4, frames/ab/C01C02_lite.mp4, EP1_C01-C08_v5_liteA.mp4 (not committed). The episode now has C02, C04, C05 on Lite; C03 (old, long line) sits between C02 and C04.

## C03 remake on Seedance 2.5 Lite, 30.10 (owner "да делай"; usage.cost 1.20, task 8edbe926)
First frame = the last frame of the new Lite C02 (frames/C03_first_lite.jpg), so the join C02 -> C03 continues the move (a very close face that eases back); first frame vs that frame diff 5.2. 720x1278, 24 fps, 8.04 s. Model: glances at the doctor and surgeon over his shoulder with the head turned (0.5-1.5 s), then back to the lens; five clean lip phrases: "The doctor" 0.5 | "The surgeon" 1.9 | "Nobody came to see them" 3.4 | silent smile 4.3-5.6 | "Everyone came for me" 5.7 | "Naturally" 7.2 s. The doctor and the surgeon (red cap) stand far behind. Motion 13.4 -> 1.3 per s, max jump 19.4. Texture 2102 (old C03 about 900), grain 3.0. Own sounds: room -58...-84 dB, no music.
Build (build_c03_lite.py): our short line on the five phrases. Phrase starts ours vs lips: 0.58/0.5, 2.02/1.9, 3.38/3.4, 5.64/5.7, 7.24/7.24 s; ours runs 0.1-0.4 s past the lips at the phrase ends (our drawl; the model's speech stem is quiet at the tails). The pause before "Everyone" is 1.3 s (old fix 0.62 s). No creaky "and": the line no longer has it. Words by ASR medium all present; C03 -17.1 LUFS, episode -15.0, TP -1.0, 68.2 s, no silence.
Episode now: C02, C03, C04, C05 on Lite (frames/EP1_C01-C08_v5_liteA.mp4, frames/ab/C02C03_lite.mp4, not committed); C01 and C06-C08 are the earlier takes. NOT VERIFIED: joins C02 -> C03 and C03 -> C04 (hard cut), C05 -> C06 by eye; the ear check.

## C09 first frame v8 with Marcel, 30.10 (owner "Да"; gen_c09_marcel.py, $0.04 usage.cost): frames/C09_v8.jpg. INSPECTED: the king's half face is cut by the left edge as designed (light eyes, upturned moustache, beauty spot, tall grey-white wig, heavy white powder: the master); the row of bowing courtiers in simple grey wigs and plain dark coats; Marcel (sky-blue coat with silver braid, small white wig with a black ribbon, round young face, alarmed look) stands in the middle of the row; a black plumed hat on the parquet in front of the row. Face check crop: frames/C09_v8_marcel_check.jpg (card front on the left, the frame on the right). Soft: Marcel stands leaning rather than bowing; the king's wig reads long and flowing (the series wig). NOT APPROVED by the owner. seedance25lite_c09.py now uses C09_v8.jpg.

## C09 on Seedance 2.5 Lite, 30.10 (owner "Да" to "C09 Lite, 720p, 8 s, about $1.20, one generation"; usage.cost 1.20, task 441f783d)
Status: GENERATED + INSPECTED, not APPROVED (owner has not seen it). 720x1286, 24 fps, 8.04 s, first frame frames/C09_v8.jpg.
Frames (2 fps sheet + 4 fps crops): 0-1.5 s the king (half face cut at the left edge as designed) talks to the bowing row, the page in the sky-blue coat watches in alarm; hat: it already lies on the parquet in the first frame, at about 1.5-2.3 s it tumbles and slides, the page bends and hurries after it (the hat does not fall off a head on camera: the model animated the hat that was on the floor); 2.3-4.4 s the king turns over his shoulder (the bowing row and the hat are in frame), mouth moving, then turns his head away at about 4.4 s; 4.5-6.2 s he turns back and yanks the phone to the face, 6.2-8.0 s large face, mouth moving to the last frame. No broken hands or feet seen in the row at this size; the page's run at 3.2-3.5 s is motion-blurred (not a defect I can name).
Marcel's face vs the card (crop frames/ab not made, scratchpad only): same type (slim boy, smooth skin, small white wig with black ribbon, sky-blue coat); in the frame he is narrower and less round than the card, freckles not visible at this size. Acceptable as a background person; NOT a copy of the card.
Model audio: speech stem has only the king's phrases: "Lower," 0.30-0.65 | "lower," 1.05-1.45 | "and there goes the hat" 2.95-4.65 | silence 4.65-6.5 | "Eyes on me, not on the hat" 6.5-7.9 (faint breath at 6.0-6.15). The model did NOT make a real "Pardon, Sire!" (only a faint blip at 2.5 s). Rest stem (htdemucs) is very quiet (peak -22 dB, hat-drop thump hardly separable): the room sounds will come from the real recordings in sound v4.
Build (build_c09_lite.py): our locked line laid on the lips, phrase borders and lengths measured on the energy of our own track (the first try used ASR word times and put the second "Lower" 0.4 s too long: caught on the energy map and fixed). Tempo: 1.25 / 1.25 / 0.80 / 1.09 (our phrase 3 is shorter than the model's slow deadpan: 1.38 s of speech vs lips 1.7 s, so the voice ends about 0.3 s before the lips; the king turns his head away at about 4.4 s, so it is not visible as a mismatch). Marcel's "Pardon, Sire!" (marcel_C09_pardon.mp3, 0.23 RUB order from earlier) at 1.83-2.71 s, gain 0.6 (further away), when the hat tumbles and he turns; his lips at that moment are NOT VERIFIED (he is half turned).
Measured on the final frames/C09L_final_A.mp4 (1080x1920, not committed): ASR medium: "Lower! Lower! Pardon, sire! And there goes the hat. Eyes on me, not on the hat." (all 14 + 2 words present); speech runs (-20 dB): 0.35-0.81, 1.13-1.68, 1.83-2.71 (Marcel), 2.92-4.33, 6.52-7.94; model lips onsets 0.30 / 1.05 / 2.95 / 6.50: within 0.06-0.08 s. Silence of voice 4.33-6.52 s (2.2 s): the pause before the joke is the model's own beat (the king turns back and yanks the phone), longer than the asked 1 s; option: jump-cut about 0.7 s of it (owner decides). Loudness -14.2 LUFS, TP -1.9 dBFS (AAC 320k), no clipping.
NOT VERIFIED: join C08 -> C09 (hard cut after the dressing burst, planned), C09 -> C10; the ear check; Marcel's lips at the cry. Not committed: the mp4 files.

## C09 Lite v2: sound re-fitted to the MOUTH, 30.10 (owner: "sound does not match")
The owner was right. v1 (above) was aligned to the onsets of the model's own speech and I called it "within 0.06-0.08 s": that compared our voice with the model's audio, not with the mouth. New measure (lip_measure.py: MediaPipe face mesh, inner-lip gap / face height per frame; lag scan of mouth opening vs speech energy, + = voice later than the mouth): v1 lag +0.16 s (0-1.6 s), -0.20 s (3.3-4.8 s), +0.40 s (5.9-8.0 s), corr 0.09 / -0.05 / -0.24 at lag 0. The model's OWN audio is not in sync with its mouth either: "Eyes" mouth opens at 6.1 s, the voice starts at 6.52 s (voicing check: breath only before 6.5 s), whole clip model corr 0.31 at lag 0.
v2 (build_c09_lite.py): our line is cut into 8 short units (words) and each is placed by a search of start (+-0.1-0.25 s) and tempo (0.55-1.5) that maximises the correlation with the mouth opening; "And there goes" (head turned away, no face 2.3-3.4 s) keeps the model-audio seed 2.97 s. Placement: Lower 0.22 | Lower 1.10 (only "Lo-wer", tail cut, tempo 1.5) | And there goes 2.97 | the 3.85 | hat 4.38 | Eyes on 6.12 (tempo 0.55) | me 6.96 | not on the hat 7.28.
Result on frames/C09L_final_A.mp4 (not committed): best lag 0.00 s in every window (0-1.6, 3.3-4.8, 5.9-8.0, whole), corr 0.65 / 0.53 / 0.56 / 0.52 at lag 0 (model's own audio 0.31). ASR medium beam 5 and beam 1: "Lower lower pardon Sire and there goes the hat Eyes on me not on the hat" (all words). -14.2 LUFS, TP -1.9 dBFS, AAC 320k. Marcel's cry 1.85-2.7 s: lips NOT VERIFIED (small face, not measured). Cost 0 (local).
Same measure on the Lite finals built earlier (indicator, face mesh on 540 px frames): C02L lag +0.40 s (corr 0.27), C03L +0.20 s, C05L +0.12 s, C04L +0.04 s (ok). C02/C03/C05 are probably late against the mouth like C09 v1: to be re-fitted the same way (free, local) after the owner's yes; NOT yet changed.

## C09 Lite v3: second check frame by frame on the delivered file, 30.10 (owner: "Ещё раз проверь")
Method: lip_measure.py on the 1080x1920 final itself (151 of 193 frames have a face; none 2.3-3.4 s and 4.8-5.4 s, head turned), table mouth opening vs voice energy per video frame. Found in v2: (1) on both "hat" words the mouth is widest (3.5-4.6 s and 7.58-7.83 s) while our deadpan "hat." trails off 17 dB down: the voice was weakest where the mouth is at its maximum; (2) the last phrase peaked at 7.5 s with the mouth closed, the wide mouth came 0.08 s later; (3) "me," starts 0.08 s before the lips open (a closed-lip "m", acceptable).
Fix (build_c09_lite.py): "not on the" and "hat." are separate units (mouth: small 7.25-7.5, closed 7.50, wide on "hat" 7.58-7.83), "not on the" compressed (tempo 1.35, 7.20-7.56) so it ends where the mouth shuts, both "hat." units flattened (gain follows a smoothed envelope, power 0.6, cap 2.2) and faded 30 ms at the end so the breath after the "t" is not lifted. "hat." at 4.38 s and 7.62 s.
Result frames/C09L_final_A.mp4 (not committed): lag 0.00 s in the windows 3.3-4.8, 5.9-8.0 and the whole clip (+0.04 s in 0-1.6), corr at lag 0: 0.65 / 0.60 / 0.54 / 0.54 (v1 at lag 0: 0.09 / -0.20 / -0.24 / -0.10; model's own audio 0.31). ASR medium beam 5 and beam 1: "Lower lower pardon Sire and there goes the hat Eyes on me not on the hat". -14.0 LUFS, LRA 2.7, TP -1.9 dBFS, AAC 320k.
Still weak / NOT VERIFIED: (a) "not on the" mouth correlation is negative (the mouth moves only 0.01-0.02 there; the placement is by span, not by shape); (b) our "hat." still falls a little before the mouth closes (the word decays); (c) Marcel's lips at "Pardon, Sire!" and the king's lips at "And there goes" (2.97-3.5 s, head turned): no face to measure; (d) the 0.55 tempo on "Eyes on" and 1.5 on the second "Lower" are time-stretches by atempo: naturalness by ear NOT VERIFIED; (e) no ear check by me. C02/C03/C05 not re-fitted yet.
