# Short (≈36 s, 9:16): "The Moon Freed the Ship That Blocked 12% of World Trade" (Zack D. structure)

Format: 1080x1920, English VO, 6 scenes, real animation (Grok Imagine from keyframes), ~82 words.
Reference: Zack D. Films "A Toddler Fell Into A Well" (tyGjLN1RaJQ), analysis in map_shorts/analysis/ref_zackd_toddler_well.md. We copy the beat structure, not the content: STAKES + number -> OBVIOUS FIXES FAIL (second number) -> UNEXPECTED SOLVER -> concrete mechanics -> RESOLVED PAYOFF (comic).

## Concept
A 400 m container ship wedges across the Suez Canal in a sandstorm and stops about 12 % of world trade (goods worth about $9.6 billion a day, $400 million an hour). Tugs, excavators and dredgers fail for days. The solver is not a person but the Moon: a supermoon king tide lifts the water, 14 tugs pull, the ship breaks free. Comic payoff: the owner pays about $540 million and throws in a tugboat.

## 3 hooks
1. (chosen) "In 2021, a ship four hundred meters long got stuck in the Suez Canal, and twelve percent of world trade stopped."
2. "One stuck ship cost four hundred million dollars every hour."
3. "Nothing could move this ship. Then the Moon helped."

## Voice-over (82 words; Kokoro test 35.7 s with lead + tail; Lumean about the same)
1. In 2021, a ship four hundred meters long got stuck in the Suez Canal, and twelve percent of world trade stopped.
2. Tugboats pulled. Diggers dug. Pumps emptied the ship. Nothing worked, and every hour cost four hundred million dollars.
3. Six days later, help came from the sky: a supermoon, and an extra-high tide.
4. Fourteen tugboats pulled together, and the ship broke free.
5. Over four hundred ships had been waiting.
6. The owner paid five hundred forty million dollars, and threw in a tugboat.
If Lumean runs over 38 s, drop line 5 and fold "four hundred ships" into the on-screen text.

## Scene table
| # | VO | Visual (keyframe) | Motion (Grok, 6 s) | On-screen text (word-timed, numbers pop in instantly) |
|---|---|---|---|---|
| 1 | 1 | Huge dark container ship wedged diagonally across a narrow desert canal, bow in the sand bank, sandstorm haze, tiny excavator on the bank for scale | slow drone push-in, dust blowing | "400 M" then "12% OF WORLD TRADE" (red glow) |
| 2 | 2 | Wide shot: 4 small tugboats pulling with taut lines, an excavator digging the bank at the bow, a dredger pipe pumping sand, orange-vest workers | tugs strain, water churns, sand pours | "$400 M / HOUR" (red glow), "STILL STUCK" |
| 3 | 3 | Dusk: giant supermoon above the canal, the ship stuck below, an engineer in hard hat and orange vest looks up at the moon, water level lines on the bank | slow tilt up from the engineer to the moon, water slowly rising | "6 DAYS" then "SUPERMOON" |
| 4 | 4 | Many tugboats (about 14) pulling and pushing from all sides at high tide, ship bow swinging free of the bank | tugs push, bow slowly swings loose, spray | "14 TUGBOATS" |
| 5 | 5 | Aerial view along the canal: a long queue of ships on the water behind the freed ship | slow flight along the queue, the first ship starts moving | "400+ SHIPS WAITING" |
| 6 | 6 | Comic payoff: a business man in a suit hands a toy-sized tugboat on a cushion to a canal official in a white uniform, canal and ship behind | man bows, official takes the tugboat, small smile | "$540 M + A TUGBOAT" |

