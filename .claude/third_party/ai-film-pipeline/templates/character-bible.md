# Character Bible — [Working Name]

> **Working name is for your notes only.** It never appears in any prompt sent to Higgsfield. Prompts describe by visual marker.

## Locked identity (never changes)

- **Visual descriptor (use this verbatim in prompts — age-blind, no proper names, no real brands):**
  - e.g. "a woman with a slim athletic build, flawless porcelain skin, soft symmetrical features, large expressive almond-shaped eyes, full lips"
  - **Do not use:** age words (young / teen / middle-aged / older), proper names, brand names. Describe by build, role, and clothing instead.
- **Hair (canonical / default):** color (every nuance — platinum, jet black, rose-pink, etc.), length, texture, parting, signature styling
- **Eyes:** color, shape, brow shape and density
- **Skin:** finish (matte, dewy, glass-skin, bare), tone, any beauty marks visible in references
- **Build & proportions:**
- **Distinguishing markers:** piercings, tattoos, freckles — only if locked into the character
- **Default expression / energy:**

## Locked character sheet reference

> **Why this can't be skipped:** without a locked sheet, the character drifts by Shot 3. Every regeneration trying to recover the face costs credits the shot list can't afford.

- **File:** `references/characters/<working-name>/sheet.png`
- **Prompt used (from banana-pro-director Mode 2):**
  ```
  [paste the 3-panel prompt here once it's locked]
  ```

### 3-panel layout (locked default) — record what you locked

`banana-pro-director` Mode 2A ships the locked default: **LEFT — full-body front, headless** (ghost-mannequin hollow for structured necklines, clean neck cut for dresses and open necklines); **CENTER — full-body rear, head attached**; **RIGHT — tight chest-up face lock**. One face on the whole sheet, roughly double the resolution per cell versus the old 6-panel grid, and far less panel-to-panel drift. 18% gray seamless, flat shadowless grade, stated as applying uniformly across all three panels.

- **Headless treatment used (LEFT panel):** [ghost-mannequin hollow / clean neck cut — note which, and why]
- **Backdrop:** [gray seamless (default) / white (explicit request)]
- **Any deviation from default panel pick:** [rare — note here if the project needed a different structure]

**6-panel (Mode 2B) — legacy, explicit-request only.** Full-body front · 3/4 turn · back · waist-up · hands · face, same 3×2 grid. Only build this if the project specifically needs it — six cells starve the face panels of resolution and drift more between panels than the 3-panel default.

- **Panels locked for this character (if 6-panel was used):** [list the six panels actually generated]
- **Reason 6-panel was chosen over the 3-panel default:** [e.g. "hands detail was load-bearing for this film"]

---

## Look 1 — [Base identity / loungewear]

- **What it is:** her personal style off-duty.
- **Wardrobe (head to toe):** every garment, fabric, fit, color, accessory, footwear.
- **Hair (if different from canonical):**
- **Jewelry & accessories:**
- **Reference image:** `references/characters/<working-name>/base.png`
- **Prompt used:**
  ```
  [paste the locked prompt]
  ```

## Look 2 — [Hero / battle / signature suit, fully closed]

- **Wardrobe / armor description:**
- **Helmet / face cover state:** on, sealed, no glass visor
- **Reference image:** `references/characters/<working-name>/look_suit_closed.png`
- **Prompt used:**
  ```
  [paste]
  ```

## Look 3 — [Same suit, helmet retracted / face revealed]

- **Wardrobe:** same as Look 2.
- **Helmet state:** retracted into suit collar
- **Hair revealed:** [should match canonical hair from identity block]
- **Reference image:** `references/characters/<working-name>/look_suit_open.png`
- **Prompt used:**
  ```
  [paste]
  ```

## Look 4 — [Performance / stadium look]

- **Wardrobe:**
- **Hair (often distinct for performance — high pony, pigtails, etc.):**
- **Performance props:** microphone, in-ear monitor, wireless pack
- **Reference image:** `references/characters/<working-name>/look_perf.png`
- **Prompt used:**
  ```
  [paste]
  ```

## Add more looks as needed

For each additional look (festival, press, casual, sleepwear, etc.), copy a block. Keep canonical identity locked; only the look changes.

---

## Cross-reference

- **Shots this character appears in:** see `shot-list.md` for filter by character.
- **Other characters seen with:** [list working names of groupmates / co-stars]
- **Speech / Movement / Stillness locks:** see `projects/<name>/story-bible.md` § [character] — paste the quoted lines here once locked
  - **Speech:** [quoted, prompt-ready line — register, cadence, signature phrasing]
  - **Movement:** [quoted, prompt-ready line — how they move, gestures, tics]
  - **Stillness:** [quoted, prompt-ready line — what they do when not moving]
