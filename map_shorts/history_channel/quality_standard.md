# Quality standard of the history channel (owner 29.10: "check everything; video quality the highest")
## Production ladder (highest tier that the catalogue offers, by cost)
| Stage | Standard | Prices (APIpod, 29.10) |
|--|--|--|
| Start frames | Nano Banana 2.1 at 2K (not 1K) for every clip start frame and burst still | 2K about $0.04 each (1K was $0.02; 22 frames = about $0.88; not run yet) |
| Dialogue clips | kling-4.0-r2v, 1080p, character element + the locked voice reference | $0.2125/s basic at 1080p = about $1.70 per 8 s (720p $0.1428/s = $1.14) |
| Alternative tiers to test on C01 | veo3-1-quality 1080p $1.00 per 8 s, veo3-1-quality-4k $1.20; seedance-2.0 1080p $0.315/s = $2.52 per 8 s, 4k $0.7245/s | no voice reference on Veo; Seedance audio_urls untested |
| Voice | ElevenLabs v4 "The Young Heir" with a French accent (voice_lock v3: tag + TTS-only respelling) and emotion tags, stability 0.5, tested on C01-C05 | about $0.0005 per clip line |
| Edit | master 1080x1920, 30 fps, our own chip layer (not AI text), no burned-in captions (owner 29.10), SRT for the platform only, AI mark, x264 CRF 14-16 (no re-encode loss), AAC 192k, -14 LUFS, true peak <= -1.5 dBFS, premium_gate.py report | free |
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

## Phone-realism checks (owner 29.10: "the camera first looks at the ceiling like the reference, realistic phone shake and lowering")
For every phone-handled shot, from the contact sheet and motion curve: (1) C01 holds on the ceiling at least 1.2 s before the tilt, and NO word is spoken before the tilt has landed on his face (owner 29.10); (2) the tilt is ONE continuous move, no cut, 1-2 s long; (3) shake is small and irregular (1-2 % of the frame, no rhythmic wobble, no jelly frames beyond a hint of rolling shutter); (4) exposure and focus react to the move (bright ceiling to warm bed, a short focus hunt); (5) the landing has a small overshoot and settle; (6) no phone UI, no modern objects, no fingers of the king where his hands are visible in the frame; (7) the end frame of C01 matches the start of C02 (propped, static).

## Camera-flight rule (owner 29.10: "everything realistic, the camera must not fly")
A phone-handled shot is a ROTATION (tilt, pan, roll) plus small shake, never a dolly or zoom unless the script says the page walks. Before generating a clip between two frames, both frames must share the same camera position (compare the scale of fixed objects: canopy, window, bed head). After generating: run `louis_ep1/phone_move_check.py <clip>` (a flag is a reason to look, not a verdict: a big pitch with an ultra-wide lens also changes the apparent scale) AND measure the subject's width (wig/face) in 4 frames next to the target frame; more than +/-10 % growth = FLY = reject; the subject's apparent size stays within +/-10 % except in a walk shot. Never write "acceptable" for a flying camera.

## No-music gate (owner 29.10)
The final mix contains no music. Check: every clip's generated audio track is muted in the edit (stream map shows only our voice and foley stems); a spectral listen of the final file for tonal/rhythmic content outside the voice; the authenticity audit states "music: none".

## Reference-manner gates (owner 29.10: "делай как референс"), measured on every clip and on the cut
| Gate | Pass |
|--|--|
| Camera moves | global camera path > 0 px over the clip (hand-held drift visible) and scale change < 12 % (no flight); a fully locked clip only if it is THE one contrast shot of the episode |
| Calm motion | mean frame difference 2-4 per second in talking stretches; under 1.0 for more than 2 s = FAIL (reads frozen) |
| Phone mistakes | at least 1 per take |
| Sound bed | no gap of 1 s or more below -50 dB in the final mix; LRA 8-12 LU (reference 11.1) |
| Framing | the face fills at least about 1/4 of the frame width in talking shots (wide-lens close-up), except planned wides |
| Cuts | no jump cut inside a setup; hard cuts between setups allowed |

## Clumsy-camera gate (owner 29.10)
Per episode: at least 2 and at most 4 deliberate bad-framing moments (face cut by the edge, too close, tilted, object in the lens); first frames for hard cuts may start badly framed; every such moment is motivated by his hand (no teleporting camera) and never hides a key fact chip or the CTA.
