# Iterative Production Loop — evidence after every generated artifact

## Preflight: define what "good" means before spending generation credits
For every pilot/hero shot, specify:
- `SHOT_ID`, parent `STYLE_BIBLE_ID`, `SCENE_LOCK_ID` and original story beat.
- Narrative readability + motivated blocking / start, action, end.
- Camera rig impression, start→path→end, subject/framing, perspective/lens family and focus.
- Lighting source/direction, depth, motion blur, materials, interaction physics and continuity anchors.
- Acoustic space, Foley and speech/emotion when present; cut in/out condition.
- *Acceptance tests*: hard failures absent, story/action understandable at normal speed, identities/props and geography stable, audio intelligible and physically appropriate.
- Any intended stylistic exception (stylized physics, animation, snap zoom, etc.) must be named in advance so QC doesn't mistakenly reject purposeful art direction.

## Iteration state machine
`SPECIFIED → READY → GENERATED → INSPECTED → (APPROVED | FIX_REQUIRED | BLOCKED)`.
- `SPECIFIED`: requirements approved/defined, no artifact.
- `READY`: assets/tools available, ready to execute.
- `GENERATED`: generation actually returned a playable/visible artifact. **Not** a QC pass.
- `INSPECTED`: actual artifact examined, record inspected segment and modality.
- `APPROVED`: hard gates pass, any accepted soft exceptions documented.
- `FIX_REQUIRED`: failure + targeted fix.
- `BLOCKED`: missing tool/media, repeated failures, credit guard or unresolved choice. Do not claim complete.

If user requested analysis or prompts but not rendering, stop at `SPECIFIED`; if generation tools are unavailable, stop at `BLOCKED` (or provide specification). Never simulate a real iteration.

## Standard cycle (one shot)
1. Select highest value/uncertainty shot; retrieve **only** STYLE_BIBLE + SCENE_LOCK + shot delta. Choose appropriate method: real shoot, stock, 3D, compositing, still animation, text-to-video, image-to-video, video-to-video.
2. Produce the smallest viable **preview**, not blindly the full long video. Record output artifact locator/path, model/vendor if verifiable, settings if actually submitted, generation duration/cost only if returned.
3. Examine the actual output at **normal speed** (meaning, motion, edit, feel), on keyframes or slowed (hands, reflections, geometry, contact/physics) and **audio-only** if audio exists. A still preview does not demonstrate video motion or speech.
4. Log errors: exact `SHOT_ID + timecode`, visible/audible failure, viewer impact (CRITICAL/HIGH/MEDIUM/LOW), evidence ID, likely cause, remedy. For uncertainty state the test that would verify it.
5. Decision: `APPROVE` (no hard failures) / `FIX` (targeted correction) / `REGENERATE` / `BLOCK` (missing capability or unresolved repeated failure).
6. Choose least expensive viable fix *without sacrificing the intended beat*: `trim/cut` → `retime/stabilize/mix/grade` → `local mask/revoice/composite` → `partial regeneration` → `full shot regeneration` → `switch production method`. Order is a heuristic, not a mandate when a cheaper method clearly won't fix the defect.
7. **Execute if tools are present**. A proposed fix is not a completed fix. Log attempt number and changed parameters only; don't restate global style.
8. Inspect revised artifact, check the original defect and a small regression set (identity, camera, continuity, color, audio). If still failing, iterate; default two corrective rounds, then reassess generator/method or label blocked.
9. On approval, lock a reusable preset and update `STATE`. Do not approve only because retries or budget are exhausted.

## Quality gates: pass by observation, not decorative numbers
### Hard stop (cannot accept)
- Face/identity/wardrobe/object/vehicle spontaneously changes when central to action.
- Obvious melting, geometry warping, finger/limb duplication, incoherent body contact, sliding feet or impossible motion of a central subject.
- Camera teleportation/unstable perspective unless deliberately surreal; unreadable key action; lighting/source violation that destroys scene continuity.
- Gross dialogue voice mismatch, bad pronunciation that changes meaning, unusable lip sync, missing vital sounds, unintelligible speech.
- Wrong story beat or unrelated output.

### Soft fix (prioritize)
- Repeated shot size/trajectory without storytelling role, slightly artificial easing, overdone DOF/neon/HDR, inconsistent subtle grain, unhelpful VFX, slight pacing flattening, thin ambience.

### Technical film checks
- **Camera**: action geography, axis, eyeline, motivations, camera mass/inertia, lens-perspective-distance consistency.
- **Animation**: anticipation/weight/contact/follow-through, natural secondary motion, vehicle/surface physics, environment response.
- **Image**: motivated key/fill/practicals, shadow/specular/reflection consistency, foreground depth, focus and motion blur.
- **Performance**: face/eyes/breath/voice subtext, pauses, pronunciation, lip sync, realistic sound perspective/ambience.
- **Editing**: information/reaction/motion cut motivation, J/L-cut where apt, variety without needless effects.

## Sequence-level iteration (after shot-level approval)
Assemble an adjacent scene block or test cut. Inspect it continuously with sound. A shot that passes alone can still fail continuity when joined to the previous/next shot: axis, screen direction, action phase, subject location, weather, light, costume/vehicle damage, spatial and sonic transitions, pace, cause→effect, emotional escalation and payoff. Reopen only affected shots and immediate neighbors. If fixes change locks, bump their versions and invalidate dependent shots only.

## Example fault report (illustrative, not an actual inspected video)
```
SHOT S02-04 / attempt 1 / video 00:02.0–00:03.1
FAIL HIGH: car front wheels rotate in inconsistent directions during turn.
EVIDENCE: OUT-E07 (video observed in player, specified time range)
FIX: maintain car identity; regenerate steering/turn phase 1.1s using a locked
front-wheel-angle end frame; preserve camera trajectory and lighting.
NEXT: inspect tire rotation, body roll, ground contact and neighboring shot.
STATE: FIX_REQUIRED (not yet fixed)
```

## Cost/stop rules
- Track `analysis effort`, `model/input tokens`, `generation charges/credits`, `human/manual fixes` separately when data exists.
- Don't estimate provider-specific dollars without current trustworthy prices and settings.
- If expected marginal cost of a fix exceeds its viewer value, propose a simpler editorial workaround or change method. **Hard failures still cannot pass.**
- `STOP = approved film sequence` OR `blocked with precise limitations, lowest-cost next step`. Never declare background/asynchronous delivery.

## Final QC evidence
Final status should include actual references to inspected artifacts, regions checked, count of unresolved hard issues (zero for approved), important soft exceptions, and whether full film or only a sample was inspected. If final output wasn't rendered in the current tool environment, say explicitly that the result is a plan/prompt, not a completed video.
