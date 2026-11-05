# MODEL_NOTES: image and video models we can reach (history channel, Louis XIV)
Written 05.11.2026 by the model-economist. Read-only survey: no generation, no submit, no spend. Update this file after every new fact (date + source).

## Кратко по-русски (для владельца)
- **Платить сейчас приходится только через APIpod.** Higgsfield MCP недоступен (ошибка 423, баланс не читается). Picaso: триал не активен, бесплатной генерации через MCP НЕТ. Unify: баланс 10 кредитов (хватает максимум на одну картинку Seedream); vidIQ: 226 кредитов (для генерации видео не проверялось). Бесплатных квот, которыми можно заменить платные вызовы, у нас нет.
- **Наше измерено:** Kling 4.0 i2v 720p = $0.145/с ($1.16 за 8 с, $1.74 за 12 с, $2.18 за 15 с), лицо держится с двумя пинами; GPT Image 2.5 Sunburst Lite 4K = $0.12 за картинку, но бывают сбои SUBMISSION_UNCERTAIN.
- **Что дешевле на бумаге (по прайсу APIpod на 05.11, качество у нас НЕ проверено):** Kling 3.0 i2v 720p без звука $0.08/с (первый+последний кадр) = $0.64 за 8 с; Gemini Omni Flash 1.1 i2v $0.06/с (первый+последний кадр) = $0.48 за 8 с; MiniMax H3 768P $0.09/с; Muse Video 10 с = $0.20 за запрос; Veo 3.1 Lite $0.08 за запрос. Ни одна из них не проверена на лицо и ручную камеру: только дешёвые пилоты по твоему "да".
- **Главная экономия:** не цена за секунду, а меньше повторов. В ledger эп.2 примерно $12-15 из $35 ушло на ретейки (T1 x4, кусок 2 x2, т.д.); промпт с покадровой картой движения и пинами уже снижает это.
- Длина клипа: речь около 0.55 с на слово (110 слов/мин) плюс паузы; в среднем с паузами 0.67 с/слово (90 слов/мин). Таблица в разделе (e).

---

