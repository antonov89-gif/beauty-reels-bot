# Gap review vs reference JUni9wxjZcU (youtube-cinematic-dna V5.1, sequence-level QC) - 26.10.2026
Evidence: frame_forensics on both files (reference /home/claude/v79/ref, ours /home/claude/v81/qc), motion.csv per second, transcripts. Reference science part = 0-23 s (the rest is a cartoon edit, not comparable).

## Measured
| Metric | Reference 0-23 s | Ours 0-32 s |
|--|--|--|
| Mean frame motion | 10.3 | 5.1 |
| Motion in the first 2 s | 17, 14 | 2, 4 |
| Visual beats | ~13 in 23 s (5.7 / 10 s) | 12 shots in 32 s (3.7 / 10 s) + counters |
| Scale dive to cells | 7.25 s (19%) | 9.7 s (30%) |
| Regrowth payoff starts | 11.5 s (30%) | 14.0 s (44%) |
| Last 4 s motion | n/a (edit) | ~1 (almost static) |
| Speech | 70 words / ~23 s = ~183 wpm | 84 words / 30.6 s = 165 wpm (not a defect) |
| Loudness | -8.7 LUFS | -14.2 LUFS (platform target; not a defect) |

## Gaps, ranked (severity, evidence, cheapest fix)
1. HIGH - Static hook: first 2 s are a still glass body (motion 2-4 vs 17/14). Reference opens on action. Fix (edit, free): open on c02 split (white line flashes, halves fly apart) under "If you gave away half of your liver", body shot later.
2. HIGH - Payoff too late: cell dive at 30%, regrowth at 44% vs 19% / 30%. Two donation lines delay it. Fix (re-voice ~1 RUB): merge L1+L2 into one line ("Surgeons take half to save someone, and what's left starts to grow."), payoff at ~9 s.
3. HIGH - Dead ending: last ~4 s motion ~1 and quiet tail (-30 dB) under a static question card -> exit point. Fix (edit, free): question over the regrowth loop (c07 pulse) with a push-in, music to the last frame, tail 0.8 s.
4. MEDIUM - Low overall motion (5.1 vs 10.3): c08, c09, c10, c04 nearly static. Fix (edit): stronger push/orbit (5% -> 12%), whip-zooms on stressed words.
5. MEDIUM - Fewer visual beats (3.7 vs 5.7 per 10 s). Fix (edit): split long shots (c07 growth 3.3 s, c09 4.8 s, c08 3.6 s) with inserts from existing clips (c05/c06 cells, c02 halves).
6. MEDIUM - Repeated angle: c07 used 3x (L2, L4, L6), c03 2x. Fix (edit): L6 "weird part" on c09 start or c05 pull-out instead of c07.
7. MEDIUM - Glitch language only at joins; reference puts RGB glitch bars inside shots on key words ("small device", "arm bone"). Fix (edit): glitch accents on "half", "grow", "full size", "weird".
8. LOW - Grade flatter/lighter than the reference (saturated cyan + red, higher contrast). Fix (edit): contrast +10%, saturation +15%.
9. LOW - Stakes weaker than "cut off your hand". Fix: big hook text "HALF YOUR LIVER" at 0 s.
10. LOW (open since QC) - stringy regrowth strands at ~15 s.

## Not gaps (deliberate)
No blood, no severed limb, no cartoon clips, -14 LUFS, own music, sourced and hedged facts.
