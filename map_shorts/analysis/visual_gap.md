# Visual gap: our map Shorts vs GeoGlobeTales (v-LJaB8y438, 32M views)

Sources: competitor storyboard (96 frames, ~1 per second), vidIQ visual audit, our renders (Aral v3, Hannibal). Picture: visual_compare.jpg.

| # | Area | Competitor | Ours | Impact |
|---|------|-----------|------|--------|
| 1 | Map base | Vivid natural satellite, teal sea with depth, mostly continent scale, slight globe curvature | Blue Marble 2004: muddy beige land, flat navy sea, regional zoom makes it soft | High |
| 2 | Graphic language | Neon strokes and fills with big bloom (15-25 px), textured fills (cracked soil), 3D wall, trees growing on the line | Thin white dashed outline, flat translucent fills, weak glow | High |
| 3 | Icons | Own consistent vector icons (people, tractors, no-signs, silos), 1-20+ at once, used as data (people multiply with the counter). Emoji only in the hook | Noto emoji stickers with white outline in almost every scene, 1-3 at a time | High |
| 4 | Subtitles | Small (2.5-3.5% of height), white, sentence case, soft shadow; the map is the hero | Big (4%+) uppercase, thick black stroke, yellow karaoke word; competes with graphics | High |
| 5 | On-screen text | Few big texts, white/cream with soft shadow, "≈" counters, labels 3-4% | Many slams (GONE?, COTTON, STARVING...) in Poppins ExtraBold with thick stroke: meme look | Medium |
| 6 | Non-map inserts | ~1/3 of runtime: soil cross-section (9.5 s), dust wall with scale bar (7.5 s), 1934 paper map card (9 s) | None: 60 s of the same satellite texture | High |
| 7 | Camera / transitions | Continuous smooth push/pull with slight rotation; mostly the same wide framing; hard cuts only into diagrams; no shake, no blur | Zoom-level jumps, whip blur + white flash + chromatic split on every cut, frequent shake: reads as a TikTok edit | High |
| 8 | Effects | Pulsing shockwave rings with "!", glowing wind curves, volumetric dust, a wall that grows | Dust streaks, shake, flash | Medium |
| 9 | 3D | Real tilt up to 30-40°, extrusions | Hillshade + fake perspective tilt | Medium |
| 10 | Density | 3-8 animated elements, a new one every 0.8-1.5 s | 2-4 elements, new one every ~1.5-2.5 s | Medium |

Rhythm note: their speed comes from new elements every second inside a calm, continuous camera, not from many cuts.

## Fix plan (free tools only)
1. Subtitles: small white sentence case, soft shadow, ~78% from top.
2. Camera: drop whip/flash/chromatic/shake on cuts; smooth continuous moves with slight rotation; a flash only on 2-3 key beats.
3. Neon kit: thick glowing lines and region fills with 20 px bloom, pulsing shockwave rings, warning "!" markers, a growing wall/line.
4. Own vector icon set drawn in code (people, ships, tractors, fish, dam, soldiers, elephants) and unit counters where icons multiply with the number; emoji only in the hook.
5. Map grade: teal sea with depth gradient from the bathymetry we already download, more saturation; option: Sentinel-2 cloudless **2016** tiles by EOX (CC BY 4.0; later years are non-commercial, avoid).
6. 2-3 non-map inserts per Short: 2D cross-section, scale comparison, paper map card for historical documents.
7. Text: no black stroke, white/cream with soft shadow, "≈" counters, max 3-4 slams per Short.
