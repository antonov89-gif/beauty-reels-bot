
## C09 re-voice 30.10 (owner "делай"; Lumean 0.23 RUB, one order)
Exception C09: ["the"] added to voice_lock.json (respelling_exceptions): plain "the" in this clip only. ASR now hears "there goes the hat ... not on the hat", all word probabilities >= 0.86 except the first "lower" (0.26-0.65, same as before). tts_ep1/C09.mp3 = new take; C09_v2_ahat.mp3 = the previous take ("a hat"), C09_old.mp3 = the first version.

## C03 re-voice 30.10 (owner "да"; Lumean 0.23 RUB, one order): FAIL, not adopted
Goal: remove the audible "switch of take" before "and" ("surgeon's here, and nobody"). TTS-only change: no comma before "and" (voice_lock.json accent.tts_text_overrides, applied in tts_locked.py; the script keeps the comma).
Result tts_ep1/C03_v2_nocomma.mp3 (7.0 s vs 6.4 s): the voice still pauses 0.32 s and says "and" in a low creaky register (114 Hz against 141 Hz on "here" and 177 Hz on "nobody"); same defect, a little smaller (2.7 semitones down instead of 4.4). Also 0.6 s longer, so it would sit worse on the lips.
Measured: the low 0.25-0.35 s sound before "and" IS the drawled vowel of "and" (removing it removes the word: ASR medium then hears "here, nobody" in both takes), so it cannot be cut out.
Current C03.mp3 = the original take (unchanged). Next options need the owner: a different word or a tag at that spot (each a new 0.23 RUB order with its own yes).

## Marcel the page voice, 30.10 (owner "голоса продублируй"; Lumean 0.23 RUB, one order)
Voice 1 "Edward" (ElevenLabs, French, young), eleven_v4, three lines with 1.2 s between: ASR medium hears "The court, Sire." / "Pardon, Sire." / "Sire, I only..." (all words); median pitch 229 Hz vs the king 140-200 Hz (a clearly higher, younger voice: good contrast); 7.05 s. Split into tts_ep1/marcel_C07_court.mp3, marcel_C09_pardon.mp3, marcel_C13_sire_i_only.mp3. Not yet heard by the owner. NOT VERIFIED by ear: age and accent, the emotion tags (panic on "Pardon"), a French accent on a French voice with no accent tag.
