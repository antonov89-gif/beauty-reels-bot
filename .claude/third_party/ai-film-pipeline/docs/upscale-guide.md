# Upscale guide — Topaz Video (optional)

A concise recipe for the final upscale pass, taken from the source creator's June 21 walkthrough. Read this when your generations came out of Seedance at 720p and need to hit delivery resolution before assembly.

## (a) When you need it

Seedance video generations from a 720p host (ArtCraft Basic, Higgsfield at the 720p setting) need an upscale pass before they're delivery-ready for most outputs.

**If you generated at 4K, skip this entirely.** Seedance 2.0 / Higgsfield now offers 4K-native generation. If your clips already came out at 4K, there's nothing to upscale — go straight to the assembly step in `WORKFLOW.md` Phase 7. This guide is for the 720p path only.

## (b) The recipe

### 16:9 (standard widescreen)

In Topaz Video's **Enhancement** tab:

- **Skip the default model (Starlight Precise).** It's slow and not the right pick for this pipeline's footage.
- **Model: Iris.** Best for faces — the right choice whenever a character is on screen. **Proteus** is an acceptable alternative if Iris isn't available or behaves oddly on a specific clip.
- **Output resolution: 3840×2160** (4K).
- **Add Noise: 2–3.** This is digital noise, not film grain — a small amount here helps the upscaler avoid an overly plastic result. Don't confuse this with the grain pass below.
- **Recover Detail: ON.** But don't over-sharpen. AI-generated cinematic images shouldn't come out razor-sharp — that reads as fake. Keep Recover Detail moderate.
- **Focus Fix: OFF.** Nothing in AI-generated video is actually out of focus in the optical sense, so Focus Fix has nothing correct to do and can introduce artifacts trying.
- **Input Condition: Low Quality.** This tells Topaz to expect a compressed/generated source, not a clean camera-original.
- **Tuning: Advanced Automatic Tuning.**
- **Codec: H.264.** ProRes is unnecessary unless you're doing heavy color grading downstream and need the extra bit depth headroom.
- **Bitrate: Dynamic.**

### 21:9 (anamorphic / cinematic letterbox)

- **Custom resolution: 5040×2160.**
- Same Enhancement settings as 16:9 above (Iris/Proteus, Add Noise 2–3, Recover Detail on without over-sharpening, Focus Fix off, Input Condition Low Quality, Advanced Automatic Tuning, H.264).
- **Bitrate: Constant, at 24.** (Not Dynamic — 21:9 delivery holds a constant bitrate at 24 for this recipe.)

### Grain

- **If you already add grain overlays in your NLE** (DaVinci Resolve, Premiere, etc.), **skip Topaz's grain entirely** — don't double up.
- **If you don't have an NLE grain workflow,** apply Topaz's grain in this pass:
  - **Type:** gray
  - **Amount:** ~70–80
  - **Size:** ~1.5–1.8
  - **Density:** default (this renders slower — budget the time)

### Finish

Drop the upscaled output into a 4K timeline. Add grain (if not already applied in Topaz) and a light color correction pass. Most clips are already graded by the cinema-mode stack in `cinema-worldbuilder`'s prompts — this is a balancing pass, not a full regrade.

## (c) Characters into real footage

A separate technique for compositing an AI character sheet into an actual filmed background plate (not a Topaz operation — this is a Claude + image-model compositing workflow, documented here because it sits in the same post-production neighborhood).

1. **Eligibility-check the still frame FIRST.** Some background objects in a real still break compositing in ways that aren't obvious until you try. Test the still with a simple composite attempt *before* investing in the full character-into-scene build — a failed eligibility check costs you five minutes; a failed full build costs a lot more.
2. **Inputs:** the background still + the character sheet, both fed into Claude (or your image-compositing tool of choice) together.
3. **Instruct "keep the frame locked."** Explicitly tell the model not to alter the background composition.
4. **Describe the action explicitly camera-relative.** "Walks in from camera right," not "walks in from the left" (which is ambiguous — left from whose point of view?). Always frame direction from the camera's perspective, matching the same convention `cinema-worldbuilder` uses for Movement blocks.
5. **Small props must be explicitly instructed too.** Don't assume a prop carries over from the character sheet into the composite — if a held object needs to appear, describe it directly in the compositing instruction.

**For Higgsfield's Omni real-footage editing** (editing an existing real video clip rather than compositing a still): use a maximum of **10 seconds** of real footage per Omni edit, and prompt it plainly — *"keep me exactly the same, change X."* Omni responds better to a short, direct instruction than an elaborate cinematography prompt; it's an edit tool, not a generation director.

## See also

- `WORKFLOW.md` Phase 7 — Post, where this pass sits in the overall pipeline
- `docs/artcraft-ui-guide.md` / `docs/higgsfield-ui-guide.md` — resolution settings at generation time (720p default vs 4K-native)
- `CLAUDE.md` — production stack table, Topaz Video's role
