# Authenticity audit: loops L01–L03 (27.10.2026)
Files checked (final renders in /home/claude/v84, not committed):
- `l01_circle_final.mp4`
- `l02_india_final.mp4`
- `l03_indonesia_final.mp4`, re-rendered after fix F1

Each file: 8.000 s, 240 frames, 30 fps, 1080x1920, H.264 + AAC 192k.
How they were checked: dense contact sheets at 4 fps (frame_forensics.py); frames at 0 s, 1 s and the last frame; frame-by-frame strips around every fade and spin; qc_loop.py (seam, motion, loudness, audio wrap).

## Claims
| Loop | On-screen text | Source opened | Verdict |
|--|--|--|--|
| L01 | "More people live inside this circle than outside it"; "Inside: more than half of humanity"; "Outside: everyone else" | Wikipedia "Valeriepieris circle": A. Rae 2022, 4,000 km around Yuxi ≈ 4.32B (55 %); Shah 2022 ≈ 52 % for Myers' circle | PARTLY: VERIFIED for the 2022 data. Still true in 2025 is ESTIMATED (55 % margin; inside populations grew with the world). The description says the share is an estimate. |
| L01 | Country labels CHINA, INDIA, INDONESIA, PAKISTAN, BANGLADESH, JAPAN, PHILIPPINES, VIETNAM | Great-circle distances from Yuxi, computed: every label point and the main cities are inside 4,000 km (Tokyo 3,766, Karachi 3,583, Jakarta 3,430, Surabaya 3,684, Mumbai 3,113, Manila 2,213) | VERIFIED as "where they are". Edges are outside (Sapporo 4,098, Jayapura 5,090), so no "all of X" claim is made. |
| L01 | Circle geometry | Geodesic circle drawn from the formula; radius 4,000 km, centre Yuxi 24.35N 102.54E | VERIFIED |
| L02 | "India has more people than all the blue"; India 1.45 billion | UN WPP 2024 via 2 sources: India 2024 ≈ 1.45B; Wikipedia UN table: 2023 1,438,069,596 | VERIFIED |
| L02 | "Europe + USA + Canada 1.13 billion" | Wikipedia UN table 2023: USA 343,477,335, Canada 39,299,105. Europe 2024 745,083,824 (Wikipedia "Demographics of Europe", table source not shown) | PARTLY: Europe is from a secondary table. The sum is 1.13B and India leads by ~320M, so the conclusion cannot flip. Recheck Europe on the UN data portal when possible. |
| L02 | Blue area = UN "Europe" + USA + Canada | Natural Earth continent "Europe" (50 countries listed in the run) includes all of Russia, like the UN region; overseas parts cut; Greenland, Turkey, Cyprus and the Caucasus not filled | VERIFIED |
| L03 | "Indonesia is wider than the USA (without Alaska & Hawaii)"; "Indonesia · east to west 5,120 km" | Wikipedia "Geography of Indonesia": 5,120 km east–west | VERIFIED |
| L03 | "USA · coast to coast 4,500 km" | Wikipedia "Contiguous United States": 2,802 mi / 4,509 km greatest distance; WorldAtlas ≈ 4,500 km | VERIFIED |
| L03 | Overlay | The Indonesia outline is moved on the sphere by a rotation (north kept up); distances preserved; ghost outline at home | VERIFIED (method) |

**F1 (FIXED):** "wider than the USA" was stronger than the source. With Alaska (Aleutians) the USA spans much more. Added the on-screen qualifier "(WITHOUT ALASKA & HAWAII)", the title says "Mainland USA", and the description names the 48 contiguous states. Re-rendered and re-checked.

## Footage
None. All visuals are our engine renders: globe, fills, labels, bars. No stock video, no photos.

## AI shots
None. No AI images, AI video or AI voice. The music is our own synthesis (audio_loop.py).

## People, logos
None.

## Sound
Own synthesised 120 BPM bed (4 bars = 8.0 s, seamless) plus own SFX (pop, whoosh, tick, ding, slide). No third-party audio in the file. Content ID risk: LOW.
A trending sound may be added by the owner in-app from the platform library, which is licensed for Shorts/TikTok. That is not part of this file.

## Imagery and data
- NASA Blue Marble via GIBS: NASA imagery, no copyright restriction, credit requested. Credit on screen (bottom line) and in the description.
- Natural Earth (admin-0 50m; India worldview 10m from naciscdn.org): public domain. Credited.
- Esri: NOT USED (Esri-free policy).
- Population: UN WPP 2024 (credited on screen in L02 and in the description).
- Circle: A. Rae 2022 (credited on screen in L01 and in the description).

## Platform policy
- Original value: own research (sources), own graphics and own music. No reused footage.
- Repetitive-content risk: LOW for three loops. Keep each loop a distinct researched fact, not template spam.
- Misleading metadata: titles match the on-screen claims (L03 "Mainland" + qualifier).
- India outline: L02 uses India's official boundary (Natural Earth IND view, including all of Kashmir). This is a political choice, not a factual claim; it may draw comments from Pakistani or Chinese viewers. It is not a policy violation.
- Altered/synthetic disclosure: not needed (animated graphics, nothing realistic faked).
- Made for kids: NO.
- Monetisation risk: LOW. Removal risk: LOW.

## Metadata and flags
publication.md has been written (EN titles, descriptions with sources and credits, hashtags, pinned comments). Not scheduled yet, so the platform flags (no AI, not made for kids) are NOT VERIFIED until the post exists; read them back after scheduling.

## Technical (qc_loop.py on the final files)
| Loop | Seam diff (last->first) vs normal step | Largest frame step | Loudness | True peak | Audio wrap |
|--|--|--|--|--|--|
| L01 | 0.28 vs 0.20: OK | 11.6 at 2.9 s (pull-out spin, intended) | −14.7 LUFS | −1.3 dBTP | OK |
| L02 | 0.22 vs 0.39: OK | 14.9 at 5.8 s (spin back, intended) | −14.5 LUFS | −1.5 dBTP | OK |
| L03 | 0.37 vs 0.22: OK | 14.2 at 5.9 s (slide back, intended) | −14.2 LUFS | −1.4 dBTP | OK |

Fixed during the check:
- Bars drawn without alpha blending popped off instead of fading. They now sit on their own layer.
- Bars counted down ("52 KM" flashes); now they fade at full value.

Music bed is present in every second (−11.4 to −12.8 dB RMS per second).

## Verdict
**FIXED.** F1 and the bar fades were corrected, re-rendered and re-checked. No false claims, no AI, no third-party media.

## Open items (owner)
1. India outline: keep India's official boundary in L02 (my recommendation for an India-targeted loop) or switch to the neutral de facto outline.
2. Europe 2024 population: confirm on the UN data portal (conclusion safe either way).
3. After scheduling: read the post back and confirm the flags (no AI content, not made for kids).
