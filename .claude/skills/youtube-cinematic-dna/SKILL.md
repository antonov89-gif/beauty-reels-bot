---
name: youtube-cinematic-dna
description: Evidence-gated YouTube/video reference reverse engineering, professional cinematic style transfer to original stories, staged generation, and verifiable iterative shot/sequence QC with token-efficient state handoffs.
---

# YouTube Cinematic DNA Analyzer V5.1 — Evidence → Produce → Verify

## Trigger and purpose
Use when the user sends a YouTube link/video and requests analysis, “как референс”, matching cinematic visual language, an original story, production prompts, a storyboard, or checking/reworking outputs. Default to **SMART / evidence-gated iterative** mode. The goal is comparable **filmmaking language and production quality**, never an unlicensed frame-for-frame duplicate.

## First rule: evidence before precision
A URL, webpage, thumbnail, transcript, title, or vidIQ/Nexlev statistics do **not** prove the camera/lens/motion/audio of the film. Before any shot-level claims, determine **what was actually viewed or heard** and at what sampling density. Follow `references/evidence-protocol.md` when extracting or diagnosing. If A/V is inaccessible, do a provisional metadata/packaging/story analysis; **never invent shot timings, scene contents, edit counts, music, effects or fonts**. State access limits briefly; ask for the video file only when crucial for the requested technical task. Do not mislabel estimated parameters as camera metadata.

Every decisive reference claim has: `CLAIM_ID`, `EVIDENCE_ID(s)`, time range, `OBSERVED | ESTIMATED | UNKNOWN`, confidence and a concrete implication. For directly seen/heard events cite inspected media; for external performance cite observed source and date. Separate source data from stylistic interpretations. Outlier/retention explanations are hypotheses without creator-side analytics. See `references/evidence-protocol.md`.

## Work phases — stop repeating work
1. **SOURCE GATE:** List accessible modalities (video frames, audio, subtitles, page, analytics) and audited ranges. Do not confuse link recognition with video inspection.
2. **SCOUT:** Map film structure, opening, climax, ending and visually distinctive regions. For Shorts, inspect all shots if accessible; for long-form, use a labeled representative sample and expand on demand. Output 3–7 specific DNA hypotheses with confidence.
3. **EVIDENCE-BASED FORENSICS:** Shot map with actual time ranges, purpose, blocking, shot size, screen direction, camera start/path/end, lens *impression*, subject/environment motion, focus/DOF, motivated lighting and material response, visual depth, editing transition, typography/VFX and sound perspective. Deep-inspect high-impact and ambiguous shots with denser sampling; audio analysis requires audio, not transcript alone.
4. **CROSS-CHECK:** Use vidIQ/Nexlev/available external tools where useful to inspect topic, packaging, audience context, published results, comparable videos and possible outlier signals. Do not pretend these tools viewed the audiovisual material; never claim access to private CTR/AVD/retention without authorized data.
5. **DNA LOCK:** Create a **versioned STYLE_BIBLE**, evidence-backed signature rules, `REFERENCE_PRINCIPLE_ID`s and severity-ranked uncertainty. Store global decisions once, then `SCENE_LOCK`s and per-shot *deltas*. Avoid repeating long prompts.
6. **ORIGINAL STORY TRANSFER:** New premise, characters, causal chain, hooks/payoffs and emotional escalation. Map each new beat to a **general reference principle** (e.g. alternating geographic wides with intimate reactions), not copied dialogue, trademarked assets, distinctive scenes or exact original shot sequences.
7. **CINEMATIC PLAN:** Beat sheet → blocking and geography → camera/lens/light map → storyboard → audio direction → keyed shot deltas → generation method and expected shot outcome. Put plausible physical constraints before adjectives. Use `references/technical-qc.md` for scene authoring.
8. **PILOT THEN PRODUCE:** First test 2–3 diverse shots: hook, close performance/dialogue, physically challenging action (adapt to genre). Actually generate only when tools are present, file/audio assets are accessible, and the user requests production. Otherwise produce implementable specifications, not fictional media.
9. **ITERATIVE QC (mandatory for every output):** Inspect the **actual generated output**, log faults with timestamps and evidence, select cheapest effective edit/regeneration, apply only with available tools, inspect the revised output, regress against scene continuity, and then accept or escalate. Follow `references/iteration-loop.md`. No "fixed", "generated", "matches reference" without a viewed artifact and completed action.
10. **DELIVER / CONTINUE:** Output film-language DNA, original script/next scene when relevant, prioritized action plan, verified status, and compact `STATE`. Persist progress as portable text/files when a filesystem is available.

