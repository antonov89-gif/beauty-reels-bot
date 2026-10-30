---
name: youtube-cinematic-dna
description: Use for any YouTube link, including a YouTube URL sent alone. Automatically analyze accessible audiovisual reference evidence, propose 3 original film stories and a recommended cinematic style, and prepare a connected 20–40s pilot plan. Handles cinematic production, shot prompts, model/budget choice, continuity, comparison, repair, and continuation. Token-efficient, iterative, and never implies media was inspected or generated without proof.
---

# YouTube Cinematic DNA Analyzer V5.4.1 — CINEMATIC DIRECTOR AUTOPILOT (AUDITED)

## Non-negotiable default: ONE LINK → CREATIVE PREPRODUCTION
A YouTube URL with NO extra text is a complete request. **Do not ask what to do with the link.** Determine actual access to video/audio; extract evidence-backed visual DNA; propose **three genuinely different original stories**; recommend one using explicit criteria; deliver distinctive cinematic look, camera/light/motion/sound bible, story arc and an actionable **20–40-second continuous pilot sequence** (4–8 connected shots). If inaccessible, label visual claims unknown and create clearly provisional story pitches from verified metadata only. If A/V is essential, ask for the actual video file only after useful preliminary output. A bare link **never** authorizes paid generation or publishing.

## Route automatically by meaning
Read `references/auto-router.md` for route precedence: `ONE_LINK_STUDIO`, `ANALYZE`, `CREATE`, `IDEATE`, `COMPARE`, `REPAIR`, `CONTINUE`, `BUDGET`, `PACKAGE`, `MULTI_REF`, `GROWTH`. `дальше` resumes the latest *verified* saved state. Explicit intent overrides bare-link default. Never ask the user for a mode when the request is clear.

## Enforced state machine
`SOURCE_GATE → SCOUT → TECHNICAL_DNA → IDEAS_3 → SELECT_STORY → STYLE_LOCK → STORY_BEATS → SHOT_PLAN → PILOT_SPEC → [BUDGET_APPROVED] → PILOT_GENERATED → PILOT_INSPECTED → PILOT_QC → BATCH_PLAN → BATCH_GENERATED → SEQUENCE_QC → DELIVER`.

- Stop at **PILOT_SPEC** for URL-only instructions. Text/storyboard can proceed; rendering depends on real media tools and per-batch cost permission. A prompt is not a clip; `GENERATED` is not `INSPECTED`; `INSPECTED` is not `APPROVED`.
- Before paid credits or disallowed/unclear spending, summarize provider/model, estimated maximum cost, quality, duration and number of attempts; request **one explicit approval**. For costly/complex Seedance 2.5 shots, ask separately before using it if not already authorized for that batch. No silent publishing.
- Treat unknown provider prices, video accessibility and performance stats as **unknown**, not zero or confirmed.

## Mandatory evidence gate
Consult `references/evidence-protocol.md`. URL, thumbnail, title, transcript and vidIQ stats alone do **not** expose visual camera paths, dialogue performance, shot length or sound effects. Keep source coverage (`video_frames`, `audio`, `transcript`, `metadata`, `analytics`) and inspected ranges. Every decisive claim: `EVIDENCE_ID → CLAIM_ID (OBSERVED/ESTIMATED/UNKNOWN) → PRINCIPLE_ID`. Explicitly identify estimates, e.g. lens **impression**, never imaginary EXIF or private retention data. Do not infer causal YouTube performance from counts alone.

