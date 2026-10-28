# VERIFIED STATE & TOKEN-EFFICIENT HANDOFF

Use a small durable JSON file per project when filesystem available. Required:
- `project_id`, `references[]` with inspected modalities/ranges, `route`, `active_stage`, `next_action`;
- `style_bible_id`, `scene_locks[]`, `shot_deltas[]` are references to durable files, not repeated giant prompt text;
- `story_status`: proposed/selected/written/approved;
- `cost_authorization`: provider, model, tier, resolution, clip count, seconds, budget cap, currency, approved boolean, explicit approval source, time;
- `artifacts[]`: real locations/IDs plus `status` generated/inspected/approved and `qc_evidence_ids`;
- `blockers[]`, `updated_at`, `pending_decision`.

Version approved decisions; update only `SHOT_DELTA` and affected scene/project events. Save provenance ledger separately; never store user API keys or private connector tokens.

In a conversation return a short `STATE` (up to ~150 words), never repeat 150 technical rules. If `дальше`, load STATE and apply `next_action` only if prerequisites were verified. Do not invent that an unmounted file still exists.

Suggested status chain: `SPECIFIED → GENERATED → INSPECTED → APPROVED`, with `FIX_REQUIRED/BLOCKED` branches. Spec creation does not count as rendering; a local validator tests consistency of logs, **not the truth of video quality claims**.
