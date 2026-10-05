# v12 — '¿Y si?' style (stock footage + flat infographics)

Matches the reference channel: real stock clips/photos with slow push-ins, light-grey flat infographics
(black pictograms, navy 3/4-view cube with km labels, grey tower silhouettes), light flat map with a red
pointer arrow and flags, a semi-transparent 3D cube over tilted satellite imagery, white bold numbers on
footage, hard cuts, no karaoke captions.

Media (not committed): `media/*.mp4` from Pexels (via vidIQ b-roll search; download full quality from
`https://www.pexels.com/download/video/<id>/`), `media/*.jpg` from Wikimedia Commons (licences in
`media/credits_wiki.json`), `manhattan_z15.jpg` + `manhattan_meta.json` (USGS z15 mosaic), `Montserrat.ttf`.
Reuses the v11 narration (`timing.json`, `voice.wav`, `music.wav`).

`python3 engine12.py prep` (cut clips to 1080x1920 frames) -> 4 x `engine12.py video A B cK.mp4` -> mux with mix.wav.
