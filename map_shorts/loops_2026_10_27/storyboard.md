# Loops L01–L03: storyboard (27.10.2026)
Format: loop_ideas_2026_10_27.md. Each loop is 8.0 s at 30 fps, 1080x1920, with no narration. The frame at 8.0 s equals frame 0, so the loop is seamless. All visuals are our own engine graphics (engine_loop.py, derived from engine83) on NASA Blue Marble GIBS imagery and Natural Earth borders, Esri-free. No AI visuals, no AI voice.
Stills are engine renders, so what is shown is what will be rendered. Sheets are in `storyboard/`: `hooks_frame0.jpg`, `l01_circle_sheet.jpg`, `l02_india_sheet.jpg`, `l03_indonesia_sheet.jpg`.
Status ladder (V5.1): SPECIFIED -> GENERATED (stills) -> INSPECTED (self-check below) -> APPROVED (owner). The current status of all three loops is **INSPECTED, waiting for the owner**.

## L01 · "More people live inside this circle than outside it"
| t, s | Screen | Motion | SFX event |
|--|--|--|--|
| 0.0 | Headline (3 lines). Globe on Asia, yellow 4,000 km circle around Yuxi; outside dimmed, inside lit | slow push-in | — |
| 0.25–2.0 | labels pop one by one: CHINA, INDIA, INDONESIA, PAKISTAN, BANGLADESH, JAPAN, PHILIPPINES, VIETNAM | push-in continues | pop ×8 |
| 2.5–3.7 | pull out to the Arabian Sea: Africa and Europe appear dimmed = "outside" | whoosh | whoosh |
| 3.6–5.9 | pills "INSIDE: MORE THAN HALF OF HUMANITY" / "OUTSIDE: EVERYONE ELSE" | slow drift | pop ×2 |
| 5.4–7.0 | push back to frame-0 framing | whoosh | whoosh |
| 6.2–7.75 | pill "ARE YOU INSIDE?" (comment trigger) | — | pop |
| 8.0 | = frame 0 | | |
Claim: C1 "More than half of humanity lives inside a 4,000 km circle around Yuxi". Source: A. Rae 2022 (4.32B, 55%), see Wikipedia "Valeriepieris circle". The 2022 data are VERIFIED; whether it still holds for 2025 is ESTIMATED (margin about 5 points; Shah 2022 got 52% for Myers' circle). We use Rae's circle rather than Quah's 3,300 km one: Quah's was the minimum for 2015 data and may now be under 50%.
Labels: every labelled country's label point lies inside the circle. Japan, Pakistan and Indonesia are only partly inside, so these are labels, not "all of them" claims.

## L02 · "India has more people than all the blue"
| t, s | Screen | Motion | SFX |
|--|--|--|--|
| 0.0 | Headline "INDIA HAS / MORE PEOPLE THAN / ALL THE BLUE". Globe over the Atlantic, Europe + USA + Canada filled blue, labels USA / CANADA / EUROPE; bar "EUROPE + USA + CANADA 1.13 BILLION" | drift | — |
| 1.4–2.8 | globe spins east to India | spin (whoosh) | whoosh |
| 2.5–3.0 | India fills orange with a pulse, label INDIA | — | glow, pop |
| 2.9–4.4 | bar "INDIA" grows 0 -> 1.45 BILLION and passes the blue bar | — | tick |
| 5.0–6.5 | spin back to the Atlantic; India bar empties 6.2–6.9 | whoosh | whoosh |
| 7.0–7.3 | labels USA / CANADA / EUROPE pop back | — | pop ×3 |
| 8.0 | = frame 0 | | |
Claims:
- C2: India ≈ 1.45B in 2024 (UN WPP 2024). VERIFIED through 2 secondary sources and the UN table: 1.438B in 2023.
- C3: Europe + USA + Canada ≈ 1.13B. The US (343.5M) and Canada (39.3M) 2023 UN figures are VERIFIED. Europe ≈ 745M is ESTIMATED from a secondary source; recheck on the UN data portal before the final. The margin is about 320M, so the conclusion cannot flip.
- The UN "Europe" region includes all of Russia, and so does the Natural Earth continent "Europe". Overseas parts of European countries are cut from the fill (French Guiana and others).
- Map choice: India is drawn with the Natural Earth India worldview, i.e. India's official boundary including Kashmir. This loop targets Indian viewers, and the de facto outline draws "wrong map" anger. The population figure does not depend on the outline.

## L03 · "Indonesia is wider than the USA"
| t, s | Screen | Motion | SFX |
|--|--|--|--|
| 0.0 | Headline. Real-size Indonesia (orange) lies over the lower 48 (blue) and sticks out past both coasts; bars "USA · COAST TO COAST 4,500 KM" / "INDONESIA · EAST TO WEST 5,120 KM" | slow push | — |
| 2.3–2.8 | bars collapse | — | tick |
| 2.5–4.5 | Indonesia slides home across the Pacific (north kept up, shape and size unchanged); camera follows | pull out + spin | slide, whoosh |
| 4.3–5.7 | at home, matches its ghost outline; pill "SAME SHAPE · SAME SIZE · REAL PLACE" | drift | pop |
| 5.6–7.4 | slides back onto the USA | spin | slide, whoosh |
| 7.0–7.7 | bars grow back | — | tick |
| 8.0 | = frame 0 | | |
Claims:
- C4: Indonesia ≈ 5,120 km east–west. VERIFIED (Wikipedia, Geography of Indonesia).
- C5: The contiguous USA's greatest coast-to-coast distance is ≈ 4,500 km (2,802 mi / 4,509 km, Florida–Washington). VERIFIED (Wikipedia, Contiguous United States; WorldAtlas ≈ 4,500 km).
- Overlay method: sphere rotation, so distances are preserved. This is not a Mercator drag.

## Self-check of the stills (done before showing)
- Frame 0 = last frame: OK for all three (stills at 0.00 and 7.97 s match).
- Headline readable at phone size: OK. A dark top gradient sits behind the text over Arctic ice in L02 and L03.
- Text clipping and overlaps: fixed in round 2. PAKISTAN was cut at the edge; INDIA/BANGLADESH and VIETNAM/PHILIPPINES overlapped; the pills went off-screen in the L01 pull-out; the IND label was cut during the L02 spin-back.
- Key text kept above y = 1600 (Shorts UI zone). The credit line at the very bottom is also copied into the description.
- Not checked yet (needs the video render): motion smoothness, loop seam at full frame rate, SFX sync, loudness, and the authenticity audit (mandatory before delivery).

## Sound
The owner adds a trending track from the YouTube Shorts / TikTok library at upload. The file carries our own beat with SFX on the events above (audio70 synth) as a fallback; no third-party audio is burned in.

## Next after approval
Render all three at full frame rate, then run the seam check (frame 239 vs 0), the self-check and the authenticity audit. Then write the publication package (EN title, description with sources and credits, hashtags) and show.
