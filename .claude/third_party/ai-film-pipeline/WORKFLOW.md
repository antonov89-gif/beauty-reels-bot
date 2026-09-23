# The Pipeline

Derived directly from the K-Pop CTRL: Hunters breakdown. This is the order that wastes the fewest credits.

## Phase 0 — Discovery (concept lock, before any generation)

Write down, in plain language, what the film is. One paragraph. Then expand it into:

- **Who** — recurring characters, named in your notes (never in prompts). For each one, how many distinct looks they'll need across the film.
- **Where** — every distinct environment. Day or night. Interior or exterior. Establishing wide or anchored medium.
- **What** — hero props and creatures. Anything the camera lingers on.
- **Why** — one-sentence emotional throughline. The reason a viewer cares.
- **How long** — total target runtime. Most AI shorts live in the 30s–2min band.

Drop these in `projects/<project-name>/shot-list.md` under the Concept section.

## Phase 1 — Worldbuilding skeleton

Translate the concept brief above into a counted, named index of every recurring character, location, and hero prop — this is also where the project workspace gets scaffolded (`./scripts/new-project.sh <project-name>`) if it hasn't been already.

### Step 1.0 — Story bible (optional, narrative projects)

For any project with recurring characters and a narrative through-line (not a single-shot brand spot), consider building the story bible *before* character builds. Say "build a story bible" — `story-bible-builder` interviews you through premise, thesis, world timeline, factions, locations, world rules, and a deep per-character pass (function, visual lock, backstory, present-tense psychology, and prompt-ready quoted **Speech / Movement / Stillness** lines), plus ensemble dynamics and production rules.

The bible saves to `projects/<project-name>/story-bible.md`. It's the voice-consistency mechanism: once it exists, every `cinema-worldbuilder` prompt for that character pulls the locked Speech/Movement/Stillness lines straight into Sound Bed and Subject Lock instead of the character's voice drifting shot to shot. Skip this step for single-scene or dialogue-free projects — it earns its keep on anything with a cast and a script.

## Phase 2 — Character builds (the part that breaks most projects)

For each recurring character:

1. **Develop or upload reference.** Either describe them to the `banana-pro-director` skill (Step 0 free-form character development), or upload an existing image and have the skill mirror back a locked spec. Iterate until the user confirms.

2. **Lock the face first (Mode 0), then build the outfit (Mode 1).** Run Mode 0 face lock (Soul Cinema, Banana Pro, or GPT-2) on 18% gray seamless with a flat, shadowless grade — identity only, no outfit. Regenerate until the face *is* the character (Soul Cinema's unlimited rerolls make this cheap to iterate). Once the face is locked, build the base outfit on top of it in Mode 1 (Banana Pro single-pass or Soul Cinema's two-step Mode 1B). The K-Pop project ran 10–20 generations per member at this stage.

3. **Lock the character sheet (3-panel, the locked default).** Once one base image truly reads as the character, run the 3-panel sheet against it — LEFT: full-body front, headless (ghost-mannequin or clean neck cut per garment); CENTER: full-body rear with the head attached; RIGHT: tight chest-up face lock. One face on the whole sheet, roughly double the resolution per cell versus the old 6-panel layout, and far less panel-to-panel drift. This is the canonical reference everything downstream pulls from. (6-panel is legacy — only build it if you explicitly need that format.)

4. **Build the other looks.** Use the character sheet as Reference Image 1, design the new outfit as a separate Soul Cinema generation on a neutral model (Mode 1B), then composite. Common pattern from the breakdown: four looks per character —
   - Base identity (loungewear / personal style)
   - Battle suit / hero suit, helmet on
   - Battle suit, helmet off
   - Performance / stadium look (often with a distinct hairstyle)

5. **Log each locked look in `projects/<project-name>/character-bible-<name>.md`.** One bible per character. Reference images saved next to the bible.

## Phase 3 — World builds

For each environment from Phase 0:

1. **Build the pure environment plate first** (Banana Pro Mode 3B / Atmospheric M5). No humans. Establishing wide. This gives you the world.

2. **Iterate on second-angle plates** of the same space if the film needs them. The breakdown notes Higgsfield can be stubborn about flipping POV on an existing plate — expect trial and error here.

