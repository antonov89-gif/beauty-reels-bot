# Ep.1 voice QC (locked voice v3, 29.10.2026)
Source: C01-C05 = audition_accent/heir_phon_eleven_v4.mp3 (accent test 2, same lock); C06-C10 and C12-C15 = two Lumean orders (0.31 RUB each, owner said yes). Per-clip files: tts_ep1/C01.mp3 ... C15.mp3 (cut at Whisper word timings, 0.08 s lead, 0.3 s tail, short fades). Times: clip_times.json. Listening file: louis_ep1_voice_all_clips.mp4 (not committed).

| Check | Result |
|--|--|
| Words (Whisper small vs script) | match ratio 0.94 / 0.96 / 0.96; all lines complete |
| Tags read aloud | none |
| Haughty laugh in C15 after "do what you like" | PRESENT: 2.6 s gap between "like." (22.58 s) and "I'm" (25.22 s) holds two voiced bursts with ~0.2 s pulses at -14 to -17 dB (laugh pattern); whether it sounds haughty = owner's ear |
| Clip lengths | C01 9.87 s and C15 7.81 s do not fit an 8 s clip comfortably: C01 and C15 become 10 s clips (Kling r2v allows 3-30 s); all others 4.0-7.5 s |
| Loudness | raw -20 to -22 LUFS; the edit normalises to -14 LUFS, TP -1.5 |

## Clarity flags (respelling side effects; captions keep normal spelling)
- C03: "the doctor's 'ere, the surgeon's 'ere" heard as "doctor's ear, surgeon's ear".
- C05: "taller, zey say" heard as "tall, as they say".
- C10: "Mine are ze tallest" heard as "Mine is a tallest".
Fix proposal: re-voice C03, C05, C10 in one order with the respelling switched off for those words only (about 0.25 RUB, needs the owner's yes). Until then the burned-in captions carry the right words.
