# Louis XIV, ep. 1 "My Morning" (Short, 32 s, 9:16) — production plan
STATE: PILOT_SPEC locked, facts checked twice. Nothing generated. Cost approval: NOT given (needs "да").
Brand: DRAFT 0.1 (map_shorts/history_channel/project.json). Channel: history POV channel, not Mr. Buck.

## Corrections after the second fact check (28.10)
- Where: the king's state bedchamber in 1685 was the Salon de Mercure (ceremonial bedchamber from 1682; lever and coucher held there ~17 years until 1701, per Versailles resources; bed position itself between 1684-1701 is not stated by the sources). So shot 1-3 = state bedchamber, NOT the Hall of Mirrors. Do not claim exact decor; keep it a gilded, painted-ceiling state room.
- The Hall of Mirrors (built 1678-1684) appears only in shot 4: the lever ends as the king goes to the Grande Galerie / daily Mass (two sources). Scene S02 = the threshold of the gallery.
- Order at the lever: the first valet wakes him; the doctor and surgeon are in the room at the start (two sources agree; one French source puts them in the "entrée familière" after the princes: so the line says "in the room before I am out of bed", no order claim).
- Shave about every two days; the king picks a wig from the barber/wig valet (one source: use as colour only, not as a chip).
- Number at the grand lever: "about a hundred" in two secondary sources (the same French teaching document may be behind both): chip says "UP TO ~100 AT THE GRAND LEVER" with the tag "secondary sources".
- Time of day: sources give 8:00 / 8:15 / 8:30: no time on screen.

## Script (VO = on-camera lines, English)
SH01 (0-8 s) "Good morning, Versailles. I have not stood up. And already... the room is full."
SH02 (8-16 s) "The doctor watches me wake. The surgeon watches the doctor. Nobody asks how I slept."
SH03 (16-24 s) "Bow. Lower. Good... lower. That is a hat. Pick it up."
SH04 (24-32 s) "Tonight, I dine in public. You may watch. Do not stare. Next time: dinner with the Sun King."

## Overlay (our graphics, not AI text)
- Corner mark all 32 s: "AI-GENERATED" (small, high contrast, top-left under the safe zone).
- SH01: title card "VERSAILLES, c. 1685" (serif, cream, gold year).
- SH02: chip "DOCTOR + SURGEON ARE IN THE ROOM BEFORE HE GETS UP" [2 sources].
- SH03: chip "UP TO ~100 COURTIERS AT THE GRAND LEVER" [secondary sources].
- SH04: chip "NEXT: DINNER, IN PUBLIC".
- Captions: cream, 1-3 word pop-ins, gold on the key word, lower third; no white-on-black.

## Scene locks
S01 state bedchamber: gilded panelling, painted ceiling, canopied bed with the curtains drawn back, tall windows (cool fill) + wax candles (warm key); period dress only; camera = the page standing at the foot of the bed, king screen-left, doors screen-right.
S02 gallery threshold: tall arched windows on one side, mirror panels on the other, daylight, polished parquet; the king walks ahead of the camera.
Character lock (face reference = the approved SH01 frame): man aged ~46, dark shoulder-length curled wig, thin moustache, heavy-lidded haughty eyes, fine linen nightshirt in S01 then an embroidered coat in S02.

