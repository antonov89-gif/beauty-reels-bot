# Brand acquisition / evidence

## Sources, coverage, confidence
List `SOURCE_ID`, `owner` (`OWN|COMPETITOR`), kind (`channel|banner|avatar|thumbnail|video|audio|brief|analytics`), uri/path, fetched/verifiable state, modality, inspected range or screenshot region, confidence. Never mix competitor imagery into an OWN source field. Uninspected items have `access: UNVERIFIED`.

For own channel page: capture channel name (if confirmed), About description, banner/avatar, upload categories, recurrent thumbnail grammar, published series, approximate posting format. For visuals: inspect actual asset pixels rather than inferring from channel handle. For owned video: sample at meaningful shot boundaries, listen to voice/audio if accessible; select 2–4 diverse channel videos, when accessible (not only one outlier hit). Mark whether a palette or camera behavior is consistent across episodes. One screenshot doesn't establish recurrence.

Extraction grid:
- **Identity:** exact logo asset, positive/negative space, logo clearance, placement, watermark, intro/outro usage, text case.
- **Palette:** sampled dominant/accent/background colors with approximate HEX and confidence; do not present guessed HEX as exact measurements.
- **Typography:** category, weights, size hierarchy, spacing, high-readability substitutes; exact font only if known from owned design files or unmistakably verified.
- **Cover packaging:** grid, subjects, expression, contrast, text ratio, headline promise; aspect ratio, mobile readability.
- **Cinematic signature:** animation mode, lens/shot distribution, grade, motivated lighting, camera trajectories, depth, effects, pace, focus / blur. Require video evidence.
- **Audio signature:** natural VO performance, voice character, language/accent, ambience, music/SFX strategy. Require audio.
- **Narrative signature:** genres, emotion envelope, hooks, viewer promise; require videos/scripts, not logo.

When only banner exists, create `visual_brand_confidence=PARTIAL`, `filmmaking_confidence=UNKNOWN`; propose distinct candidate cinematic treatments clearly marked as creative options. Do not silently lock a guessed style.

Source changes: detect a changed banner/channel look, show conflict with current approved version, and ask only when it changes persistent brand rules. Never overwrite `APPROVED` brand without explicit new approval.
