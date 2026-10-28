# Channel Style DNA V1.0 — Own Channel First

Standalone Codex-style skill plus bridge to **YouTube Cinematic DNA V5.4.1**.

## The goal
You provide **your channel URL or banner**, then **a competitor channel/video URL**. This skill builds an evidence-labeled brand identity, isolates transferable competitor format/camera/retention techniques, and develops **new content recognizable as YOUR channel**. On later videos, only the new competitor reference is needed because the approved brand is saved per project. For a brand-new channel, the style bible stays a draft until approved.

### Examples (both inputs can arrive in any order)
- `Мой канал: https://www.youtube.com/@MyChannel` then `https://www.youtube.com/watch?v=EXAMPLE`.
- Upload a banner/avatar and paste competitor link.
- `Наш стиль сохрани, вот референс` plus competitor video.
- Upload our new output and say `проверь, чтобы выглядело как наш канал`.

### Installation
1. Extract `channel-style-dna` into your project's `.agents/skills/` or into a Codex skills directory configured for discovery.
2. Verify `SKILL.md` exists immediately inside the folder. Optional: install **youtube-cinematic-dna** alongside it, not inside it.
3. For even more reliable default behavior, copy the optional entry from `examples/AGENTS-snippet.md` into the project's `AGENTS.md`.
4. Keep `.channel-style-dna/project.json` inside your project; copy it when moving between workspaces. Storing approved brand state in project files is more reliable than assuming a fresh chat remembers it.

### What changes when only a banner is provided?
Colors/logo/type/layout can be estimated directly. Cinematic camera, editing, audio and actor performance **cannot** be proven from a still image, so these remain creative recommendations rather than observations. One or more videos from your own channel increases evidence quality.

### What's real vs aspirational?
- Real now: structured process, project status/permissions validator, deterministic compact prompt compiler, examples and integration policy.
- Conditional: actual YouTube video viewing, channel fetching, vidIQ/Nexlev metrics, paid video generation, file publishing, visual/video/audio quality assessment. Require separate authorized tools and media access.
- `scripts/*` enforce only schema and handoff consistency; they cannot evaluate pixels, audio, professional film quality, or scrape YouTube.

## Test
```bash
python -m unittest discover -s .agents/skills/channel-style-dna/tests -v
python .agents/skills/channel-style-dna/scripts/validate_channel_project.py .agents/skills/channel-style-dna/examples/sample-project.json
python .agents/skills/channel-style-dna/scripts/compile_shot_prompt.py .agents/skills/channel-style-dna/examples/sample-project.json --shot SH01
```

## Source priority
1. Last explicitly **approved** user brand bible
2. User-provided current brand brief or corrections
3. Verified owned-channel videos/audio
4. Verified banner, avatar, thumbnails
5. Provisional creative proposals
6. Competitor visuals: inspiration for transferable mechanics only, never owned brand source

## Do not confuse
- A premium cinematic look is not automatically the channel's visual identity.
- Title/thumbnail identity, font, colors, sound, camera grammar and storytelling must be separated, then coordinated.
- High competitor performance cannot by itself prove why viewers watched.
