# Ep.1 sound bed C01-C08, v3 (phone sound) on top of v2, 30.10.2026
v3: owner "в референсе звуки от телефона, у нас этого нет": handling rumble, grips and knocks, phone-mic voice with proximity, low-frequency air. Details and measurements: sound_reference_vlog1.md. Below: the v2 notes.

Owner on v1: "звук постоянно один и тот же". Correct: v1 was one stationary hiss (one noise, its low-frequency band always on, the same in every scene) plus a few rustles. Spectrogram of v1 showed a steady horizontal band in every clip. v2 rebuilds it so that nothing repeats. Script: build_bed.py (own synthesis, no samples, no library, no music; free). Reference: Vlog 1 LjfGP7wpjVs measured on the owner's mp4 (voice_source.md): pause floor about -49.5 dB (10th percentile), no silence > 1 s at -50 dB, ambience differs per shot, -15.4 LUFS.

## What changed
1. Air: 4 frequency bands, each with its own random gain (+-9 dB, 0.8-2.5 s), no steady hum band, darker (less hiss). Colour differs per scene (bedroom A, wig table B, court C).
2. People: synthetic voices (pulse train through vowel formants, syllables, phrases, pauses), unintelligible, in a palace reverb. Scene A 3 voices (quiet), B none, C (court C07-C08) 8 voices.
3. A library of 18 different sounds: silk, wool, hair, cloth swish, footstep with heel click, shuffle, door creak + latch, wood creak, knock on wood, ring clink, metal case, powder puff, wig tap, fire crackle, cough, far birds (C01, C04), tools.
4. Three layers of placement: on the real motion peaks of each clip; at hand-set story moments (C03 the doctor and surgeon already stand at the far end: silk when he glances; C04 wig set on the table: wood; C06 powder puff; C07 door, 6 steps of the entering court, wig tap at "wig"; C08 bowing swishes and a knee creak); random ambient events with a per-clip kind mix and density, never on top of speech.
5. Events are ducked 9 dB under speech; reverb on murmur and partly on events.

## Measured (frames/<clip>_bed.mp4, frames/EP1_C01-C08_bed.mp4, 67.4 s; videos not committed)
| Item | Reference | Ours v2 | Verdict |
|--|--|--|--|
| Silence >= 0.5 s at -50 dB | none > 1 s | none in any clip or in the episode | PASS |
| Pause floor, 10th percentile | -49.5 dB | -46.6...-53.7 dB per clip, -50 dB episode | PASS |
| Loudness | -15.4 LUFS | -14.8 LUFS (clips -13.8...-15.5), LRA 6.9 | PASS |
| True peak | -1.1 | -4.4 | PASS |
| Variation of the bed itself (bed only, mean over 7 octave bands of the temporal std in 0.25 s windows) | - | 2.9-4.5 dB (v1 was a constant hiss with only a few rustles) | PASS (numbers are mine, not a standard) |
| Words (ASR medium, beam 5) with and without the bed | - | identical in all 8 clips | PASS |
| Narrow-band peaks (tone/music) | noise | v1 check same as the reference; v2 adds birds and clinks (short, natural), no sustained tone | PASS by design, not re-measured on v2 |

Notes from the check:
- C01 "Oops, the ceiling": with Whisper small beam 5 the bed flips this mumbled phrase to "there's a ceiling" (the same phrase is borderline without the bed too, low word probability). Small beam 1 and 3 and medium beam 1/3/5 all hear "the ceiling" with the bed: PASS.
- AAC at 192 kbps overshot to +0.7 dBFS in one channel; 320 kbps used.

## NOT VERIFIED
- By ear: I cannot listen. The owner must. Synthesised foley sounds are simpler than recorded ones; if a sound reads fake (the footsteps, the crowd), the fix is paid real-sounding SFX (ElevenLabs sound effects through Lumean, a few kopecks per sound, needs a separate yes with the price) or a licensed free library.
- Foley follows the picture's motion peaks and a few hand-set moments, not a frame-by-frame look at every action.
- C09-C15 are not built yet; the same script runs on them (add the clips, a scene D = Hall of Mirrors with a longer reverb).
