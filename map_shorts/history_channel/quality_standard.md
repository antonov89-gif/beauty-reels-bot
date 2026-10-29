# Quality standard of the history channel (owner 29.10: "check everything; video quality the highest")
## Production ladder (highest tier that the catalogue offers, by cost)
| Stage | Standard | Prices (APIpod, 29.10) |
|--|--|--|
| Start frames | Nano Banana 2.1 at 2K (not 1K) for every clip start frame and burst still | 2K about $0.04 each (1K was $0.02; 22 frames = about $0.88; not run yet) |
| Dialogue clips | kling-4.0-r2v, 1080p, character element + the locked voice reference | $0.2125/s basic at 1080p = about $1.70 per 8 s (720p $0.1428/s = $1.14) |
| Alternative tiers to test on C01 | veo3-1-quality 1080p $1.00 per 8 s, veo3-1-quality-4k $1.20; seedance-2.0 1080p $0.315/s = $2.52 per 8 s, 4k $0.7245/s | no voice reference on Veo; Seedance audio_urls untested |
| Voice | ElevenLabs v4 "The Young Heir" with a French accent (voice_lock v3: tag + TTS-only respelling) and emotion tags, stability 0.5, tested on C01-C05 | about $0.0005 per clip line |
| Edit | master 1080x1920, 30 fps, our own caption/chip layer (not AI text), AI mark, x264 CRF 14-16 (no re-encode loss), AAC 192k, -14 LUFS, true peak <= -1.5 dBFS, premium_gate.py report | free |
| Gates | frame check -> clip check at full resolution -> sequence check -> authenticity audit -> owner approval | no automatic approvals |

## Per-clip checklist (every generated clip, frames inspected at full resolution, not thumbnails)
1. Identity: same face, patch, moustache, wig as the lock (A3_white_wig.jpg / D2 for the night wig).
2. Hands: count per frame, each hand with an arm, no fused or extra fingers, rings stay on the same fingers.
3. Props: the mirror, hat, wigs, heel keep shape; no floating parts; the cutter-style touch rule (the tool touches what it acts on).
4. Emotion: the face shows the named emotion of the line (emotion_map.md), not a blank talking head.
5. Mouth: lip sync to the line at 0.25-s steps on the first 3 s and the last 3 s; no teeth/lips melting.
6. Voice: the locked voice (compared with heir_eleven_v4.mp3), no accent or timbre drift between clips; speech detector + transcription match the script.
7. Background: no modern clothes, roofs, lamps, signs; background people in period dress; no AI text garble (text only as our overlay).
8. Camera: the planned move happens (tilt, roll, push, rack focus), the phone-mistake intrusion is present where planned.
9. Seams: chained clips match framing, light and wig state; no black or frozen frames.
10. Audio: no clipping, room tone consistent, loudness in range.
Status words stay GENERATED != INSPECTED != APPROVED; anything not verified is NOT VERIFIED.

## Change 29.10.2026 (owner): the outro laugh
The laugh now comes AFTER "do what you like" and is cold, arrogant, haughty (chin up, looks down the nose, eyes half-closed). Updated in the series bible, script, emotion map, tagged lines, recording sheet and the C15 frame prompt. The current C15 storyboard frame still shows a warm smile (old prompt): it is regenerated in the 2K pass (about $0.04, inside the $0.88) and inspected before approval. The emotion voice test must check that the laugh sounds haughty, not friendly.

## Change 29.10.2026 (owner): self-praise once per video
"What a handsome man I am" is said ONCE per video, in the opener (C01). The other direct-praise lines were rewritten into situational jokes (C03, C05, C07, C08, C10, C12, C13). Start frame C13 changes from "swooning at the mirror" to "icy glare and a hand waving the courtier away": regenerated in the 2K pass (about $0.04, inside the $0.88) with the new prompt in frames_louis.py. The other frames still fit.
