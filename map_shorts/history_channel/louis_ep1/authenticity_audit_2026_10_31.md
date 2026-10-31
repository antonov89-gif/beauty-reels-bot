# Authenticity audit: Louis XIV vlog, episode 1 "My Morning" (31.10.2026)
File checked: `frames/EP1_full_C.mp4` (not committed): 133.46 s (2:13.5), 245 MB, H.264 1080x1920 24 fps, AAC 48 kHz stereo, -15.2 LUFS, true peak -0.9 dBFS. Cut C = cut B (owner removed the corner AI mark) + one plate reworded by this audit. Built by `build_ep1.py` from the clips listed in `reference_check.md` ("EPISODE 1 FULL CUT A/B").
Channel: history channel (NOT Mr. Buck). Genre: comedy reconstruction with real facts; the king and his lines are performed comedy, the plates carry the facts.
Method: stills at 0 s, 1 s, every cut and the last frame (`check_ep1.py` sheets), plates on frames, ASR of every clip, blackdetect/freezedetect, loudness, tone test for music; facts re-checked today against the pages listed under Sources (WebSearch/WebFetch 31.10).

## 1. Claims
| Where | Claim | Source checked 31.10 | Verdict |
|--|--|--|--|
| C01 voice | "I am Louis, King of France. They call me the Sun King." | common knowledge; Ballet de la Nuit page (sun emblem) | VERIFIED |
| C01 plate | VERSAILLES, FRANCE · 1685 | court at Versailles from 1682, Hall of Mirrors finished 1684 (Hall of Mirrors pages) | VERIFIED (setting date consistent) |
| C02 voice + plate | "A hundred people watch me wake up" / LE LEVER (THE RISING): UP TO ~100 PEOPLE | chateauversailles.fr "A day in the life of Louis XIV": about 100 spectators at the getting-up, all men | VERIFIED (the plate says "up to ~"; the king's line is his round number) |
| C03 voice + plate | doctor and surgeon in the room before he got up | chateauversailles.fr (First Doctor and First Surgeon come first); Wikipedia "Levee (ceremony)" (chief physician, chief surgeon and nurse enter together) | VERIFIED |
| C04 voice + plate | hair loss from ~17 (about 1655), then wigs | popular histories agree on age 17 / 1650s, one gives 1655 (bookophile, historyfacts, mentalfloss); no primary source opened | PARTLY (hedged with "~" and "about") |
| C05 voice + plate | "They say it makes me taller" / TALL WIGS ADDED HEIGHT | sources agree heels and wigs added height; the motive (to look taller) is disputed (Getty Iris) | VERIFIED for the plate (no motive claimed); the line is hedged "they say" |
| C06 voice | white powdered wig, "one day everybody will wear this, I'm just early" | joke [comedy]: white powdered wigs became general in the 18th century | COMEDY, an intended anachronism: the king wears a tall white wig from C07 on. Say it in the description |
| C07 plate | was "THE COURT ENTERED IN ORDER OF RANK" | Wikipedia "Levee": successive entrées by privilege (grande entrée, première entrée, chambre, later ladies, children), not by rank as such | FIXED: now "COURTIERS CAME IN / BY ORDER OF PRIVILEGE" |
| C08 voice | "nobody may speak before me" | comedy line on etiquette, no plate | COMEDY (not a fact claim) |
| C10 voice + plate | red heels for favoured nobles / RED HEELS: A COURT PRIVILEGE, 1670s | Bard Graduate Center article, Barringer (citing Mansel), popular articles; no primary text of a decree | PARTLY ("1670s", not a year; no decree claimed) |
| C11 plate | AT 14 HE DANCED THE SUN GOD APOLLO (1653) | Wikipedia "Ballet Royal de la Nuit": 23 Feb 1653, he danced Apollo / the rising sun; born Sept 1638 = 14 (some pages say 15 by rounding) | VERIFIED |
| C12 voice + plate | Venice kept the mirror secret, France got their glassmakers / HALL OF MIRRORS: 357 MIRRORS · 1678–1684 | destination-yvelines (357 mirrors, 17 arches), Wikipedia Hall of Mirrors (1678–1684), several sources on Colbert recruiting Venetian glassmakers, some in secret; the Venetian poisoning story is a legend and is NOT used | VERIFIED |
| C14 voice + plate | "Next time, I dine in public" / NEXT: DINNER, IN PUBLIC | chateauversailles.fr: courtiers watched the royal meals (dinner at the Royal Table) | VERIFIED (a tease, no detail claimed) |
| End card | THE SUN IS NEVER LATE. | catchphrase | COMEDY |

## 2. Footage
No real footage. Every picture is AI-generated (see 3). The places are recognisable Versailles rooms re-imagined by the models: state bedchamber with painted ceiling, a dressing table, the gallery, the Hall of Mirrors. AI inventions noted: the bedchamber and ceiling are not copies of the real Salon de Mercure; ladies stand among the courtiers at the start of the lever in C07 (historically ladies came in only at a late entrée); modern-looking bystanders are NOT in this cut (the Seedance 2.0 test take with them was not used). Acceptable for a labelled comedy reconstruction.

## 3. AI content
- Video: Kling 4.0 i2v (C01), Seedance 2.5 Lite i2v (C02-C05 remakes), Seedance 2.5 (C06-C08), Seedance 2.5 Lite r2v (C09, C10, C12-C15); stills B1-B8 (burst) AI images; first frames and character cards AI images.
- Voice: ElevenLabs v4 "The Young Heir" via Lumean (C01-C08: our TTS laid on the lips); C09-C15: the video model's own speech made from that voice as reference audio (trial v4).
- Sounds: real recordings (BigSoundBank) + the video models' own non-speech sounds. Music: none.
- Disclosure: the owner removed the persistent corner mark (31.10). What stays: the end card line "AI-generated comedy reconstruction" (on screen 131.6-133.5 s), the description, the YouTube altered/synthetic content flag and the TikTok AI-generated label at upload. AI is never presented as real footage or as a real event. PARTLY: no label DURING the shots (owner's decision, recorded in `louis_series_bible.md`); compliant with YouTube's rule once the flag is set.

## 4. People, faces, logos
Louis XIV is a historical public figure (died 1715), shown as comedy; no living person is depicted on purpose. The king's face is our generated face master; I cannot prove it does not resemble a living actor (NOT VERIFIED, low risk). Courtiers are generated. No logos, brands or readable modern text seen on the stills.

## 5. Music and sound
- BigSoundBank (Joseph Sardin), "Royalty-Free Sound License (CC0-like)", commercial use without attribution, licence page checked 30.10 (`../sfx/SOURCES.md`): beds 3431, 2855, 3433 (two regions), foley 0013, 1104, 2016-2019, 0087, 3211, 0376, 3053, 3060. Recording 3432 was tried for the gallery and dropped (steady 1050/1570 Hz tones, possibly music).
- Model sounds: own generations; steady tones in them notched out (C01, C02, C03, C04 223 Hz, C05, C15).
- Music test on the final mix: strongest persistent peaks above 400 Hz in 1.9 % of frames; 210-230 Hz in 7 % = the voice's harmonics in speech frames, 4.5 % in quiet frames. No melody found. Ear check NOT VERIFIED by me. VERIFIED (by measurement).
- Voice licence chain: PARTLY / OPEN. ElevenLabs Terms (1(c)(ii)) allow commercial use on paid plans; we buy through Lumean (reseller): Lumean's own commercial terms NOT read. ElevenLabs Use Policy s.12 forbids using Output "to develop, train, fine-tune, or improve any AI model or service"; s.3 restricts cloning the voice of a living individual without consent. Feeding our ElevenLabs output to Seedance as reference audio is not training, but the model then speaks in a voice close to the library voice's creator outside ElevenLabs (C09-C15, similarity 0.68-0.88): a real risk for a monetised channel. The Voice Library Addendum (elevenlabs.io/vla) was found but not read in full.

## 6. Imagery and data
No maps, satellite imagery, stock photos or third-party pictures. Fonts: Liberation Serif (SIL OFL), DejaVu Sans (free licence). VERIFIED.

## 7. Platform policy
- YouTube: original script, character and edit (own plates, own sound design), not reused content. Realistic AI depiction of a real historical figure and a real place: the altered/synthetic disclosure is REQUIRED at upload. Not made for kids. Series template: vary setting and hook every episode (inauthentic-content policy).
- TikTok: AIGC label ON at upload; original content.
- Monetisation risk MODERATE (AI-heavy; voice licence chain open; YPP reviewers look for original value: we have it). Removal risk LOW.

## 8. Metadata and flags
NOT DONE: no publication package and no channel account yet (Zernio has only Mr. Buck, which must not get this video). Before any upload: title, description (comedy reconstruction, AI visuals and voice, invented dialogue, the white-wig joke, facts with sources), YouTube altered/synthetic flag ON, TikTok AIGC ON, made-for-kids NO; read the post back after scheduling.

## 9. Technical honesty
Duration 2:13.5 (Shorts limit 3:00), 9:16, English speech, no burned-in captions (by design). blackdetect/freezedetect: only the planned end card (131.46-133.42 s black with text); no other freeze >= 1 s. Loudness -15.2 LUFS, per clip -17.4...-17.9 LUFS, burst -27.8. All lines complete by ASR.

## Verdict
FIXED: the C07 plate overstated the order of entry and was reworded; the gallery bed with tonal content was replaced; tones in the model sounds were notched; the file was re-rendered (cut C) and re-checked (frames, loudness, length).
NOT yet cleared for upload: item 8 (package and flags) and the voice licence item in 5.

## Open items (owner)
1. Voice licence: (a) read Lumean's commercial terms; (b) decide on the model voice of C09-C15 (ElevenLabs Use Policy risk) vs laying our ElevenLabs voice over the picture as in C01 (owner rejected word-sliced comps, phrase-level laying works: C01 lips 0.68).
2. Two plates rest on popular sources only (hair loss ~17, red heels 1670s): keep hedged as now, or drop.
3. Package + channel account, flags at upload.

## Sources (opened or searched 31.10.2026)
- https://en.chateauversailles.fr/discover/history/key-dates/day-life-louis-xiv
- https://en.wikipedia.org/wiki/Levee_(ceremony)
- https://en.wikipedia.org/wiki/Ballet_Royal_de_la_Nuit
- https://destination-yvelines.fr/en/castles/the-hall-of-mirrors ; https://www.wikiwand.com/en/articles/Hall_of_Mirrors
- https://bookophile.com/en/worlds-of-books/articles/a-venereal-disease-determines-a-fashion-trend ; https://mentalfloss.com/article/31056/why-did-people-wear-powdered-wigs ; https://historyfacts.com/?p=8253
- https://www.bgc.bard.edu/research/articles/557/nicole-dee-collins-souvenir-louis ; https://psource.sitehost.iu.edu/PDF/Archive%20Articles/Spring2014/2014%20-%20Spring%20-%204%20-%20Barringer%20Sarah.pdf ; https://blogs.getty.edu/iris/?p=23772
- https://elevenlabs.io/terms-of-use ; https://elevenlabs.io/use-policy ; https://elevenlabs.io/vla (found, not read in full)
- https://bigsoundbank.com/droit.html (checked 30.10)

## Re-render 31.10: cut D (frames/EP1_full_D.mp4, 129.50 s, 265 MB)
Changed: silent heads trimmed, darker grade, texture, bed levels (compare_ep1_full_vs_reference.md). Re-run checks: all lines complete by ASR (check_ep1.py), plates present and timed on frames, blackdetect/freezedetect only the planned end card (127.50-129.46 s), -15.1 LUFS, TP -0.9 dBFS, no music by the tone test. Claims, AI list, people, licences unchanged. Verdict unchanged: FIXED; upload still waits for item 8 and the voice licence item.

## Voice licence, update 31.10 (Lumean terms read)
Lumean user agreement (https://lumean.app/terms): s.8.2 a simple non-exclusive irrevocable licence to use results "в личных и коммерческих целях на территории всех стран мира"; s.8.3 the user's rights may be limited by the terms of the third-party service; s.6.2.1 and s.8.4 ban imitating a real person's voice without explicit consent (public figures included); s.5.12 catalogue voices are given as published by the provider. Public offer (https://lumean.app/offer) has no clause on rights to results.
Result: our ElevenLabs/Lumean TTS lines (C01-C08) are licensed for commercial use: VERIFIED (subject to ElevenLabs' paid-plan terms on Lumean's side). The model voice of C09-C15 (Seedance re-creating the library voice from our TTS as reference audio) is the open risk (Lumean s.8.4 / ElevenLabs Use Policy s.3, s.12). Free fix available: lay our existing TTS lines (tts_ep1/C09, C10, C12-C15 mp3, no new orders) over C09-C15 by whole phrases, the C01 method (lips corr 0.68 vs the model's own 0.71). Owner's decision (the owner preferred the model voice in C09 on 30.10).

## Re-render 31.10: cut E (frames/EP1_full_E.mp4, 129.50 s, 265 MB): the voice licence item CLOSED
Owner 31.10 "Проверяй и дальше поехали" (after the recommendation): C09, C10, C12-C15 now carry OUR licensed v3 TTS (voice/tts_ep1/<clip>.mp3, Lumean s.8.2 commercial licence), laid by whole phrases on the model's phrase starts (build_r2v_ourvoice.py; no new voice orders). The model's own speech is no longer in the episode (its non-speech sounds stay). C13: the courtier's extra "...your majesty" was part of the model's vocals and is gone with them.
Re-run checks: every line complete by ASR; speaker similarity to our v3 take C09 0.82, C10 0.95, C12 0.87, C13 0.85, C14 0.86, C15 0.89 (was 0.68-0.80), neighbours 0.78-0.92; lips (our voice vs the model's mouth, lag 0): C09 0.59, C10 0.49, C12 0.47, C13 0.53, C14 0.58, C15 0.38 (the model's own voice: 0.51, 0.44, 0.46, 0.67, 0.54, 0.31); click test identical to cut D (the 13 candidates are the planned phone knocks and the hat drop); blackdetect/freezedetect only the end card; -15.0 LUFS, TP -0.9 dBFS; no music by the tone test.
Verdict: FIXED; items 3-7 and the voice licence pass. Upload still waits only for item 8 (channel account, flags at upload).
