# Project integration (read with SKILL.md)

V5.4.1 (audited) installed 28.10.2026 from the owner's upload youtube-cinematic-dna-v5.4.1-audited_1.zip, replacing V5.1 (26.10). Owner: "установи и используй когда скидываю ссылку". Project rules win on any conflict: CLAUDE.md > this note > SKILL.md.

## Trigger (owner's rule)
Every YouTube link the owner sends (youtube.com, youtu.be, /shorts/) runs this skill. A bare link = ONE_LINK_STUDIO (no question "what to do with it"); a link plus words follows the auto-router (ANALYZE, CREATE, COMPARE, MULTI_REF and so on). The `video-dna-analyzer` skill stays the data and numbers layer (vidIQ stats, comments, transcript, events per 10 s, wpm, the 18 blocks when an analysis is asked for).

## Order of work for a link
1. Channel routing first (CLAUDE.md): geography -> Mr. Buck in its own look; anything else -> another channel, never Mr. Buck, styles never mixed. Do not ask which channel; say where it goes.
2. SOURCE_GATE: vidIQ get_videos_by_ids + comments + vidiq_watch_shortform_content (L1), Nexlev transcript. YouTube blocks yt-dlp here, so the visual part is "НЕ ПРОВЕРЕНО НА КАДРАХ" until the owner sends the mp4; then `map_shorts/prompts/frame_forensics.py <mp4> <out> --dense 10` or the skill's `scripts/inspect_media.py` (run with python3 -I) and timestamped claims.
3. One concise reply in Russian: access and limits, 5-7 DNA rules (provisional labels where not seen), 3 original stories, the recommended one, the look, beats, a 20-40 s pilot shot table, the next action and a short STATE. Stop at PILOT_SPEC.
4. Paid steps only after the owner's explicit "да/делай" with the provider price named (CLAUDE.md). Pilot before batch, max 2 corrective attempts per shot, statuses SPECIFIED -> GENERATED -> INSPECTED -> APPROVED.

## Mapping to our pipeline
| Skill piece | Our piece |
|--|--|
| Evidence IDs, OBSERVED / ESTIMATED / UNKNOWN | VERIFIED / STRONG INFERENCE / HYPOTHESIS / UNKNOWN in the DNA reports |
| GLOBAL_STYLE_BIBLE, SCENE_LOCK, SHOT_DELTA | `<project>/plan.md`, shot scripts (LOCK + SHOTS) |
| smart-model-router | APIpod catalogue: Nano Banana 2.1 frames, Veo 3.1 fast/quality, Seedance 2.0/2.5, Kling 4.0; prices read from the API cost field after each call |
| pilot-studio, quality-judge | contact sheets per clip, crops of hands/objects, `map_shorts/prompts/premium_gate.py` |
| sound-director | native clip audio checked with VAD/Whisper; own synth foley/room tone; -14..-15 LUFS |
| STATE (state_cli.py) | `<project>/STATE.json` or plan.md notes; run `python3 -I scripts/state_cli.py` |
| Lessons from the bracelet Short (28.10) | count hands per frame and check that every hand has an arm; no floating object parts; no stripes or bands on skin; the tool must touch what it cuts; boosted native audio can trip VAD: check before mixing |

## Overrides (our rules, not the skill's)
- Paid generation: ask first and name the cost (CLAUDE.md); a bare link never authorizes spending or publishing.
- AI visuals and voice are disclosed (description + platform flags; no on-screen tag unless asked); fiction is never presented as real.
- The authenticity-check audit stays mandatory before any delivery; the skill's QC does not replace it.
- Replies to the owner in Russian and brief; video text in English. Format 9:16 Shorts unless the project says otherwise.
- Copy principles, never frames, characters, music or graphics (not-a-copy check).
- Only Mr. Buck is connected to Zernio; another channel's video is delivered as a file.

## Channel Style DNA V1.0 (installed 28.10.2026, `.claude/skills/channel-style-dna`)
Owner's upload channel-style-dna-v1.0.zip, applied to @tudor.with.elizabeth. Use when the owner gives a competitor link for a channel that has (or needs) its own brand: BRAND_LOCK first, competitor mechanics second (TRANSFER matrix KEEP / TRANSLATE / REJECT / UNKNOWN), then three original stories and a 4-8 shot pilot. Per-channel state lives in `map_shorts/<channel>/project.json` (history channel: `map_shorts/history_channel/project.json`); validate with `python3 .claude/skills/channel-style-dna/scripts/validate_channel_project.py <json>`. Brand status stays DRAFT until the owner approves it; brand approval is not spend approval (cost_approval.approved stays false until "да/делай" with the price). Mr. Buck's geography look is never used for another channel, and no other channel's look is used for Mr. Buck.
