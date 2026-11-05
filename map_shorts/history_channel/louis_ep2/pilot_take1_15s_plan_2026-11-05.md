# Pilot: first 15 s of Take 1 as ONE pinned generation (owner 05.11: "да, делай пилот, но проверить все детали сначала")
## Checked before any spend
| # | Detail | Result |
|--|--|--|
| 1 | API limits (OpenAPI spec read 04.11): image_urls = first + optional last (max 2), keyframe_urls up to 8, tags @first_frame/@keyframe_N/@last_frame required in the prompt, duration 3-30 s, >= 9 s caps the frames at 10, 720p | OK: the pilot uses 1 first + 2 keyframes + 1 last = 4 frames |
| 2 | Price: charged rate is exactly linear (8 s $1.16, 10 s $1.45, 11 s $1.595): 15 s = $2.175 | OK, $2.18 |
| 3 | Aspect: F01a 941x1672, anchors 1080x1919, A3 edit 768x1365 (all 0.563); raw URLs return HTTP 200 | OK |
| 4 | Time spacing of the pins: in T1_anchored (8 s, first + 1 keyframe + last) the keyframe pose appeared at exactly 4.0 s, the middle | evidence for even spacing (0, 5, 10, 15 s for 4 frames) |
| 5 | Speech fit: first 24 words (Is it... is it on? Ah. There I am. Bonjour. I am Louis, King of France. Welcome to Versailles. And this is my channel.) in 15 s = 1.6 words/s, relaxed; "They call me the Sun King. Yes... I'm that handsome." goes to the next piece | OK |
| 6 | Pins vs the card (SFace): A3 edit 0.86, E2 0.81, E1 0.73 (1.00 = identical); pins vs each other 0.70-0.77 | OK |
| 7 | **F01a (the fumble first frame) vs the card: 0.10**, and by eye (crop): a thick BROWN moustache with a long loop and a pale heavy face, while the card and all anchors have a thin DARK moustache with small curled tips. In T1_anchored the first 1.5 s showed this brown moustache and then it turned into the thin one: an identity jump that I did not flag | **BLOCKER for "one strictly identical face"** |
| 8 | Backgrounds differ slightly between the pins (windows, a bust behind E1, candelabra position) and the lace/jabot differs a little between A3 edit, E1 and E2 | SOFT risk: the model must blend between them |
| 9 | Hand on the A3 edit (four fingers + thumb, rings) | OK |
| 10 | Quality gates ready: face_gate.py (median >= 0.65, p10 >= 0.45, outliers by eye), sharpness at s3+, first/last frame RMSE vs the pins, seam scan (frame-difference spikes), fps | READY |

## Fix for the blocker (needs the owner's yes, $0.12)
A new fumble first frame made by EDITING the A3 edit anchor (not from F01a): same man, same hall, but the phone is held far too close: extreme close-up, tilted about 20 degrees, face off-centre right, only nose, lips with the thin dark moustache and one eye visible, the top half covered by his own scarlet sleeve with gold sun and his fist, out of focus. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, one image (A3 edit) as the source. Check by eye (moustache thin dark with curled tips, beauty mark) and by the clean crops; F01a stays as the owner's original, replaced only as the pilot's first frame.

## Pilot generation (after the fix is approved)
Kling 4.0 i2v, 720p, 15 s, $2.18.
- @first_frame = the new fumble frame
- @keyframe_1 (about 5 s) = T1_keyframe_edit_768.jpg (A3 edit: smug pause, ringed hand at a wig curl)
- @keyframe_2 (about 10 s) = ANCHOR_E1_haughty_1080.jpg (straight at the lens, heavy lids)
- @last_frame (15 s) = ANCHOR_E2_smug_1080.jpg (smug half-smile)
Beats: 0-3 s fumble "Is it... is it on?"; 3-4.5 s pulls back, "Ah. There I am."; 5 s the A3-edit pause, clears his throat; 5.5-8.5 s "Bonjour. I am Louis, King of France."; 9-10.5 s sweeps a hand at the hall, "Welcome to Versailles."; 10 s the E1 pose in the pause; 11-13.5 s "And this is my channel."; 15 s the E2 half-smile.
Acting limits: heavy lids, no wide eyes, no broad grin, no lean toward the lens, medium distance; hand-held sway, no gimbal, no zoom; no music; no text.

## Update 05.11 (owner: "У нас уже есть кадры, зачем опять"): no new frame
I tried to make the fumble first frame for free from the existing A3 edit (crop + tilt + blurred sleeve): it looked fake (enormous nose, a blob instead of a sleeve), discarded. Decision (owner wants existing frames, the face must be strictly the card face, F01a is 0.10 to the card with a brown moustache): the pilot starts from the EXISTING A3 edit; the "phone too close" beat is acted by the model as a move (the phone comes in close, then pulls back), not by a special first frame. F01a stays as the owner's original and is not used in the pilot.
Pins (even spacing, 0 / 5 / 10 / 15 s): @first_frame = T1_keyframe_edit_768.jpg (A3 edit); @keyframe_1 (5 s) = ANCHOR_E2_smug_1080.jpg; @keyframe_2 (10 s) = ANCHOR_E1_haughty_1080.jpg; @last_frame (15 s) = T1_keyframe_edit_768.jpg again (closes on the same smug pose). Kling 4.0 i2v, 720p, 15 s, $2.18 (the pilot the owner approved).