## Explicit traceability chain
`REFERENCE_EVIDENCE → OBSERVED_CLAIM → TRANSFERABLE_PRINCIPLE → ORIGINAL_BEAT → SHOT_SPEC → GENERATED_ARTIFACT → QC_EVIDENCE → DECISION`.

A link in the chain can be `UNKNOWN`/`PENDING`; never silently fill it. Prioritize evidence for the 5–10 rules that most influence production. A defensible partial audit is better than false certainty.

## Mandatory iteration contract
- Define shot-specific **acceptance criteria before generation**: readable story beat; physically believable action and camera; correct character/wardrobe/object continuity; motivated light and exposure; usable speech/audio; intended mood and rhythm.
- `HARD FAIL`: broken identity/geometry in focal action, severe temporal warping, nonsensical camera/physics, broken key sound/lip-sync/intelligibility, contradiction of story/geography. Cannot approve.
- `SOFT ISSUE`: minor grading mismatch, secondary sound weakness, slightly flat timing or repeated camera angle. Triage by viewer impact.
- **Default repair order:** edit/trim → retime/sound/color → local rework → regenerate the affected segment/shot → change production method. Do not rerender an entire scene to repair a small local fault unless cheaper overall.
- Every pass uses `attempt N`, artifact identity, inspected range, defects, precise delta, method, cost implication, outcome and remaining problems.
- Default to at most **two corrective attempts per shot** before reassessing the approach; this is a budget guard, not automatic acceptance. If blocked, label `BLOCKED`, show alternatives or escalate a method change. Never claim success due to hitting an attempt cap.
- Sequence-level checks run after shot fixes: axis, screen direction, eyeline, wardrobe, weather, lighting, location geometry, action continuity, dialogue/ambience and overall emotional rhythm.
- Scores (if used) are **reviewer judgments**, not objective similarity percentages. Preserve observable fault descriptions and evidence.

## Lean mode — default compact output
Unless asked for FULL, return only: (a) evidence access and coverage, (b) decisive 5–7 DNA principles with evidence IDs, (c) compact shot map and a few high-value deep dives, (d) STYLE_BIBLE ID + only changed settings, (e) next batch of shot deltas, (f) QC failures and exact remedies *only if generated outputs exist*, (g) `STATE` <=350 words. Do not output 150 repeated checklist items. For direct questions on a single shot, reply with that shot alone and updated STATE.

Modes: `SCOUT` (quick accessible review), `SMART` (default selective deep analysis + production and pilot QC), `FULL` (all inspectable shots, with coverage limitations), `REPAIR` (affected shots, evidence and fixes only). A user can choose otherwise explicitly.

## Token and generation cost controls
- Load reference modules only when relevant. E.g. basic scout needs evidence protocol; generation needs technical QC + iteration loop; artifact handoff needs templates.
- Work using `STYLE_BIBLE` once, `SCENE_LOCK` once per location/time and `SHOT_DELTA` per cut. Cache approved character/voice/environment cards.
- Reuse evidence/analysis already inspected; re-open only when missing/conflicting or revisiting a new interval. Never remove necessary evidence in the name of economy.
- Spend deep-analysis effort on hero shots, complex physical interactions, appearance changes, audio transitions and suspected flaws; for repetitive low-risk segments use brief confirmations.
- Report **exceptions and decisions**; do not restate passing checks. Keep tool/model input payloads lean, but **give a rendering model sufficient concrete shot physics, camera and lighting instructions**.
- Compare cost of fixes before new generation. Rendering credits, context tokens, human review and external-service pricing are different cost categories; do not invent savings or prices.

## Source integrity and realistic-looking content
AI-assisted photoreal fiction is fine. Never falsely represent synthetic scenes as actual incident footage, authenticated documentary records or a real-person recording. Do not fabricate viewer analytics. Follow applicable disclosure/provenance obligations where relevant. Do not use realism as a reason to mislead about real events.

## Files to load on demand
- `references/evidence-protocol.md` — admissible sources, evidence ledger, coverage, verified vs inferred claims, source gate.
- `references/iteration-loop.md` — generation/QC/repair cycle and pass/fail gates.
- `references/technical-qc.md` — professional camera, lens, blocking, light, motion, editing, audio and continuity rubric.
- `references/compact-templates.md` — compact record structures and STATE contract.
- `prompts/master-command.md` — reusable stand-alone command for compatible models.
- `examples/commands.md` — common calls and expected mode.
- `scripts/validate_project.py` — optional machine-readable ledger/status lint. It does NOT perform audiovisual QC.
