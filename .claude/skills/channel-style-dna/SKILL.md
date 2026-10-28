---
name: channel-style-dna
version: 1.0.0
description: >
  Own-channel-first visual identity and cinematic consistency for YouTube creation.
  Use when the user supplies their YouTube channel, banner/avatar, approved video(s),
  or saved brand bible together with a competitor channel/video reference (in any order),
  or asks to recreate a successful competitor format in their OWN recognizable channel style.
  Autonomously audit accessible evidence, lock the user's channel DNA, extract transferable
  competitor mechanisms, pitch original stories and plan/QA videos without cloning.
  Integrates with youtube-cinematic-dna V5.4.1 and uses compact persistent project state.
---

# CHANNEL STYLE DNA V1.0 — OWN CHANNEL FIRST / COMPETITOR MECHANICS SECOND

## Core contract: ONE CHANNEL, MANY STORIES, ONE RECOGNIZABLE WORLD
**USER BRAND > COMPETITOR TECHNIQUE > GENERATOR DEFAULTS.** Goal: a new original video that unmistakably belongs to the user's channel while borrowing transferable *mechanics* (hook, structure, shot rhythm, narrative tension, techniques) from a competitor. Never replace the user's channel identity with a competitor's look, palette, logo, characters, distinctive scenes, or voice.

User should NOT need a master prompt. Accept inputs in any order: own channel URL, channel banner/avatar/screenshots, original approved videos, competitor channel URL, competitor video URL, short phrases ("как у конкурента, но в моём стиле"), and `дальше`. When both channel and competitor references are known, auto-run BRAND_SCAN → REF_SCAN → TRANSFER → ORIGINAL_IDEAS → DIRECTOR_PLAN → PILOT_SPEC. If a previously verified `BRAND_LOCK` exists, a **single new competitor URL** is enough; do not request the channel again.

## Route quickly
1. `OWN_SOURCE` only → extract and draft channel style with explicit confidence/unknowns; propose a brand lock and possible content formats, no competitor claims.
2. `OWN_SOURCE + COMPETITOR` (either order) → make the transferable competitive adaptation with 3 original pitches, recommendation, cinematic bible, pilot storyboard.
3. `COMPETITOR` only + existing approved `BRAND_LOCK` → use that brand; analyze new competitor reference.
4. `COMPETITOR` only + no usable brand → inspect competitor if possible, then ask **one** direct question requesting the user's channel URL or banner. Do not invent a house style.
5. `OUR_VIDEO` + brand + competitor → compare/repair our delivered footage: prioritize true brand fit, then filmcraft, then competitor mechanism effectiveness.
6. `дальше` → load saved verified project state and continue the next pending action. Don't redo already inspected material unless changed.
7. Bare reference URL when BOTH references present in project STATE → treat as *additional competitor reference*, unless the user labels it otherwise. An isolated URL with no other clues stays provisional until origin is established. **Two unlabeled channel links without ownership context must not be arbitrarily assigned**; ask one short ownership question only if needed.

## Evidence and source gate — no fictional inspection
Record what actually was accessed: own channel page/metadata, banner/avatar image pixels, actual own videos (frame ranges/audio), competitor channel page, competitor video (frame ranges/audio), transcript, public metrics and vidIQ/Nexlev results if truly available. **A banner is NOT evidence for the channel's camera, lens, voice, average shot length, or storytelling.** Brand visual traits inferred from banner only are labeled `BANNER_ONLY / PROVISIONAL`. A YouTube URL/page does not prove video/audio inspection. For claims about visuals, use observed frames/timecodes and source coverage; audio claims require audio. For unavailable media, deliver a preliminary style plan and identify what's unknown without inventing evidence.

Read selectively: `references/brand-acquisition.md` for sources, `references/competitor-transfer.md` for mechanism extraction, `references/brand-bible.md` for identity locks, `references/directing-and-qc.md` for video plan/quality, `references/state-and-output.md` for records. For cinema-level analysis and piloting, invoke the existing `youtube-cinematic-dna` skill if installed, particularly its evidence, camera, pilot and repair modules. Both skills may cooperate; **this** skill owns Brand Lock and brand-fit QA, `youtube-cinematic-dna` owns detailed cinematic forensics.

## Brand hierarchy — distinct from format
- **IMMUTABLE BRAND CORE (when approved):** official channel name, approved logo/avatar/banner assets, typography system, signature accents, recurring graphic language, intended audience, approved narrative voice, permitted look range, forbidden styles.
- **CINEMATIC STYLE RANGE (brand-specific, adjustable):** photographic realism / stylization, camera grammar, lens family, lighting logic, grading, motion/animation language, transitions, sound signature; don't infer from banner alone.
- **FORMAT-ADAPTIVE LAYER:** competitor hook pattern, narrative structure, pace, genre-specific devices, retention techniques, CTA logic, thumbnail *principles* — **never competitor brand identifiers**.
- **EPISODE DELTAS:** new story, cast, setting, plot, props and per-shot trajectories within the approved brand.

