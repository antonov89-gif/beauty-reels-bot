# Ep.2 "Dinner in Public": storyboard (31.10.2026, from script.md draft 3)
No generation is ordered by this file. Camera base for every clip = CAMERA_BASE in louis_ep1/camera_plan_ep1.md (phone in one hand at arm's length, clumsy, never a gimbal move). The king is the only star; Marcel and the crowd stay plain.

## Set and look (locked for the whole episode)
- **Place:** the antechamber of the royal apartment, evening. One long table with a white cloth along the frame, one armchair for the king at the head, gold plates and candlesticks. Behind the table a standing crowd in plain wigs and dark clothes; at the front, 4-5 ladies on folding stools. Painted ceiling (from C01). Tall windows black with night.
- **Light:** warm candlelight only, from the table; faces lit from below and the side, deep soft shadows; no daylight, no cold fill. Grade as ep.1 (brightness about 90, grain and sharpen like C06/C08).
- **King:** tall white-powdered wig, white court makeup, scarlet coat with gold suns, lace cravat, napkin tucked in (face master v3 in louis_card/face_master_v3/).
- **Marcel:** descriptor and livery from marcel_card/README.md (sky-blue coat, silver braid, small white wig with black ribbon). Refs: marcel_front.jpg + marcel_three_quarter.jpg.
- **Extras:** courtiers in simple period wigs; nobody copies the king's wig, coat or makeup.
- **Sound (no music):** room tone of a big hall, a low crowd murmur, cutlery on gold, candle flicker, fabric, footsteps on parquet. Phone knocks on the clumsy moments. Foley detail in the table below. Video model audio is muted; our v3 voice is laid by phrases (build_r2v_ourvoice.py).

## Continuity props (state over time)
| Prop | State by clip |
|--|--|
| Napkin | tucked in the cravat C01-C13; used to wipe fingers C14 |
| Soup bowls | empty stack of 4 beside him from C05; a 6th is put down in C05; gone after the burst |
| Pheasant leg | in his hand C06-C08 (greasy); bone on the plate after C09 |
| Phone | clean C01-C09; wine on the lens C10; wiped with the sleeve C11; the red smear stays on his cuff |
| Wine stain | a red splash on the cloth and on the right cuff from C10 to the end |
| Gold button | on the coat until C15, then lost (shoots off in C15); a gap on the coat in C16-C17 |
| Partridge | one leg left on a silver dish from the burst to C15, then gone |
| Peas | a small silver dish from C12 on |
| Hand mirror | on the table from C16, in his hand for C16-C17 |

## Shot list
Columns: frame = what the picture shows; camera = path with the clumsy moment; sound = diegetic only; first frame = what must be made before the video; risk = what the model usually gets wrong.

### Setup 1. Antechamber (0:00-0:27)
| Clip | Frame | Camera | Sound | First frame | Risk |
|--|--|--|--|--|--|
| **C01** 0:00-0:11 | Painted ceiling, candle smoke drifts across it. He swings the phone down onto his face: seated at the head of the long table, napkin in the lace, plates behind. | Starts on the ceiling shaking; a fast tilt down, overshoots to the chin, he re-centres. | Phone rustle, candles, murmur far behind | Reuse the ep.1 C01 method (ceiling first frame + keyframe), new set | Ceiling-to-face tilt: Kling first-frame control, our voice laid on top |
| **C02** 0:11-0:19 | Close selfie, then the phone dips to the empty gold plates and back. | Dip to the table (2 s), return with a sway. | Cutlery set down, murmur | New frame: table close-up + face | Plates must stay empty; keep the stack of bowls out of frame until C05 |
| **C03** 0:19-0:27 | He over the shoulder at a side door: people enter and bow, one bows too little. Back to the lens, he looks the viewer up and down. | Swing right with his shoulder, back with a jerk; face cut at the left edge for a moment. | Footsteps, fabric, a cough | Door + 4-5 bowing extras behind his shoulder | Bowing crowd faces; keep them small and in the background |

### Setup 2. Marcel films (0:27-0:37)
| Clip | Frame | Camera | Sound | First frame | Risk |
|--|--|--|--|--|--|
| **C04** 0:27-0:37 | The phone is handed out to the side. Marcel takes it: picture jumps, wide view of the room: table, ladies on stools in front, crowd standing behind. Marcel tilts down too far: the king's double chin fills the frame, he frowns. | Hand-off jump (1 s of blur), wide pan across the room (3 s), over-tilt to the chin (2 s), the king's hand pushes the phone up. | Rustle of the hand-off, crowd murmur, Marcel's breath | Two frames: wide room (made with the crowd) and the king's chin from below | Two people, hand-off physics: if the model fails, cut hard on the jump |

### Setup 3. First course (0:37-1:11)
| Clip | Frame | Camera | Sound | First frame | Risk |
|--|--|--|--|--|--|
| **C05** 0:37-0:47 | Phone back in his hand. Four empty bowls stacked beside him; he drinks soup from a fifth. On "she can't count" a servant's hand puts down a sixth in the corner. | Selfie with sway; at the pause the camera slides towards the new bowl, then back. | Spoon on gold, slurp, bowl set down | Frame with the stack of 4 bowls and the king | Bowl count: say "stack of four" in the prompt and check the count on frames |
| **C06** 0:47-0:55 | A roast pheasant is carried in. Marcel holds a silver fork into the lens. He pushes it aside, tears off a leg with his fingers. | Fork fills the lens (focus hunts), phone swings back to his face. | Plate on cloth, fork scrape | Pheasant + Marcel's hand with fork in the foreground | Fork in the lens may become a sword; keep the fork thin and clearly a fork |
| **C07** 0:55-1:03 | Over his shoulder: in the crowd a courtier eats a chicken leg with both hands, licks his fingers, very serious. | Slow pan over the shoulder, the phone drifts; the courtier is held in the centre. | Chewing, a murmur | Courtier frame in the crowd | Hands and fingers; hold the leg in the centre, no fast moves |
| **C08** 1:03-1:11 | The greasy pheasant leg points at the lens, then he pulls it back to speak to us. | Leg thrust at the lens (focus hunt), back to the face. | Chew, swallow | Selfie with the leg | Reuse C06 frame; same pheasant |

### Setup 4. The drink (1:11-1:37)
| Clip | Frame | Camera | Sound | First frame | Risk |
|--|--|--|--|--|--|
| **C09** 1:11-1:19 | He raises one finger without looking. Behind him a gold cup goes from hand to hand through the crowd. | Phone steady-ish on his face, the cup travels in the background from left to right. | "A drink for the King!" passed along (our extra voices), footsteps | Frame with the chain of hands behind him | The cup chain: keep three hands at most |
| **C10** 1:19-1:27 | The cup arrives. Marcel bumps the table: wine splashes over the lens, red blur, silence. He laughs. He turns the red phone onto Marcel, who freezes, terrified; beat; the king laughs: "I'm joking." | Splash (1 s), red blur (2 s), a rough turn to Marcel's frightened close face (3 s), a jolt on the laugh. | Table knock, wine slap on glass, silence, laugh | Marcel e7_terrified close face + wine-blur overlay | Wine on the lens is hard for models: make it as a post overlay (red blur plate), not generated |
| **C11** 1:27-1:37 | He wipes the lens with his sleeve (smeared red), turns the phone to Marcel, who reads the screen over the king's shoulder. | Wipe (cloth fills the lens), two-shot at arm's length, Marcel reads. | Fabric on glass, a murmur | Two-shot king and Marcel | Phone screen text must not be readable; keep it blurred |

### Burst (1:37-1:45)
Eight macro shots, 1 s each, hand-held on the table, quick pushes: (1) soup with a floating spoon, (2) pheasant, (3) partridge, (4) big salad bowl, (5) mutton, (6) ham, (7) pastry, (8) fruit and the one remaining partridge leg on its dish. Sound: plates, silver, murmur. Made as stills with an animated push-in (free) or 8 short clips (own yes).

### Setup 5. Dessert (1:45-2:27)
| Clip | Frame | Camera | Sound | First frame | Risk |
|--|--|--|--|--|--|
| **C12** 1:45-1:53 | Small silver dish of green peas, one pea held to the lens, focus hunts; his face behind, hurt. | Close macro pea, focus pulls to the face. | Tiny silver clink | Pea macro + face | Pea size; keep one pea clearly in focus |
| **C13** 1:53-2:01 | He slides low in the armchair, hands on his belly, eyes half-closed, the phone held loosely above his face. Long happy sigh and laugh. | Looking up at his face from the belly; slow drift, no jerk (calm contrast beat). | Fabric, sigh, chair creak | Low-angle frame, belly and face | The ONE calm shot of the episode; keep it |
| **C14** 2:01-2:13 | He sits up, wipes his fingers on the napkin, glances at the crowd, then chin up into the lens, haughty laugh. | Phone jerks up with him; chin up; the face slides off-centre on the laugh. | Napkin, laugh | Selfie, chin up | Haughty laugh: lip sync is laid, face only needs open mouth |
| **C15** 2:13-2:27 | Laughing too hard: a gold button shoots off and hits Marcel's forehead. Marcel rubs it. Beat. At the edge Marcel's hand reaches for the last partridge leg. The king sees it on the screen. | Two-shot; button flies (cut to Marcel's forehead if the model fails); the phone drifts to the dish. | Metal tick, Marcel's "ow" held back, silence | Two-shot with the dish at the edge | Small flying button: cut on the hit, the button itself may be a post element |

### Ending (2:27-2:48)
| Clip | Frame | Camera | Sound | First frame | Risk |
|--|--|--|--|--|--|
| **C16** 2:27-2:38 | He stands, the crowd bows. Looks into the hand mirror, nods to himself, points at the camera. | Phone swings up with the stand-up, mirror in view, finger to the lens. | Chairs scrape, fabric, murmur | Standing frame with bowing crowd | Standing up while holding the phone; keep the crowd soft |
| **C17** 2:38-2:48 | Orders by finger, back of the hand on "do what you like", cold laugh, then turns and sits at the full table; the gilded mirror covers the lens. | Finger at the lens, tilt away on the laugh, whip-pan to the table, mirror over the lens = cut. | Cold laugh, chair, cutlery | Reuse the ep.1 C15 pattern | Gilded mirror = a clean cut to the end card |
End card: "THE SUN IS NEVER LATE." plus "AI-generated comedy reconstruction", no corner mark.

## Plates and burned-in text
C01 VERSAILLES, FRANCE · 1685 | C02 THE KING'S PUBLIC DINNER · EVERY NIGHT AT 10 PM | C04 A FEW HIGH-RANKING LADIES SAT IN FRONT, THE REST STOOD | C05 HIS SISTER-IN-LAW WROTE: 4 SOUPS, A WHOLE PHEASANT, A PARTRIDGE, A BIG SALAD, AND MORE | C06 HE FORBADE HIS GRANDSONS TO USE FORKS | C09 GLASSES WERE BROUGHT ONLY WHEN THE KING ASKED | Burst SOUP, ROASTS, SALADS, SWEETS, THEN FRUIT | C12 1696 LETTER: THE COURT'S CRAZE FOR GREEN PEAS (year still open) | C16 NEXT: THE OPERATION.

## Production plan (needs your yes for each paid step)
1. **First frames** (images, about $0.04 each as in the card work): about 17 clips, most share the set; character refs exist. New: the long table with the crowd, Marcel two-shot, pheasant, courtier, peas, low-angle belly.
2. **Order of work:** pilot of 2-3 clips (C01, C05, C10 overlay test) before the batch, at most 2 corrective attempts per clip, GENERATED is not INSPECTED is not APPROVED (reference_check.md).
3. **Video route (proposal):** Kling 4.0 i2v ($0.2175/s, exact first frame, own voice only) for solo king clips: C01, C02, C05, C08, C12, C13, C14, C16, C17. Seedance 2.0 r2v ($0.126/s, 720p) for clips with Marcel or a crowd action: C03, C04, C06, C07, C09, C11, C15. C10 and the burst: still plus overlay or the cheapest shots. Rough total for about 150 s of video: $20-30 (price per second from the ep.1 orders, to be re-checked on the provider before the order).
4. **Voice:** v3 TTS (about 1 RUB) first, to fix the real length; Marcel and the cupbearer get other AI voices.
5. After assembly: authenticity audit, captions in 7 languages, dubs as in ep.1.
