# COMPARE: ep.1 C01-C08 (EP1_C01-C08_snd.mp4, 67.4 s) vs reference Vlog 1 (LjfGP7wpjVs, 128.3 s), 30.10.2026
Skill: youtube-cinematic-dna V5.4.1, route COMPARE. Owner: "изучи чем отличается от референса: камера, звук, качество, монтаж и т.д." + "предложи улучшение как профессиональный режиссёр".

## Evidence and coverage
| Source | Coverage | Level |
|--|--|--|
| REF video | frame sheets 4 fps 0-10 s, 1 fps 10-128 s (owner's mp4, 360x640, 30 fps), frames_vlog1_LjfGP7wpjVs.md, motion.csv per second | L2-L3 (sampled frames) |
| REF audio | full 128 s (a.wav): loudness, events, floor, Whisper words | L3 audio |
| REF sound labels | vidIQ AI watch 30.10 | hypothesis unless matched by measurement |
| OURS | full file: same frame_forensics.py (sheets, cuts, motion), same audio analyzer, picture stats on the same sheet tiles | L3 |
Not inspected: the reference mp4 itself again (not on disk), so per-frame motion of the reference is per second only.

## Measured differences (same tools on both)
| Area | Reference | Ours | Gap |
|--|--|--|--|
| Speech pace (takes 1-3 / our clips) | 83-99 wpm; 2.5-3.1 words per speaking second; 7-9 pauses > 0.5 s per take | C02 133, C03 142, C04 120, C05 156 wpm; up to 5.2 words per speaking second; 1-3 pauses per clip; C01, C06, C07 are fine (82-93 wpm) | **BIG**: C02-C05 talk 1.5-1.8x faster than the reference; no air for the jokes (owner felt it at 24-25 s). Cause: too many words per 8-9-s clip + tempo up to 1.2 to fit the lips |
| Structure | 3 long takes 24-30 s carry 64 %; 1 burst of 9 cuts; 13 cuts in 128 s | take 1 = C01-C03 28 s (joins invisible), take 2 = C04-C06 23 s with a jump cut, take 3 = C07-C08 16 s; 3 cuts in 67 s | similar logic (OK); the burst and the gag-with-another-person are still ahead (C09, C11) |
| Camera movement | almost never still: 3 % of seconds below 2 (mean frame diff) | 16 % of seconds below 2: C04-C05 (33-42 s) are frozen (propped phone, nothing moves) | **BIG** in C04-C05 |
| Camera variety | table-level looking up, dutch roll, extreme close-ups, objects shoved at the lens (jar 42-45 s), hand re-aims, push into the face | mostly arm's-length selfie at eye level; good moments: C01 ceiling, C06 wig into the lens, C08 push-in | medium |
| Foreground "phone mistakes" | 5 in 128 s (thumb, hand, toothpick, thumb over the lens) | 3 in 67 s (plume C01, wig C06, crop C08) | small |
| Picture: brightness | 86 (darker, moody) | 116 (bright, airy) | **BIG**: ours looks over-lit |
| Picture: texture | Laplacian 2360, fine noise 2.8 (skin pores, cracked makeup, straw, grain) | 645, 1.8 (smooth "clean AI" skin and surfaces) | **BIG**: ours reads synthetic/beauty-filtered |
| Picture: colour | natural overcast daylight, warm costume, chalk face; saturation 98 | gold everywhere (bed, gown, ceiling, canopy); saturation 91, R/B similar | medium: "gold on gold" flattens the frame |
| Frame rate | 30 fps (phone) | 24 fps (film) | small: 24 fps reads "cinema", not phone |
| Character | grotesque truth (rotten teeth, smallpox scars, white lead): the gross-out is the hook | a handsome, clean vain king; the vanity is the hook | by design; but nothing "ugly true" to make the viewer gasp |
| Acting | slow deadpan, touches her face, lifts props to the lens, sighs, laughs with tears | quick delivery, few prop actions (wig) | medium |
| Event with another person | servant drops a tray, wide view, she laughs | not yet (C09 hat drop planned) | planned |
| Captions | small word-build captions burned in | none (owner's rule: no burned-in subtitles) | deliberate |
| Sound (v4) | one phone recording, room per take, handling, objects, sighs/laughter, no music | real CC0 room/foley + phone colour; no music; no echo; floor centre 824 Hz vs 170-624 | small now; still no breaths/sighs in the voice |
| Lip sync | native | built: offsets 0-0.3 s (C03 0.2 s after the pause fix) | small |

## Director's verdict
The camera language and the sound are now close. What separates us from the reference is the PERFORMANCE RHYTHM and the PICTURE: our king talks 1.5x too fast in C02-C05 (no air, jokes do not land), two clips are frozen, and the image is bright, smooth and golden where the reference is darker, textured and naturalistic. These three are the priority; they also make the AI look stronger.

## Plan (priority, cost)
1. **Air in the delivery** (largest effect). Rule for every clip: max 14-16 words per 8 s, at least one 0.6-1.0 s pause before the punchline, tempo <= 1.1. C02-C05: shorten the lines by about 30 % (e.g. C02 "A hundred people watch me wake up. They call it the rising. I call it opening night."), re-voice (one Lumean order for C02-C05 together, about 0.3 RUB, own yes) and rebuild (free). C09-C15: rewrite the lines to the rule before any video. Pause beats get a silent reaction (eyebrow, look at the court).
2. **Picture grade + texture** (free, all clips): exposure about -0.35 EV, gold saturation -15 %, lift contrast in the mids, fine film/phone grain and a light texture sharpen; 30 fps export with frame blending checked for artefacts (or keep 24 fps if blending shows ghosts). A/B on C02 first, then all.
3. **C04-C05 frozen** (free first): digital hand-held sway from the reference's motion statistics (8 % crop, slow drift + 2 re-aims), plus his hand reaching to the phone at the jump cut. If it still reads fake: re-generate C04-C05 with the camera plan (about $5 each, own yes).
4. **Prompts for C09-C15** (no extra cost): "front camera of a phone, slightly underexposed, real skin texture and pores, no beauty filter, natural daylight, not golden everywhere"; one object to the lens per clip (hat C09, heel C10, mirror C14/C15); one silent reaction beat; SOUND block (handling, room, court, steps, cloth; no music) so the model's own sounds can be kept after removing its speech (htdemucs).
5. **The set piece with another person** (C09): wide view of the hat falling, the courtier's "Pardon, Sire!" (page voice: owner to pick 1-6), the king's cold laugh, swing back to him; as in the reference's tray gag, this is the episode's peak.
6. **Breath and life in the voice** (cheap, at the next re-voice): ElevenLabs tags [inhales], [sighs], [chuckles] at 2-3 places per episode; the laugh in C15 stays.
7. **Optional "ugly truth" beat** (script, needs facts checked with two sources before use): the reference's engine is the gross historical truth; for Louis a candidate is his teeth (reported tooth extraction and palate injury around 1685). Only after a fact check, and only if the owner wants it in the series.

## Done 30.10 (owner "делай"): items 2 and 3, free
- Grade (grade_ep.py) on all clips: episode picture brightness 116 -> 96 (ref 86), texture 645 -> 1307 (ref 2360), grain 1.81 -> 2.28 (ref 2.81); gold calmer (saturation -20 %, yellows -25 %).
- 30 fps: tested (minterpolate on C06 fast move) and REJECTED: interpolated frames double the wig stand and smear the face. 24 fps kept.
- C04-C05 digital hand-held (make_sway.py): drift + roll + nudges at the pauses (C04 1.7 s, 5.4 s; C05 1.85 s) with knocks in the sound; C05 settles back to the original frame in its last 0.7 s, so the invisible C05 -> C06 join stays (frame diff at the join 4.2 vs neighbours 3.5). Still seconds 16 % -> 0 %.
- Sound v4 rebuilt on the swayed clips; episode -15.0 LUFS, TP -1.2, no silence, every word by ASR medium.
- Output: frames/EP1_C01-C08_v5.mp4 (not committed).

## Correction to item 1 (pace)
A re-voice alone cannot slow C02-C05: the model's lips speak the long lines, so a shorter voice leaves the mouth moving with no sound. Slower, airier delivery in C02-C05 needs those clips re-generated with the short lines (about $4.3-5.1 each via the draft route, about $18-20 for the four, APIpod quota must be topped up; each its own yes), which also fixes their static camera properly. For C09-C15 the short-line rule applies before generation (free).
Proposed short lines (owner to approve):
| Clip | Now (words, wpm) | Proposed | Words |
|--|--|--|--|
| C02 (9 s) | Some mornings, a hundred people watch me wake up. The ceremony is called the rising. I call it opening night. (20, 133) | A hundred people watch me wake up. [beat] I call it... opening night. | 11 |
| C03 (8 s) | The doctor's here, the surgeon's here, and nobody came to see them. Everyone came to see me. Naturally. (18, 142) | The doctor. The surgeon. Nobody came to see them. [beat] Everyone came for me. Naturally. | 14 |
| C04 (9 s) | Now, the wig. My hair started falling out at seventeen. I took it personally, so I got a wig. (18, 120) | Now, the wig. My hair started falling out at seventeen. [beat] I took it personally. | 13 |
| C05 (5.4 s) | It makes me look taller, they say. I wouldn't know. I never look down. (14, 156) | They say it makes me taller. [beat] I never look down. | 10 |
