# Frame forensics: "Elizabeth I - vlog 1" (LjfGP7wpjVs), camera analysis from the owner's mp4, 28.10.2026
Source: owner upload (mp4 not committed). 360x640, 30 fps, 128.27 s, stereo AAC. Tool: map_shorts/prompts/frame_forensics.py --dense 10 (4 fps sheets for 0-10 s, 1 fps for the rest, all 14 sheets viewed) + scene-cut scan at thresholds 0.1/0.15/0.2/0.3 + two 720 px crops (1:34, 1:46).
Coverage: video_frames YES (every second), audio MEASURED ONLY (loudness, silence), transcript = burned-in captions read from frames. Limits: 360 px width, so fingers, small text and skin micro-texture are judged at low resolution.

## Verdict on the camera (VERIFIED on frames unless marked)
1. The video is 3 long continuous takes (23.6 s, 28.8 s, 30.1 s = 64 % of the runtime), one 6-second burst of 9 micro-cuts, and 3 medium shots (9.8 s, 12.7 s, 17.4 s). 14 shots, 13 hard cuts, mean shot 9.2 s but the median is 1.9 s: the average hides the structure.
2. Within a take the camera does not cut, it MOVES: a tilt from the ceiling to level (2.5-4.5 s), a roll and drift around the face (24-52 s), a pan to a jar (40-43 s), a hand sweeping in to re-aim (53-55 s), a slow push into an extreme face close-up (64-72 s). The "editing" is the performer handling a phone.
3. Wide front-camera look: strong perspective distortion at close range (nose enlarged, body small at 24-34 s), roughly an ultra-wide 16-20 mm equivalent (ESTIMATED impression, no EXIF).
4. Camera heights: table-level looking up (23-52 s and 52-82 s: ceiling beams visible), eye-level propped (4.5-23.6 s, 1:54-2:08), a hand-held low swing (1:29-1:50).
5. Deliberate "phone mistakes" in the foreground: thumb at the left edge 0-3 s; pink thumb at the lower right 26-34 s; a hand sweeps in from the top 53-55 s; fingers and a toothpick in the foreground with rack focus 76-81 s; a huge thumb covers the lens 1:51-1:53 as the transition into the last scene. 5 events in 128 s.
6. One shot-type change for the gag: wide vignetted fisheye-like view of the servant and the spilled almonds (1:39-1:42), then a swing back to her laughing at the left of the frame with the servant behind.
7. Captions: small bold white uppercase sans with a thin dark outline, 1-2 lines, at about 78 % of the frame height, centred, words building up (newest word first dim then white), about 3.5 % of the frame height. Not the large TikTok style.
8. Light: soft overcast window light, no hard key, warm oak and amber against a chalk-white face; same look in every location.
9. Audio (MEASURED): integrated -15.4 LUFS, true peak -1.1 dBFS, LRA 11.1 LU, no silence longer than 1 s at -50 dB. Music presence NOT MEASURED.
10. AI or live: STRONG INFERENCE = AI-generated (not proof). Frames show glyph and diamond-like marks on the forehead and cheeks at 1:29-1:35 and 1:43-1:50 (see crops) that differ from the crackle pattern in the earlier shots; a different scar pattern on the cheek in shot 2 vs shot 1; plus the channel owner sells an AI course. The vidIQ verdict "AI" for this video is consistent; its verdict "live" for the kitchen tour is still unchecked.