## STYLE LOCK (all keyframes)
Semi-realistic high-end 3D explainer render (NOT a photograph, NOT cartoon, NOT Pixar), game-cutscene CG like our Pangaea/Samoa Shorts: smooth slightly plastic human skin, realistic proportions, simple matte textures, flat clear sky (hazy yellow in scene 1, dusk in scene 3), simplified readable environments, soft grounded shadows, shallow depth of field. Generic ship and tug designs: NO company names, NO logos, NO readable letters on hulls or containers (do not copy the real ship's lettering). Free space above for captions. Vertical 9:16.

## Keyframe prompts (Nano Banana 2.1, 9:16, 2K, $0.04 each; each starts with the STYLE LOCK)
- K1: "A gigantic dark-blue container ship stacked high with colourful containers, wedged diagonally across a narrow desert canal, the bow stuck in the sandy bank, the stern touching the opposite bank, sandstorm haze in a yellow sky, a tiny yellow excavator on the bank for scale. High aerial view."
- K2: "Wide shot of four small orange tugboats pulling with taut ropes on the bow of the huge stuck container ship, a yellow excavator digging the sand bank at the bow, a dredger with a pipe pumping sand, workers in orange safety vests and white helmets on the bank, warm daylight."
- K3: "Dusk at a desert canal: an enormous glowing supermoon low in the sky, the huge stuck container ship in the dark water below, in the foreground an engineer in a white helmet and orange vest standing on the bank looking up at the moon, wet marks on the bank showing the water rising."
- K4: "At high tide about fourteen small tugboats pushing and pulling the huge container ship from all sides, the bow swinging free of the sandy bank, white spray, golden evening light, high angle."
- K5: "Aerial view along a straight desert canal: a very long queue of container ships and tankers on the water stretching to the horizon behind the freed ship, calm blue water, sand banks, clear sky."
- K6: "A man in a dark suit bowing and offering a toy-sized orange tugboat on a small velvet cushion to a canal official in a white uniform with gold shoulder boards, the canal and a huge container ship behind them, friendly mood, sunny day."

## Animation prompts (Grok Imagine 1.5 Fast, 6 s, image_urls = keyframe, $0.108 each)
- A1: "Slow drone push-in toward the stuck ship, dust blows across the canal, the tiny excavator moves slightly, haze drifts."
- A2: "The tugboats strain on their ropes, water churns, the excavator digs and the sand pipe pumps, workers wave; the huge ship does not move."
- A3: "Slow camera tilt up from the engineer to the glowing moon, the water in the canal rises slowly and quietly, the engineer lifts a hand."
- A4: "The tugboats push and pull together, the bow slowly swings loose from the bank, spray and foam, smooth camera."
- A5: "Smooth slow aerial flight along the queue of ships, the first ship begins to move forward, small waves."
- A6: "The man bows deeper, the official takes the toy tugboat with both hands and smiles slightly, a light breeze moves the flags."
Avoid in prompts (filter): "disaster", "crash", "explosion", injuries, panic.

## Negative prompt / continuity
Negative: text, letters, numbers, logos, company names, ship name on the hull, watermark, extra limbs, distorted ships, cartoon eyes, Pixar look, photograph, blurry.
Continuity: the ship is always the same dark-blue hull with colourful containers and NO lettering; tugs always orange; workers in orange vests and white helmets; the engineer in K3 is the same face as the canal official's side character if reused (generic).
Overlays/captions: Poppins ExtraBold 3-word captions at ~78 % height; number slams in Poppins ExtraBold with red glow as in the Madagascar Short; numbers appear instantly (no count-up).

## Fact check (Wikipedia "2021 Suez Canal obstruction" and "Ever Given", read 2026-10-15)
- Grounded 23 March 2021, freed 29 March 2021 at 15:05 EGY after "6 days and 7 hours" -> "six days later" is right (and "6 DAYS" on screen).
- Length 400 m (399.94 m); 224,000 tons; 20,000 TEU capacity.
- About 12 percent of global trade passes through the canal; goods worth about US$9.6 billion a day held up; Lloyd's List: US$400 million per hour -> VO "every hour cost four hundred million dollars".
- Fuel and about 9,000 tonnes of ballast water removed; an excavator dug the bow; suction dredgers removed sand; pumps shifted weight; "over a dozen tugboats", final freeing with fourteen Egyptian, Dutch and Italian tugs (Ever Given page says eight tugs worked on the refloat - sources differ, so the VO uses the 2021 obstruction page's 14 and the description says "over a dozen").
- A high tide on 27 March helped; the final pull used "the ebbing king tide of a supermoon on 29 March" (wording is odd: the ship was freed as the supermoon tide peaked, so VO says "supermoon, and an extra-high tide" without claiming it alone freed her).
- At least 369 ships queued by 28 March; more than 400 waiting on the evening of 29 March -> "Over four hundred ships had been waiting".
- Settlement: the Suez Canal Authority cut its claim from about $900 million to $600 million and settled for $540 million, plus a 75-ton tugboat from the owner -> VO "paid five hundred forty million dollars, and threw in a tugboat". Wording in the description: "reported".
- Cause: sandstorm with winds over 40 knots; official cause inconclusive -> the VO does not blame the crew.
- One person died during the salvage (SCA, June 2021); we do not show or mention it (not part of the story), but keep the tone respectful and the payoff about the settlement, not the ship.
- Tonal rule: no blame, no "captain's mistake".

## Title, description, tags (draft; goes into publication.md after the render)
Titles: 1) "The MOON Freed the Ship That Blocked 12% of World Trade 🌕🚢"  2) "One Stuck Ship Cost $400 Million an Hour 🚢💸"  3) "This Ship Blocked the Suez Canal. The Moon Fixed It."
Description: In March 2021 a 400-metre container ship got wedged across the Suez Canal after a sandstorm and blocked about 12% of world trade for six days. Tugs, excavators and dredgers could not free it, until an extra-high supermoon tide helped over a dozen tugboats pull it loose. Delayed goods were estimated at about $400 million per hour. The owner later settled for a reported $540 million plus a tugboat. Sources: Wikipedia "2021 Suez Canal obstruction", "Ever Given". All scenes are AI-generated illustrations, not real footage. AI voice.
Tags: suez canal, ever given, ship stuck suez canal, supermoon, world trade, shipping, geography, facts, tugboat, money, shorts.

## Cover plan (after the render, $0.04, same mechanic as the Wallace's Line / Gold cube covers)
Big contrast: tiny tugboat vs the giant ship wedged in the canal; red-glow "$400 M / HOUR" with arrows, yellow/white title "STUCK!"? Better "THE MOON FIXED IT?" (curiosity). Real NASA/Esri strip of the Suez Canal (free) at the top.

## Cost (nothing spent yet; each paid step needs a "yes")
6 keyframes $0.24 + 6 Grok clips $0.648 + Lumean voice ~0.25 RUB + cover $0.04 (optional) = about $0.93

## Checks before delivery (standard QC)
1080x1920 30 fps, -14 LUFS, caption sync, frame sheet over the whole timeline, numbers match the VO (400 m, 12 %, $400 M/h, 6 days, 14 tugs, 400+ ships, $540 M), no readable text or real company marks in AI frames, chat copy under 30 MiB, no secrets in the repo.
