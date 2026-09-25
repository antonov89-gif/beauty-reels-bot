---
name: render-and-verify
description: Render a beauty-reels-bot draft through HyperFrames and verify the output MP4 is real (non-empty, actually decodable) before telling the user it's ready. Use whenever asked to render, preview, or re-render a draft, or to debug why a rendered video looks wrong or empty.
---

# Render and Verify

Project-specific workflow for this repo's `VideoRenderAgent` (`reels_mvp.py`).
Rendering silently producing a broken or empty file is the failure mode this
skill exists to catch — HyperFrames can exit 0 while writing a truncated or
corrupt MP4 if the composition template has bad data.

## Steps

1. **Confirm the draft's fields are filled.** `VideoRenderAgent._fill_template`
   HTML-escapes `title`/`hook`/`body`/`cta` into
   `reels-video/templates/reel-card.template.html`. If any field is empty,
   the render will "succeed" with blank text — check the draft row first.

2. **Render.**
   ```bash
   hyperframes render -q "$HYPERFRAMES_RENDER_QUALITY" -o "$output_path" reels-video/templates/reel-card.template.html
   ```
   (or call `VideoRenderAgent.render_draft` directly if working through the
   bot's async code path). Capture stderr — `VideoRenderAgent` already
   raises `RuntimeError` with the stderr tail on a non-zero exit, but a
   silent success still needs verification below.

3. **Verify the output is real, not just present:**
   ```bash
   test -s "$output_path" || echo "EMPTY FILE"
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "$output_path"
   ```
   A file that exists but is 0 bytes, or that `ffprobe` can't read a
   duration from, is a failed render even though the CLI exited 0.

4. **Only after verification passes**, report success or send the file —
   never claim "rendered successfully" from exit code alone.

## Common failure causes seen in this project

- Asset path in the template isn't root-relative (HyperFrames' StaticGuard
  rejects `../assets/...`; must be `assets/...`) — see `hyperframes-core`.
- `_render_lock` contention: concurrent renders writing to the same
  temp path. Check `reels_mvp.py`'s `_render_lock` usage if two renders
  overlap.
- Missing Chrome/ffmpeg in the runtime (only reproducible in the Docker
  image, not local dev where `hyperframes browser ensure` was already run).
