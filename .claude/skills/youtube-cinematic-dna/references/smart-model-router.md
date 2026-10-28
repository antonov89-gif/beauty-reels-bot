# SMART MODEL & METHOD ROUTER (QUALITY FIRST, COST-AWARE)

## Avoid vendor-by-default bias
For each SHOT classify A (easy), B (moderate), C (hard); list failure modes: hands/faces, multiple actors, vehicle physics, complex occlusion, crowd, camera travel, 2+ interacting objects, long dialogue, lip-sync, precise text, continuity. Also assess whether a shot can be achieved by **editing/stock/CGI/2.5D** instead of generated video.

## Routing decision order
1. Can a cut/retime/color/SFX or available stock satisfy the requirement without a render?
2. Does controlled 3D or layered graphics produce better geometry/continuity?
3. Is image-to-video with locked start/end frames sufficient?
4. Only then compare text-to-video/video-to-video models using **current verified API availability, documented duration/resolution/audio features, failure cases and price**. Never treat a brand/version as universally superior.
5. Run small representative tests when affordable/approved; empirically revise model choice based on accepted-shot rate and QC.

## Cost objective
`expected_accepted_shot_cost = price_per_attempt × expected_attempts + optional_editing/upscale/audio + human_or_compute_overhead_if_counted`.
For probabilities only if measured in the same project: `expected_attempts ≈ 1 / observed_success_rate`, capped by configured budget/attempt policy; theoretical forecasts must be labeled assumptions. Report range if unknown, not a false exact quote. Currency FX needs rate/date and conversion source.

## Provider comparison compact record
`METHOD | MODEL/VERSION | VERIFIED_SOURCE + AS-OF DATE | RESOLUTION | MAX CLIP LENGTH | AUDIO | ESTIMATED FAILURES | PER ATTEMPT | EXPECTED ACCEPTED COST | RECOMMENDATION | CONFIDENCE`.

## Guardrail
Only explicit consent may authorize chargeable rendering; approvals define max budget, model, tier, resolution, number/duration of generations and expiration/scope. Recommend expensive Seedance 2.5 only for validated need and **ask before using** in complex scenes unless this exact work batch was approved. Do not invoke unsupported external services or insert secret API keys into project logs.