Resolve conflicts using the last expressly **approved** user's `BRAND_LOCK` rather than automatically trusting a newly observed banner, a competitor aesthetic, or generative defaults. Flag differences and ask for confirmation only when changes would contradict the locked brand. If approval is absent, label `DRAFT` and proceed with provisional non-destructive concepts.

## End-to-end steps (in this order)
1. **SOURCE_GATE:** identify and label owned/competitor sources and actual inspected modes/ranges; do not mix sources.
2. **BRAND_SCAN:** extract brand visual DNA (palette, hierarchy, font *impression*, logo usage, negative space, texture, motifs, layouts, grading), voice/tone and film grammar *only if videos/audio available*. Produce `BRAND_BIBLE_DRAFT` with confidence by attribute, no invented specifics.
3. **BRAND_LOCK:** reuse previously approved version; if new, suggest draft identity, declare which rules are provisional, allow user approval before treating it as permanent. User can keep creativity open without forcing an identity decision immediately.
4. **COMPETITOR_FORENSICS:** distinguish mechanics behind attention/retention from expressive assets and unique creative content. For a **competitor channel** rather than a specific video, identify recurring formats and (where actually accessible) inspect 2–4 representative videos including at least one high-performing example; do not infer channel formula from a thumbnail alone. If full media available, analyze hook, tempo, visual grammar, camera, animation, sound, emotional escalation, climax and packaging; if not, avoid temporal precision.
5. **TRANSFER_MATRIX:** classify each successful competitor mechanism as `KEEP_AS_PRINCIPLE | TRANSLATE_TO_BRAND | REJECT | UNKNOWN`. Write its new brand-native implementation. Disallow copy of logos, footage, scripts, exact distinctive character/story beats, protected music, trademarked package elements, etc.
6. **STORY_STUDIO:** suggest exactly 3 substantially different *original* pitches unless user specifies otherwise; recommend one based on brand-fit, plot/emotion, production feasibility, viewer value and budget risk. Don't promise virality.
7. **DIRECTOR_PLAN:** build 20–40s contiguous pilot scene (usually 4–8 shots) and concise original beat sheet; specify story purpose, camera blocking/lens/light/motion, voice, ambience/foley, cut transitions, continuity. Maintain global `BRAND_LOCK` once, `SCENE_LOCK`s by setting and brief `SHOT_DELTA`s; model-ready prompts on demand.
8. **PRODUCTION_GATE:** do not claim rendering without accessible generators; before unapproved paid video generation or posting ask explicitly for authorization and planned spend. Make the user approve particularly expensive model choices if outside an approved batch. Prefer low-cost pilot tests, then scale.
9. **QUALITY / BRAND GUARD:** actually inspect generated clips and audio before accepting. Brand violations are HARD FAIL even if footage is technically cinematic. Compare `BRAND_FIT`, `FILMCRAFT`, `MECHANICS_TRANSFER`, `ORIGINALITY`, `STORY_CLARITY` as reasoned, evidence-backed rubrics; don't fabricate precise scientific similarity percentages. Repair cheapest focal issue, review again; version the outcome.
10. **SAVE / CONTINUE:** persist compact project artifacts where permitted (e.g. `.channel-style-dna/project.json`, source ledger, approved locks, decision history), then `дальше` resumes verified phase. No background action without explicit automation setup.

## Mandatory output, no repetitive wall of text
When user provides own brand + competitor, return (i) coverage/limits, (ii) distinct **OWN DNA** (evidence/confidence), (iii) **COMPETITOR MECHANICS** (evidence/confidence), (iv) **TRANSFER MATRIX** with 3–7 high-value moves, (v) 3 new story premises + recommendation, (vi) **BRAND-NATIVE LOOK** including camera, animation, palette/typography, voice/sound and thumbnail, (vii) short connected pilot shot list, (viii) next verifiable step and missing permissions only when blocking. Keep detailed tables/files off the chat unless asked. Brand scans must not make unsupported claim the channel owns a specific font, lens or grading profile.

## Integrity constraints
- Make a technically great video, not a fake 'human-shot' documentary presented as genuine event evidence.
- Distinctive character identities, competitor channel visual logos, scripts, voice cloning and protected footage/soundtracks are not transferable principles.
- Published views are observations; causal reasons/retention without creator-side analytics are hypotheses.
- Always separate an approval of the channel identity from an approval to spend, generate, publish or impersonate.
- Don't duplicate costly full-video analysis when an unchanged evidence ledger and approved brand bible already exist.

## Files used on demand
- `references/brand-acquisition.md` — source coverage and confidence.
- `references/brand-bible.md` — stable identity architecture.
- `references/competitor-transfer.md` — lawful/original mechanism adaptation.
- `references/directing-and-qc.md` — pilot, camera, animation and brand QA.
- `references/state-and-output.md` — compact JSON contracts + lifecycle.
- `references/integration-v5.4.md` — complementary skill routing.
- `prompts/master-command.md` — portable launch policy.
- `scripts/validate_channel_project.py` — schema/status checks (not image understanding).
- `scripts/compile_shot_prompt.py` — short scoped per-shot handoff; no generation API.
