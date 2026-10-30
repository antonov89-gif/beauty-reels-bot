# CINEMATIC SHOT COMPILER

## Purpose
Turn compact `STYLE_BIBLE + SCENE_LOCK + SHOT_DELTA` into *model-adapted* visual/image/video prompts. Keep the reusable bibles in project files; inline them only as needed by an actual generator. A model with no memory needs explicit grounding for every submitted shot even if the agent stores a shared bible.

## Compiler input
`SHOT_ID; BEAT_ID; start_frame; end_frame; camera_rig/height/side/lens_feel; movement_path; motion_timing; subject_action; environment_and_foreground_motion; motivated_lighting; focus_and_blur; geometry/character/prop locks; audio cues; expected_duration; acceptance_checks`.

## Image-only output
Describe single frozen instant: subject and action state, camera location/optics/perspective, layer composition, light source/direction/materials, continuity references, color treatment; discourage synthetic artefacts specifically relevant to scene. Do not write temporal camera commands in a still-image-only prompt.

## Video output
1. **Initial condition**: who/where, rig position and spatial layout.
2. **Blocking/physics**: 1 primary physical action, realistic acceleration, contacts, inertia and follow-through.
3. **Camera path**: start → justified motion/velocity → endpoint, lens/rig consistency, screen direction.
4. **Independent motions**: subject, foreground parallax, environmental response without noise overload.
5. **Focus/exposure/light**: motivated source, shadows and target at cut.
6. **Continuity locks**: reference frame(s), identity/wardrobe/geometry/state and environment.
7. **Restrictions**: only relevant constraints; distinguish controllable negative prompts from instructions not supported by target tool.
8. **Audio**: include only if target model handles sound; otherwise separate sound cues for editing timeline.

## Multi-model adaptation
Check official/current accepted arguments for selected provider before API calls; e.g. cannot assume one provider supports `negative_prompt`, `end_frame`, camera controls, or audio flags used by another. Provide (a) generator-readable prompt and (b) internal editor notes. Never send a verbose entire skill to model API.

## Compiler validation
All shots should have clear physical camera intent and start/end states (or intentionally locked-off), a camera/subj motion relationship, and a perceptible narrative function. Avoid the generic adjective-only prompt `epic cinematic dynamic video`.
