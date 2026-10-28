# Cinematic DNA Analyzer V5.4.1 — Director Autopilot (Audited)

**One YouTube link → truthful audiovisual source check → technical DNA → 3 new film premises → selected story and cinematic bible → full 20–40-second edited pilot specification.**

V5.4.1 builds on V5.4 and fixes stale sampling on repeated video inspection, extracts matching audio for local inspection and supports persistent STATE updates. V5.4 originally upgraded V5.3 with an evidence-aware visual scanner, AI film director, continuity state tracking, budget/model router, shot-specific prompt compiler, sound director, continuous pilot studio, artifact-based QC and follow-up YouTube feedback. Multiple references are also supported.

## Codex installation

1. Unzip; keep the directory name `youtube-cinematic-dna` and its `SKILL.md`.
2. Put this directory in your project's `.agents/skills/youtube-cinematic-dna/` (or another directory supported by your installed Codex version). Replace older versions rather than retaining duplicate names.
3. Refresh/restart skill discovery when necessary. You can explicitly invoke `$youtube-cinematic-dna`, but ordinary YouTube URLs are intended to match the description automatically **when the agent supports skill discovery**.
4. Send a YouTube link with no extra text. Automatic skill selection is heuristic, not guaranteed. For a one-link workflow that is more reliable, add `examples/AGENTS-snippet.md` instructions to your project-root `AGENTS.md`. The response includes 3 stories and a pilot production plan, not merely a link summary.

Codex/agent support, YouTube media download/decoding, access to vidIQ or Nexlev, paid rendering tools and a local FFmpeg installation are **separate capabilities**. This package does not magically add these tools or a subscription. If video cannot be inspected, the skill explains the evidence gap. Production remains gated by actual tools and cost permission.

## Behavioral examples

| Input | Action |
|---|---|
| A bare YouTube link | ONE_LINK_STUDIO: evidence → cinematic DNA → 3 pitches → selected original film → 20–40s continuous pilot plan |
| `Сделай своё кино как референс` | CREATE, develop story → directing → pilot, request cost approval before paid render |
| `Дальше` | Resume exactly from saved verified STATE |
| `Исправь зум на 00:12` | REPAIR, inspect actual clip then precise local changes |
| `Сравни с референсом` | COMPARE two actual inspected sources, otherwise request missing output |
| Two or more URLs | MULTI_REF: split camera, color, story/sound influences with evidence |
| `Сколько будет стоить?` | BUDGET: price/source/expected attempts; no imaginary totals |

## Structure

- `SKILL.md`: lean orchestration and safety/production gates.
- `references/`: on-demand methods for source, camera/story, continuity, budget, sound, pilot, QC, growth and multi-ref.
- `prompts/master-command.md`: portable instructions for agents without native skill support.
- `examples/`: sample project with honest unstarted stages and expected behavior.
- `scripts/route_intent.py`: deterministic routing smoke-test; semantic judgment is still agent's job.
- `scripts/state_cli.py`: persistent small state file helper.
- `scripts/validate_project.py`: source/status ledger lint, not AI video QC.
- `tests/`: local stdlib unit tests.

## Quick local tests

```bash
python -m unittest discover -s tests -v
python scripts/validate_project.py examples/sample-project.json
python scripts/route_intent.py 'https://youtu.be/abc123'
python scripts/state_cli.py init /tmp/cinematic-state.json
python scripts/state_cli.py show /tmp/cinematic-state.json
# To persist an agent-written state patch:
# python scripts/state_cli.py update /tmp/cinematic-state.json path/to/state-patch.json
```

## Important cost boundary

Text analysis and creative planning can be automatic. **No paid video generation or posting from a bare link.** Before rendering, obtain tool access, current prices and explicit batch approval. Complicated shots may justify Seedance 2.5 or a more expensive approach, but request approval before spending unless the user already approved that exact batch.

## Final principle

`SOURCE PROOF → FILM LANGUAGE → ORIGINAL STORY → CAMERA/BLOCKING/LIGHT/SOUND → PILOT → REAL QC → TARGETED FIX → BATCH`. A prompt written is not a film delivered.

## Continuous pilot timeline validator

```bash
python scripts/validate_pilot.py examples/sample-pilot.json
```

This checks timeline continuity and presence of camera, action and sound plans, **not whether the finished footage actually works**.

## Optional local video probe (FFmpeg required)

For a video file you can lawfully access locally:

```bash
python scripts/inspect_media.py path/to/clip.mp4 --out inspection --start 0 --duration 10 --fps 6
```

This extracts bounded frames, synchronized audio when available, and container metadata; it does not itself understand the images or access YouTube. The generated `manifest.json` explicitly marks what was extracted and what is still uninspected.

## Repeated inspection safety

An existing output with prior sample files is rejected unless `--overwrite` is passed. This prevents old frames from contaminating a new analysis. `--overwrite` deletes only previous numbered extracted JPEG files plus sample audio and manifest in the chosen output directory. Extracted audio is **not yet listened to by the script**.
