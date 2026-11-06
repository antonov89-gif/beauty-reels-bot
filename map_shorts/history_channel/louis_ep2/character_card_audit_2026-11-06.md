# Character card audit, 06.11.2026 (character-card-specialist)
Scope: louis_card/, louis_ep2/refs/, face_master_v3/, three scripts (gen_t5a_start, gen_t7b_start, gen_t4b2_start). Nothing generated, nothing spent, no images or scripts edited. Metrics: tools/quality_metrics.py (gates: subject sharp>=150, detail>=2.0, blocks<=1.20; room sharp>=80, detail>=1.3, blocks<=1.30). Images opened at full size: R1, R7, R8, R10, K_front, K_E1_up, T3d_start.

## Verdict
The king is recognisable but the card is NOT good enough as a professional character card: one usable master (A3 = R1, 768x1376, FULL FIGURE, the face is only about 250 px wide, about 33 % of the width), no full-size angle set, no expression set, no written descriptor block with a conflict-free age, no hall plate without glasses/chandelier, Marcel has a single good ref whose face is about 200 px wide. Drift seen so far (older/heavier face, beige wig, glasses) comes from this, not only from wording.

## Table of refs (full size, measured)
| File | Size | sharp / detail / blocks | Role | Defects | Verdict |
|---|---|---|---|---|---|
| R1_king_card_A3_white_wig.jpg (= louis_card/A3) | 768x1376 | 940 / 6.6 / 0.99 | king master, full figure | face only ~250 px wide; real-looking faces and a window in the background; hand with 3 rings at the wig; beauty mark on VIEWER'S RIGHT of the mouth (confirmed); wig cool silver-grey | KEEP as identity ref 1, but REMAKE a face-sized master v4 (2K+ face) |
| louis_card/A2_face.jpg | 768x1376 | 867 / 6.1 / 0.96 | dark-wig version | different wig | not used; keep as archive |
| R7_sheet_a1_left34.jpg | 1440x2558 | 747 / 5.4 / 1.21 | left 3/4 on plain wall | face ~460 px wide (best face detail we own); older, lined forehead; blocks 1.21 (limit 1.20, borderline) | KEEP as 2nd identity ref candidate for 3/4 shots (eye check first) |
| K_front / K_left34 / K_right34 / K_profile_left / K_profile_right / K_back | 512x512 | 61-98 / 0.48-0.61 / 1.19-1.37 | angle tiles | small, upscaled-soft, K_front and K_right34 blocks 1.37 | FAIL, do not attach; REMAKE at full size or replace by words |
| K_E1..E8 (384x430), K_E*_up (960x1075 upscaled) | | 20-28 / 1.2-1.4 / 1.17-1.30 | expression crops (source undocumented; look like crops of a real photo) | soft, upscaled, source/rights not documented, wig warm-grey | FAIL, do not attach; document the source or drop |
| K_A3_face_crop.jpg | 476x494 | 213 / 3.7 / 1.08 | face crop of A3 | small | usable only as a 2nd ref next to R1 (passes gate, but low pixel count); better remade |
| R8_marcel_full.jpg | 1536x2752 | 610 / 4.6 / 0.91 | Marcel full figure (powder-blue coat, silver braid cuffs, white linen cravat, white wig with ribbon, black tricorn in hands, daylight hall with real faces) | face only ~200 px wide (13 % of width); tricorn and floor/people in the ref | KEEP but REMAKE a Marcel face master; say "ignore tricorn, floor, people" |
| R8_marcel_full_768.jpg | 768x1376 | 304 / 3.7 / 1.04 | downscale of R8 | tiny face | do not use |
| R2_marcel_front / R3_three_quarter / R4_terrified | 1280x2294 | 272/3.1/1.22; 200/2.7/1.26; 116/1.6/1.36 | Marcel angles | blocks above 1.20 on all three; R4 fails sharp and detail | R2 borderline, R3 borderline, R4 FAIL: remake in a Marcel pack |
| R10_hall_clean.jpg | 1686x1920 | 105 / 1.52 / 1.29 | hall ref, night | NOT clean: crystal glasses, a chandelier top right, ladies' backs and courtiers with faces | passes room gate; use only with "ignore people, glasses, chandelier"; REPLACE by a hall-only plate |
| R9_hall_only.jpg | 711x1100 | 15 / 0.58 | hall | soft | FAIL |
| R5 framing ref | 1284x1722 | 58 / 0.55 / 2.15 | composition | compression blocks | FAIL for identity; composition by words |
| T2c/T3a/T3c/T3d/T4a/T4b starts and ends | 2161x3840 | 132-363 / 1.8-3.7 / 1.0 | our 4K stills | face older/heavier than A3 (T3d: rounder, deeper lines); beauty mark right, OK; hall with chandelier | OK as scene refs, NOT as identity refs (never chain identity from them) |
| face_master_v3 front/three_quarter/smile | 800x800 | 14-38 / 0.5-0.7 | video frames of the old Seedance king | soft, a different (younger, v3 "age 35") man, brown wig | DEPRECATED, do not attach |
| face_master_v3 tall_wig_ref (420x780), white_wig_C06 (620x1140, sharp 3.8) | | 114 / 3.8 | wig refs | tiny / blurry | do not attach |

Identity checks by eye (A3 vs R7 vs K_front vs T3d): beauty mark viewer's RIGHT in all; thin moustache with curled tips; heavy lids; wig cool silver-grey and white; scarlet coat with gold suns. Conflict found: the written descriptor (face_master_v3) says "about 35, light grey-hazel eyes", while A3/R7/T3d read about 45 with brown-hazel eyes. The prompts say "same age" without a number; the face master text and the pictures disagree. The owner decides the age; the text must follow the pictures (A3), or the pictures must be remade.

