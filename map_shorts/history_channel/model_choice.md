# Model choice for the Louis XIV vlog (APIpod catalogue read 28.10.2026)
Sources: apipod.ai/pricing (prices per request/second, partly hidden tiers), docs.apipod.ai OpenAPI pages for seedance-2.0-r2v, kling-4.0-r2v, seedance-2.5-i2v. The catalogue has NO dedicated lip-sync / talking-avatar model and no Hailuo; Sora 2 and Wan exist.
Need: photoreal documentary-vlog i2v from our start frames, ONE fixed voice on every video (owner rule), identity stable across 14 clips, 8-s-friendly, as cheap as possible.

## Candidates (720p, price per 8 s clip)
| Model | Price | Fit for our need | Status |
|--|--|--|--|
| **kling-4.0-r2v** | $0.1428/s = **$1.14** per 8 s (lower rate "audio/video input" $0.085/s = $0.68, applies when video/audio is input; not known for voice refs) | Documented fields: `kling_elements` (2-4 images of the character = face lock), `voices` (a public audio URL per voice, referenced as @name in the prompt = the fixed voice), 3-30 s per generation (a whole 24-s take in one clip), native audio. ONLY model in the catalogue with a voice reference. | Lip-sync and how close the voice stays to the reference: UNKNOWN until a test |
| veo3-1-fast (i2v) / veo3-1-fast-ref | $0.18 per 8 s | Cheapest good photoreal i2v, 8 s fixed, proven in our pipeline. Own speech, no voice reference: the voice drifts between clips, would need speech-to-speech conversion (tool not in APIpod) | Fine for silent inserts and as the cheap fallback |
| seedance-2.0-r2v / i2v | $0.126/s = $1.01 | `audio_urls` reference audio (needs an image/video reference); voice/lip-sync behaviour NOT documented; 4-15 s | Second candidate to test |
| seedance-2.5-i2v | $0.2205/s = $1.76 | 4-30 s, no audio input | Too expensive, no voice control |
| kling-3.0 i2v/omni | ~$0.12/s with audio = $0.96 | native audio, no voice reference documented | Skip |
| gemini-omni-flash-1.1 | $0.06/s = $0.48 | cheap, behaviour unknown | Skip until needed |
| grok-imagine, wan3.0 | $0.036-0.09/s | cheap, weaker realism for faces | Inserts only |
| motion-control-m1 / kling-2.6 motion control | $1/request / $0.07-0.105/s | transfers motion from a reference video; no speech | Not for dialogue |

## Recommendation
1. Dialogue shots: **Kling 4.0 r2v** with the character element (A3_white_wig.jpg + 2-3 storyboard frames) and the fixed voice sample as `voices`. It is the only way in this catalogue to keep ONE voice by design.
2. Silent inserts (heel macro, burst stills with Ken-Burns): our frames and ffmpeg, or Veo 3.1 fast at $0.18.
3. Fallback if Kling's voice drifts or lip-sync is poor: Seedance 2.0 r2v with `audio_urls` (test), then Veo 3.1 fast + speech-to-speech conversion.
4. Economics: 2:00 episode on Kling r2v = 14 x $1.14 = $16 raw (about $27 with rerolls) against $2.5 on Veo fast. The forecast says a mid-case Short earns tens of dollars a month: so keep early episodes SHORT (60 s, about $8.6 raw) or use Kling only for the talking close-ups and Veo/stills for the rest, and measure views first (gate: median of 10 Shorts).

## Test plan (cheap, before any batch)
1. Voice: audition 6 voices (1.38 RUB) -> owner picks -> a 10-s sample line in that voice (about 0.23 RUB) as the voice reference.
2. One 8-s test clip of C01 on Kling 4.0 r2v: about $1.14 (price of the voice-input rate to confirm from the first charge). Check: face vs the card, mouth sync, voice vs the sample, hands, no modern items. Max 2 corrective attempts.
3. In parallel the same C01 on Veo 3.1 fast ($0.18) for the price/quality comparison.
4. Decide the model per shot type, then the pilot C01-C04.
Nothing in this plan has been started or paid.

## Test findings 29.10 (C01)
- kling-4.0-r2v: the voice reference (`voices`) rejected our locked voice 3 times ("Not enough speech in the voice audio"), with 12.8 s, 23.7 s continuous mp3 and the same as WAV. The fixed-voice-by-reference route does not work for this voice. Its `image_urls` are reference images, NOT a first frame (official spec).
- Next route: kling-4.0-i2v (first frame + keyframes + last frame, 3-30 s; prompt mentions @first_frame/@keyframe_N/@last_frame) for the camera and identity, model's own speech for lip movement, then our locked TTS laid over in the edit; or seedance-2.0-r2v with our audio in `audio_urls` (lip-sync to a given audio undocumented).
