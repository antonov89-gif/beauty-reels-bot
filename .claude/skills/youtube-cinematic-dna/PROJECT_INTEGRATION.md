# Mr. Buck integration (read with SKILL.md)

Installed 26.10.2026 from the owner's upload youtube-cinematic-dna-v5.1.zip. Project rules win on any conflict: CLAUDE.md > this note > SKILL.md.

## How it plugs into our pipeline
| V5.1 piece | Our existing piece | How we use it |
|--|--|--|
| Evidence levels L0–L4, coverage ledger | CLAUDE.md reference rule, `map_shorts/prompts/frame_forensics.py` | L3 only after frame_forensics ran on the real mp4. vidIQ/Nexlev/Gemini text = L1, a hypothesis ("НЕ ПРОВЕРЕНО НА КАДРАХ"). |
| Claim IDs (OBSERVED / ESTIMATED) | DNA analyzer tags VERIFIED / STRONG INFERENCE / HYPOTHESIS / UNKNOWN | OBSERVED = VERIFIED; ESTIMATED = STRONG INFERENCE or HYPOTHESIS. |
| STYLE_BIBLE + SCENE LOCK + SHOT DELTA | `prompts/style_zackd_3d_render.md`, `<project>/plan.md`, shot prompt files | One SB version per project in plan.md; each shot prompt = SB + scene lock + delta. |
| Acceptance gate written before generation | PHASE 94 reference/ours table | Each shot gets its gate in plan.md before any paid call. |
| Pilot 2–3 shots, then batch | test frame + test clip (Tristan flow) | Mandatory: pilot before any batch of paid frames/clips. |
| Max 2 corrective attempts per shot | — (new) | After 2 failed fixes: change method (crop, cut, other shot) or ask the owner. |
| SPECIFIED→GENERATED→INSPECTED→APPROVED + honesty markers | self-check rule, `reference_check.md` | Statuses go into reference_check.md; NOT_OBSERVED is never PASS. |
| Technical QC HARD FAIL / SOFT ISSUE | AI-clip checklist (PHASE 95) | Contact sheet of every clip; HARD FAIL = regenerate or cut, SOFT = edit/grade. |
| Shot-level + sequence-level QC | final self-check of the montage | Check neighbouring cuts for axis/action/sound continuity. |
| STATE capsule (≤350 words) | growth_log / project notes | Write `<project>/STATE.md` at handoffs and after compaction. |
| `scripts/validate_project.py` | — | Optional: lint `<project>/ledger.json` (run with `python3 -I`). Structure only, not quality. |

## Overrides (our rules, not the skill's)
- Paid generation: ask the owner first and name the provider price (CLAUDE.md).
- AI visuals and AI voice are labelled (description + platform flags; no on-screen tag unless asked).
- The authenticity-check audit is still mandatory before delivery; V5.1 QC does not replace it.
- Replies to the owner are in Russian and brief; video text in English.
- Format is 9:16 Shorts unless the project says otherwise (SB example is 16:9).
- Copy principles, never frames, characters, music or graphics (PHASE 89, not-a-copy check).
- FULL output only on explicit request; default is SMART/compact.