## Card plan (prices from MODEL_NOTES.md, APIpod, 05.11; each call needs its own yes, retries too)
Route: edit/derive from the best original (A3 + R7 as refs), never from video frames or the K_ tiles. GPT Image 2.5 Sunburst Lite 4K high = $0.12 per image (measured; SUBMISSION_UNCERTAIN failures happen, probably not charged). Flare-lite 4K $0.08 and Nano Banana Pro 4K $0.12 are alternatives; Nano Banana Pro edits did not hold eye colour/powder (ledger 31.10); Flare-lite NOT CHECKED, worth one pilot.
1. King master v4: neutral frontal head-and-shoulders, even light, plain grey wall, no hand over face, face >= 1000 px wide (face about 45 % of a 2K+ frame), the wig fully inside. Refs: R1 then R7. 1 image, $0.12 (budget 2 tries $0.24). Check: SFace vs A3, side-by-side by eye (mark side, wig colour/height, age).
2. Angle set from the master: left 3/4, right 3/4, left profile, right profile, slightly low, slightly high = 6 images x $0.12 = $0.72, each its own call, each >= 1024 px short side and passing the gate. Risk: profile tiles drift; judge by eye.
3. Expression set: closed smirk, heavy-lid bored, laugh with teeth, shocked, = 4 images x $0.12 = $0.48 (neutral is the master).
4. Marcel pack: neutral front face master (face >= 1000 px), left 3/4, terrified = 3 x $0.12 = $0.36; refs R8 (face, ignore tricorn) + R2.
5. Courtier set (simple wigs, men and ladies, 3 stills) = $0.36.
6. Clean hall plate, no people, no glasses, no chandelier, candlelit gilded antechamber, 4K = $0.12 (budget 2 tries $0.24).
Total one try each: 0.12 + 0.72 + 0.48 + 0.36 + 0.36 + 0.12 = $2.16; with a 30 % retry reserve about $2.8. Minimum useful start: items 1, 2 (front, left 3/4, low) and 6 = about $0.60. Order: 1 -> check -> 2 -> 3 -> 4 -> 6 -> 5.

## Step C: prompt review (line-level fixes, scripts NOT edited)
### gen_t5a_start.py (ref 1 = R1 king, ref 2 = R10 hall)
- OK: order matches image_urls; mark side stated as the viewer's right; wig colour positive first, then NOT beige/cream/golden; "do not copy pose or background"; hall ref stripped of glasses; face 28 % and wig 60 % (ratio 2.1, matches A3).
- Fix 1: "same age" has no number: write "a man of about 45 as in reference 1" (or the owner's chosen age); add "heavy-lidded brown-hazel eyes" (A3 shows brown-hazel, not grey).
- Fix 2: "turned three-quarter toward the lens": state the direction, "his face turned toward the viewer's LEFT, so the cheek with the beauty mark stays in view"; otherwise the mark can vanish.
- Fix 3: R10 contains a chandelier; the prompt says "no chandelier" and "no glass" OK, but also add "ignore its chandelier" to the Reference 2 sentence.
- Fix 4: raised counting hand: add "three jewelled rings on the raised hand, four fingers and a thumb" (A3 has them; the ring hand is a known extra-finger trap).
- Fix 5: "only one king" is acceptable here (R10 has no king) but put it in the positive: "one man in the red coat, everyone else in plain wigs".
- Risk: face is only 250 px in R1 and goes to 600 px in the output: expect the heavier/older drift seen in T3d; compare side-by-side with R1 before any clip.
### gen_t7b_start.py (R1, R10)
- Same Fix 1, 2 (a low 30-degree angle with a raised chin foreshortens the face; add "the face still frontal enough that both eyes and the beauty mark are visible"), 3.
- Face 36 % with the tall wig (about 76 % wide) leaves about 12 % each side, the prompt says "at least 6 percent": say 10 percent, otherwise the side curls get cropped; the top of the wig must clear the gilded ceiling edge: "at least 8 percent free above the wig".
- Low angle + chin raised = highest identity risk of the three (no low-angle tile exists, K_ tiles are unusable): the eye check decides, plan a retry or make angle tile "slightly low" first (plan item 2).
- Hand pressing on the cloth: "five natural fingers, rings on the ring and middle finger as in reference 1".
- The mark and moustache are not stated for the bow beat: nothing else to add; the courtiers "dipping" are fine (plain wigs).
### gen_t4b2_start.py (R8 Marcel full, R10 hall)
- Biggest risk: Marcel's face is 13 % of the width in R8 (about 200 px) and the output wants it at 46 %: 3.5x enlargement, identity will be invented. Fix: make the Marcel face master first (plan item 4) or attach R2 as ref 2 (face larger), and keep R8 for costume only.
- Coat: the prompt says "plain blue livery coat" but R8 is a powder/light-blue coat with silver braided cuffs: write "a powder-blue coat with silver braid on the cuffs" (the cuffs are out of frame, so "powder-blue coat" is enough).
- "a strip of white lace at the lower edge": the ref has a plain white LINEN cravat, no lace: write "a white linen cravat".
- Wig: write "a white powdered wig with side curls and a black ribbon at the nape" (as in R8).
- "thick dark brows" is stronger than R8 (moderate dark brows): write "dark straight brows".
- Tricorn trap handled ("no hat, no tricorn") and the pose is disclaimed; also add "ignore the floor, the bright daylight and the people in reference 1" because R8 has a daylight parquet hall with courtiers.
- R10 sentence is OK but add "ignore its chandelier".
- The king is correctly absent ("no king in the frame").
Honest limits: judged by eye and by sharpness numbers; SFace not run (no generated frames); only the owner approves.
