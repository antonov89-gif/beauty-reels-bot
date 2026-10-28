# VISUAL QUALITY JUDGE — ARTIFACT-BASED ITERATIVE QC

## Evidence prerequisite
Quality judgment requires inspecting the **actual output video and audio**. A generator completion message, thumbnails, filenames or previous prompt cannot prove a sequence is good. Give inspected timestamps and observed defects. Compare *general cinematic principles* rather than exact copyrighted shot/framing copies.

## Per-shot rubric (0–5 per dimension, judgment not benchmark)
- Story/readability and framing
- Camera physicality and justified motion
- Subject/object weight, contacts and motion/physics
- Light/source/material response, depth and DOF
- Temporal identity/geometry/texture stability
- Continuity with neighboring shots
- Natural acting, voice/lip-sync where applicable
- Sound perspective, foley and ambience where applicable
Only score what was **inspected**; mark others NOT_ASSESSED. Severity outranks average score: broken character identity or unusable dialogue = hard failure regardless of high mean.

## Defect taxonomy
`CAMERA_FLOAT / JITTER / ZOOM_JERK / SLIDESHOW / INVALID_PHYSICS / GEOMETRY_DRIFT / IDENTITY_DRIFT / LIGHT_JUMP / CONTINUITY_BROKEN / AUDIO_FAKE / BAD_LIPSYNC / WEAK_STORY / OVERCUT / STATIC_OVERLONG / TYPOGRAPHY / MIX_PROBLEM`.

## Remediation policy
1. Identify `shot_id`, time and exact visible/audible defect.
2. Decide `trim/edit → retime → sound/color/rotoscope → local regeneration → full shot replacement → alternate 3D/stock/other method` with least overall cost.
3. Change only parameters responsible for defect. Preserve shared locks.
4. Re-render only after permission if credits are involved.
5. Inspect revised file *again*, log new artifact and regression checks.
6. When 2 attempts fail, reassess base method; cannot approve because an attempt cap was hit.

## Pilot benchmark
Reference values may be `VISUAL_DNA_FIT` and `FILMMAKING_QUALITY`, but label scores as subjective structured reviews. Never market made-up 97% similarity or promise undetectable AI. Deliberate fiction can be photoreal; never pass it off as actual news footage. Defects shown in output always outrank a reassuring prompt.
