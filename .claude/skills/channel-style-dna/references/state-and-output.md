# Persisted state and token-efficient records

Save in project `.channel-style-dna/project.json` or user-approved workspace directory. Sample JSON in `examples/sample-project.json`. The local scripts validate status and compile limited prompts; they do not query YouTube or render/inspect video.

Top-level fields:
- `skill_version`: `1.0.0`.
- `project_id`: stable string.
- `phase`: `SOURCE_GATE|BRAND_SCAN|BRAND_LOCK|COMPETITOR_SCAN|TRANSFER|STORY|PILOT_SPEC|PILOT_GENERATED|PILOT_INSPECTED|PILOT_QC|BATCH|DELIVER`.
- `sources`: separately annotated OWN vs COMPETITOR.
- `brand`: `status` (`DRAFT|PROPOSED|APPROVED`), `version`, `approval_evidence` when approved, `core`, `cinema`, `can_vary`, `forbidden`, each media-derived claim with source tags/uncertainty in evidence ledger.
- `competitor`: `reference_ids`, `transfer_matrix`; reuse-only evidence IDs, don't copy scripts.
- `stories`: each distinct, recommended ID (or null).
- `scenes`: global conditions per location; `shots`: per-shot delta references, no full prompt duplicates.
- `pilot`: `status` (`NOT_STARTED|SPECIFIED|GENERATED|INSPECTED|QC_PASSED|QC_FAILED`), `actual_media_path` when output exists, `inspected_evidence` for `INSPECTED/QC_*`.
- `cost_approval`: `approved` false by default; `scope`, `budget_cap`, `approval_evidence` if true. Never infer from general enthusiasm.
- `state`: `next_action`, `verified_completed`, `pending`, `updated`.

## Tokens
`GLOBAL_BRAND_BIBLE` once → `SCENE_LOCK` once → `SHOT_DELTA` for every shot. Store reference evidence and approved decisions; only material differences are communicated. When generating a single shot, compile *only* relevant global rules + scene lock + shot delta + transferred mechanic.

## Output in chat, compact
1. What is actually inspected/unknown (2–3 lines)
2. 'Our brand, non-negotiable' vs 'Competitor mechanics worth borrowing' (short distinction)
3. 3 truly different story pitches + strongest recommendation
4. 20–40 sec pilot in a compact shot-by-shot table
5. Which media / generator / approval is needed next
6. Saved `STATE` summary; don't dump entire JSON unless asked.