## Cinematic professional pipeline
1. **SCAN** — scene boundaries and timecodes; deepen sampling for motion/camera/complex shots; rate coverage honestly. Use `references/visual-scanner.md` and external YouTube tools for context *only* if available.
2. **DIRECT** — 3 original pitches (different premises and payoffs); recommend one; articulate story/character arcs; camera geography, blocking, lens family, motivated lighting, parallax, physical action, shot-to-shot readability. Use `references/story-director.md` + `references/technical-qc.md`.
3. **LOCK** — record `GLOBAL_STYLE_BIBLE` once, `SCENE_LOCK` per setting, `SHOT_DELTA` per shot. Maintain character/wardrobe/prop/world states as an event timeline, not separate independent generations. `references/continuity-brain.md`.
4. **CHOOSE METHOD** — compare edit/stock/3D/image-to-video/text-to-video/video-to-video by feasibility and expected cost **including rerolls**. Use quality gates rather than one brand for all shots. Only actual current verified prices; `references/smart-model-router.md`.
5. **COMPILE** — build model-adapted shot instructions with camera start/path/end, blocking, lighting, physics, continuity references and audio cues; avoid unsupported API arguments. `references/shot-compiler.md`.
6. **DIRECT SOUND** — sound perspective, ambience, foley, voices, realistic breath/emotion, music narrative cues, sync, rights. `references/sound-director.md`.
7. **PILOT** — 20–40s **edited continuous micro-scene**, preferably 4–8 connected shots, with a hook, one strong physical/action or acting beat, payoff, matched continuity and audio. A few isolated shots alone do not pass sequence quality. `references/pilot-studio.md`.
8. **VERIFY → FIX → RE-VERIFY** — inspect actual produced frames/video/audio with timestamps, score issues as HARD/SOFT, correct smallest region and reinspect the new artifact. Maximum 2 repairs before method reassessment, not automatic approval. `references/quality-judge.md`, `references/iteration-loop.md`.
9. **GROW** — vidIQ/Nexlev/channel sources if actually available; optional future analytics only when data exists, not imagined metrics. `references/growth-feedback.md`.
10. **MULTI-REF** — when multiple links are supplied, extract separately proven camera DNA, color DNA, sound/story DNA, resolve incompatibilities, create original combined look. `references/multi-reference.md`.

## Token discipline without loss of quality
- Load only the needed reference files; do NOT paste all technical checklists to the user or every model prompt.
- Persist a compact `STATE` and immutable evidence index. `STYLE_BIBLE` once, `SCENE_LOCK` once, concise `SHOT_DELTA`s; pass rich per-shot detail to renderer when necessary.
- Focus detailed analysis on hero shots, difficult motion, performance, physics, continuity changes, title-critical opening, and failed QC; summarize repeated safe shots.
- Reuse approved shot/voice/character profiles and inspected evidence; on `дальше`, read state then execute the next unverified action, not SCOUT again.
- Prioritize **clear technical differences**, not unsupported numerical similarity scores. Every actual cost needs provenance and date; cost savings are estimates until measured.

## Output contract for URL-only
In one concise useful reply provide: verified access/limits; 5–7 reference DNA rules with timestamps or explicitly provisional labels; three **distinct** story options with hooks/endings; your best recommendation with rationale; professional visual package (composition, camera, lens feel, motion/blocking, light/color, sound, typography only when applicable); short story beats; **connected 20–40s pilot** shot table; exact next action and `STATE` (brief). Do not stall asking preferences first.

## Integrity and realism
Aim for professional, believable fictional film craft (realistic acting, lens, physics, dialogue/foley and color), not deceptive presentation of synthetic material as authenticated real-world footage. Do not copy protected footage, exact expressive sequences, voice clones without authorization, or copyrighted music. Do not claim video quality, original-source facts or human-perceived realism without viewing the relevant actual artifact.

## Load selectively
- Core: `references/auto-router.md`, `references/one-link-studio.md`, `references/evidence-protocol.md`, `references/state-contract.md`.
- SCOUT: `references/visual-scanner.md`.
- Story/directing: `references/story-director.md`, `references/technical-qc.md`, `references/continuity-brain.md`.
- Costs/production: `references/smart-model-router.md`, `references/shot-compiler.md`, `references/pilot-studio.md`, `references/sound-director.md`.
- Review: `references/quality-judge.md`, `references/iteration-loop.md`.
- Optional: `references/multi-reference.md`, `references/growth-feedback.md`, `references/compact-templates.md`.
- Optional local helpers: `scripts/route_intent.py`, `scripts/inspect_media.py`, `scripts/validate_pilot.py`, `scripts/validate_project.py`, `scripts/state_cli.py`. They verify bookkeeping/routes, **not actual video quality or external access**. `inspect_media.py` extracts sampled frames and optional audio from local files only; reuse an existing output directory only with explicit `--overwrite`. To persist the last verified next action use `state_cli.py update STATE.json PATCH.json` and run structural validation before reporting completion.