## 0. Status of the survey (what was reachable 05.11.2026)
| Source | Result | Date |
|--|--|--|
| APIpod pricing page (apipod.ai/pricing, first 100k of 275k chars read) | full price list for image and video models; "+N more" hidden variants listed as such | 05.11 |
| APIpod OpenAPI specs (docs.apipod.ai/api-reference/openapi/*.yaml) | read: gemini-omni-flash-1.1-i2v, seedance-2.0-lite-i2v, seedance-2.0-i2v, minimax-h3-i2v, kling-3.0-i2v, veo3-1-lite, muse-video-i2v. Earlier (04.11): kling-4.0-i2v | 05.11 |
| Higgsfield MCP (models_explore, balance) | FAILED: HTTP 423 on workspaces; show_plans_and_credits returned no plans, no links. Higgsfield = NOT CHECKED, unusable now (same 423 on 30.10) | 05.11 |
| Picaso MCP (list_models, get_account) | plan "Free trial", active=false, generation_included=false. All 4 models (PicassoIA Image, Image Editor Pro, PicassoIA Video, Seedance 2.5 Lite) `available:false`: "free on Infinite and Wonder plans" only. NOTHING free for this account | 05.11 |
| Unify MCP (balance, list models, free quotes) | balance 10 credits; quotes below | 05.11 |
| vidIQ MCP vidiq_balance | 226 credits (106 renewable of 150, +120 add-on; renews 02.12.2026). vidiq_generate_video exists but its model, price and input options were NOT CHECKED (a tool call would risk spend) | 05.11 |
| Veo Quality access of the owner | not visible in any tool reachable here: NOT CHECKED | 05.11 |
| Web search (Veo, Kling, Seedance, Runway, Luma prices) | third-party blogs only, conflicting; no vendor price sheets reached. Treat as hypotheses | 05.11 |

## 1. APIpod (our paid provider; key at /home/claude/.apipod_key, never printed)
Endpoint pattern: POST /v1/videos/generations, status GET /v1/videos/status/{id}; images /v1/images/generations. Note (ledger 30.10): `/v1/pricing/estimate` ignores duration and resolution, so real prices are the charged `usage.cost` values.

### 1.1 Video models: provider claims (price page 05.11 + OpenAPI), then OUR results
Prices are USD from apipod.ai/pricing read 05.11 unless said otherwise. "2-pin" = accepts first AND last frame.

| Model | Inputs (spec) | Duration / res (spec) | Price (claim) | Our measurement | Notes for us |
|--|--|--|--|--|--|
| **kling-4.0-i2v** | first frame (`image_urls[0]`, needs `@first_frame` in prompt), optional last (`image_urls[1]`), up to 8 `keyframe_urls` (`@keyframe_N`); no audio input; own native audio | 3-30 s; 720p / 1080p; duration >= 9 s caps frames at 10 total | 720p $0.145/s, 1080p $0.2175/s | **MEASURED**: charged $1.16/8 s, $1.45/10 s, $1.74/12 s, $2.175/15 s (720p); 1080p $0.6525 for 3 s (29.10). Face SFace to card 0.74-0.79 median with two pins and keyframes; WITHOUT an anchor 0.33-0.35 (fail); chain from last frames decays (-0.05..-0.08 per link, sharpness -80 % over 3 links). Sharpness drop 0 to -27 % per clip with pins (ok). Motion calm after ~5 s unless the prompt has a per-beat camera score (T3a/T2c still body 60-75 %); lips on its own faster voice (words 0.4-0.9 s early) so we lay our TTS over | current workhorse, best picture so far; best use: 2 pins + 1-3 keyframes, 8-12 s |
| kling-4.0-r2v | `kling_elements` 2-4 images, `voices` | 3-30 s | 720p $0.1428/s; audio/video-input rate $0.085/s | `voices` rejected our voice 3 of 3 (29.10); no first-frame role | rejected |
| **kling-3.0-i2v** | `image_urls` 1-2 = first (+ last) frame; multi-shot only first frame; NO keyframes; no audio input; `generate_audio` optional | 3-15 s; 720p / 1080p / 4K | 720p no audio $0.08/s; 720p audio $0.12/s; 1080p audio $0.16/s; 4K $0.40/s ("+1 more" hidden) | NOT CHECKED by us (30.10 note only: "skip, no voice ref") | 2-pin but no keyframes: face anchor in the middle impossible; cheapest 2-pin Kling. Pilot candidate |
| **gemini-omni-flash-1.1-i2v** | first frame required, last optional (`image_urls`); no keyframes/references in i2v; audio input not specified | 4, 6, 8 or 10 s; 360p/720p/1080p/4K; 16:9 or 9:16; described as "lightweight preview model" | $0.06/s at 360p/720p/1080p, $0.12/s 4K (page); `-lite` $0.30/clip 720p; r2v with ref $0.036/s | NOT CHECKED | cheapest 2-pin video model on the list; quality for faces unknown; Unify quote 42 credits per 8 s 720p (Unify's own unit) |
| **minimax-h3-i2v** | `first_frame_image`, optional `last_frame_image`; no references | 4-15 s; 768P / 2K | 768P $0.09/s, 2K $0.1395/s; lite $0.04/$0.062; max 480P $0.05 | NOT CHECKED | 2-pin, 4-15 s; 2K option interesting for sharpness; quality for faces unknown |
| **muse-video-i2v** (MU Video) | first frame required, optional second = last frame; voice/sound optional (`generate_audio`) | 5, 10, 20, 30, 40, 50, 60 s; 720p only; 9:16 ok; style preset `cinematic_realistic` | per REQUEST: 5 s $0.15, 10 s $0.20, 20 s $0.30, 30 s $0.30 (+3 more hidden) | NOT CHECKED | absurdly cheap on paper (a 20 s take $0.30 vs Kling $2.90); unknown model, likely weak at faces; worth one pilot only |
| **seedance-2.5-lite-i2v** | first + last frame, no audio input | 4-30 s; 720p | $0.15/s | **MEASURED** (pilot C04): $1.35/9 s, texture 1969 vs 645-1594, grain 3.0, first frame "close, not exact" (diff 7.2); room sound when asked | best "look" rated 4.5 in ep.1; ep.2 gates (SFace to A3, motion) not run on it |
| seedance-2.5-lite-r2v | images as references, `audio_urls` | 4-30 s; 720p | $0.15/s ($0.09/s with a ref) | **MEASURED** C09: re-speaks the line in a voice only close to ours, lips follow its own audio; no true lip-sync | use for voice colour only |
| seedance-2.5 i2v / r2v / draft | 2.5 i2v first+last; r2v refs + audio refs | 4-30 s; 480p/720p/1080p | 480p $0.098/s, 720p $0.2205/s, 1080p $0.54194/s; r2v with ref 720p $0.1323/s | **MEASURED** 29-30.10: direct 720p jumps from the first frame (C05, C08); draft route needs 1080p final (draft $0.098/s + final $0.542/s = about $5.2/8 s) | too expensive for the gain |
| seedance-2.0 i2v | `image_urls` first frame only (last frame not in schema); no audio input | 4-15 s; 480p-4K | 480p $0.063, 720p $0.126, 1080p $0.315, 4K $0.7245 per s | MEASURED 29-30.10: charged $1.26/10 s; sharpness 389 vs Kling 880 on C01 | older; first frame only |
| seedance-2.0-lite i2v | first frame only, `generate_audio` | 4-15 s; 720p only | $0.085/s | NOT CHECKED | cheap, no last pin: face drifts without the 2nd pin (see Kling v1/v2 lesson) |
| seedance-2.0-fast / mini / mini-lite | i2v/r2v | 4-15 s | fast 720p $0.09/s, mini 720p $0.05/s, mini-lite $0.02/s | NOT CHECKED | quality tiers below 2.0; skip unless a pilot shows faces hold |
| seedance 1.0/1.5 pro | i2v | to 12 s | 1.5 pro 720p $0.075/s | NOT CHECKED | old |
| veo3-1-lite | optional `image_urls` (start or end frame; how many and roles NOT documented); native audio; no duration param (8 s assumed from our Veo use) | 720p / 1080p; 16:9 or 9:16 | per request: 720p $0.08, 1080p $0.12 (apipod.ai/pricing) | NOT CHECKED | very cheap per clip; second-hand (benchlm 11.09.2026) Google list price Lite $0.05/s 720p. Face-hold with a single image likely weak |
| veo3-1-fast / fast-ref | images; 8 s | 720p/1080p/4K | per request 720p $0.18, 1080p $0.225, 4K $0.54 | MEASURED earlier: "about $1 / 8 s" (30.10 table, old price; today's page says $0.18) rated face 3, camera 3; first frame not kept | price now much lower than our earlier note: re-check |
| veo3-1-quality | images | 8 s | per request 720p $0.80, 1080p $1.00, 4K $1.20 | NOT CHECKED (the owner's "Veo Quality access" is not visible here) | best-looking Veo, still one first frame only |
| wan 2.7 / 3.0 (+prime, spicy) | i2v with `audio_url` in 2.7; 3.0 r2v/i2v | up to 15-30 s | 3.0 720p $0.09-0.20/s, 2.7 720p $0.10/s | **Rejected by the owner 29.10** for video quality | skip |
| grok-imagine, 1.5 | i2v | short | 720p $0.036-0.11/s | NOT CHECKED | weak realism for faces (earlier note) |
| sora-2 / sora-2-pro / sora-2-vip | i2v | | per request $0.15 / $0.50; vip $0.09/s | NOT CHECKED | no pins documented |
| motion-control-m1, kling-2.6-motion-control | video + image | | $1.00/request; $0.07-0.105/s | not tested | no speech; not for dialogue |
| Runway, Luma, Hailuo/MiniMax direct, Kling direct, Sora direct | not reachable by us (no account) | | web only: Runway Gen-4.5 about $0.12/s, Luma Ray 3.2 $0.30/5 s 720p, Kling 4.0 about $0.157/s (apiframe/toolcolumn blogs) | NOT CHECKED, third-party blogs, conflicting | APIpod already resells the cheaper equivalents |

### 1.2 Image models (APIpod)
| Model | Inputs | Price (page 05.11) | Our measurement |
|--|--|--|--|
| **gpt-image-2.5-sunburst-lite** | text, up to several reference images, edits | 1K $0.03, 2K $0.06, 4K $0.12 (quality tiers; high 4K $0.12 charged) | **MEASURED**: 4K high $0.12/image (usage.cost); face to card 0.79-0.87 when edited from card A3; hall refs ok; intermittent `SUBMISSION_UNCERTAIN` failures (T2b start still failed twice, P1/P2: charge not shown, probably $0); refusal by 5-task concurrency limit |
| gpt-image-2.5-flare-lite | same family | 1K $0.02, 2K $0.04, 4K $0.08 | NOT CHECKED (same family as Sunburst Lite, 33 % cheaper at 4K): pilot candidate |
| gpt-image-2-fast | | 1K $0.015, 2K $0.03, 4K $0.06 | NOT CHECKED |
| nano-banana-pro | refs/edit | 1K $0.06, 2K $0.09, 4K $0.12 | **MEASURED** ep.2 masters: 4K $0.12, 2K $0.09; the king's eye colour/powder edits did not hold across v5 (ledger 31.10) |
| nano-banana-2.1 | refs/edit | 1K $0.02, 2K $0.04, 4K $0.05 | one test 04.11: REJECTED at submit by the content filter on the sheet prompt (not charged); otherwise NOT CHECKED |
| nano-banana-2 | | 1K $0.04, 2K $0.06, 4K $0.08 | NOT CHECKED |
| seedream-5.0-pro / -edit | up to 10 refs (Unify) | 1K-1.5K $0.035, 2K $0.07 | NOT CHECKED (2K cap) |
| seedream-5.0-lite/flash, 4.5 | | $0.018-0.06 | NOT CHECKED |
| wan2.7-image(-pro), z-image, qwen-image-edit | | $0.015-0.075 | NOT CHECKED; Wan family rejected for video, faces unknown |

## 2. Unify (MCP, free quotes read 05.11; balance 10 credits)
Models: Nano Banana 2 and Pro, Seedream 5.0 Lite/Pro, Grok Imagine image, Seedance 2.5 (4-30 s, 480-1080p, refs for images/videos/audio), Kling 3.0 Motion (needs driving video), Wan 3.0, Gemini Omni 1.1 Flash (3-10 s, native audio, frames or references, up to 3 reference images), FLUX 3.0 video (5-20 s). No Kling i2v, no Veo.
Quotes (credits, text-only prompt, 9:16): Seedance 2.5 720p 8 s no audio **92**; Gemini Omni 1.1 Flash 720p 8 s **42**; Wan 3.0 720p 8 s **56**; FLUX 3.0 hd 8 s **68**; Nano Banana Pro 4K **12**; Nano Banana 2 4K **12**; Seedream 5.0 Pro 2K **4.5**.
Dollar value of a Unify credit: NOT CHECKED (images suggest about $0.01 per credit, because Nano Banana Pro 4K = 12 credits vs APIpod $0.12; the Seedance quote would then be $0.92 vs APIpod $1.76, which is inconsistent, so do not rely on it). With 10 credits only one Seedream image fits. Reference upload needs prepare_unify_reference_upload. Not a source of savings without topping up.

## 3. Higgsfield, Picaso, vidIQ, Veo Quality
- Higgsfield: MCP 423 on 05.11 (and 30.10); earlier notes: Seedance 2.0 with start_image+end_image+audio roles, balance 0.1, plan pro. Prices NOT CHECKED.
- Picaso: models PicassoIA Image / Image Editor Pro / PicassoIA Video / Seedance 2.5 Lite, all unavailable: needs Infinite or Wonder plan; account on inactive Free trial; 5 parallel generations limit. Free allowance for us: none.
- vidIQ: 226 credits; generation tools exist (generate_video, generate_broll, voiceover) but their model, price in credits and inputs are NOT CHECKED; the tool descriptions say each call spends credits.
- seeddance.io reseller (30.10 analysis): Premium $149 with a 7-day unlimited Seedance window; not for our rule "ask before every generation"; unknown whether reference audio is covered; the offer page said valid until 1 Nov, so probably expired. Details in model_choice.md.

## 4. Our gates (fixed, from CLAUDE.md and quality_standard)
Face SFace to card A3 median >= 0.70 / p10 >= 0.55 (earlier working gate 0.60 mean, 0.45 min); sharpness drop <= 30 % per clip; no seams; motion gate (still body <= 15 %, frozen background <= 10 %, head >= 0.18 fw/s); correct pins; no music; hand-held feel.

---

## (a) Ranked table: video routes for a two-pin 8-12 s clip (720p)
Ranking = proven first, then cheap pilots. "Price/clip" = 8 s / 12 s.
| # | Route | 8 s | 12 s | Status |
|--|--|--|--|--|
| 1 | Kling 4.0 i2v 720p, first+last+keyframes | $1.16 | $1.74 | PROVEN by us (face 0.74-0.79, sharpness ok); motion needs the per-beat score |
| 2 | Seedance 2.5 Lite i2v 720p, first+last | $1.20 | $1.80 | partly proven (C04 look good, first frame not exact); ep.2 gates not run |
| 3 | Kling 3.0 i2v 720p no audio, first+last (no keyframes) | $0.64 | $0.96 | UNPROVEN, provider price; pilot |
| 4 | MiniMax H3 i2v 768P, first+last | $0.72 | $1.08 | UNPROVEN; pilot |
| 5 | Gemini Omni Flash 1.1 i2v 720p, first+last (max 10 s) | $0.48 | n/a (10 s max: $0.60) | UNPROVEN, "preview"; pilot |
| 6 | Veo 3.1 Lite 720p per request | $0.08 | n/a (8 s fixed assumed) | UNPROVEN; pins unclear; pilot |
| 7 | Muse Video i2v 720p, first+last | 10 s $0.20 | 20 s $0.30 | UNPROVEN, unknown model; pilot |
| - | Seedance 2.5 draft->1080p | about $5.2 | | too expensive |
| - | Kling 4.0 1080p | $1.74 | $2.61 | owner keeps 720p |
| - | Wan family | | | rejected by owner |
Rule: a cheaper route is never adopted on its price; only after a pilot passes the same gates.

## (b) Ranked table: stills and edits (4K 9:16 unless said)
| # | Route | Price | Status |
|--|--|--|--|
| 1 | GPT Image 2.5 Sunburst Lite 4K high, edit from card A3 | $0.12 | PROVEN (face 0.79-0.87), but SUBMISSION_UNCERTAIN failures |
| 2 | Nano Banana Pro 4K (fallback when GPT fails) | $0.12 | proven for masters, weaker on small edits |
| 3 | GPT Image 2.5 Flare Lite 4K | $0.08 | UNPROVEN, same family; pilot |
| 4 | Nano Banana 2.1 4K | $0.05 | UNPROVEN, content filter risk seen once |
| 5 | Nano Banana 2 4K | $0.08 | UNPROVEN |
| 6 | gpt-image-2-fast 4K | $0.06 | UNPROVEN |
| 7 | Seedream 5.0 Pro 2K | $0.07 | UNPROVEN, 2K ceiling: fails the "native 4K source" rule |
| - | virtual hand-held / crop punch-in in the edit (ffmpeg) | $0 | measured: removes frozen background, costs head sharpness (436 -> 225) |

## (c) Free allowances we hold
None usable: Picaso inactive trial; Higgsfield unreachable; Unify 10 credits (one Seedream image at most); vidIQ 226 credits (generation use NOT CHECKED); Lumean ElevenLabs voice is paid in RUB (0.23-0.96 RUB per order). Free tools: ffmpeg edit, htdemucs, face_gate, clip_qc, free price quotes.

## (d) Cheap pilots to propose (each needs the owner's yes AFTER she sees the Russian prompt and references; one yes = one call)
| # | Pilot | Cost | Gate that judges |
|--|--|--|--|
| 1 | Kling 3.0 i2v 720p no audio, 8 s, the SAME first/last stills and prompt as an accepted Kling 4.0 clip (T3c fork gag) | about $0.64 (vs $1.16) | face_gate (median >= 0.70, p10 >= 0.55), sharpness vs start still, ref_compare motion gate, pins |
| 2 | Gemini Omni Flash 1.1 i2v 720p, 8 s, same stills | about $0.48 | same gates; plus does it add its own music/voice |
| 3 | GPT Image 2.5 Flare Lite 4K edit of A3 (one pose still already made on Sunburst Lite) | about $0.08 (vs $0.12) | face to A3 >= 0.79 vs the Sunburst result, full-size quality metrics (sharp >= 150, detail >= 2.0, blocks <= 1.20) |
| 4 | Muse Video i2v 10 s with first+last stills (cinematic_realistic) | about $0.20 | same video gates; stop at once if the face fails |
| 5 | Veo 3.1 Lite 720p one start still | about $0.08 | face_gate; only worth continuing if it takes the last frame |
Total of all five about $1.5, less than one Kling retake plus a spare. MiniMax H3 768P (about $0.72 / 8 s) is the sixth if the first two fail.

## (e) Clip-length guidance from our script pace
- Reference pace: 90 words per minute overall = 0.67 s per word including pauses; our plan used 110 wpm for the spoken part = 0.55 s per word. From script v7: 310 words = about 3:26.
- Our takes (shots_and_generation_length_2026-11-05.md): 59 words about 32 s, 52 about 28 s, 60 about 33 s, 45 about 25 s, 36 about 20-24 s, 24 about 13 s, 51 about 28 s, 9 about 5 s: roughly 0.54 s per word, 0.5-0.6 for dense lines.
- Rule of thumb: seconds = words x 0.55 + pauses; add 1.5 s for the laugh/gag silent beat, 0.7 s per short pause, 1 s of lead-in and 1 s tail so the TTS phrase starts inside the clip.
  - 10 words = about 6-7 s -> 8 s clip; 15 words = 9-10 s -> 10 s; 20 words = 12-13 s -> 12 s; 25+ words = 15 s (Kling cap on frames at >= 9 s: 10 total).
- Money per second: Kling 4.0 720p $0.145/s. Every second trimmed = $0.145; a 12 s clip that needs only 10 s saves $0.29. Every extra pin does not cost money (only the still, $0.12).
- Prefer one longer pinned take (15-30 s) over a chain of 8 s clips only if the pilot (15 s, $2.18) shows no face drop; a failed 30 s take costs $4.35 vs $1.16.
- Inserts (food burst, cutaways, Marcel reaction) as stills with the Ken Burns/virtual hand-held cost $0.12 per still against $1.16 per 8 s clip.

## Not verified / open
Real price list tiers hidden as "+N more" on apipod.ai/pricing (kling-3.0 extra tier, muse-video, wan, seedance r2v variants); the second 175k characters of that page were not read. Unify credit to dollar rate. Higgsfield, vidIQ generation, Veo Quality, any direct vendor price. Quality of every UNPROVEN route for faces and hand-held motion.

## Kling 3.0 i2v on APIPod: spec verified 05.11.2026 (economist, read-only, nothing submitted)
Sources: docs.apipod.ai/api-reference/openapi/kling-3.0--kling-3.0-i2v.yaml (the real file name has the double-dash form; llms.txt lists it; the short name kling-3.0-i2v.yaml is a 404) and apipod.ai/pricing (first 100k chars), both read 05.11.
- Model id `kling-3.0-i2v`; endpoint POST /v1/videos/generations; async task. Related ids exist: kling-3.0-turbo-i2v, kling-3.0-omni-i2v/r2v/edit (price NOT on the first 100k chars of the price page; NOT CHECKED).
- `image_urls`: 1 = first frame, 2 = first + last (index 0/1). Aliases first_frame_image / last_frame_image. Aspect follows the first frame. NO `@first_frame` / `@last_frame` tags in the spec (they are Kling 4.0 only; do not rely on them, write the prompt without tags). NO keyframes, no negative prompt, no audio input. Multi-shot (multi_shot + multi_prompt up to 5 shots, 500 chars each) allows only a first frame, so no last pin.
- `duration` integer 3-15 s (10 s allowed), default 5. `resolution` 720p / 1080p / 4k, default 720p. `generate_audio` default false for single-shot (native audio only; we mute it anyway).
- PROMPT LIMIT: 2,500 characters (Kling 4.0: 8,000). Our T3d prompt (take3_T3d_prompt.txt) is 3,880 chars, so it does NOT fit and must be condensed (about -35 %) before any Kling 3.0 pilot; this is a change to the prompt, so it needs a new owner review.
- Image size / format limit: not stated in the spec (NOT CHECKED); our 4K JPG refs were accepted by Kling 4.0.
- Price (page, 05.11, per second): 720p no audio $0.08; 720p audio $0.12; 1080p audio $0.16; 4K $0.40; 1080p no audio hidden ("+1 more"). 10 s 720p no audio = $0.80 (8 s = $0.64) vs Kling 4.0 $1.45 (measured) = saving $0.65 per 10 s clip. A provider claim until a real charged usage.cost is seen.
- Quality for OUR gates (face SFace, sharpness, motion): NOT MEASURED. Pilot only with the owner's yes, same pins, same words, judged by clip_qc / ref_compare.
