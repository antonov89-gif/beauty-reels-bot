# Louis XIV series bible: signature phrases and self-praise rule (owner 28.10.2026)
Rule: every video STARTS with the same signature opener, ENDS with the same signature outro (the CTA-and-feast ending), and the king says "what a handsome man I am" ONCE per video, in the opener (owner 29.10). One TTS voice for all lines (see channels.md section 2b). English lines, nasty, arrogant, haughty; ElevenLabs tags per line: [smug], [haughty], [admiringly], [sneering]. The king has a FRENCH ACCENT (owner 29.10; locked in voice/voice_lock.json v3: tag "[thick French accent]" + TTS-only respelling, captions in normal spelling).

## Text style rules (owner 29.10: no traces of AI in the text, clear to an English-speaking audience)
Write like a person talking, not like a model. Contractions (I'm, don't, that's). No em dashes. No "not X, but Y" constructions, no stock punchline pairs, no chains of one-word sentences (one short burst per clip at most). Say plainly what a thing is the first time ("the rising" instead of the French "lever"; no "c." or Latin). Idioms must be ones a US/UK viewer uses. About 15-19 words per 8-s clip. Read-aloud test: if an English friend would not say it, rewrite it. No burned-in subtitles (owner 29.10: like the reference); platform closed captions (SRT) only, in ordinary spelling, so every line must be clear by ear. French words limited to the ones English speakers know ("my friends", "no?", "Magnifique").

## Signature opener (fixed text, first ~8 s of EVERY video; owner 29.10)
"Oops, the ceiling. There. Welcome to Versailles. Yes, I'm that handsome. Try not to faint."
Ep.2 variant (owner 04.11): no ceiling swing ("Oops, the ceiling. There." removed, 6.1) and no "Try not to faint"; text: "Is it... is it on? Ah. There I am. Bonjour. I am Louis, King of France. Welcome to Versailles. And this is my channel. They call me the Sun King. Yes... I'm that handsome."
Since 29.10 the king films HIMSELF (selfie arm in frame, like the reference): the video opens on the painted ceiling, he turns the phone onto himself and speaks only after the phone points at him. Owner chose this opener (option B). "Bow. Lower. Good." stays only as his command to the court when it enters (C07 in ep.1). Marcel the page is a side character (off screen, "my left side, MY left").

## Signature outro (fixed text, last ~16 s of EVERY video; owner 29.10)
"Subscribe to my stunning channel. Hit like. Ring the bell. Anyway, do what you like. [haughty, arrogant laugh] I'm off to the table to feast!"
Laugh rule (owner 29.10): the laugh comes AFTER "do what you like" and is cold, arrogant and haughty (chin up, down the nose, eyes half-closed), not a warm giggle. He commands the audience, waves them off with the back of the hand, laughs at them and walks away to a banquet table (mirror flash = cut). The title card "THE SUN IS NEVER LATE." is the on-screen sign-off (not voiced; the voiced "The sun is never late." is retired from the outro and may appear as a line inside an episode).

Ep.2 variant of the outro (owner 05.11): "So... I was wondering what else to show you here. Ha. Probably... nothing. That's all. Bye. I'm busy. ...And you: subscribe to my stunning channel. And like. Or... whatever." (no bell, no "I'm off to the table to feast", no next-episode teaser in ep.2).

## Self-praise ("what a handsome man I am"): ONCE per video (owner 29.10: "раз в ролик")
Rule: exactly ONE direct praise of his own looks per video, and it is the signature opener ("Yes, I'm that handsome."). No other direct praise of his face, profile, ankle or body anywhere else in the video. His vanity stays in the situations (the audience, the mirrors, the wig, the heels, the dinner in public), as the joke itself and not as a praise tag. Superseded: the earlier "one tag every 15-20 s" rule (28.10).
Reserve bank (NOT used while the opener carries the line; a future episode may swap the single line, never add a second): "Look at me. Magnificent, no?" / "What a face, though." / "Handsome again. Every single morning." / "I could cry. Look at that profile." / "White suits me. Everything does." / "Only one worth looking at. Me, obviously." / "Look at that ankle." / "Lucky mirrors." / "Ah... what a profile." / "They're all my good side." / "Magnifique. Me, I mean." / "Sorry. I can't help it." / "Even my shadow is handsome." / "Don't touch. Just admire."

## Fixed cast and props
Marcel the page (off screen, "my left side, MY left"), the gilded hand mirror (cut device), the plumed hat gag, the red heels, the white-grey wig.

## Sound rule (owner 29.10)
NO music in any video of the series: no score, no sting, no harpsichord. Only the locked voice, room tone and foley. The audio that the video models generate is always muted and replaced (it can contain music).

## Reference manner (owner 29.10: "Где мы отстаём: это учти далее и делай как референс")
Measured gaps of ep.1 0-42 s vs the reference (louis_ep1/reference_compare_0-42.md) and the newer reference "Tower of London" (map_shorts/ref_tudor_vlog_2026_10_28/one_link_studio_lBkoOcM-r5k.md). From C06 on, every clip and every episode:
1. Camera is a phone in a hand and never stands still: hand-held drift, small roll, walking bob, re-aims, tilt down/up to an object, push-in to the face. ONE locked (propped) shot per episode at most, used as a contrast beat. Still realistic: the phone stays within arm's reach (camera-flight rule).
2. Framing close and wide-lens: face and hands fill the frame, real ultra-wide distortion at close range; the room behind.
3. One clip = one setup of about 8 s; hard cuts between setups are fine (like the reference's 15 shots in 2 min); inside a setup no jump cuts.
4. Phone mistakes: at least one per take (an object filling the lens, a hand re-aiming the phone, the lens brushing a shoulder or a door frame, the camera dropping to the feet, a hand reaching to stop the recording at the very end).
5. Supporting cast react and may speak short lines (a page, a courtier, a guard); the king's deadpan line lands on them; one beat of silence after a gag. The king keeps the ONE locked voice; others use other voices, disclosed as AI.
6. Sound: a full diegetic bed under everything (room tone of the palace, distant voices, footsteps on parquet, fabric, jewellery, doors, objects), never dead digital silence; still NO music; the video models' own audio stays muted.
7. Personal hook per episode (a past humiliation turned into power, a secret, a rule only he may break) and one fact per setup.

Full list of what we take from the references: REFERENCE_RULES.md (05.11).

## Reference gate (measured 05.11 on the owner's Vlog 1 file and transcripts; binding for every clip and episode)
Owner 05.11: "он снимает с телефона, не должно быть статических кадров, должна быть тряска рукой... всё как у референса: паузы, ракурсы, длина склеек". Numbers measured by me on the reference (map_shorts/history_channel/louis_ep2/shots_and_generation_length_2026-11-05.md, compare_vlog1_first30s_vs_T1_2026-11-05.md, frames_vlog1_LjfGP7wpjVs.md):
| Item | Reference | Gate for our clips |
|--|--|--|
| Camera | a phone in her hand: drift, roll, re-aims, push-ins; in 128 s 7 different setups (low selfie with a thumb, table-height dutch close-up, very low looking up, food burst, side-on, wide from low, new spot) | hand-held in EVERY clip; NO propped/static shot; a new angle for every setup |
| Seconds with a frozen background (camera and people) | 0 % | <= 10 % |
| Seconds with still hands/body | 0 % | <= 15 % |
| Head motion | 0.20 face widths per second | >= 0.18 |
| Shot lengths | 14 shots in 128 s: three long takes 23.6/28.8/30.1 s, three medium 9.8/12.7/17.4 s, one 5.9 s burst of 9 micro-cuts; mean 9.2 s, median 1.9 s | per episode: 2-3 long takes 15-30 s, 3-4 medium 8-17 s, one burst of 6-9 cuts (0.2-1.5 s) of objects/food, cuts only between setups |
| Speech pace and pauses | Vlog 1 about 110 words in 131 s (~50 wpm, Vlog 2 note), Vlog 6 187 words in 125 s (~90 wpm); short lines, silence after gags | 60-90 wpm per episode (our draft 7.1 has 339 words for about 3:00 = 113 wpm: too dense, cut or lengthen with action beats); one beat of silence after each gag |
| Phone mistakes | 5 in 128 s (thumb, hand sweeping in, fingers in front, a thumb covering the lens as a transition) | at least 1 per take |
| Sound | room tone always, no silence > 1 s | voice + room tone + foley, never dead silence; no music |
| Face | one face | SFace to A3 median >= 0.65, p10 >= 0.45, eye check |

## Face lock v3 (owner 29.10: "почему лица разные ... плохо делаешь промты и фотокарточку")
The face master is the king of the video clips: louis_card/face_master_v3/ (README there: descriptor block, ref order, side-by-side check before any video). Card v2 and the old storyboard frames C07+ are not used as identity sources. Every new first frame is made from the face master and checked against it before generation of video.

## Clumsy camera = character trait (owner 29.10, on a reference frame where the face is cut by the frame edge: "он не умеет профессионально держать, нужно показать это зрителям")
Louis cannot hold a phone. The viewer must SEE it, the way the reference shows it (frame from "Tower of London": face pushed to the left edge and cut, far too close, the coin shoved at the lens, the horizon tilted). In every episode, 2-4 moments of bad framing, never the whole video:
- the face slides off-centre and is cut by the frame edge (half a face, the top of the wig cut off);
- far too close: the nose and one eye fill the frame, ultra-wide distortion;
- tilted horizon, the camera sags while he talks, then he jerks it back;
- an object shoved into the lens (coin, wig, heel, mirror), focus hunting;
- he notices and fixes the framing mid-line, annoyed ("Marcel!" if the page gag is approved).
The words must stay clear (the mouth may leave the frame for a moment, the voice continues). Not a camera flight: all of this is a hand moving within arm's reach.

## The king is the only star (owner 29.10)
Courtiers, pages and guards wear simple period wigs and plain clothes; nobody copies his wig, coat or makeup. Only Louis has the tall powdered wig, the white court makeup and the scarlet sun coat.

## Camera manner lock (owner 29.10: "больше внимания на камеру ... он не умеет держать камеру")
Every video prompt starts with CAMERA_BASE from louis_ep1/camera_plan_ep1.md and adds the per-clip camera beats (0-2 / 2-5 / 5-8 s) with one clumsy moment per clip. A clip whose camera is calm or tripod-like fails the gate and is not shown.

## Series hook engine (owner 30.10)
"My body fails, I declare it the fashion": a vain handsome king whose body betrays him; every defect becomes a court trend; a courtier in the background copies the newest one. Own hooks, not the reference's teeth: see louis_hooks_unique.md (adopted: 4 "perfume and shirts"; proposed: 1 fistula, 2 appetite, 3 peas, 5 close-stool audiences). Every fact needs two sources; legends only as rumours the king denies, and the description says so.

## Lines like the reference (owner 30.10: "идем дальше, с учетом референса: фразы, мысль, паузы")
From C12 on (and in every redo of C01-C08, C13-C15), measured against the reference in louis_ep1/lines_vs_reference.md:
1. A thought, not a gag: fact + a small confession or sly admission + a turn; the joke comes from the situation, not from a tag line.
2. Spoken shape: "so", "well", "now", unfinished sentences; contractions; no polished punchline pairs (at most one smug tag every two clips).
3. Air: about 14-15 words per 8-9 s (reference 83-99 wpm), 1-2 real pauses of 0.6-1 s, one before the turn.
4. Range: now and then a soft moment (he laughs at himself), not only arrogance.
5. Facts stay with two sources; legends only as rumours he denies (and say so in the description).


## AI disclosure on screen (owner 31.10: "Убери надпись Аи генератор")
No persistent corner "AI-GENERATED" mark on the history-channel videos. Disclosure stays: the end-card line "AI-generated comedy reconstruction", the first line of the description (visuals and voice AI-generated, dialogue invented for comedy) and the YouTube altered/synthetic content flag (and TikTok AI-generated label) at upload.

## On-screen AI line removed (owner 04.11: "AI-generated comedy reconstruction это убрать")
From episode 2 on, the end card shows only "THE SUN IS NEVER LATE." No AI text on screen at all. Disclosure stays: the first line of the description (visuals and voice AI-generated, dialogue invented for comedy) and the platform flags at upload (YouTube altered/synthetic content ON, which makes YouTube show its own label; TikTok AI-generated label ON). This narrows the CLAUDE.md line "label AI visuals on screen" for this channel by the owner's decision.