3. **Log each environment in `projects/<project-name>/environment-bible-<location>.md`** with the prompt that produced it and the reference image filename.

For creatures and hero props (alien creatures, arcade machines, vehicles, weapons):

4. **Build a creature/prop reference sheet** (3-panel default cadence against 18% gray seamless, flat shadowless grade — 6-panel legacy only if the prop's detail load genuinely needs it).
5. **Log in `projects/<project-name>/prop-bible.md`.**

## Phase 4 — Shot list (story flow lock)

Before generating a single video shot:

1. **Map the film beat by beat in `projects/<project-name>/shot-list.md`.** Every cut. Every transition. Every payoff.
2. **For each shot, write down what the viewer sees and what they hear.** If a character looks off-frame, what's she looking at? The next shot has to deliver it.
3. **Mark which cinema mode (M1–M5) each shot uses.** This locks camera grammar.
4. **Mark which characters and which look** appears in each shot.
5. **Decide auto-edit per shot.** Multi-shot sequences in one prompt = auto-edit ON. Sustained single takes = OFF.

This phase is what separates a film from "the sickest poster of all time." The HTML breakdown is emphatic: shots that don't follow from the shot before are wasted.

## Phase 5 — Seedance generation

For each shot in the shot list:

1. **Feed the scene + references into `cinema-worldbuilder`** on claude.ai. Name the element tags for each reference (`@sol_ref`, `@loft_plate`, etc.) if you haven't already, confirm runtime explicitly, and confirm the pre-prompt summary. The delivered prompt comes back as a title line plus a single code block of ten labeled blocks (Scene & Mood, Frame Map, Subject Lock, Cross-Frame Rules, Movement, Last Frame, World Plate, Sound Bed, Capture Realism, Camera Capture) with your tags placed inline at each anchor point. If a story bible exists for the project, pull the character's Speech/Movement/Stillness lines into the conversation before asking for a dialogue-bearing shot.
2. **Paste the prompt into Seedance.** Attach the same reference images in the Higgsfield UI under the matching tag names.
3. **Generate. Review.** If it lands, log it in `projects/<project-name>/generation-log.md` with the prompt, references used, and the result filename.
4. **If it misses, iterate.** Small adjustments don't need a full re-prompt — the skill skips the pre-prompt check on minor iterations.

Tips that save credits:
- Let Seedance handle multi-shot cuts. The model is good at edits.
- Don't waste credits on shots whose narrative role you haven't confirmed.
- 11–15 seconds is the sweet spot per generation. Longer often degrades.

## Phase 6 — Music (Suno) and title card

1. **Music via Suno.** Use your project's copy of the suno-music-prompt template for a style prompt and a lyric sheet. Two generations is usually enough. Upload the chosen track into Higgsfield in 12–15s slices so Seedance can sync lip movement.

2. **Title card via Banana Pro.** Use your project's copy of the title-card-prompt template — product-render letterform grammar from the breakdown.

## Phase 7 — Post

1. **Topaz Video** to upscale every clip to delivery resolution (see `docs/upscale-guide.md` for the recipe — optional and skippable if you generated at 4K natively).
2. **Edit the assembly.** A real NLE (DaVinci Resolve, Premiere, FCP). AI generations are clips, not the cut.
3. **Layer music + dialogue + diegetic sound effects.** Seedance produces diegetic audio natively — keep what's useful, mute what isn't, layer Suno on top.
4. **Color pass if needed.** Most clips are already graded; the assembly may need balancing.

## Credit discipline (from the breakdown)

The K-Pop project burned ~7,500 credits, half wasted, across 133 video generations averaging 11s each. The author estimates it could have been done in ~3,000 with the workflow they wrote *after* the project. The biggest credit sinks were:

- Fighting Seedance instead of feeding it the right prompt grammar → the skills fix this.
- Generating before the shot list was locked → Phase 4 fixes this.
- Regenerating characters that weren't fully locked → Phase 2 fixes this.

Every generation should answer: *which shot in the shot list is this for, and which look from the character bible.* If you can't answer both, stop and lock that first.
