# v11 — tile-camera map Shorts (city-scale zooms)

`engine11.py` renders from web-mercator tiles: NASA GIBS Blue Marble (z<=8) and USGS National Map
orthoimagery (z9-16, US only; public domain). No-data pixels (black/white) are filled from parent tiles.

Pipeline: `tts_lumean.py go` -> `timing_from_align.py` -> `engine11.py prefetch` (downloads tiles; run before
rendering so parallel chunks never fetch at the same time) -> 6 x `engine11.py video A B cK.mp4` ->
`audio11.py` -> concat + mux -> `srt11.py`. Needs `assets/` from v10 (fonts, Natural Earth) and `.lumean_key`.
