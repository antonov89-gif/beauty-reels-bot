# Louis XIV series bible: signature phrases and self-praise rule (owner 28.10.2026)
Rule: every video STARTS with the same signature opener, ENDS with the same signature outro (the CTA-and-feast ending), and the king says "what a handsome man I am" ONCE per video, in the opener (owner 29.10). One TTS voice for all lines (see channels.md section 2b). English lines, nasty, arrogant, haughty; ElevenLabs tags per line: [smug], [haughty], [admiringly], [sneering]. The king has a FRENCH ACCENT (owner 29.10; locked in voice/voice_lock.json v3: tag "[thick French accent]" + TTS-only respelling, captions in normal spelling).

## Text style rules (owner 29.10: no traces of AI in the text, clear to an English-speaking audience)
Write like a person talking, not like a model. Contractions (I'm, don't, that's). No em dashes. No "not X, but Y" constructions, no stock punchline pairs, no chains of one-word sentences (one short burst per clip at most). Say plainly what a thing is the first time ("the rising" instead of the French "lever"; no "c." or Latin). Idioms must be ones a US/UK viewer uses. About 15-19 words per 8-s clip. Read-aloud test: if an English friend would not say it, rewrite it. No burned-in subtitles (owner 29.10: like the reference); platform closed captions (SRT) only, in ordinary spelling, so every line must be clear by ear. French words limited to the ones English speakers know ("my friends", "no?", "Magnifique").

## Signature opener (fixed text, first ~8 s of EVERY video; owner 29.10)
"Oops, the ceiling. There. Welcome to Versailles. Yes, I'm that handsome. Try not to faint."
Since 29.10 the king films HIMSELF (selfie arm in frame, like the reference): the video opens on the painted ceiling, he turns the phone onto himself and speaks only after the phone points at him. Owner chose this opener (option B). "Bow. Lower. Good." stays only as his command to the court when it enters (C07 in ep.1). Marcel the page is a side character (off screen, "my left side, MY left").

## Signature outro (fixed text, last ~16 s of EVERY video; owner 29.10)
"Subscribe to my stunning channel. Hit like. Ring the bell. Anyway, do what you like. [haughty, arrogant laugh] I'm off to the table to feast!"
Laugh rule (owner 29.10): the laugh comes AFTER "do what you like" and is cold, arrogant and haughty (chin up, down the nose, eyes half-closed), not a warm giggle. He commands the audience, waves them off with the back of the hand, laughs at them and walks away to a banquet table (mirror flash = cut). The title card "THE SUN IS NEVER LATE." is the on-screen sign-off (not voiced; the voiced "The sun is never late." is retired from the outro and may appear as a line inside an episode).

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
