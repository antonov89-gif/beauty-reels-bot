# Gap analysis: our Shorts vs reference jTJ2UFF3B0I (rajography), 22.10.2026

Sources for the reference: two vidIQ AI watches (scene walkthrough + camera/visual breakdown), video stats and comments (see dna_jTJ2UFF3B0I.md). The reference video itself was not downloaded, so reference details are STRONG INFERENCE, not frame-measured.
Our videos were measured with ffmpeg (cuts, loudness, motion per shot) and checked frame by frame.

Legend: YES = matches, PART = partly, NO = missing.

| # | Element | Reference | Lofoten v4 | Maldives v2 |
|---|---|---|---|---|
| 1 | Length | 20 s | YES 19.8 s | YES 19.8 s |
| 2 | Hero subject | ONE subject (the temple) in every shot, centred | NO: 6 different places | NO: 7 different places |
| 3 | Footage | real 4K drone | YES real 4K drone (Pexels) | NO satellite with a virtual camera |
| 4 | Globe zoom length | ~3 s | YES 2.9 s | YES 2.85 s |
| 5 | Globe look | Google-Earth-like 3D terrain, atmosphere glow, cloud layer | PART glow yes; flat imagery, no clouds, no 3D terrain | PART same |
| 6 | Zoom depth | down to rooftop height (~100-200 m), top-down | PART ends ~1.2 km above the coast | NO stops at country scale, then cut |
| 7 | Zoom image quality | clean | PART Esri mosaic seams and blur in the last frames | PART |
| 8 | Hook text | 1 block, top-centre, white, dark shadow, ~6 words + emoji, 3 s | YES style; PART 8 words, drawn flag instead of emoji | YES style |
| 9 | Hook meaning | emotional conflict claim ("The ocean tried. This temple survived") | NO informational ("This is Lofoten... Above the Arctic Circle") | PART tension ("The sea is rising... 1.5 m high") |
| 10 | Text after the hook | none | YES | YES |
| 11 | Shot lengths | varied: ~4/4/3/1/1/4 s | YES 3.9/2.9/3.9/1/1/4.3 s | NO uniform 2.4 s |
| 12 | Shot 1 after the zoom | drone ascend (pedestal up) on the subject | YES ascend over the ridge (Reine revealed) | PART virtual push |
| 13 | Low telephoto pan from the sea | yes | NO (our pan is high drone) | NO |
| 14 | High forward push with slight yaw | yes | PART digital push + yaw on 4K (not a real move) | PART virtual |
| 15 | 1 s close-up + 1 s wide sweep | yes | YES | NO |
| 16 | Finale | true top-down (nadir) descent with slow rotation, 4 s | NO steep oblique, no rotation (no such Lofoten clip) | YES virtual top-down push with rotation |
| 17 | Light | daylight + one golden/dusk shot | NO all midday | NO all midday |
| 18 | Colour | high saturation, contrast moderately high, no grain/vignette/flare | YES footage (+14% sat); PART engine vignette on the globe part | PART vignette |
| 19 | Cuts | hard cuts on the beat | YES on beat (+20-50 ms) | YES after the 35 ms fix |
| 20 | Music | real recorded music, regional vocals + percussion, ~120-128 BPM | PART synthesized 124 BPM, synth "voice"; not regional, weaker than a real recording | PART same |
| 21 | Sound effects | none | YES none | YES none |
| 22 | Loop to the start | nadir end -> globe start | PART | YES |
| 23 | Title | place + claim + place hashtags | YES | YES |
| 24 | Emotion | awe + pride/belonging of a community | PART awe only | PART awe + worry |
| 25 | Comment trigger | debatable claim (comments argue about it) | NO | PART ("Would you live here?" not in v2) |
| 26 | Channel fit | drone channel with an audience for this format | NO our audience comes for map explainers (not fixable in the video) | NO |

## Biggest gaps (by expected effect, HYPOTHESIS)
1. No single hero subject (rows 2): the reference circles ONE place; ours is a tour.
2. Hook without conflict (row 9): the reference opens with a struggle and a survivor.
3. Zoom not deep enough and no 3D look (rows 5-7): the reference lands on the roof.
4. Finale is not a true top-down descent (row 16) and there is no golden-hour shot (row 17).
5. Music is synthetic (row 20).

## Fix plan
- Lofoten v5 around ONE subject, Reine village: search Pexels for more Reine clips (vidIQ broll, ~1 credit per search), all shots of Reine from different angles; hook with tension, e.g. "Winter here: weeks without sunrise. They stay." (check the polar-night fact for Reine before use); zoom down to ~200 m with extra Esri imagery and a final tilt (oblique engine) for a 3D feel, add a light cloud layer on the globe; remove the vignette on the globe part; one golden-hour shot if a Reine clip exists.
- Music: a licensed or royalty-free recorded track (no copyrighted or trending music without a licence), or the user adds a trending sound inside TikTok.
- Maldives: keep as is (user decision); it cannot match the drone look without real footage.

## v5 status (22.10, after the user's "делай все недочеты как у референса")
Fixed: one hero subject (all shots Reine) | hook with tension + colour emoji | clouds on the globe, dive to the rooftops (~350 m view), top-down | dusk/golden shot (ascend reveal) | ascend reveal as the first drone shot | real recorded music (Mixkit, 125 BPM, cuts on its beats) | no vignette | comment trigger (debatable "sea doesn't freeze", hedged in the description) | real forward drift (no digital push).
Still different: finale is satellite rooftops, not a drone nadir; no low telephoto shot from the sea level; no 3D terrain in the zoom; channel/audience effect.

## v6 status (22.10, "Делай все отличия")
Fixed now: 3D look in the dive (terrain relief from AWS Terrain Tiles baked into the imagery as hillshade + oblique camera that tilts like a Google-Earth fly-in and levels to straight down on the roofs); cuts snapped to the measured drum hits (offset <= 12 ms).
Searched and not available for free: a drone nadir clip of Reine and a sea-level telephoto shot of Reine (Pexels: none; Wikimedia Commons: API rate-limited from this network). Only AI generation could add them (paid, waits for the user's approval; would be labelled AI).
