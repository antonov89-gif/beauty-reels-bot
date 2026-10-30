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

## Lip sync to OUR voice (29.10, C01)
- Kling 4.0 i2v speaks its own faster line: phrase starts match, words inside phrases are 0.4-0.9 s early vs our drawled voice -> FAIL with our voice laid over.
- Owner 29.10: Wan is NOT acceptable for video quality (wan2.7-i2v has `audio_url`, rejected).
- Candidates that take our audio: (1) APIpod seedance-2.0-r2v: `image_urls` + `audio_urls` references (no first-frame role in the spec; lip sync to a given audio undocumented), 720p $0.126/s, 1080p $0.315/s; (2) Higgsfield Seedance 2.0: start_image + end_image + audio_references roles (first-frame control), needs a credit top-up (balance 0.1, plan pro); (3) a dedicated lip-sync model on the Kling clip (not in APIpod or the first Higgsfield results); (4) re-voicing our line at the model's pace = x1.6-2.4 faster, rejected (kills the drawl).

## Seedance 2.5 (owner 29.10: "take Seedance 2.5, first the draft")
seedance-2.5-draft (APIpod spec): stage 1 = 480p draft (any prompt/images/audio, 4-30 s), stage 2 = same task rendered at 1080p with `draft_task_id` (reuses prompt, media, duration, seed). Estimator (4-s unit): draft $0.392, 2.5 r2v / i2v 720p $0.882 (= $0.2205/s). Draft 12 s about $1.18 (estimate), final 1080p price NOT VERIFIED. Caveat in the spec: 1-2 images WITHOUT other media = first/last frames; with audio they are references (so the ceiling is a reference, not a guaranteed first frame). i2v 2.5 has first/last frame but no audio input.

## 4K upscale check (owner asked 29.10: "Апскейл")
- Seedance 2.5 (APIpod): max 1080p, the draft cannot be finalised in 4K (apipod.ai/models/seedance-2.5). 4K exists only as generation in other models (Seedance 2.0 std, Kling 3.0 Omni 4k mode on Higgsfield), i.e. a re-generation, not an upscale.
- APIpod: no dedicated upscale/Topaz model found on apipod.ai/models.
- Higgsfield upscale_video (ByteDance preset "aigc" 4k, or Topaz 2160p): available, but no cost preflight and the balance is 0.1 credits; price per second NOT VERIFIED.
- Third-party Topaz video upscale list prices seen: Evolink $0.055-0.088/s (4x = $0.088/s), Apiframe $0.02/s for 1080p. No account here.
- YouTube Shorts: a secondary source (Hopper HQ) says Shorts accept 4K uploads but are served at max 1080p; NOT VERIFIED on YouTube Help.
Decision pending with the owner.

## Seedance 2.5 draft route: final only in 1080p (verified 29.10 on the API)
The final step from a draft_task_id answers 400 "supports only 1080p resolution" for 720p (rejected at validation, no charge). So the draft route costs draft 0.098 $/s + final 0.542 $/s (about $5.2 per 8 s with the final at 1080p); the direct i2v route offers 720p at 0.2205 $/s (about $1.76 per 8 s) but does NOT keep the exact first frame (C05, C08 jumped). Use the draft route for continuations (no visible cut), the direct 720p route only for planned hard cuts.

## Model ratings after the C01-C08 work (30.10, 0-5, mine, subjective; measured facts in reference_check.md)
| Model | Face/texture | Lips on OUR voice | Phone camera | Keeps first frame | Own sound | Price | Verdict |
|--|--|--|--|--|--|--|--|
| Seedance 2.5 draft -> 1080p | 4 | 4 | 3 | exact | almost none (no sound asked) | about $5.1 / 8 s | for hidden joins (C01-C03, C06, C08) |
| Seedance 2.5 direct 720p | 4 | 4 | 3 | NO (jumps in C05, C08) | same | $1.76 / 8 s | hard cuts only (C07) |
| Seedance 2.5 LITE i2v 720p | 4.5 (texture 1969 vs 645-1594, grain 3.0) | 4 (0.06-0.12 s after phrase-level alignment) | 4 | close, not exact (diff 7.2) | yes, room and knocks when asked | $1.35 / 9 s (pilot C04, actual) | best value; only C04 tested |
| Kling 4.0 i2v 1080p | 3.5 | 2 (own faster line, words 0.4-0.9 s early) | 3 | yes | own voice | about $2 / 9 s | rejected for dialogue |
| Kling 4.0 r2v | n/a | rejects our voice reference (3 of 3) | - | no | - | about $1.14 / 8 s | rejected |
| Veo 3.1 | 3 | not tested | 3 | no | - | $1 / 8 s | fallback only |
| Wan 2.7 | - | - | - | - | - | - | rejected by the owner |
Plan: Lite where the join may be a cut (C04, C05, C07, C09+), the draft route only where the join must be invisible (C02, C03); every prompt carries a SOUND block; the model's speech is removed with htdemucs (free) and its sounds kept.

