# YouTube Cinematic DNA Analyzer V5.1

**Evidence-gated forensic analysis + original film production + iterative QC, with lean token usage.**

This updates the prior V5.0 package. The key new rule is strict provenance and an actual **reference evidence → production decision → generated artifact → inspected QC → verified repair** chain. Nobody can pass a shot just because a prompt sounds professional.

## Files
- `SKILL.md` — primary skill instruction; keep loaded while using the workflow.
- `references/evidence-protocol.md` — mandatory when source/video analysis begins.
- `references/iteration-loop.md` — mandatory during generation and correction.
- `references/technical-qc.md` — film-grade technical checklist, loaded only when needed.
- `references/compact-templates.md` — tiny handoff states and evidence/shot/QC records.
- `prompts/master-command.md` — copy/paste launch instruction.
- `examples/commands.md` — invocation examples.

## Usage
1. Place skill files in a skill-compatible environment and configure your AI assistant to read `SKILL.md`. Or paste `prompts/master-command.md` for an assistant without native skill support.
2. Send a YouTube link **or** accessible video file, and optional instruction e.g. `Разбери по DNA, SMART`.
3. Receive a source/coverage statement, audited cinematic DNA, then original script/shot plan on request.
4. With video/image/audio generation and editing tools available, make a 2–3-shot pilot. QC actual outputs; fix, recheck, and then batch.
5. Carry the compact `STATE` to the next stage so analysis isn't repeated.

**Not an auto-installed ChatGPT skill or video-generation service.** It is portable instruction files. A URL alone cannot guarantee audiovisual inspection. Real vidIQ/Nexlev lookups, generated clips, rendered edits, and independent QC require suitable tool connections and media access.

**Token economy:** reuse global Style Bible and per-scene locks; generate concise shot deltas; inspect high-risk segments at finer resolution; record only unresolved defects. This preserves film-quality gates rather than omitting them.

**Truthfulness:** no fabricated frame audits, performance metrics or rendered video. For photoreal factual contexts, do not present AI reconstructions as authenticated real footage.

## Optional structural evidence validator
Run:

```bash
python scripts/validate_project.py examples/sample-project.json
```

Create/update a similar project JSON as real evidence, claims, shots and QC outputs arrive. The script checks references between records, prevents status jumps and rejects `APPROVED` records without inspected output QC or with open hard failures. It **cannot watch footage, validate that evidence is truthful, or automatically assess cinematography**; genuine media review remains mandatory.
