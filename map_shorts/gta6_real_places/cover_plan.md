# GTA 6 Short v4 (0:52, 9:16): cover plan

Video: "Most places in GTA 6 are reportedly based on real Florida" (3 pairings widely reported, 3 not reported, Mount Kalaga vs 105 m).
Goal of the cover: a GTA fan stops the scroll in under a second, and the cover promises exactly what the video delivers (game vs real Florida), without claiming "leak", "confirmed" or "game footage".

## What a "GTA look" means here (analysis)
Fans read GTA from four signals, in this order:
1. Colour: hot sunset gradient (pink, orange, purple) against teal water and neon. Highest-recognition signal.
2. Palms + art deco + a car or bike at an angle. Vice City shorthand.
3. Loading-screen / box-art language: flat illustrated figures, thick clean outlines, collage panels.
4. Chunky title type with a thick outline, plus a stripe or badge.
What must NOT be on the cover: the real GTA VI logo, Rockstar marks, Jason/Lucia look-alikes, a fake "official" badge, a claim of confirmation. Not affiliated with Rockstar or Take-Two (already in publication.md).

## Variants

| ID | Idea | GTA signal | Curiosity gap | Matches the video | Risk |
|---|---|---|---|---|---|
| A | Loading-screen key art: illustrated couple-less collage (car, palms, helicopter) at sunset, title "GTA 6 IS REAL FLORIDA?" | strongest | weak (nothing to decode) | partly | looks like every GTA thumbnail; no hook |
| B | Diagonal split: left = neon Vice City street in game style, right = real satellite Miami Beach with a red pin, same angle of the coast, title "GTA 6 = REAL FLORIDA?" | strong (left half) | strong: "is that one real?" | exact: this is the video's first 3 seconds | needs a real tile (free, our own engine) |
| C | Mount Kalaga mystery: misty granite mountain over a Florida swamp, giant "105 M" slam, title "A MOUNTAIN IN FLORIDA?" | medium | very strong | only the last 8 s | sells one beat of the video, not the whole |
| D | Map-pin collage: Florida outline in neon, six giant pins with tiny game-style insets, title "6 PLACES. 3 ARE REAL?" | medium | strong | exact (3 widely reported / 3 not) | busy at phone size, small insets unreadable |
| E | Over-the-shoulder rooftop shot (our G07 idea) with a hot pink skyline and "WHERE IS THIS?" | strong | medium | weak | the character is the same as the video body, adds nothing |

Scoring (1-5): GTA signal / curiosity / video match / phone legibility / honesty+legal / cost = total
- A: 5 / 2 / 3 / 4 / 4 / 5 = 23
- **B: 4 / 5 / 5 / 5 / 5 / 5 = 29**
- C: 3 / 5 / 2 / 4 / 5 / 5 = 24
- D: 3 / 4 / 5 / 2 / 5 / 5 = 24
- E: 4 / 3 / 2 / 4 / 4 / 5 = 22

## Pick: B (split: game vs real)
Why it wins: the left half is pure GTA colour and props (fans stop), the right half is real satellite imagery (the thing the video proves), and the diagonal seam with a pin makes the viewer ask "which one is real?" before reading a word. It is also the only variant where the cover and the first 3 s of the video are the same idea, so retention does not drop after the click. Honesty: the title ends with a question mark (same as the v3/v4 wording), the left half carries a small "AI CONCEPT" tag, and nothing says "confirmed".
Runner-up: C as a second cover for A/B testing later (it sells the Mount Kalaga twist).

## Layout for B (1080x1920)
- Top 0-520 px: title zone, 2 lines, heavy outline: "GTA 6 =" (white, pink stroke) / "REAL FLORIDA?" (yellow, black stroke). Keep out of the bottom 25 % (YouTube UI).
- Diagonal seam from (1080, 560) to (0, 1500), thin white line + shadow.
- Upper-left triangle: AI game-style frame (neon Vice City boulevard, drifting purple car, palms, art deco hotel, helicopter).
- Lower-right triangle: real Esri satellite of Miami Beach (Ocean Drive strip), slightly warm-graded to match, with a big red map pin and a thin white target ring.
- Small tag bottom-left on the AI half: "AI CONCEPT" (white on dark pill). Small tag bottom-right on the satellite half: "REAL".
- Badge on the seam: "VICE CITY = MIAMI?" (pink pill, rotated -6).
- The base AI image has no text in it; every letter is added by hand (PIL), same pipeline as the Samoa covers.

## Prompt for the AI half (Nano Banana 2.1, 9:16, 2K) - ready to paste
> Illustrated-looking but richly rendered open-world crime game key art, NOT a photograph, in the spirit of a modern sun-drenched Miami-style open-world game loading screen: low angle from the asphalt of a neon-lit boulevard at dusk, a glossy purple sports car drifting toward the camera with white tyre smoke, tall palm trees on both sides, a pastel art deco hotel with pink and cyan neon glowing on the left, a police helicopter high in a hot pink-orange-purple sunset sky, wet asphalt reflecting the neon, small generic pedestrians in the distance, litter and tyre marks on the road. Saturated colours, strong rim light, cinematic depth of field, clean bold shapes readable at thumbnail size. Composition: all the action in the lower-left two thirds, the upper-right third is open sky and glow with free space; the car is the single focal point. No text, no letters, no numbers, no signs with words, no logos, no brand names, no real people, no recognisable game characters, no watermarks. Vertical 9:16.

Negative prompt (when the model supports it): text, letters, logo, watermark, Rockstar, GTA logo, recognisable character, celebrity face, blurry, low contrast, cluttered, extra limbs, deformed car, photo of a real street.
Continuity with the video: same look as keyframes G00/G01 (neon dusk Vice City), so the cover feels like the same world. Reference image option: pass G00 (keyframes/G00.jpg URL) as `image_urls` to keep the car and hotel style; the grid sheet shows G00 as the best match.

## Prompt for variant C (only if tested later)
> Game-style render, NOT a photograph: a forested granite mountain rising out of a flat Florida swamp, cypress trees with Spanish moss in the foreground water, low golden fog, one tiny wooden cabin, dramatic god-rays from a hot orange sunset, an unreal "too tall for Florida" feeling. Clear single focal point (the mountain peak) in the upper-middle, free space above for a title. No text, no letters, no numbers, no logos, no people. Vertical 9:16.

## Real half (free, no generation)
Esri World Imagery, Miami Beach / Ocean Drive, zoom about 16-17, rotated so the coastline runs parallel to the seam; same tile fetcher as the video engine (credits: Esri, Maxar, Earthstar Geographics, already in publication.md). Warm grade (+8 % saturation, soft orange overlay) to sit next to the AI half.

## Cost and next step (only after "yes")
- AI half for B: 1 image, Nano Banana 2.1, 9:16, 2K: **$0.04**
- Optional C for an A/B test: **$0.04**
- Composition, text, real satellite tile: free (own PIL code)
Nothing is generated yet.