## Prompts (model-ready; frames Nano Banana 2.1 $0.02 each, clips Veo 3.1 fast $0.18 each)
Frame style prefix (all): "Photorealistic vertical 9:16 vlog-style frame, handheld 24mm wide-angle lens, natural candle and window light, true-to-life fabrics, skin and wax, 17th-century French court, no text, no logos, no watermark, no modern objects."
SH01 frame: "Medium close-up selfie-style view from the foot of a canopied state bed: a haughty man of about 46 with a short curled wig, thin moustache and heavy-lidded eyes sits propped on pillows in a fine linen nightshirt, looking straight into the lens. Bed curtains drawn back, gilded panelling, painted ceiling, blurred waiting courtiers in period dress at the edge of the room."
SH01 motion: "Handheld, slight sway. He looks into the lens and says in a haughty, theatrical, slightly amused voice: 'Good morning, Versailles. I have not stood up. And already... the room is full.' On the last words a valet's gloved hand lifts a curled wig into the frame. Quiet room tone, a murmur, candle flicker."
SH02 frame: "Medium shot, handheld, king in bed, a first valet holds three curled wigs on his forearm and a stand, a physician in a dark robe and a surgeon with a small case stand at the bedside, gilded state bedchamber, candle and window light."
SH02 motion: "Handheld pan from the valet to the bedside. The king, deadpan, says: 'The doctor watches me wake. The surgeon watches the doctor. Nobody asks how I slept.' He lazily points at the middle wig. Fabric rustle, whispers."
SH03 frame: "Medium wide handheld, king in the foreground in bed or sitting up, tall double doors open behind him and richly dressed courtiers in period court dress filing in and bowing in a line."
SH03 motion: "The courtiers bow in turn. The king, unimpressed: 'Bow. Lower. Good... lower.' One courtier bows too low and his plumed hat tumbles to the floor. The king: 'That is a hat. Pick it up.' At the end a gilded hand mirror swings up into frame and flashes over the lens. Door latches, boots on parquet."
SH04 frame: "Handheld view from ahead of the king as he walks along a gallery threshold: arched windows on the left, tall mirror panels on the right, polished parquet, daylight; the king in an embroidered coat and full curled wig faces the lens, a few courtiers trailing."
SH04 motion: "Camera steps backwards, the king strides toward it and says with a raised eyebrow: 'Tonight, I dine in public. You may watch. Do not stare. Next time: dinner with the Sun King.' He turns away. Footsteps, a short harpsichord sting, hard cut."
Negative (all): "no modern clothing, no metal roofs, no phones, no glasses, no extra fingers, no text overlays, no crosses held in odd ways, no watermark."

## Sound
Native Veo speech first (voice may drift between clips: if so, re-voice the 4 lines with one TTS voice and keep the Veo ambience). Own harpsichord sting (synthesised), room tone, wood and fabric foley. Loudness -15.5...-12.5 LUFS, TP <= -1 via premium_gate.py.

## Gates (per skill + CLAUDE.md)
1. Frames first ($0.08), contact sheet, check: one face, same man across frames, hands/arms count, no modern items, bed/doors geometry. Max 2 corrective attempts per frame.
2. Clips ($0.72), check frame by frame: hands (5 fingers, each with an arm), the hat physics, the mirror, background people (no modern clothes, no roof/lamp), mouth sync, voice consistency. GENERATED != INSPECTED != APPROVED.
3. Edit: chips + captions + AI mark, own sting, loudness gate.
4. authenticity-check audit for fiction-with-real-history (facts, AI labels, no real descendants, music, sources), saved as authenticity_audit_<date>.md before any delivery.
5. Budget: planned $0.80; cap $2.4 (3 attempts per shot); stop and ask if more is needed.

## Publication draft (not published; no Zernio account for this channel yet)
Title: "A Morning with Louis XIV: 100 People Watch Him Wake Up"  [check the "100" once more before use; fallback: "A Morning with Louis XIV (AI Comedy)"]
Description: "A comedy reconstruction of the morning ritual at Versailles around 1685, in the voice of Louis XIV. The visuals and voice are AI-generated; the dialogue is invented for comedy. Facts: the lever had a small petit lever and a larger grand lever; the doctor and surgeon were present at the start; up to about a hundred courtiers attended the grand lever (secondary sources). Sources: Wikipedia 'Levée (ceremony)'; Shannon Selin 'Watching French Kings Rise'; earlymodernfrance.org 'The Lever du Roy'. Next: dinner in public. #history #versailles #louisxiv". Platform flags: altered/synthetic content ON.