## Our voice as INPUT (30.10, owner: "Можно ли сразу в генерацию засунуть нашу озвучку")
- APIpod Seedance 2.5 Lite Reference-to-Video (`seedance-2.5-lite-r2v`, docs.apipod.ai/seedance/2-5-lite-reference-to-video): `audio_urls` up to 10 reference audios, 2-30 s each, total <= 30 s, must come with at least one reference image or video; up to 30 images; 4-30 s; 720p only. APIpod estimate 30.10: $0.60 per 4 s = the same $0.15/s as Lite i2v (8 s = $1.20); the charge with audio input NOT VERIFIED.
- Lite i2v (`seedance-2.5-lite-i2v`) has first/last frame but NO audio input. In r2v the image is a reference, not an exact first frame (fine for hard cuts, not for invisible joins).
- Lip sync to the given audio is not documented for the route: to be proven on C09 (seedance25lite_c09_r2v.py, reference audio voice/tts_ep1/C09_ref8s.wav). If it works, it replaces the cut-and-fit method for all dialogue clips (no stretching of our voice afterwards).
- Same idea elsewhere: Seedance 2.5 r2v (non-Lite) $0.882 per 4 s = $0.22/s; Seedance 2.0 r2v $0.63 per 4 s; Higgsfield Seedance 2.0 with start frame + audio roles (MCP answered 423 / balance error 30.10: not usable now). Kling 4.0 r2v voice reference rejected our voice 29.10.
- RESULT 30.10 (C09): seedance-2.5-lite-r2v with our voice in `audio_urls` does NOT lip-sync to it: the model speaks the line again on its own timing in a voice that is only closer to ours (speaker similarity 0.77-0.79 vs 0.90 between our own takes), and the lips follow its own audio. Use the reference audio route for voice colour only. True lip sync to OUR voice needs a dedicated lip-sync (video + audio -> mouth redrawn) model, not in the APIpod catalogue.

## seeddance.io (SeedVideo AI) pricing and the "Halloween unlimited" offer (page read 30.10.2026, owner asked: is it worth it, how many generations per day)
Who: a third-party aggregator of Seedance, Veo, Kling, Wan ("SeedVideo AI", seeddance.io; not ByteDance). Price table from the page (annual-billed rate / monthly rate): Lite $13 / $14.9 (100 credits), Pro $14.5 / $29 (200 credits), Premium $99 / $149 (1,300 credits); credits valid 30 days. "Videos" on the page are counted as 5-s videos (page text: "about N 5s Seedance 2.0 videos"); Seedance 2.5 on Premium: about 185 videos per month = $0.54 each at the annual rate, $0.805 at the monthly $149.
The offer: "7 days of unlimited Seedance" (2.5 and 2.0 family, up to 1080P, up to 10 s per video, 8 parallel) is included ONLY in Premium; Pro and Lite: "not included" for video (Pro gets 365-day unlimited images: Nano Banana 2.1, GPT Image, Seedream). Until 1 Nov per the page (the countdown showed about 1 day 3 h when read). Refund: 3 days if no credit used; NO refund once even one video was made in the unlimited mode. Russian-card / SBP / YuMoney / USDT payments are one-off for the period, no auto-renewal. Monthly Lite has no commercial-use right; Pro and Premium do.
Math (our Lite price at APIpod $0.15 per second = $1.20 per 8-s clip; an episode = 14 clips x 1.3 re-rolls = 18 generations, about $23):
- Unlimited week alone: $149 / $1.20 = 124 generations of 8 s in 7 days = 18 per day = about 7 episodes' worth of generations (one episode every day).
- Realistic pace (the limit is checking and scripts, not generation): 4 per day = $34 of APIpod value, 8 per day = $67 (about 3 episodes in the week), 12 per day = $101. Below $149 at any realistic pace.
- Premium credits themselves at the monthly price: $0.161 per second of Seedance 2.5 = the same as APIpod Lite ($0.15). Only the annual-billed rates are cheaper ($0.107 per second Premium, 29 % below APIpod; Pro $0.116 per second but only about 125 s per month), and they need $1,188 or $174 up front.
- Total value of Premium for 30 days = the unlimited week plus 925 s of credits (about $139 at APIpod prices): break-even about 6.5 episodes in 30 days at $149; our plan of 2-3 episodes per week is 8.6-12.9 episodes (APIpod $197-296 per month), but the unlimited part exists only in this promo week.
Unknown / to test before paying: whether this route takes reference audio (r2v) at all; that its "Seedance 2.5" is the model we use through APIpod; 1080P quality; the commercial-use and refund terms in practice.
