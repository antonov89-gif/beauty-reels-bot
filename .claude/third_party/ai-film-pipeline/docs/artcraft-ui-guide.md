# ArtCraft UI Guide — How to Run a Seedance Shot

A producer's-eye walkthrough of the ArtCraft interface ([getartcraft.com](https://getartcraft.com/)) for running Seedance 2.0 shots from this pipeline. Use this when you've just signed up and you're staring at the Generate page wondering where everything is.

> **What ArtCraft is now:** ArtCraft has repositioned as an open-source desktop app — "the IDE for interactive AI image and video creation" ([github.com/storytold/artcraft](https://github.com/storytold/artcraft)). Pricing is Basic $10/mo (or $96/yr) **or** pay-as-you-go credit packs from $10 for 1,000 credits with no subscription required. It hosts many models beyond Seedance 2.0 — Veo 3.1, Kling 2.6, Sora, Flux, Seedream 4/4.5 — in the same app. The walkthrough below documents the generate-panel UI as last captured here; if the live app has moved things around, trust what's actually on screen over this guide.

> **TL;DR for first-time users:** ArtCraft's generate panel is a single view. The big text field in the middle is where the prompt goes. The bar of pill-shaped buttons across the bottom is where every per-shot setting lives — model, aspect ratio, resolution, runtime, input mode, character anchoring. Everything on this page is everything you need.

## The toolbar at a glance

This is what the ArtCraft generate panel looks like:

![ArtCraft generate toolbar — Start Frame and End Frame slots at the top, the "Describe the video..." prompt field in the middle, and the controls bar across the bottom: Seedance 2.0 · 16:9 (Wide) · 720p · 5s · Keyframe · @Characters · Generate](images/artcraft-toolbar.png)

Top to bottom:

1. **Start Frame** *(left, "Animate an image")* — drop an image here when you want the video to start from that exact frame and animate forward. Most shots in this pipeline don't use this — we use **Reference mode** (covered below) for character / environment / prop anchoring instead. Leave Start Frame empty unless the orchestrator specifically tells you to animate from a still.
2. **End Frame** *(right, "How video ends," optional)* — drop an image here when you want the video to end on that exact frame. Useful for locking a final beat (a hero pose, a logo reveal, a specific look). Optional and rarely needed.
3. **Prompt field** *("Describe the video you want to generate…")* — this is where the Seedance prompt from `cinema-worldbuilder` goes. `cinema-worldbuilder` delivers prompts as a title line plus a single code block of ten labeled blocks (Scene & Mood, Frame Map, Subject Lock, Cross-Frame Rules, Movement, Last Frame, World Plate, Sound Bed, Capture Realism, Camera Capture). Paste the entire code block exactly as written, including the `@tag` references and any distributed color/grade language. Don't edit it down — `cinema-worldbuilder` writes prompts that fit Seedance's input budget.
4. **Bottom toolbar** *(left to right)* — the seven controls below. Each is a pill you click to open.

## The bottom toolbar — every per-shot setting

### Seedance 2.0 (model selector)

> 📊 **Seedance 2.0** ← click this if it shows a different model.

This is the video model. **Always confirm it's set to Seedance 2.0** before generating — every prompt in this pipeline is written for Seedance 2.0's specific grammar (the ten labeled blocks, `@tag` references, FOV-degree lens anchor, the photoreal stack, the cinema-mode camera language). If ArtCraft has defaulted to a different model, click and switch.

### 16:9 (Wide) — aspect ratio

> 🖥 **16:9 (Wide)** ← click to change

Click and pick the aspect ratio for this shot. The orchestrator will tell you which to use per shot. Common choices:

- **16:9 (Wide)** — YouTube, TV, traditional cinema
- **9:16 (Tall)** — Instagram Reels, TikTok, YouTube Shorts, vertical mobile
- **1:1 (Square)** — Instagram feed posts
- **2.39:1 / 21:9** — anamorphic / cinematic letterbox (some hosts; check availability)
- **4:5** — Instagram portrait feed

**Set this per shot.** Don't assume the last shot's aspect ratio carries over — confirm before every generation.

### 720p — resolution

> 🖥 **720p** ← click to change

Resolution. **720p is the right default for this pipeline** — Topaz Video in post-production upscales 720p cleanly to 1080p or 4K, and generating at 720p costs significantly fewer credits than 1080p. Only generate at 1080p if you have a specific reason and credits to spare.

### 5s — runtime

> ⏱ **5s** ← click to change

Per-shot runtime. The orchestrator hands you the runtime for each shot from the shot list. Common values: 3s, 5s, 8s, 10s, 12s, 15s. **Every second costs credits**, so don't over-budget — if `cinema-worldbuilder` quotes 7 seconds, use 7 seconds, not 10.

### Keyframe — input mode (THIS IS HOW YOU ADD REFERENCES)

> 🕓 **Keyframe** ← click to change to **Reference**

This is the one that's hardest to find on your first shot. **By default, ArtCraft is in "Keyframe" input mode**, which means it expects Start Frame / End Frame images for first-frame and last-frame animation. To attach reference images (locked character sheets, environment plates, prop sheets — the heart of how this pipeline works), you have to switch to **Reference mode**.

**How:** click the "Keyframe" pill in the bottom toolbar. A small dropdown appears with two options:

![Input Mode dropdown — Keyframe (currently checked) and Reference; click Reference to switch to reference-image attachment mode for this shot](images/artcraft-input-mode-menu.png)

- **Keyframe** *(default, currently checked)*
- **Reference** ← **click this**

Once you switch to Reference mode, the top of the panel changes from "Start Frame / End Frame" slots into a reference upload area. **Drag your locked references into the reference slots** (character sheet, environment plate, prop sheet — whichever the shot calls for, up to 9 individual images per generation). Match each upload to the `@tag` name `cinema-worldbuilder` used for that reference in the prompt (`@sol_ref`, `@loft_plate`, etc.) — ArtCraft doesn't read the tag names itself, but keeping your own slot order consistent with the tags in the prompt is what prevents attaching the wrong image to the wrong anchor. The orchestrator will tell you exactly which references to attach per shot.

This is the mode you'll use for almost every shot in the pipeline. Set it once at the start of your generate session; ArtCraft will usually remember it for subsequent shots, but **double-check** the toolbar pill says "Reference" before generating each shot — sometimes it reverts.

### Audio Ref (lip-sync / music slices)

> 🎵 **Audio Ref** ← lives in the same reference panel that opens when you switch to Reference mode

Music-video shots where a character is on-camera mouthing the lyric need this slot. It sits in the reference panel alongside the image reference slots — **3 slots × 15s total budget**. Attach the Suno lyric slice for this shot (the `audio/track_v01_slice_<NN>.mp3` file from the track you sliced in `WORKFLOW.md` Phase 6 / `ai-film-director` Step 6.1) into one of the three slots. This is what gives Seedance the audio to sync the character's mouth motion against.

Pair the attached slice with the matching lip-sync line `cinema-worldbuilder` writes into the prompt's **Movement** block — *"lips visibly mouthing the words '[exact lyric]' with exaggerated clarity."* The slice and the prompt line have to agree on the same lyric, or the sync has nothing to lock onto.

*(This slot layout reflects the ArtCraft UI as last documented here — if it looks different when you get to the Generate page, go with what's actually on screen.)*

### @Characters — identity anchoring (optional)

> 👥 **@Characters** ← click to bind a specific character identity

If you've saved characters in ArtCraft's character library (built from your locked sheets), `@Characters` lets you bind one of them by name into the shot. This forces tighter identity lock than reference images alone. **Not required** — reference images attached via Reference mode work fine on their own — but useful if you find character drift creeping in across many shots of the same person.

### Copy count (📋 1) — batch generations

> 📋 **1** ← click to bump higher for parallel generations

The little "1" with the copy icon is **how many generations to run from this single prompt**. ArtCraft will run them in parallel and let you pick the winner. **Default to 1** for cost reasons. Bump to 2 or 3 only if you know this is a hard shot that's going to need multiple attempts anyway — burning the credits upfront and picking the best of three is cheaper than re-rolling three times sequentially.

### Generate (with credit cost preview)

> 🪙 **Generate · 80** ← click when everything is set

The blue **Generate** button on the right kicks off the actual generation. The number next to it (e.g. `80`) is the **credit cost** for this specific configuration — it updates live as you change aspect ratio, runtime, resolution, and copy count. **Always glance at this number before clicking Generate** — it's your cost preview. If it's way higher than you expected (e.g. 240 when you expected 80), something's misconfigured (probably runtime too long, resolution too high, or copy count above 1).

Click Generate. Wait. The clip appears in the gallery to the right of the generate panel when it's done.

## Per-shot generation checklist

Run this mentally (or actually) every single shot:

- [ ] **Prompt pasted** into the central text field, exactly as the orchestrator wrote it
- [ ] **Seedance 2.0** confirmed in the model pill
- [ ] **Aspect ratio** set for this shot (orchestrator tells you)
- [ ] **Resolution** at 720p (unless explicitly going 1080p)
- [ ] **Runtime** set to what the shot list says
- [ ] **Input mode** showing **Reference** (not Keyframe), references uploaded into the reference slots
- [ ] **Copy count** at 1 (unless you've already accepted you need parallel attempts)
- [ ] **Credit cost** in the Generate button matches what you expected (~$0.50–$1.00 per typical 5–10s shot at 720p)
- [ ] Click **Generate**

Then take the result back to your conversation with the orchestrator and say "Shot N kept" (save it), "Shot N iterate" (re-roll with a tweak), or "Shot N wasted" (log and move on).

## What you don't need (skip these)

- **Extra installs beyond the app itself** — ArtCraft now ships as the open-source desktop app ([github.com/storytold/artcraft](https://github.com/storytold/artcraft)); this walkthrough was captured on the generate-panel UI, which is what you'll see whether you're running the desktop build or an in-browser preview of it. Either way, the panel layout below is what matters — don't go hunting for a separate "real" interface.
- **Other models** in the model picker — the pipeline is Seedance 2.0-specific. Don't switch models mid-project; cinema-worldbuilder prompts won't translate cleanly.
- **Start Frame / End Frame slots** — these belong to Keyframe input mode (default), not Reference mode (what we use). Once you've switched to Reference mode, those slots disappear and reference slots take their place.

## When something goes wrong

- **Clip looks nothing like the references** → check the input mode pill in the toolbar. If it reverted to "Keyframe," your reference images were ignored. Switch back to Reference, re-attach, re-generate.
- **Credit cost on Generate button is way higher than expected** → check runtime (probably too long), resolution (might have flipped to 1080p), or copy count (might be above 1).
- **Character looks wrong** → check that the locked character sheet is one of the attached references. If you have a saved character in `@Characters`, bind it.
- **Wrong aspect ratio in the rendered clip** → the aspect pill must be clicked and confirmed before each generation. Don't trust the previous shot's setting to carry over.
- **Mouths not syncing to the music** → confirm the Audio Ref slice is actually attached (not just uploaded elsewhere), and that the prompt's lip-sync line in the Movement block quotes the exact lyric the slice contains — a mismatch between the two is the most common cause.
- **You hit the monthly Basic-tier cap mid-project** → either wait until the cycle resets (date shown in account settings), upgrade tier inside ArtCraft, or for one or two specific shots, spin up a Higgsfield Plus month and use it just for those (see `docs/higgsfield-ui-guide.md`).

## See also

- `docs/higgsfield-ui-guide.md` — same walkthrough for Higgsfield Plus / Ultra (the professional-tier alternative)
- `ai-film-director/SKILL.md` Step 5.0.1 — the orchestrator's first-time host setup walkthrough that points here
- `CLAUDE.md` — the workspace-level overview of where ArtCraft fits in the full production stack
