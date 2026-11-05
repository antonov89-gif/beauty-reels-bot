# Reference "Elizabeth I - Vlog 1" (first 30.8 s, the owner's mov, 05.11) vs our T1_anchored.mp4 (05.11)
Source: the owner's file (1080x1920, 30 fps, 30.78 s, mov, 15.9 MB), run through map_shorts/prompts/frame_forensics.py --dense 10; all 4 dense sheets and sheet_rest_01 viewed. Coverage: video_frames YES, audio measured only, transcript read from the burned-in captions. This is the first 30 s of Vlog 1 only; Vlog 6 and Vlog 2 are still NOT VERIFIED ON FRAMES.
All picture numbers are measured at the same width (both frames scaled to 724 px), head and wig area, seated medium shots: reference 6-29 s (24 frames), ours 3-7 s (5 frames).

| Measure | Reference (Vlog 1) | Ours (T1 anchored) | Reading |
|--|--|--|--|
| Resolution / fps | 1080x1920, 30 fps | 724x1284, 24 fps | GAP |
| File bitrate | 4.1 Mbit/s | 12.1 Mbit/s | not the cause: ours has more bits but less detail |
| Detail (Laplacian variance, head area) | 810 | 129 | GAP: about 6x. Part of it is the reference's heavy crackled skin texture and the 1080 source, but on the side-by-side ours is visibly softer and smoother |
| Fine grain / micro-texture (std of the high-pass residual) | 13.4 | 8.4 | GAP: the reference has more micro-texture |
| Colour: saturation / brightness (HSV mean) | 96 / 102 | 167 / 141 | GAP: ours is much more saturated and brighter |
| Colour: mean R/G/B | 101 / 84 / 70 (muted, neutral-warm daylight) | 141 / 86 / 53 (strong orange-gold) | DIFFERENT LOOK: ours is gilded and orange, the reference is natural overcast daylight |
| Motion in the calm stretch (mean frame difference per second) | 2-4 (8-22 s) | 4-6 (4-6 s), 2.9 at 7 s | MATCH (both calm in the medium, small hand-held drift) |
| Opening | extreme low angle, face large with a thumb at the left edge, ceiling, tilt up to level seated medium in 4 s | extreme close-up under the king's own sleeve and fist, pull-back at ~2 s, seated medium | SAME IDEA, different gesture (deliberate: own character) |
| Cuts in the first 30 s | 1 (at ~23 s) | 0 (an 8 s clip) | not comparable yet |
| Captions | burned-in white uppercase, words building up | none (owner: platform SRT only) | deliberate difference |
| Light | soft overcast window light, chalk-white face, tapestry and oak | candlelight, gilded hall, warm rosy face | DIFFERENT BY DESIGN (own channel identity), but ours is far more saturated |

## What it means / fixes (free ones first)
1. Colour grade in editing: pull saturation down to about 120-130 and brightness to about 120, a little cooler skin: free, closes most of the "AI gold" look.
2. Fine film grain and a mild sharpen in editing (honest: it adds apparent crispness, not real detail).
3. Delivery format: export 1080x1920 (the platforms expect it) by upscaling in the edit; 30 fps conversion by duplication was rejected earlier (duplicate frames), so the delivery stays 24 fps.
4. The real detail gap needs a different render: Kling 4.0 i2v 1080p was measured in ep.1 as the sharpest (880 vs 389 for Seedance 2.0 720p, model_choice.md); it costs $0.2175/s against $0.145/s (8 s clip $1.74 against $1.16; about +$14.5 over 25 clips). Not ordered; the owner decided 720p for ep.2 to keep the price down.
