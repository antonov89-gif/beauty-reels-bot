# French accent for the king (owner 29.10.2026: "у него должен быть французский акцент")
Status: LOCKED as v3 on 29.10 (owner: "Да нормально" to test 2, variant B). Locked voice v2 (The Young Heir, Eleven v4) is a posh-British designed voice; the owner wants a French accent. Nothing is changed in `voice_lock.json` until a test is approved.

## Candidates (all found free through Lumean `voices/elevenlabs/library?accent=french&gender=male`, 27 voices; previews in `french_accent_voices.mp4`, metadata in `french_candidates.json`)
1 Antonin (warm, unsettling, elegant) · 2 Cyril (French-accented narrator, confident) · 3 Henri (French-American narrator) · 4 JP (social media, classy) · 5 Marcel (charming native accent, strongest accent) · 6 Jamie (French accent, charismatic) · 7 Nicolas (French English male) · 8 Antoine (articulate, calm, bright) · 9 Jimmy (documentary). Dropped: Bacbuc, Mathis, Alex (their previews are French-language).
Name clash: the voice "Marcel" is unrelated to Marcel the page in the script; harmless, but the audience never sees voice names.

## Tests (paid, Lumean; the exact price comes from `accent_test.py preview`, which is free)
Lines C01-C05 with the emotion tags, about 1000 characters: 0.39-0.40 RUB per voice (about $0.005). Seven variants (heir + the tag "[strong French accent]", marcel, antonin, cyril, jamie, nicolas, henri) = about 2.8 RUB. Run: `python3 accent_test.py go [names]`.
Pick criteria: accent clearly French but every word intelligible to an English listener (check by transcription), arrogant and haughty delivery, emotion tags obeyed (haughty laugh after "do what you like" in the C15 test), pace 0.95, no stock-AI sound.
After the owner picks: lock v3 in `voice_lock.json` (voice id, owner id, model, settings, a 10-12 s reference sample for the Kling `voices` input), re-run the emotion test on C06-C15 with the locked voice.

## Rules for the accent
- Light-to-medium French accent, comic but clear. No burned-in subtitles (owner 29.10); the platform SRT uses ordinary English spelling. Every line must be clear by ear.
- French words only the English audience knows: "my friends", "no?", "Magnifique", "Bon". At most one per clip.
- AI voice stays disclosed (platform flag and description).

## Owner verdict 29.10: the 9 library voices are rejected ("голоса не понравились")
Wider free search (keywords: french king, aristocrat, villain, pompous, snobby, butler, chef, Louis, Napoleon, noble, haughty; use case characters_animation): no new English-speaking French-accent male character voice. Most hits speak French (narrators); "Gaston - Theatrical French Accent" speaks Spanish. Lumean offers only TTS (no voice design, no voice changer).
Next, in order:
1. The voice the owner already liked (No. 7 "The Young Heir") + the accent tag "[strong French accent]" on Eleven v3 and on Eleven v4, lines C01-C05: 0.4 RUB each, 0.8 RUB total (`python3 accent_test.py go heir_tag` with EL_MODEL=eleven_v3 and eleven_v4). Keeps the arrogant voice, adds the accent.
2. If the tag does not give a clear accent: Voice Design (a new voice from a text description, "a haughty French king in his forties, strong Parisian accent in English, nasal, drawling, contemptuous") on ElevenLabs directly or Higgsfield `create_voice`; both need the owner's account or a top-up (Higgsfield balance 0.1 credits).
3. Most natural: a human performer, a French native who speaks English, recorded with recording_sheet.md, written licence for AI processing.

## Test 1 result (29.10, owner approved, 2 orders x 0.38 RUB = 0.76 RUB)
Files: audition_accent/heir_tag_eleven_v3.mp3 (39.2 s), heir_tag_eleven_v4.mp3 (34.8 s); listening file accent_test_v3_v4.mp4 (not committed).
Self-check: every word transcribed correctly (Whisper small), no tag read aloud, loudness -19.7 / -21.4 LUFS (normalised in the edit).
Accent proxy (Whisper language detection, probability "French" per 10 s): no-accent heir 0.006, heir + tag v3 0.002, heir + tag v4 0.003, library Marcel (strong native accent) 0.884, library Cyril (accented narrator) 0.012. Reading: the tag did NOT measurably add a French accent; the proxy is crude (Cyril has an audible accent at 0.012), so the owner's ear decides.

## Test 2 result (29.10, owner said "да", 1 order 0.37 RUB)
heir_phon_eleven_v4.mp3 (35.9 s): The Young Heir, Eleven v4, tag "[thick French accent]" plus TTS-only respelling (ze, zat, zem, zey, 'ere, 'undred, 'air, 'andsome). Listening file accent_test2_tag_vs_spelling.mp4 (A = tag only, B = respelling; not committed).
Self-check: no tag read aloud; loudness -21.9 LUFS. The transcript shows the accent features landed in places: "here" heard as "ear" (dropped h), "taller, zey say" heard as "tall, as they say", "Bow" as "Bau". Clarity risk: "the doctor's 'ere" can read as "doctor's ear"; captions carry the normal spelling. French proxy still near 0 (Whisper normalises the words), so the owner's ear decides.

## Decision 29.10
Owner accepted variant B. voice_lock.json v3 = The Young Heir, Eleven v4, prefix "[thick French accent]", TTS-only respelling list, emotion tags; reference sample heir_fr_sample.mp3 (12.8 s). Next voice step: emotion test C06-C15 with the locked voice (one order per 5 lines, about 0.4 RUB each) after the owner's yes.
