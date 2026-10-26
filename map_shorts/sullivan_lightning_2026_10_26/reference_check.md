# Reference check + self-check (26.10.2026) - final /home/claude/v78/su_final.mp4 (31.71 s, 1080x1920, 24 fps)
Method: frame_forensics on our final (4 fps 0-13 s, 1 fps after), loudness (ebur128), speech vs gap levels, STT (faster-whisper), last frame. Reference = frame-verified DNA (dna_c3aRLh3SoAs.md).

| Element | Reference (L3 frames) | Ours (measured) | Status |
|--|--|--|--|
| Danger in the first words | "rode his Segway right next to the cliff edge" 0-3 s | "lightning" at 1.80 s (line rewritten after self-check; first draft had it at 4.98 s) | PASS (FIXED) |
| Act 1 camera | continuous, whip-blur joins | 7 shots joined by 4-frame whip-blur joins 0-11.7 s | PASS |
| Reveal | hard cut + location jump ~19.5 s | hard cut + sub hit at 11.73 s ("Now, this wasn't the first time") | PASS (earlier, 37% vs 60%) |
| Keyword graphics | glow outline on object/edge + path arrow | yellow ring on the truck on "truck", dashed roll arrow, white glow on the cliff edge on "cliff" | PASS |
| Own graphics added | - | 1969, STRIKE #2, x7, #1·1942, #3·1970, #4·1972, #7·1977, 7/7 SURVIVED | PASS |
| Captions | 1-3 words, white bold + shadow, ~77% | 1-3 words, DejaVu Sans Bold + shadow, MarginV 430 (~78%); lifted over the ringed truck 1.75-3.3 s | PASS |
| Ending | reaction close-up, no loop | face to the storm, then puts hat on facing the storm (irony line) | PASS (differs on purpose) |
| Music | bed present (BPM UNKNOWN) | own synth 118 BPM; bed -21.8 dB (0-11 s), -18.4 dB (12-25 s); speech -13.6 dB; in act-2 gaps -20..-26 dB | PASS (after raising bed 0.32->0.62) |
| SFX | wind, motor, whoosh, drop | rain, 7 synthesised thunder hits, sub hit on the reveal, stings | PASS |
| Loudness | -12.3 LUFS | -14.4 LUFS, TP -1.3 dBFS | PASS |
| Voice | male, ~138 wpm | male (Lumean David), 81 words / 30.4 s = 160 wpm; STT matches the script word for word | PASS |
| Burned-in text in AI clips | brand sign, "off-road model" | none | PASS |
| Last frame | reaction | ranger with hat on, facing the storm | PASS |

## Faults found and fixed before showing (attempt log)
1. c01 fake fireball after the strike visible at 2.75-3.0 s -> source trimmed to 0.10-1.45 s. FIXED, re-checked on frames.
2. Caption over the ringed truck -> caption lifted (pos 540,1180) for 1.75-3.3 s. FIXED.
3. Music bed too low in act 1 (gaps -36/-37 dB) -> bed 0.62, act 1 x1.0. FIXED (bed now audible; short act-1 gaps stay ducked by sidechain).
4. Hat continuity: hat on (c13) then hat in hand (c06) -> order swapped. FIXED.
5. On-screen AI label was dropped, then restored as small "AI RECONSTRUCTION" (real person + real events). FIXED.
Clip trims (HARD faults avoided by edit, no regeneration): c04 tip-over/fall after 1.2 s cut; c13 hat vanishes after 2.2 s cut; c02/c06 identity drift later in the clip cut.
SOFT open: c12 face younger/softer than other shots; c09 spark FX exaggerated; c03 eyebrows not visibly singed.
