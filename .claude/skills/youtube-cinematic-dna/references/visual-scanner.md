# EVIDENCE-GATED VISUAL DNA SCANNER

## Capture coverage before inference
Record: URL, access time, actual reachable source (A/V file, platform stream, user-uploaded video), duration, video/audio availability, timestamps inspected, frame sample rate and sampling strategy, transcript/metadata origin. If only page available, never label an observation about movement/lighting/sound as verified.

## Scan algorithm
1. Examine opening 0–10s densely. If source has fast edits, sample densely enough to resolve them; 1 frame/sec is often insufficient for sub-second changes.
2. Establish scene boundaries and a compact shot list (actual timestamp IN–OUT only when verified). Avoid treating automatic scene-cut detection as perfect.
3. Select hero shots, new locations, large camera moves, action/physics, unusual visual effects, actor close-ups and scene transitions for deep inspection. Expand sample when ambiguity is material.
4. For each chosen shot: narrative purpose; camera position/lens *feel*; shot size; blocking; motion vectors and speed/acceleration; parallax; focus; source-motivated lighting; color/contrast; FX; likely edit motivation; SFX and acoustic distance only if audio inspected.
5. Derive style principles; attach `evidence_ids` and reliability. Estimate lens/FPS/zoom only as impression unless metadata genuinely contains it.
6. Validate against atypical examples; do not declare a style rule based on a single incidental shot.

## Optional local capture (only for authorized, already accessible files)
- `ffprobe -v error -show_format -show_streams -of json input.mp4` for actual container metadata.
- `ffmpeg -ss 00:00:03 -i input.mp4 -frames:v 1 frame.png` for manually selected frames.
- `ffmpeg -i input.mp4 -vf 'fps=4' frames/%05d.jpg` for dense sample **of short selected ranges**, not an entire multi-hour upload.
- `ffmpeg -i input.mp4 -af astats -f null -` only for audio properties, not music identification.
- Tools can aid inspection but do not manufacture perceptual evidence. Respect distribution rights and access rules; don't bypass paywalls/DRM.

## Minimal shot evidence record
`EVIDENCE_ID | verified range | actual modalities | source | visual/action observation | confidence`.
`CLAIM_ID | category | OBSERVED/ESTIMATED/UNKNOWN | evidence_ids | transferable implication`.

## Blind spot handling
Report uninspected parts and whether representative sampling might miss late stylistic changes. vidIQ/Nexlev validate content strategy, not physical camera motion, shutter, foley or image texture.
