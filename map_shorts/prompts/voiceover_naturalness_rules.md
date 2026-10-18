# Voice-over naturalness rules (standing, set by the user 18.10.2026)

Goal: the narration sounds like a real person talking, with no audible synthetic artefacts.
The AI-voice disclosure stays in every description and in the platform toggles (YouTube `isAiGeneratedContent`, TikTok `isAigc`): it is a platform rule and never removed.

## 1. Write for the ear
- Short spoken sentences, 5–18 words, mixed lengths; contractions where a person would use them ("it's", "didn't").
- Numbers spelled out ("fifty-eight", "four thousand five hundred"); no stacked lists of foreign names in one breath.
- Foreign names: use the surname or a phonetic spelling if a voice mispronounces the first name (test: "Ivan" came out as "Yvonne" on 18.10 → say "Moskvitin" only).
- One idea per line; punctuation marks where a person would breathe; no tongue-twisters.

## 2. Delivery settings (ElevenLabs via Lumean)
- stability 0.35–0.45, similarity 0.75–0.8, style 0.25–0.35, speaker boost off, speed 1.0–1.05.
- Pauses `{{pause=0.25–0.45}}` only at sentence ends, vary them; no pause inside a sentence.
- Target 140–150 words per minute.

## 3. Check before using (free)
- Transcribe the result with faster-whisper (`small.en`) and compare with the script: every name and number must be heard correctly.
- Check pauses (no silence > 0.9 s inside a line), no clipping, no low rumble, no harsh sibilance.

## 4. Post-processing (free, in the mix chain)
- high-pass 85 Hz; gentle de-esser; small dip around 250 Hz and a small lift around 3.5 kHz; light compression (2:1); a very short room echo (≤ 10 % wet) so the voice sits with the music; no hard gate; no heavy pitch or formant effects.
- Voice leads: music ducked under it (sidechain), loudness −14 LUFS, true peak ≤ −1.5 dBTP.

## 5. Money
- Regenerating a voice costs money: name the cost and ask first.
