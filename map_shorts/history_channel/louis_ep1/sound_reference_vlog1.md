# Sound of the reference Vlog 1 (LjfGP7wpjVs), 30.10.2026 (owner: "посмотри ещё раз на референс, там звуки от телефона и от всего")
Evidence: (M) MEASURED on the reference audio from the owner's mp4 (a.wav, 128 s; sndref/analyze.py in the session: Whisper word times, spectral-flux onsets classed by band, take-by-take floors); (V) vidIQ AI watch 30.10 (10 credits) = HYPOTHESIS where not confirmed by (M).

## What the reference sound is made of
| # | Feature | Reference | Evidence | Ours v2 (before) |
|--|--|--|--|--|
| 1 | Phone handling: thumps, finger rubs, mic scrape | at the start of takes (0-4 s, 23-26 s, 52-56 s) and at the end (lens covered 111-113 s); 24 low thumps in 128 s, most of them under speech | M (thumps at 52.4, 54.7, 55.0, 55.3, 56.0, 112.2, 112.6, 112.9 s ...) + V (labels) | none (1 thump) |
| 2 | Quiet floor = low-frequency phone-mic rumble, not hiss | centre of the quiet floor 170-624 Hz per take, most energy below 200 Hz | M | hiss, centre 1-4 kHz |
| 3 | Floor changes per take | p10 -46 / -53 / -45 / -47 dB, colour differs | M + V | per scene, yes |
| 4 | Proximity: voice louder and boomier when close, thinner and roomier when far or off-axis | word level range 13.8 dB (ours 10.0); V: 0:01-0:03 boomy close, 0:08-0:15 more distant, 0:40-0:43 off-axis | M (range) + V (where) | constant studio voice |
| 5 | Phone-mic voice colour | darker: spectral tilt -8.4 dB/oct (ours -5.5), top rolls off about 7.1 kHz | M | brighter |
| 6 | Room echo | strongest in the wide hall, weakest in close-ups | V | small |
| 7 | Objects and body | jar clink, toothpick ting, crust crack, chewing, platter crash, sighs, laughter, another person's line | V (partly M: clicks) | partly (rings, cloth, steps, door) |
| 8 | Music | none | V + earlier measurement | none |

## What v3 adds (build_bed.py)
1. Handling: a low rumble whose level follows the real camera speed of each clip (ORB on the frames), grips and knocks on the phone body at the camera jerks and at hand-set moments: C01 0-3 s (the phone turned from the ceiling, like the reference 0-4 s), C04 the phone set on the table, C06 the pick-up from the table, C07 re-grip and the too-close re-centre, C08 the push-in; light grips in the C02/C03 selfies. Dry, at the mic, not ducked under speech (in the reference most thumps are under speech).
2. Phone-mic voice: low cut 110 Hz, darker top, 8 kHz roll-off; proximity from per-clip distance keyframes plus the measured zoom of the picture: close = more bass and drier, far = thinner, up to -9 dB quieter, more room. C01 starts far/off-axis (camera on the ceiling) and comes close at 2.4 s; C04 is far (propped on the table); C06 goes from far to close when he picks the phone up; C08 gets closer with the push-in.
3. Air: low-frequency, the hiss removed.

## Measured after v3 (frames/EP1_C01-C08_bed.mp4)
| Item | Reference | v2 | v3 |
|--|--|--|--|
| Quiet-floor centre | 170-624 Hz | 1-4 kHz | 489 Hz |
| Share below 200 Hz | -1...-2.9 dB | - | -3.2 dB |
| Voice tilt | -8.4 dB/oct | -5.5 | -6.5 |
| Word level range | 13.8 dB | 10.0 | 11.0 (most of C01-C08 is a close selfie; the far clips C04/C05 are quieter) |
| Low thumps (classifier) | 24 in 128 s | 1 | 6 in 67 s + 24 hand-set grips/knocks (grips are classed as rustle) |
| Loudness / TP | -15.4 LUFS / -1.1 | -14.8 / -4.4 | -15.0 / -1.0 |
| Silence >= 0.5 s at -50 dB | none > 1 s | none | none |
| Words (ASR medium) with/without the sound | - | same | same in all 8 clips |

## NOT VERIFIED
- By ear (I cannot listen): the owner judges whether the grips and knocks sound like a real phone.
- vidIQ's labels of the reference sounds are a hypothesis; the times of the handling thumps are confirmed by the measurement, the names of objects (jar, toothpick, crust) are not.
- My metrics (tilt, word range, thumps) are my own tools, not a standard.
