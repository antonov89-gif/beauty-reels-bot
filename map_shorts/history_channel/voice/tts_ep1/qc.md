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

## Re-voice 29.10 (owner said yes, 1 order 0.28 RUB): C01 (new opener), C03, C05, C10
Respelling switched off for "here" (C03), "they" (C05), "the" (C10); accent prefix and all other respellings kept.
- C01 "Marcel, not the ceiling. Me. Good. Welcome to Versailles. Yes, I'm that handsome. Try not to faint.": 8.8 s, all 17 words heard; stays a 10 s clip (the opening tilt needs the room).
- C03: heard "The doctor's here, the surgeon's here..." (no more "ear"); 6.45 s.
- C05: heard "...I never looked down" (Whisper adds a "d" where "look" runs into "down"; meaning unchanged; owner's ear decides); 4.05 s.
- C10: heard "Mine are the tallest, of course" (fixed); 5.98 s.
clip_times.json and the per-clip files C01/C03/C05/C10 replaced; listening file rebuilt (louis_ep1_voice_all_clips.mp4, not committed).

## BUG found and fixed 29.10 (my error)
The per-clip cut used output seeking with a fade-out timed on the input timeline, so every clip that did not start at 0 s of its source file came out SILENT (only C01, C06, C12 had sound). The listening file sent to the owner earlier was therefore broken. Fix: re-cut with atrim + asetpts; every clip checked for level (mean -19 to -25 dB) and transcribed one by one; the rebuilt listening file was checked segment by segment (14/14 with sound). Rule added: after any cut, measure each output file, not only the source.

## Per-clip transcription (each file alone, Whisper small)
14 clips; similarity to the script 0.82-1.0. Two more clarity flags that the group transcription had hidden:
- C02: "ze rising" heard as "Z-Rising".
- C04: "Now, ze wig. My 'air..." heard as "Now, is he wig? My air...".
Respelling exceptions added for C02 ("the") and C04 ("the", "hair"); re-voice of C02 + C04 = 1 order (about 0.23 RUB) after the owner's yes.

## Re-voice C02 + C04 (29.10, 0.23 RUB)
C02 7.78 s, heard "...The ceremony is called The Rising..." (ratio 1.0); C04 6.84 s, heard "Now, the wig. My hair started falling out..." (ratio 0.95). Both clear by ear now; levels -22 dB mean.

## C08 + C09 re-voice (29.10, owner "Да"; one order 350 chars, 0.23 RUB; C08-C09.mp3 split at 6.90 s)
C08.mp3 6.95 s: ASR "All these people, and nobody may speak before me, I love listening to myself, mostly." PASS.
C09.mp3 5.54 s: ASR "Lower lower and there goes a hat eyes on me not on the hat": the first "the hat" (respelled "ze") is heard as "a hat"; meaning unchanged, the second "the hat" is clear. Soft; fix = respelling exception [the] for C09 + re-voice (0.23 RUB), needs a yes.
Old takes kept: C08_old.mp3, C09_old.mp3.