## Shot table (timecodes from cut detection + frames)
| # | Time | Length | Camera | Content | Cut |
|--|--|--|--|--|--|
| 1 | 0.0-23.6 | 23.6 s | selfie, extreme low angle with a thumb on the left edge (0-3 s) -> a tilt to level (2.5-4.5 s, one continuous move, NOT a cut) -> static medium, propped, eye level to slightly low (4.5-23.6 s) | she sits on a carved chair, tall mullioned windows on the right, tapestry on the left: "Why am I upside down? Good. Right. Good morrow. I am Elizabeth, Queen of England and Ireland and, well, France on paper. My advisors say a queen must be seen by her people. So here I am being seen." | hard cut at 23.6 |
| 2 | 23.6-52.4 | 28.8 s | table-height, rolled (dutch) and very close, handheld sway; pink thumb lower right 26-34 s; tilt up to her face 40-43 s | profile of her face, jars, a brush, pearls, straw on the floor; "When I was 29 I caught the small pox. It nearly [killed me]. It left these. I do not like people [seeing]." finger on the cheek with rings (34-39 s); she lifts a jar to the lens (42-51 s): "So every morning my ladies paint me white. White lead and [vinegar]." | hard cut at 52.4 |
| 3 | 52.4-82.4 | 30.1 s | very low angle from the table looking up at her, ceiling beams behind; a hand sweeps in from the top (53-55 s); drift and push into an extreme face close-up (64-72 s); toothpick and fingers in the foreground with rack focus (76-81 s) | "They say it is the sugar. And yes, my teeth... I know it is the sugar. I adore sugar. This year a tooth hurt so badly a bishop pulled out his own tooth to show me it was brave. My remedy: a golden toothpick." | hard cut at 82.4 |
| 4 | 82.4-88.3 | 5.9 s | burst of 9 cuts (82.43, 83.33, 83.5, 84.0, 84.17, 87.1, 88.0, 88.17, 88.33); whip pans, motion blur; a close-up of hands breaking a lattice tart (87.1) | the banqueting table: marzipan towers, candied fruit, tarts, candles: "And this is the banqueting room only." | cuts |
| 5 | 88.3-98.1 | 9.8 s | handheld, side-on medium close-up, then a swing and a push-in to the servant's face (1:38) | she eats marzipan, "Hmm, the doctor said less sugar"; a servant enters behind her with a tray of almonds, "Ah, come" | hard cut at 98.1 |
| 6 | 98.1-110.8 | 12.7 s | wide vignetted view from low (1:39-1:42), swing back to her left of frame (1:43-1:50) | the servant drops the tray, almonds pour onto the floor, "Saints preserve me"; she laughs with her hand over her mouth, tears | hard cut at 110.8 |
| 7 | 110.8-128.3 | 17.4 s | she pushes the camera (1:51), a thumb fills the lens (1:52), re-aim; then static, eye level, propped (1:54-2:08), a sideways glance off camera at 2:04 | new room (carved panelling, candles): "Next time I will show you my routine and how I cover [the scars]. So keep an eye on my... oh yes, profile." | end |

## First 10 seconds, second by second (frames)
| t | What is on screen |
|--|--|
| 0.00-0.75 | extreme low angle, face close, a thumb on the left, a painted heraldic ceiling above; caption "WHY" appears at 0.5 |
| 0.75-2.0 | the camera rolls and pulls back, the face shrinks, she frowns; "WHY AM I UPSIDE" |
| 2.0-3.0 | she looks down into the lens, ceiling edge slides out of frame; "DOWN" |
| 3.0-4.0 | the tilt continues, windows and tapestry enter; she is now seated, the thumb leaves the frame; caption "GOOD" |
| 4.0-6.0 | level, static medium; her arm moves in the lower right; "GOOD", "RIGHT" |
| 6.0-9.75 | static; "GOOD MORROW" (7.5-8.75), "I AM ELIZABETH" (9-9.75) |
First visual change after frame 0: 0.25 s (framing); the longest still stretch: 4.5-23.6 s (19 s, mean frame difference 2-4).

## Motion energy (mean frame difference per second, motion.csv)
Calm 8-22 s (2-4), peaks at 23-25 s (cut), 40-43 s (pan to the jar), 82-88 s (burst: 27-43), 95-98 s, 102-115 s (laughing and the lens-cover transition: 12-21), calm again 117-128 s (1.6-4.6). Events per 10 s (hard cuts): [0, 0, 1, 0, 0, 1, 0, 0, 9, 1, 0, 1, 0].

## vidIQ (L1) vs frames
| vidIQ claim | Frames |
|--|--|
| 11 cuts, ASL ~11.6 s | 13 hard cuts, mean 9.2 s, median 1.9 s; 9 of the cuts in a 6-s burst |
| cut at ~3 s to the medium shot | NOT a cut: one continuous tilt 2.5-4.5 s |
| thumb "top left" at 0-1 s | thumb at the LEFT edge, 0-3 s |
| 11 shots with jump cuts between thoughts | 3 long takes carry 64 % of the video; jump cuts only in the burst |
| cut to the profile close-up at ~25 s | cut at 23.6 s |
| servant "trips and drops a platter of marzipan" | he is carrying a tray of almonds; it tips and spills; wide vignetted view |
| Verdict AI | consistent (glyph marks on the face, different scar patterns between shots) |
| Quotes and facts (29 and smallpox, ceruse, bishop's tooth, marchpane, doctor said less sugar, saints preserve me) | all read in the burned-in captions |

## What we take (transfer, not copy)
- Long takes with a moving hand-held camera, not a cut every 3-4 s: with an 8-s generator, chain 2-3 clips with the same framing (a static framing hides the seam) and keep micro-cuts for one reward moment per Short.
- A foreground "phone mistake" in the first seconds. NOT a thumb on the lens (their signature): ours = a courtier's plume or a wax candle brushing the lens.
- A burst of 6-9 micro-cuts for the "feast" b-roll (Louis: the dinner in public, episode 2).
- A wide vignetted view for the gag beat, then a swing back to the star's reaction (our hat-drop).
- The lens-cover transition at the end; ours = the gilded mirror flash.
- Wide front-camera look (about 18 mm equivalent) with real distortion at close range.
Not taken: the exact 0-3 s upside-down gag, thumb, "peasants", the ceruse/teeth gross-out as the engine, white captions.
