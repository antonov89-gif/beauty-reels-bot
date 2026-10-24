# Growth Learning Log — Mr. Buck (Module 15, V3.0 PRO)

How to use it: after each publish batch or audit, fill in the results, the extracted principle and the confidence level. Commit every update. Sources: vidIQ (V), YouTube Studio screenshots from the user (S, only those already received; not requested further), Metricool (M).

Main metrics (no per-video stayed/swiped data): views at 24 h and 72 h vs the channel median, relative retention from vidIQ, likes and comments per 1k views.

## 1. Baseline (17.10.2026)
| Metric | Value | Source / tag |
|---|---|---|
| Views, 28 days | 25.4k, 93% Shorts | V, FACT |
| Traffic from the Shorts feed | 88% | V, FACT |
| Stayed / swiped (all Shorts, 28 days) | 55.6% / 44.4% | S, FACT |
| Best Short, 28 days | Wallace Line, 2,302 views | V, FACT |
| Median Short | ≈1.2k views | V, ESTIMATE |
| Gambia | 2,118 views, stayed 46.2%, AVD 0:26 (42.7%), +2 subs | S, FACT |
| Wallace audience | 99.9% non-subscribers; US 13.1%, IN 9.8%, PH 8.3% | S, FACT |
| Visual pace vs views | Amazon ~2 events/10 s → 290 views; Wallace 7–8 → 2,302; Geo Spark (competitor) ~14 → 4.8M | V watch + count, HYPOTHESIS (correlation) |

## 1a. Baseline snapshot 18.10.2026 03:00 MSK (vidIQ, before the scheduled batch starts)
- 28 days (20.09–18.10): 25,367 views, engaged views 12,790 (50.4%), 465 likes, 21 comments, 31 subscribers, 9,197 min watched. FACT.
- Shorts published 4–15.10 and at least 2 days old (n = 18): views min 290, median 1,245, mean 1,226, max 2,305 (Wallace). FACT.
- Split by publish date: 4–7.10 (n = 10) median 1,095; 12–15.10 (n = 8) median 1,350. Different topics, ages and hours: HYPOTHESIS of a ~+20% drift, not proof.
- Life curve (Wallace, hourly/daily data): 70% of lifetime views within the first 13 h, 88% by day 2, plateau from day 3–4. So 24 h views are the main metric, 72 h confirms. FACT (n = 1, check on more videos).
- Shorts of 16–17.10 are too young: Thrillbilly 1,151 (38 h), Real Life vs GTA 119, ocean floor 62, GTA launch day 49. Panama (long, 6:34): 14 views.
- Nothing from the scheduled batch has been published yet (first post 18.10 10:00 MSK).

### Monitoring 18.10 09:58 MSK
- Queue intact: Vice City (10:00), Madagascar (12:00), GTA s3 (14:00), GTA s1 (15:00), Hannibal (16:00) all Pending in Metricool. FACT.
- Nothing new published since 17.10 evening. Views: Thrillbilly 1,152, Snake Island 1,288, Kiribati 1,595, Moon 1,451, Yap 1,228, Palmerston 1,760; 16–17.10 GTA/ocean Shorts 64–129 (young). 28-day totals unchanged (25,367).
- Metadata fix: Amazon bridges (N0U5OgVv7_4): removed another channel's name ("geography by geoff") and an irrelevant "united states" tag; set 10 relevant tags. FACT (vidIQ update confirmed).

### 18.10 10:21 MSK check-in
- Vice City vs REAL Miami (long, 8:27) published by Metricool at 10:04 MSK, public, title and tags as planned (nij4WjfDKeY). Cover cover_a.jpg set via vidIQ (status updated). FACT.
- Madagascar 12:00 (first TikTok copy), GTA s3 14:00, GTA s1 15:00, Hannibal 16:00 still Pending at 09:58. Not yet verified as published.
- Not done through the API: "Related video" link and the pinned comment (manual in Studio).

### 18.10 12:17 MSK check of the published long video (Vice City vs REAL Miami, nij4WjfDKeY)
- Published 10:04 MSK, public, 8:27, title/description/chapters/tags as planned; auto-transcript matches the script; cover_a applied (visually confirmed on i.ytimg.com). FACT.
- Views at 2 h 12 min per vidIQ: 0 (Madagascar, published 12:03, also 0 at 13 min). vidIQ lags by hours, so DATA MISSING until the 17:00 check. 
- Risks (HYPOTHESIS): cover text "IT'S REAL" vs the video's own mixed verdict (official vs fan matches) can read as clickbait; the channel's audience comes from the Shorts feed (88%), so a long video may get little reach (counter-hypothesis: new topic/cover). Test: Studio Test & Compare cover_a vs cover_b ("SAME PLACE?"), desktop only.
- Master loudness −13.8 LUFS, peak 0.0 dBFS: slight clipping risk after YouTube re-encode; fix for next long videos (limiter at −1 dBTP).
- Still manual: Related video links on the GTA Shorts, pinned comment.

### 18.10 views-drop analysis (map_shorts/views_drop_analysis_2026-10-18.md)
- Daily views follow the number of new Shorts (r = 0.91, 4–15.10). Per-video median did not fall. FACT.
- 16–17.10: 2 of 5 Shorts got the feed push, 3 stuck at 68–134 (Real Life vs GTA, Pangaea, GTA Launch Day). All 3 published 18:47–23:25 MSK, vague or textless first frame. HYPOTHESIS (H2, H3); tested by the 10–16 MSK queue from 18.10.
- Browse traffic 265/day (4–8.10) → 19/day (9–15.10). FACT.

### Monitoring 18.10 21:57 MSK (vidIQ public counts; Analytics still ends 15.10)
- Queue of 18.10 published on time by Metricool (+3-4 min): Madagascar 12:03, GTA s3 14:03, GTA s1 15:03, Hannibal 16:04, Vice City long 10:04. FACT.
- Views at 6-12 h: GTA s1 (slogan) 265 / 7 h; GTA s3 (flea market) 50 / 8 h; Madagascar 8 / 10 h; Hannibal 6 / 6 h; Vice City long 2 / 12 h. FACT.
- 16-17.10 Shorts now: Launch Day 281, Real Life vs GTA 232, ocean floor 80; Thrillbilly 1,235, Snake Island 1,294. FACT.
- Reading: two geography Shorts in the 10-16 MSK window got no feed push in the first hours, so timing alone (H3) does not explain the flops. HYPOTHESIS, check at 24 h (trigger 19.10 17:00). GTA Shorts today beat geography Shorts today (E4 signal, n = 2 vs 2).
- Metadata: no errors found in the 5 new videos (titles, tags, descriptions match publication files). No edits made.

### Decision 18.10 22:15 MSK (user: "GTA только на ТТ")
- GTA s2 (19.10 10:00) and GTA ep.2 (20.10 10:00): YouTube removed in Metricool, TikTok kept (new ids 399363806, 399363880; uuids unchanged). FACT (response shows providers = tiktok only).
- YouTube queue now geography/general only: 19.10 12:00 Suez, 14:00 coin, 16:00 Libya; 20.10 12:00 Aral, 14:00 gold cube, 15:00 long $100B, 16:00 $100B short. No GTA on YouTube until the H6 test result (check 22.10-23.10: do geography Shorts get a feed push again?).
- E4 rule (GTA < 50% of geography median -> pause until 19.11) replaced by the H6 test: success = at least 2 of the next 5 geography Shorts reach ~1k views at 24 h.

### TikTok monitoring set up 19.10 00:10 MSK (user request)
- Source: Metricool analytics (brand 7486051), connector `posts` (TKPO07 views, TKPO08-10 likes/comments/shares, TKPO11 reach, TKPO13 full-watch rate, TKPO15 avg watch time, TKPO16 For You share) and `evolution` (TKEV02/07/08). Routine "Mr. Buck monitoring" (9:56 and 21:56 MSK) now reports a TikTok block and, once a day, runs a niche outlier search (vidIQ, 5 credits).
- First read (1-19.10): Metricool sees only 2 TikTok videos, both of 16.10 (gta6_ep2_tg 3 views, gta6_real_places_chat 0 views), followers 0, new followers 0. None of the Metricool-published TikTok copies of 18.10 (Madagascar, GTA s3, GTA s1, Hannibal) appear. DATA MISSING: the API may lag, or the account is personal/limited. Check on the 21:56 run; if still missing, the user opens TikTok Studio analytics or connects a Business account. FACT for what is visible, cause UNKNOWN.

### Monitoring 19.10 09:57 MSK (vidIQ + Metricool TikTok)
**YouTube (vidIQ public counts / Analytics 16-19.10).**
- 18.10 uploads at ~20 h: GTA "slogan" 450 views (7 likes), GTA flea market 70, Hannibal 15, Madagascar 18, Vice City long 3. Earlier: GTA launch-day 537 (48 likes), Thrillbilly 1,241, Snake Island 1,304 (the only Short with 76% avg view and 6 subs in 3 days).
- Analytics 16-19.10: Shorts feed 3,650 of ~3,850 views (95%), 1,716 engaged (47% vs baseline ~52%), avg view 67.5% (baseline 62%), search 119. Top: Snake Island 1,237 (610 engaged, 76% viewed, +6 subs), Thrillbilly 1,181 (441 engaged, 35.9% viewed, 0 subs), moon bags 622 (67%, +3 subs).
- Reading: the two geography Shorts of 18.10 (Madagascar 18, Hannibal 15) got no feed push while the GTA Shorts of the same day did (450, 70). Consistent with H6 (the feed now treats the channel as a GTA/gaming audience), not proof; the geography-only queue from 19.10 is the test. Thrillbilly (GTA) has the weakest retention of the top group (35.9%): views without subscribers.
**TikTok (Metricool, 12-19.10).** The 18.10 copies are visible now (earlier DATA MISSING was lag). Account views on 18.10: 1,558. Times in Metricool are UTC.
| Video (18.10) | Dur | Views | Likes | Likes/1k views | Comments/shares |
|---|---|---|---|---|---|
| Hannibal elephants | 62 s | 497 | 20 | 40 | 0 / 0 |
| Madagascar no lions | 39 s | 443 | 13 | 29 | 0 / 0 |
| GTA slogan (cruise capital) | 33 s | 433 | 14 | 32 | 0 / 0 |
| GTA flea market (Opa-locka) | 32 s | 185 | 2 | 11 | 0 / 0 |
- Median of the TikTok copies of the last 7 days (6 videos incl. two old ones with 3 and 0 views) = ~309; nothing reaches 3x (~930), so no video has "taken off" yet. Fastest: Hannibal (497 in ~6 h after posting). Highest interest by likes per 1k: Hannibal (40), then GTA slogan (32) and Madagascar (29). Weakest: Opa-locka (11).
- Observation (FACT): on TikTok geography/history (Hannibal 497, Madagascar 443) did as well as GTA (433), while on YouTube the same two geography Shorts got 15-18 views. So the TikTok audience is not GTA-biased; the YouTube feed is. Hypothesis only, n = 4, 6 h of data per video. The longest (62 s) history Short leads on both views and likes.
- DATA MISSING: TKPO13/15/16/21 (full-watch rate, avg watch time, For You share, search) are empty for every post; comments and shares are 0. The 17.10 launch-day Short and the 18.10 Vice City long have no TikTok copy in Metricool. Outlier search runs in the evening run only.
- Not touched: tag "space documentary / asia / europe" on the ocean-floor Short (hUNAthRmw1w) looks misleading; no publication.md for it, left for the user to confirm.

### Checkpoint 1: 19.10 17:00 MSK (vidIQ public counts; baseline median 1,245)
| Video | Published | Age | Views | % of median | Likes/1k | Comments/1k |
|---|---|---|---|---|---|---|
| Madagascar no lions | 18.10 12:03 | ~29 h | 20 | 1.6% | 200 | 0 |
| Hannibal elephants | 18.10 16:04 | ~25 h | 18 | 1.4% | 167 | 56 |
| GTA slogan (s3) | 18.10 15:03 | ~26 h | 470 | 38% | 19 | 0 |
| GTA flea market (s1) | 18.10 14:03 | ~27 h | 76 | 6% | 53 | 0 |
| Vice City vs Miami (long) | 18.10 10:04 | ~31 h | 3 | n/a (long) | 667 | 0 |
| Euro coin zoom loop (25 s) | 19.10 14:03 | ~3 h | 494 | 40% in 3 h | 2 | 0 |
| Libya river | 19.10 15:03 | ~2 h | 72 | 6% | 56 | 0 |
| Suez / Moon | 19.10 12:03 | ~5 h | 2 | 0.2% | 0 | 0 |
| Russia 58 years | 19.10 16:05 | <1 h | 1 | - | - | - |
(Later-than-listed: GTA launch-day 17.10 reached 701 views, 80 likes/1k, 10 comments/1k at ~70 h; Thrillbilly 1,244.)
- FACT: none of the 18.10 Shorts reached the 1,245 median in 24 h. Both geography/history Shorts (Madagascar 20, Hannibal 18) stayed under 2% of it; GTA s3 reached 38%, GTA s1 6%.
- FACT: the coin loop (non-GTA, 25 s, seamless loop) collected 494 views in ~3 h, while Suez, published 2 h earlier, stands at 2 views. HYPOTHESIS (n = 1): the feed push depends on the format/runtime (short loop with replays) rather than only on "GTA vs geography", so H6 is narrowed further; the geography-only test is not yet decisive (Suez 2, Libya 72 so far).
- Likes per 1k are meaningless for videos under 100 views (n < 5 likes). Coin's 2 likes/1k on 494 views means weak liking, probably passive replays: watch retention and subscribers before copying it.
- Next: Libya and coin at 24 h (20.10 15:00), Russia (E6) at 20.10 17:00. Test success remains: at least 2 of the next 5 geography Shorts near 1k at 24 h.

### Monitoring 19.10 22:00 MSK (vidIQ + Metricool + niche outlier search; ~20 vidIQ credits)
**YouTube (vidIQ public counts; Analytics for 17-19.10 returned no rows, data lag, so no retention/traffic split this run).**
| Video (19.10) | Age | Views | % of 1,245 median | Likes |
|---|---|---|---|---|
| Libya river (68 s) | ~7 h | 1,075 | 86% | 13 |
| Euro coin loop (25 s) | ~8 h | 1,012 | 81% | 5 |
| Suez / Moon (37 s) | ~10 h | 3 | 0.2% | 1 |
| Russia 58 years (85 s, E6) | ~6 h | 5 | 0.4% | 1 |
Older: Madagascar 35, Hannibal 19, GTA slogan 478, GTA flea 80, Vice City long 6, launch-day 772.
- FACT: two non-GTA Shorts (Libya, coin) took a feed push of ~1k views in 7-8 h, while two others posted the same day (Suez, Russia) got a handful. So "geography = no push" is wrong, and "GTA = push" is not the rule either (GTA flea 80). H6 as "GTA audience poisons geography" is weakened further; the difference is per-video. Not yet explained.
- HYPOTHESIS (n = 4, unproven): Libya and coin have a strong hook question / visual loop; Suez has a long title statement with emoji, Russia opens on a globe with a number. Need retention (vidIQ relative retention, 24 h) before any conclusion. Russia (E6) has a weak start (5 views at ~6 h): judge at 24 h on 20.10 ~16:00.
**TikTok (Metricool 12-19.10).** Numbers identical to the 09:57 run (Hannibal 497, Madagascar 443, GTA slogan 433, GTA flea 185; account views 18.10: 1,558). DATA MISSING for every 19.10 post (GTA s2 10:00, Suez, coin, Libya, Russia): Metricool shows none of them yet, probably sync lag (the 18.10 copies appeared ~half a day later). TKPO13/15/16/21 empty again. No video above the 3x-median threshold.
**Niche outliers (vidIQ, TikTok, last 7 days, English geography/map/history, 5 results).** 627k-1.3M views, 10-50x creator median:
| Creator | Views | x median | Length | Format |
|---|---|---|---|---|
| theglobefacts | 628k | 10x | 79 s | "oldest country wins" map battle simulation |
| rilttoril | 768k | 50x | 162 s | straight line drawn across the map, countries highlighted |
| 3dspectra | 1.3M | 13x | 161 s | 3D explainer, Great Wall |
| kirkiimad | 660k | 35x | 5 s | green screen, "why no bridge Italy-Albania" |
| historyproductions.v2 | 858k | 10x | 35 s | map animation + archive footage, Korean War |
- Repeating: (1) a question or contrast as on-screen text on frame 0 (4 of 5); (2) music or voice from the first second, no intro (5 of 5); (3) a visible map device, not a still: moving line, VS graphic, front-line animation (4 of 5); (4) high cut rate (3 of 5 "fast"); (5) 3 of 5 are 79-162 s, only one under 40 s. Instagram twin results (Italy closest-neighbour map, Canada-USA border oddities, "cities on a vanished beach") use the same recipe: a counter-intuitive anomaly with one map device.
- Not copied: content. Use as a pattern for TikTok only: our TikTok copies are 32-85 s, so length is not the gap; frame-0 question/contrast text is.
- Not touched: the misleading tags of the ocean-floor Short (hUNAthRmw1w: "space documentary", "asia", "europe") still wait for the user's OK.

### Russia Short cover changed 19.10 ~23:15 MSK (user request)
New YouTube cover on uonb7oq7ttw: question "HOW DID RUSSIA GET SO BIG?" + route globe with "58 YEARS" (frame from the video, 1080x1920). Set via vidIQ (5 credits). The Short had 5 views at ~6 h before the change; compare 24 h views (20.10 ~16:00) with this note, n = 1, no A/B (covers show on the channel page and in search, not in the Shorts feed). TikTok cover not changed.

### Monitoring 20.10 09:57 MSK (vidIQ + Metricool; ~15 vidIQ credits)
**YouTube (vidIQ public counts; baseline median 1,245).** Analytics for 17-20.10 lags (only 390 Shorts-feed views in the window, data ends ~18.10), so no retention/traffic split this run.
| Video | Age | Views | % of median | Change since 22:00 |
|---|---|---|---|---|
| Libya river (19.10 15:03) | ~19 h | 1,244 | 100% | +169 |
| Euro coin loop (19.10 14:03) | ~20 h | 1,032 | 83% | +20 |
| Russia 58 years, new cover from ~23:15 (19.10 16:05) | ~18 h | 23 | 1.8% | +18 |
| Suez / Moon (19.10 12:03) | ~22 h | 8 | 0.6% | +5 |
| Madagascar / Hannibal (18.10) | ~45 h | 39 / 21 | 3% / 2% | +4 / +2 |
| GTA slogan / flea (18.10) | ~45 h | 493 / 79 | 40% / 6% | +15 / -1 |
- FACT: Libya and the coin loop each got a ~7-8 h push (about 1k views) and then flattened; Libya ended exactly at the median, coin at 83%. Neither exceeded the median, so by the E-rule they are "median, not growth". Suez and Russia got no push.
- FACT: Russia (E6) at ~18 h has 23 views, 1.8% of the median. The 18 views gained since the cover change (~23:15) are not attributable to it (n = 1, no A/B, covers sit on the channel page/search, not in the feed). E6 verdict at 24 h (20.10 ~16:00); if still below 5% of the median, the dense-globe system is rejected for the Shorts feed.
- H6 status: 2 of 4 geography Shorts of 19.10 got a push (Libya, coin), none of the geography/history Shorts of 18.10 (Madagascar, Hannibal). Test criterion (2 of the next 5 near 1k at 24 h) is currently 2 of 4 close, so provisional "partly met"; not enough to conclude. Judge after Aral (12:00), gold cube (14:00), $100B Shorts today.
**TikTok (Metricool 13-20.10).** Identical to 19.10 (Hannibal 497, Madagascar 443, GTA slogan 433, GTA flea 185). DATA MISSING for all 19.10 posts (GTA s2, Suez, coin, Libya, Russia), now >24 h after posting; Metricool analytics ends 18.10 (TKEV02 has no 19.10 row), so this is a reporting lag of at least a day, not missing posts. TKPO13/15/16/21 empty, comments/shares 0. If still absent on 21.10, ask the user for TikTok Studio numbers or a Business-account connection.
- Not touched: ocean-floor Short tags still wait for the user's OK. Pinned comments: vidIQ cannot post or pin (reply only); three draft texts given to the user to post manually.

### Monitoring 20.10 22:00 MSK (vidIQ + Metricool + niche outliers; ~15 vidIQ credits)
**YouTube (vidIQ public counts; baseline median 1,245; Analytics for 18-20.10 still returns no rows, so no retention/traffic split).**
| Video | Published (MSK) | Age | Views | % of median |
|---|---|---|---|---|
| Aral Sea | 20.10 12:03 | ~10 h | 1,713 | 138% (best of the week) |
| $100B Short | 20.10 16:03 | ~6 h | 975 | 78% and rising |
| Gold cube | 20.10 14:02 | ~8 h | 437 | 35% |
| $100B long (13 min) | 20.10 15:07 | ~7 h | 1 | n/a |
| Russia 58 years (new cover 19.10 ~23:15) | 19.10 16:05 | ~30 h | 1,057 | 85% (was 23 at 09:57 today) |
| Libya | 19.10 15:03 | ~31 h | 1,261 | 101% |
| Euro coin loop | 19.10 14:03 | ~32 h | 1,043 | 84% |
| Suez / Moon | 19.10 12:03 | ~34 h | 10 | 0.8% |
- FACT: since GTA left YouTube (19.10), 4 of 7 non-GTA Shorts reached ~1k views (coin, Libya, Russia, Aral); the $100B Short is at 975 after 6 h; gold cube 437; Suez 10 is the one dud. The H6 test criterion (>= 2 of the next 5 geography Shorts near 1k at 24 h) is MET. The 18.10 geography/history Shorts that ran alongside GTA (Madagascar 44, Hannibal 65) got no push. Consistent with H6 ("GTA/gaming audience on the YouTube feed suppresses non-GTA Shorts"), n = 7 vs 2, not proof. Decision: GTA stays off YouTube (TikTok only) for now; re-test with one GTA Short only after >= 10 more non-GTA Shorts, one at a time.
- E6 (Russia): rose from 23 to 1,057 views within one day, 85% of the median. The rise began after the cover change (19.10 ~23:15) but the push could equally be the normal delayed one (Libya/coin also surged); correlation only, n = 1, no A/B. Verdict: E6 is at the level of the other geography Shorts, not above. Not enough to prefer the dense-globe system over the others. E5 Turkey (24.10) will decide.
- Long video $100B has 1 view at 7 h: expected for a 13-min long with no feed push; check at 72 h, do not publish another long this week (rule: <= 1 per week).
**TikTok (Metricool 14-20.10): 19.10 posts are visible now (lag was ~1.5 days).** Account views: 18.10 1,702; 19.10 1,036; 20.10 66 so far (partial day).
| Video | Dur | Views | Likes/1k | Shares |
|---|---|---|---|---|
| Hannibal (18.10) | 62 s | 545 | 37 | 0 |
| Madagascar (18.10) | 39 s | 465 | 28 | 0 |
| GTA slogan (18.10) | 33 s | 465 | 30 | 0 |
| Libya (19.10) | 67 s | 346 | 43 | 0 |
| Euro coin (19.10) | 24 s | 299 | 27 | 0 |
| Russia (19.10) | 84 s | 282 | 35 | 1 |
| GTA flea (18.10) | 32 s | 227 | 9 | 0 |
| Suez (19.10) | 36 s | 109 | 9 | 0 |
| GTA "Six places" ep.2 (20.10 10:02) | 85 s | 66 | 0 | 0 |
| GTA Tequesta (19.10 10:02) | 46 s | 0 | - | 0 |
- Median of the 10 recent TikTok copies = ~290; 3x = ~870; nobody "took off". Highest interest by likes per 1k: Libya (43), Hannibal (37), Russia (35, the only share). On TikTok the long map stories (62-84 s) lead on views and likes; the 24 s loop is mid; the 85 s GTA quiz is weak (66 in ~12 h). Account views fell from 1,702 (18.10) to 1,036 (19.10).
- Still DATA MISSING: 20.10 12:00 Aral, 14:00 gold cube, 16:00 $100B Short (not yet in Metricool); TKPO13/15/16/21 empty; comments 0.
**Niche outliers (vidIQ, TikTok, last 7 days, 5 new creators, excluding yesterday's).** 617k-1.3M views, 4-308x creator median: Romans-name-your-country map (68 s), window tax 3D (32 s), Nepal meme green screen (9 s), "strangers redrew US borders" screen recording (126 s), top-producing countries list (74 s). Instagram: Italy nearest-neighbour map, Canada-US border, Amazon scale, Fall Line cities.
- Repeating over two days of searches (10 outliers): (1) the hook addresses the viewer or their own place ("your country", "from where you stand", "which neighbour", "every state border strangers drew"): 5 of 10; (2) a question or contrast as text on frame 0 (7 of 10); (3) sound from the first second (10 of 10); (4) one visible map device (zoom, line, circle with arrows); (5) lengths mostly 32-126 s, only 2 of 10 under 35 s. Content is not copied. Test idea for TikTok: a second-person hook ("Which country is closest to yours?") with a question on frame 0, 40-70 s.

### Decision 20.10 ~22:30 MSK (user)
GTA Shorts stay in the TikTok queue as planned (user: "Для тик ток пусть будут"). No pause. GTA stays off YouTube until 19.11 (E4 rule). Re-check TikTok GTA vs geography medians on the next monitoring runs (E4 TikTok: GTA ~146 vs geography ~322, 45%).

### Monitoring 21.10 09:58 MSK (vidIQ + Metricool; ~10 vidIQ credits)
**YouTube (public counts; baseline median 1,245).**
| Video | Age | Views | % of median |
|---|---|---|---|
| Aral Sea (20.10 12:03) | ~22 h | 2,089 | 168% (best since the audit) |
| $100B Short (20.10 16:03) | ~18 h | 1,094 | 88% |
| Russia (19.10 16:05) | ~42 h | 1,089 | 87% |
| Libya (19.10 15:03) | ~43 h | 1,277 | 103% |
| Euro coin (19.10 14:03) | ~44 h | 1,068 | 86% |
| Gold cube (20.10 14:02) | ~20 h | 480 | 39% |
| Suez / Moon (19.10 12:03) | ~46 h | 10 | 0.8% |
| $100B long (20.10 15:07) | ~19 h | 3 | n/a |
- FACT: since GTA left YouTube (19.10), 5 of 7 non-GTA Shorts are at ~1k or more (Aral 2,089, Libya, $100B, Russia, coin); gold cube 480 and Suez 10 are the weak ones. H6 test criterion remains met; the strongest result is Aral (168% of the median, the first Short clearly above the baseline). No new GTA on YouTube.
- Analytics 18-21.10 (lags to ~19.10): launch-day GTA (17.10) 478 views, 253 engaged (53%), 43.8% viewed, +3 subs, 36 likes; GTA slogan 462 views, 134 engaged (29%), 60% viewed. FACT: the GTA slogan has the lowest engaged share of the batch, which supports "views without interest" for that Short. Traffic sources not re-pulled (lag).
**TikTok (Metricool): DATA MISSING for everything.** The query for 15-21.10 returned no post rows and zero views for 16-21.10; a second query from 12.10 returned only a 21.10 row. Yesterday the same account returned 10 posts with views and likes. So the posts did not vanish: the Metricool TikTok analytics feed is empty or disconnected (cause UNKNOWN: API glitch, expired TikTok authorization, or a Metricool change). No TikTok numbers were invented. Next step: user checks Metricool > Connections > TikTok (reconnect if needed) or sends TikTok Studio numbers; I retry on the 21:56 run.
- Not touched: ocean-floor Short tags (user OK pending); no niche outlier search (evening run only).

### Monitoring 21.10 22:00 MSK (vidIQ + Metricool + niche outliers; ~10 vidIQ credits)
**YouTube (public counts; baseline median 1,245).**
| Video (published, MSK) | Age | Views | % of median |
|---|---|---|---|
| Pheasant Island (21.10 10:02) | ~12 h | 1,098 | 88% (strong start) |
| Baarle double borders (21.10 14:03) | ~8 h | 325 | 26% |
| Aral Sea (20.10 12:03) | ~34 h | 2,147 | 172% (+58 since morning: plateau) |
| Libya | ~2 d | 1,351 | 109% |
| Euro coin | ~2 d | 1,147 | 92% |
| Russia | ~2 d | 1,111 | 89% |
| $100B Short | ~30 h | 1,123 | 90% |
| Gold cube (title now "What If You Melted All The World's Gold?") | ~35 h | 779 | 63% (+299 since morning, likes 15 -> 38) |
| Suez / $100B long | - | 11 / 3 | - |
- FACT: the title of the gold-cube Short was changed between the 09:58 and 22:00 reads ("All Gold Ever Mined = One Cube. How Big?" -> "What If You Melted All The World's Gold? 🪙 #whatif #gold #money"); I did not make this change (user or YouTube Studio). Its views rose +299 and likes 15 -> 38 in the same window. HYPOTHESIS only (n = 1, timing overlaps with a normal late push): the "What if" framing helps; test once more on the next scale/comparison Short.
- Baarle is the Short flagged in the plan as having a weak frame 0: 26% of the median at 8 h. Decision rule stays: if its 24 h views < 50% of the median (22.10 ~14:00), border Shorts get the most unusual visual on frame 0.
- H6: from 19.10, 6 of 9 non-GTA Shorts reached ~1k or more (Aral, Libya, $100B, Russia, coin, Pheasant), gold cube 779 and Baarle 325 pending; Suez the only dud. Still consistent with H6, GTA stays off YouTube.
- Analytics (traffic sources/retention) not re-pulled; lag of ~2 days.
**TikTok and Instagram (Metricool): DATA MISSING.** TikTok: no post rows, zeros for 14-21.10 (same as the morning run); Instagram (account tiger.91353485 is connected to the brand): followers and reels empty. User is checking the connections in Metricool (21.10). Nothing invented.
**Niche outliers (TikTok + Instagram, 14-21.10, 10 creators, none repeated from before).** TikTok 690k-1.3M views (4.7-22x median), lengths 12/27/45/60/69 s; Instagram 0.8-15M views (11-716x).
- Repeating: (1) on-screen text hook on frame 0: 10 of 10; (2) sound from the first second: 10 of 10; (3) a hook that makes a claim, a myth or a "right now" question: 5 of 10 (e.g. "People say Turkey isn't in Europe", "What's happening in France right now", "Reportedly France is"); (4) lengths on TikTok mostly under 70 s (median 45 s); (5) a map zoom plus one icon/highlight on the first frame (4 of 10).
- Useful for E5 (Turkey, 24.10): a Turkey myth-vs-data reel (799k, 35x median on Instagram) used the hook "People say Turkey isn't in Europe" with a red X on the map. Our Turkey Short is already scheduled; not changed. Content not copied.

### Monitoring 22.10 10:00 MSK (vidIQ + Metricool; ~15 vidIQ credits)
**YouTube (public counts, 12 h change since 21.10 22:00; baseline median 1,245).**
| Video (published, MSK) | Age | Views | 12 h change | % of median |
|---|---|---|---|---|
| Pheasant Island (21.10 10:02) | ~24 h | 1,141 | +43 | 92% (24 h, slowing) |
| Baarle double borders (21.10 14:03) | ~20 h | 688 | +363 | 55% (late push) |
| Gold cube "What If You Melted..." (20.10 14:02) | ~44 h | 1,016 | +237 | 82% (still growing after the title change) |
| Libya (19.10 15:03) | ~3 d | 1,478 | +127 | 119% |
| Aral Sea (20.10 12:03) | ~46 h | 2,173 | +26 | 175% (plateau) |
| $100B Short (20.10 16:03) | ~42 h | 1,169 | +46 | 94% |
| Euro coin (19.10 14:03) | ~3 d | 1,190 | +43 | 96% |
| Russia (19.10 16:05) | ~3 d | 1,129 | +18 | 91% |
| Suez / $100B long | - | 11 / 3 | 0 | - |
- Baarle rule (24 h < 50% of median -> border Shorts get the most unusual visual on frame 0): at 20 h it is already 55% (688 > 622), so the rule is NOT triggered; it recovered from 26% at 8 h. Final 24 h read at ~14:00 in the evening run.
- Gold cube: +237 in 12 h after +299 the previous 12 h; the only older Short still climbing fast. "What if" title hypothesis stays open (n = 1).
- vidIQ analytics 19-22.10 (data lag ~2 days, so it covers 19-20.10 mostly): Shorts feed 2,476 of 2,713 views (91%); feed average view percentage 67.3% (baseline 62%); engaged/views 50% (baseline 52%), so about half of feed viewers swipe away. Leaders by engaged share: Libya 52% (AVP 73.4%), coin 48% (63.3%). Weakest: Russia 42% engaged and AVP 33% at 85 s (the longest Short: length probably hurts). Search 141 views (5%).
- Today's queue in Metricool: Bolivia 10:00 (status PENDING at read time), Egypt 14:00, time zones 16:00 (E7). Tomorrow: Chile 10:00, Australia 14:00, Hormuz long 15:00.
- Metadata: no errors on new uploads (Pheasant, Baarle). Ocean-floor tag fix still waits for the user's go. Nothing changed.
**TikTok (Metricool): DATA MISSING.** Post rows empty; TKEV02/07/08 return 0 or null for 16-22.10. No TikTok video is visible (Pheasant, Baarle, Aral, Libya and the rest), so no ranking. Nothing invented. User was checking the connection on 21.10.

### DNA analysis 22.10 (user request): GeoGlobeTales "Which Country Is Closest to Space?" (XpYfmHoPEAs)
Report: `map_shorts/ref_geoglobetales_2026_10_22/dna_XpYfmHoPEAs.md` (cost: ~25 vidIQ credits: video data 5, watch 10, comments 5, channel Shorts 5, transcript 5). Reference: 30.3M views, 21.9 likes/1k, 85 s; the channel's 50 top Shorts are all 11.8-61M.
- Measured: 267 words in 85 s = ~188 wpm (our Russia ~130 wpm); ~4.9 events/10 s, 12 cuts in 84 s (STRONG INFERENCE); 18 of 25 top comment threads (72%) are about one mid-video fake-out ("our planet is flat... just kidding"), top three by likes.
- Principles to test (not copied): question-superlative hook; obvious answer -> "that's wrong" -> true answer; one absurd retracted line at ~35% of the length; mechanism + one number; end on the answer, ideally as a loop. Experiment idea E7 (after user approval): one Short in this structure vs the batch median.

### Time zones Short (E7, structure of the GeoGlobeTales DNA report) - production 22.10
Voice: Lumean (ElevenLabs), 0.46 RUB (user approved the price), 67.7 s, 175 words = ~155 wpm; transcribed back with faster-whisper small.en: 175/175 words, 96% match (only digit-vs-word differences and "Wallis" heard as "Wallace", accepted). Engine65 (copy of engine64 + new overlays "chips" and "ring"); imagery Esri (WLD, FRA, MON) + Natural Earth. Render in /home/claude/v62 (not in the repo). Source: `map_shorts/timezones_2026_10_22/` (scripts.py, engine65/, timing65.json, recording_brief.md for the human-voice option, not used).

**E7 card - time zones Short (structure and look of the GeoGlobeTales reference, our topic).** HYPOTHESIS: question hook + obvious answer -> "wrong" + one retracted absurd line (Monaco) + answer at the end gets at least the median of the 19-21.10 geography Shorts (~1.1k at 24 h). CONTROL: Aral 2,147, Libya 1,351, Russia 1,111, coin 1,147, Pheasant 1,098 (median ~1.15k). TEST: this Short (68 s). METRIC: 24 h / 72 h views, vidIQ relative retention, comments per 1k (the reference had 0.25 comments per 1k views). LIMITATIONS: n = 1, new topic, voice 155 wpm vs 188 in the reference (voice not sped up on purpose: natural delivery first). RESULT: - . NEXT DECISION: if >= control median, 3 more Shorts in this structure.
Production notes: engine66 = engine65 + reference look (space plate with teal nebula and drifting dust, isometric map opening with rising pins, tracked neon title, red triangle markers, magnifier lens, red X, white captions). v2 render QC: 68.2 s, 1080x1920 30 fps, -15.2 LUFS, peak -1.4 dBFS, 177/177 words heard back (99.4%, only "Wallis" heard as "Wallace"). Voice cost 0.46 RUB.

### Time zones Short scheduled 21.10 23:54 MSK (user: "Ставь")
Metricool id 402553525 (uuid -3423952026791228371), YouTube Short + TikTok, **22.10 16:00 MSK** (best free slot: Metricool benchmark YouTube Thu 16:00 = 11,979, TikTok 1,118; free in the queue, 2 h after Egypt 14:00). AI flags on (YouTube isAiGeneratedContent, TikTok isAigc). Higgsfield media f36c42bf-7f5f-4a1a-ac9f-c91ab8a72f0c; Metricool copy size 46,037,305 bytes = the local file. Check 24 h / 72 h on 23.10 ~16:00 and 25.10 ~16:00 against E7 control median ~1.15k.
| Date | Video | Events/10 s | Hook (frame 0) | 24 h | 72 h | Principle |
|---|---|---|---|---|---|---|
| 22.10 16:00 | Which country has the most time zones? | ~5-6 | isometric map tilting + pins on Russia/USA, "MOST TIME ZONES" | | | question hook, obvious answer -> wrong, retracted joke, answer at the end (E7) |

## 2. Video log
Columns: date (MSK) | video | format | hook (frame 0) | events/10 s | cost | views 24 h | views 72 h | result / principle | confidence.

### Scheduled in Metricool (YouTube + TikTok), batch 18–23.10
| Date | Video | Format | Hook | Cost | 24 h | 72 h | Principle |
|---|---|---|---|---|---|---|---|
| 18.10 10:00 | GTA 6 Vice City vs REAL Miami | long 8:26 | — | — | | | |
| 18.10 12:00 | Madagascar has no lions | Short | | | | | |
| 18.10 14:00 | GTA s3 Tisha-Wocka | Short (E4) | | | | | |
| 18.10 15:00 | GTA s1 port slogan | Short (E4) | | | | | |
| 18.10 16:00 | Hannibal | Short | | | | | |
| 19.10 10:00 | GTA s2 Miami Circle | Short (E4) | | | | | |
| 19.10 12:00 | Suez / moon | Short | | | | | |
| 19.10 14:00 | €1 coin zoom | Short | | | | | |
| 19.10 16:00 | Libya river | Short | | | | | |
| 20.10 10:00 | GTA ep.2 guess | Short (E4) | | | | | |
| 20.10 12:00 | Aral Sea | Short | | | | | |
| 20.10 14:00 | Gold cube | Short | | | | | |
| 20.10 15:00 | Could You Spend $100 Billion? | long | — | | | | |
| 20.10 16:00 | $100B | Short | | | | | |
| 23.10 15:00 | Hormuz bypass | long 5:21 | — | | | | |

### New batch 21–24.10 (engine60, control group for E1, test group for E2)
Production: Lumean voice ≈2.14 ₽ for all 7, Esri imagery and render free. Rule applied: key visual and title on frame 0, counters show the final number at 0.0 s.
| Date | Video | Hook (frame 0) | 24 h | 72 h | Principle |
|---|---|---|---|---|---|
| 21.10 10:00 | Pheasant Island | island + ES/FR flags + title | | | |
| 21.10 14:00 | Baarle | enclaves map + title | | | |
| 22.10 10:00 | Bolivia navy | coast lost + title | | | |
| 22.10 14:00 | Egypt 95% / 5% | Nile strip + "95%" | | | |
| 23.10 10:00 | Chile long and thin | Chile over Europe + km | | | |
| 23.10 14:00 | Canberra | SYDNEY? / MELBOURNE? pins | | | |
| 24.10 10:00 | Diomede | TODAY / TOMORROW pins | | | |


### New batch 25–28.10 (engine61: E1 test group, >= 10 visual events / 10 s; first frame carries the answer, E2)
Production: Lumean voice 2.02 RUB for all 7, Esri imagery and render free. Topics from Module 14 (`ideas_v3_2026-10-18.md`), demand from other channels' videos (FACT), our result UNVERIFIED.
| Date | Video | Events/10 s | Hook (frame 0) | 24 h | 72 h | Principle |
|---|---|---|---|---|---|---|
| 25.10 10:00 | Point Roberts | 13.2 | peninsula, US + CA flags, "4 BORDER CROSSINGS" | | | |
| 25.10 14:00 | France's longest border = Brazil | 13.1 | French Guiana highlighted, "~730 KM BORDER" | | | |
| 26.10 10:00 | Peñón, 85 m border | 10.8 | rock + red border line, "BORDER: 85 m" | | | |
| 26.10 14:00 | South Africa, 3 capitals | 13.4 | 3 pins + "3 CITIES · 1 COUNTRY" | | | |
| 27.10 10:00 | Llívia | 10.5 | town, ES + FR flags, "1.6 KM FROM SPAIN" | | | |
| 27.10 14:00 | Bir Tawil | 11.4 | desert, EG + SD flags, "0 COUNTRIES CLAIM IT" | | | |
| 28.10 10:00 | Northwest Angle | 10.9 | NW Angle pin, US + CA flags, "~149 PEOPLE" | | | |

Metrics here (no per-video stayed/swiped): 24 h / 72 h views vs the 21–24.10 batch median and vs channel median (~1.2k), vidIQ relative retention, likes and comments per 1k views. Baarle (21.10) is the one with a weak frame 0: if its 24 h views are below half of the 21–24.10 median, start border Shorts with the most unusual visual.

### Single Short 24.10 14:00 — strict remake of a reference (engine63, E5)
Reference: MapTrail "Spain: The Hidden Superpower" (5wEVWjvaX2k, 196k views), DNA report `map_shorts/turkey_2026_10_24/dna_5wEVWjvaX2k.md`. Production: Lumean voice 0.49 RUB, Esri / Natural Earth / AWS terrain free, render free. Metricool id 399259968 (YouTube + TikTok), copy size matches the original.
| Date | Video | Events/10 s | Hook (frame 0) | 24 h | 72 h | Principle |
|---|---|---|---|---|---|---|
| 24.10 14:00 | Turkey: two continents | ~5-6 (reference style) | flag-filled Turkey + pin, "not just an ordinary country"; flexing character at 2 s | | | |

### Single Short 19.10 16:00 - Russia, 58 years (engine64, system of OneCriticalMoment q6L_j157rGo, E6)
Reference: OneCriticalMoment "How the Mongols Conquered Russia (Part 2)" (93.8k views, 24.7 likes/1k, 153 comments), DNA report `map_shorts/russia_2026_10_24/dna_q6L_j157rGo.md`. Production: Lumean voice 0.50 RUB, imagery/render free. Metricool id 399429455 (YouTube + TikTok), voice transcribed back 181/183 words.
| Date | Video | Events/10 s | Hook (frame 0) | 24 h | 72 h | Principle |
|---|---|---|---|---|---|---|
| 19.10 16:00 | Russia crossed a continent in 58 years | 10.8 | globe, gold Russia, "11 TIME ZONES" on frame 0 | | | |
Libya moved to 15:00 on 19.10 (user: yes). Voice regenerated 19.10 00:05 (0.49 RUB: 'Moskvitin' only, softer settings); Metricool post replaced (id 399439229), copy size matches, loudness -15.0 LUFS / -1.6 dBTP, 179 of 182 words heard back.

## 3. Experiment cards
**E1 — Visual density.** HYPOTHESIS: ≥ 10 events/10 s and no pause > 2.5 s lower the swipe share. EVIDENCE: pace vs views above (correlation only). VARIABLE: number of pop-ups, zooms, highlights. CONTROL: batch 21–24.10 (6–7.7 events/10 s). METRIC: median of 24 h / 72 h views vs control, vidIQ relative retention. WINDOW: 7 Shorts per variant. LIMITATIONS: different topics, compare medians. RESULT: — . NEXT DECISION: — .

**E2 — Answer on frame 0.** HYPOTHESIS: a number or contrast visible at 0.0 s lowers swipes vs a title over satellite imagery. CONTROL: Shorts 18–20.10 (pop-in hooks). TEST: batch 21–24.10. METRIC: median of 24 h views vs the 18–20.10 Shorts and vs the channel median ≈1.2k; vidIQ relative retention in the first quarter (baseline 0.46–0.6). RESULT: — .

**E3 — Niche title convention.** VARIABLE: "number-contrast + #geography #map" vs our style. METRIC: search share (vidIQ traffic_sources), 24 h views. LIMITATIONS: no A/B for Shorts, sequential only. RESULT: — .

**E5 — Strict reference remake / continuous camera.** HYPOTHESIS: copying a working channel's system (virtual camera across scales, character on the country at 2 s, textured fills, 1-2-word captions, ~2 SFX/10 s) gives at least the median of our cut-heavy batch. CONTROL: median 24 h / 72 h of batch 25-28.10 (10-13 events/10 s). METRIC: 24 h / 72 h views, vidIQ relative retention, likes per 1k. LIMITATIONS: n = 1, different topic. RESULT: — . NEXT DECISION: if >= control median, 2-3 more Shorts in engine63.

**E6 — Dense globe + dated campaign (OneCriticalMoment system).** HYPOTHESIS: ~10 events/10 s, number on frame 0, dated banner and a map that changes season hold attention better than the calmer MapTrail system (E5). CONTROL: Turkey (E5, 24.10) and batch 25-28.10. METRIC: 24 h / 72 h views, vidIQ relative retention, comments per 1k. LIMITATIONS: n = 1, new topic, queue of 19.10 is geography-only (H6 test) so the result also depends on H6. RESULT: - . NEXT DECISION: pick the system with the higher median for the next batch.

**E4 — GTA series.** HYPOTHESIS: GTA Shorts reach another audience and don't hurt geography. METRIC: 24 h views of 4 GTA Shorts 18–20.10 vs geography Shorts on the same days. DECISION 20.10: if GTA median < 50% of geography median, no new GTA until 19.11. RESULT 20.10 22:00 MSK (YouTube public counts, ~24-30 h): GTA Shorts that were on YouTube in 18-20.10: slogan (s3) 523, flea (s1) 80 -> median ~300 (s2 and ep.2 went TikTok-only, so not on YouTube). Geography/other Shorts of 18-20.10: Madagascar 44, Hannibal 65, Suez 10, coin 1,043, Libya 1,261, Russia 1,057, Aral 1,713, gold cube 437, $100B Short 975 -> median 975. GTA/geography = ~31% (< 50%): the rule is triggered (FACT). BUT the split by day reverses it: on 18.10, next to GTA, GTA 300 vs geography (Madagascar, Hannibal) 55 -> GTA 5x higher; from 19.10, with no GTA on YouTube, geography reaches ~1k. So the sign depends on the window (FACT); n = 2 GTA Shorts, so no statistical weight. Counter-hypotheses: (a) topic demand: GTA is hyped before 19.11 but the audience may be the 'gaming' one that does not watch maps afterwards (H6); (b) hook: the two GTA Shorts had question/claim hooks, geography winners have a 'why' question or a loop; not isolated; (c) publish time: 18.10 GTA 11:00-12:00 and geography 12:00 and 16:00 MSK, 19-20.10 all at 09:00-16:00, differences small, not the cause. DECISION: follow the rule: no new GTA on YouTube until 19.11 (already in force; also the H6 test), GTA stays TikTok-only. TikTok check: GTA median (465, 227, 66, 0) = ~146 vs geography median (545, 465, 346, 299, 282, 109) = ~322 -> 45%, also below 50%, with the newest GTA copies (85 s quiz 66, Tequesta 0) weakest: recommend the user decides whether to pause remaining TikTok GTA posts until the 19.11 launch; not changed by me. CONFIDENCE: medium for 'GTA hurts YouTube geography' (H6), low for TikTok.

## 4. Principles (confirmed / rejected)
| Date | Principle | Evidence | Confidence |
|---|---|---|---|
| 17.10 | Daily views follow uploads: no upload → views drop ~40× (7.10: 4,376 vs 11.10: 100) | V daily | FACT (pattern), cause HYPOTHESIS |
| 17.10 | Peak window 10–16 MSK | user observation + Metricool best time | ESTIMATE |

## 5. Decision journal
| Date | Hypothesis | Change | Result | Conclusion |
|---|---|---|---|---|
| 17.10 | First 3 s are the main leak (44.4% swipe) | 7 new Shorts rebuilt with key visual on frame 0 | pending (21–24.10) | |

### 21.10 Nexlev check for reference jTJ2UFF3B0I
rajography is a creator-owned drone channel (137K subs, avg ~806k views, no 3x outliers). Copies of its "tsunami couldn't destroy this temple" claim got tiny views, and the small-channel "satellite" search returned nothing. Conclusion: the reference's reach is footage- and channel-driven, not claim-driven; a satellite Maldives Short is a low-confidence experiment (HYPOTHESIS), awaiting user go (animation approval).

### 21.10 Maldives Short built (E8, awaiting publish go)
Silent 17 s Short from the rajography DNA report: globe zoom + 3 s text hook, 5 hard cuts on the beat (124 BPM), pan along the airport runway, number card (1.5 m vs adult ~1.7 m), pull-out to globe, loop. Esri imagery, synthesized music, 0 RUB, no AI voice. LUFS about -16.7 (mean -13.5 dB, peak -1.6 dB). Source: map_shorts/maldives_2026_10_21. Facts hedged: only the average elevation is shown because the highest-point sources conflict. Not yet uploaded or scheduled: free slots 28.10 14:00/16:00 (suggested), user go pending.

### 22.10 Maldives Short rebuilt to the reference (v2)
User asked to re-read the master prompt and match the reference. Conformity check found v1 broke six rules (neon title, text all video long, SFX, 5 cuts, flat top-down only, no top-down finish). v2: engine68 (oblique pseudo-drone camera), single white text hook, 8 cuts on the beat (124 BPM, 19.8 s), 7 Maldives places (archipelago, Malé, Velana, Thulusdhoo, Fuvahmulah, Gan, Fuvahmulah top-down), music only, LUFS -14.8. Table in map_shorts/ref_geoglobetales_2026_10_22/dna_jTJ2UFF3B0I.md. Not uploaded or scheduled; user go pending.

### 22.10 Lofoten Short built (E9, awaiting publish go)
User: keep the Maldives Short, make another one like the reference with real drone. Lofoten (north of the Arctic Circle): real Pexels portrait drone clips found via vidIQ generate_broll (about 8 credits in total), 7 cuts on the 124 BPM grid, globe zoom with one white text block, music only (A minor, own melody), 0 RUB, no AI footage, no AI voice. LUFS -15.7. Last shot is steeply down, not a true nadir (no such clip). Source: map_shorts/lofoten_2026_10_22. Not uploaded or scheduled.

### 22.10 Lofoten Short: closer zoom like the reference
User: zoom must come closer, as in the reference. Before: globe zoom stopped at continent scale and cut to the drone. Now: globe 0-1.35 s, 0.2 s crossfade to a flat satellite map that falls at constant zoom rate from the region (span 25 deg) down to the coast at Reine (span 0.022 deg, about 2.4 km), imagery NOR/LOF/LO2/MID/REI from Esri, then the hard cut to the drone shot of Reine at 2.85 s. Same hook text. Maldives left as is (its globe zoom is shorter; offer to deepen it the same way).

### 22.10 Lofoten v3: camera moves and look like the reference
User: camera movement and visuals like the reference. Re-watched the reference with vidIQ (10 credits). Changes: zoom dives to ~0.9 km (RE2 imagery) instead of 2.4 km; shot lengths 4/3/4/1/1/4 s with the described moves (ascend, lateral pan, high forward drift, 1 s close-up, 1 s sweep, downward finish); footage grade saturation +14% / contrast +5%; audio accents on every cut. Limit: no true nadir descent clip for Lofoten.

### 22.10 QC pass ("Проверь") on Lofoten v3 and Maldives v2
Measured with ffmpeg (scene detect, ebur128, freeze/black detect) and a per-shot motion metric.
Found and fixed: (1) Lofoten cuts were 2-3 frames ahead of the kick (cut times were beat minus 0.05 s plus rounding) -> cuts now on exact beat frames 87/203/290/406/435/465, measured offset +20...50 ms incl. detector bias; (2) harbour shot almost static (motion 0.77) -> digital push-in 1.08x->1.25x with slight counter-clockwise yaw on the 4K source (no upscaling); (3) zoom end too abrupt -> short settle in the last 0.3 s, ends ~1.2 km top-down; (4) Lofoten loudness -15.9 LUFS mono -> -13.6 LUFS stereo, peak -1.3 dBFS; (5) Maldives audio shifted 35 ms earlier so its cuts sit on the kick, -14.8 LUFS.
No black frames, no freezes, durations 19.78 s, 1080x1920 30 fps. Remaining limits: no true nadir finish for Lofoten; Esri mosaic seams visible for a few frames at the end of the satellite dive.

### 22.10 Lofoten v7: two AI shots (user approved Veo 3.1 Lite, chose WaveSpeed)
APIpod: "insufficient quota" (nothing charged). WaveSpeed: Nano Banana 2.1 Edit keyframe $0.038 + 2 x Veo 3.1 Lite 4 s $0.20 = $0.44 (balance 3.297 -> 2.860; price was higher than the APIpod quote of ~$0.18 because WaveSpeed charges $0.20 per 4 s clip; still within the user's go for Veo 3.1 Lite, noted for the user). AI flags (YouTube isAiGeneratedContent, TikTok isAigc) must be ON for this Short. Source: map_shorts/lofoten_2026_10_22/engine69_v7.

### 22.10 Authenticity audit (user: "Проверяй на Аутентичность") - Lofoten v7b
Report: map_shorts/lofoten_2026_10_22/authenticity_audit_2026_10_22.md. Verified: Arctic Circle claim, footage identity (3 of 4 clips titled Reine/Reinebringen, 1 titled Lofoten), no identifiable people in the used segments, Pexels credits. Partly verified: "sea doesn't freeze" (no measured ice statistic), Mixkit music licence (text not read, Content ID unconfirmed), Esri terms (not verified). Fixed: on-screen "AI-GENERATED SHOT" labels on both AI shots (+ Esri credit on the finale), description wording. YouTube inauthentic-content risk assessed moderate for monetisation (stock-heavy), low for removal.

### 22.10 New standing rule: authenticity check on every video
User: "Создай правило себе проверка обязательно на все ролики". Saved as the project skill `.claude/skills/authenticity-check/SKILL.md` (9-point checklist, verdict PASS/FIXED/BLOCK, audit file per video), the repo-level `CLAUDE.md`, and hooks in `cinematic-youtube` (mandatory gate) and `youtube-growth-engine` (Mode 3: no READY without the check). First applications: Lofoten v7b (audit 22.10) and Maldives v3 (hook "1.5 m high" corrected to "1.5 m on average", description notes the 1.8 m figure). Videos already published or scheduled before the rule (Bolivia, Egypt, Chile, Australia, time zones, Hormuz long) have NOT been audited yet: backlog, proposed next.

### 22.10 15:30 Retroactive authenticity pass on the queue (user: "если есть что исправить, исправь")
Report: map_shorts/retro_authenticity_audit_2026_10_22.md. Fixed: time zones description (13 explained with both sources; post id now 403094439, slot 22.10 16:00 kept), Peñón description (1930 vs 1934, "shortest" hedged; id 403094507, slot kept), Egypt YouTube description (5% is an approximation; vidIQ update, 5 credits; published TikTok text not editable). Verified OK: Chile, Point Roberts, Northwest Angle, Llívia, ICJ ruling. Not re-verified: Australia, Diomede, France-Brazil, South Africa, Bir Tawil, Turkey, Hormuz long, Bolivia details. Flags: all posts have the AI flags on.

### 22.10 Esri licence check (user: "Проверь")
Report: map_shorts/esri_licence_check_2026_10_22.md. Esri static-map terms list personal/internal/marketing/academic/government uses; anything else, with "commercial monetization" as an example, needs Esri's permission; video is not addressed; binding E204/E300 documents could not be opened. Channel is NOT monetised (Nexlev). Verdict: NOT VERIFIED, real risk before monetisation. Actions: ask Esri for written permission (draft in the report), keep attribution, use open imagery where the zoom allows (NASA, Landsat; not EOX cloudless), decision needed on rooftop-level Esri dives. Skill authenticity-check updated.

### 22.10 Esri-free rework started (user: "делаем без рисков, ролики проверь все и переделывай по одному")
Pipeline: `map_shorts/open_imagery/` (NASA GIBS Blue Marble + Copernicus Sentinel-2 L2A via AWS STAC, SCL cloud mask, water tone matching) plus `hires.py` for close zooms: USGS NAIP (US, public domain), IGN France orthophotos (Licence Ouverte Etalab by default per cartes.gouv.fr CGU, to be re-read per dataset), IGN Spain PNOA (CC BY 4.0, stated in the WMS capabilities; no coverage at Peñón de Vélez). Done and replaced in Metricool (media + credits + audit file each): Time zones (23.10 16:00), Chile (23.10 10:00), Australia/Canberra (23.10 14:00), Diomede (moved to 02.11 10:00: the voice says 21 h, true only outside US daylight saving which ends 1 Nov). Credit text: "Contains modified Copernicus Sentinel data 2023-2026" (southern-hemisphere summer scenes are from 2026). Lesson: shared /tmp file between parallel GIBS fetches corrupted images (fixed, per-process temp); a mid-sea Sentinel tone is near black with tile seams (flattened by fix_sea). Remaining Esri in the queue: Hormuz long (tiles being rebuilt from Sentinel-2), Turkey, Point Roberts, France-Brazil, South Africa, Peñón, Bir Tawil, Llívia, NW Angle, Maldives, Lofoten; published Bolivia/Egypt/earlier videos still carry Esri (decision pending with the user).

### 22.10 17:00 MSK Checkpoint 3 (Mode 4, vidIQ channel_videos short, YouTube only; TikTok data not available)
Baseline median 1,245 views. Ages are real (the routine said 24 h; Pheasant is 7 h old):
- Pheasant "This Island Changes Country Every 6 Months" (21.10 10:00): 1,152 views at ~7 h, 38 VPH, breakout 1.48. Already ~93% of the median: the strongest new map Short of the week so far. E1 (>=10 events per 10 s, loop ending) holds on this one.
- Baarle "The House with Two Borders" (21.10 14:00): 703 views at ~27 h, 27 VPH, 9 likes. Below median, as predicted by the weak frame-0 risk. E2 (hook/frame 0) -> frame 0 of Baarle needs a stronger first image next time.
- Bolivia (22.10 10:00): 163 at 7 h (27 VPH). Egypt (22.10 14:00): 558 at 3 h (279 VPH): the best early velocity so far; check at 24 h.
- 72 h batch 18-19.10: Libya 1,500 (breakout 9.2), Russia 58 years 1,143 (3.8), coin zoom 1,260 (7.7), Aral 2,175 (6.2, 20.10), $100B 1,172, gold 1,024. Weak: Hannibal 65, Madagascar 44, GTA flea market 82 / Miami slogan 524, MOON ship 11. Geography/map Shorts with a visual hook beat GTA/history here.
Schedule: Metricool holds posts through 28.10 (Diomede moved to 02.11); the batch from 29.10 is NOT made yet. Esri-free rework is running, so new batch work waits for it.
Monetisation (main goal): none of these changes the YPP position yet; keep the channel clean (imagery licences, AI labels) while views grow.

### 22.10 evening: Esri-free rework of the queue finished except Peñón
Replaced media + credits + audit file (each PASS, some facts PARTLY): Time zones (23.10 16:00), Chile (23.10 10:00), Australia (23.10 14:00), Hormuz long (23.10 15:00, 5:22, tiles rebuilt from Sentinel-2 + Blue Marble: 95 cells, 1,557 tiles), Turkey (24.10 14:00), Point Roberts (25.10 10:00, USGS NAIP), France-Brazil (25.10 14:00, IGN France), South Africa (26.10 14:00), Llívia (27.10 10:00, PNOA CC BY 4.0 + IGN), Bir Tawil (27.10 14:00), NW Angle (28.10 10:00; NAIP dropped, striping over water), Diomede moved to 02.11 10:00. Peñón de Vélez set to DRAFT (26.10 10:00): no open imagery finer than 10 m exists for the rock (PNOA has no coverage), the closest zooms are unusable; options: stylised drawn finale, shorter zoom, or replace the topic. Still with Esri: published Bolivia, Egypt and the earlier videos (Russia, Libya, Aral, Pheasant, Baarle ...), Maldives and Lofoten (not scheduled). Lessons: the container disk allowance filled up once (old whisper cache and render parts), which truncated a concat; keep >2 GB free and encode straight from the concat list; S2 mosaics need scene tone matching and fix_sea; NAIP over open water produces stripes.

### 22.10 22:00 MSK Scheduled check (vidIQ + Metricool TikTok; 20 vidIQ credits, balance was 1,941 before)
YouTube (user_videos, newest 25): all public, nothing private or scheduled on YouTube (the queue lives in Metricool, through 28.10; Peñón is a draft). Last 12 h: Bolivia 252 views / 9 likes at ~12 h (weak, below the 1,245 median); Egypt 1,226 / 11 at ~8 h (best new Short, ~155 VPH average, will pass the median tonight; check at 24 h). Pheasant 1,158 (flat since 17:00: +6), Baarle 724, Aral 2,189, Libya 1,561, Gold 1,028, $100B Short 1,192. Long videos: $100B long 3 views, GTA long 49, Panama 37 (no traction). Analytics 19-22.10 are lagged (Aral, Egypt, Pheasant missing from top_videos): use only as directional. Libya 1,251 views, 52% engaged, 73% avg viewed, 2 subs; coin 1,035, 48% engaged, 63%; Shorts feed = 2,476 of ~2,715 views (91%), 50% engaged, 67% avg viewed (baseline 52% / 62%: unchanged); search 141 (5%); subscribers gained in the period: 3 in total. No avg-swipe-away figure was returned by these calls.
TikTok (Metricool, 15-22.10; column mapping inferred, no headers returned): median views of the copies with data (15 posts) = 283; nothing at 3x. Leaders by views: Hannibal 549 (20 likes), Madagascar 500 (14), GTA slogan 467 (14), Libya 371, coin 303, Baarle 301. Engagement per 1k views: gold 57, $100B 44, Libya 40, Hannibal 36, Russia 35; shares: only Russia has 1; comments: only Aral has 1. Avg watch 9-15 s on 24-85 s videos; For You share 88-100%; Madagascar has the highest search share (12%). Daily views fell 1,744 (18.10) -> 1,067 -> 1,027 -> 577 (21.10): no follower growth in the daily rows (0 new). DATA MISSING: Egypt copy, Tequesta (0 views, probably delay), Bolivia reach (0), GTA ep2/real-places (3 and 0 views). Note: Hannibal and Madagascar are the TikTok leaders but near-zero on YouTube (65 and 44): TikTok likes history and animal scenes more than YouTube Shorts does.
Outliers (vidIQ, 5 credits, TikTok + Instagram, last 7 days, maps/geography): repeating techniques: (1) frame 0 = a map plus a myth or counter-intuitive claim ("People say Turkey isn't in Europe", "Africa is 14x bigger than you think", "Two countries. One roof."), text equals the first spoken words; (2) fast animated map, many cuts/zooms, SFX, voice + music; (3) looped ending in 4 of 5 TikTok outliers; (4) TikTok map outliers run 68-162 s, not only 40 s; (5) one outlier on the Turkey 3%-in-Europe fact at 841K (37x the creator's median) uses the myth-rebuttal hook; ours (scheduled 24.10) leads with "country on two continents".
Metadata: nothing changed (no clear errors found with publication text available). Possible cleanup, not done: "Why the ocean floor is constantly expanding" has off-topic tags (space documentary, asia, europe).
Next steps proposed: (1) reframe the Turkey Short title/first line as a myth rebuttal ("People say Turkey isn't in Europe") before 24.10 (needs re-render of hook text and a new authenticity pass); (2) Egypt-style hooks (a striking ratio in the title) and loop endings for the 29.10 batch; (3) decide on Peñón and the published Esri videos (open questions to the user). Monetisation: no change in position this check; the sub gain is 3 in 3-4 days.

### 23.10 01:10 MSK Turkey v2 (myth hook) replaced in Metricool
Change per the 22.10 outlier search: new hook "People say Turkey isn't in Europe. But about three percent of its land is..." + on-screen "NOT IN EUROPE?" and a "3% IN EUROPE" counter (East Thrace lit). New Lumean voice-over for the whole Short: 0.51 RUB (preview price; user approved about 0.3 RUB; the first order's polling dropped on a proxy reset, the order was found by name and downloaded, one order only, no double charge). Video 69.6 s, -14.0 LUFS, QC clean. Post uuid 2041355585894893073 (24.10 14:00, YouTube + TikTok), new title "People Say Turkey Isn't in Europe. Here's the Map", description and tags updated, AI flags ON. Audit appended to turkey_2026_10_22/authenticity_audit_2026_10_22.md (PASS). Measure: compare Turkey v2 views at 24 h against the 283 TikTok median and the 1,245 YouTube median; if the myth hook wins, apply it to the 29.10 batch (Egypt-style ratio titles, loop endings).

### 23.10 01:20 MSK Esri videos: keep published, delete before monetisation (user decision)
User: "Публикуй, потом перед монетизацией удалим". Peñón de Vélez un-drafted and scheduled as made (26.10 10:00, Esri imagery, description credits Esri). Published Esri videos stay public. Checklist of what to delete or replace before the YPP application: map_shorts/esri_delete_before_ypp.md. Risk accepted by the user: Esri terms for monetised use are unclear (NOT VERIFIED); removal before applying is the mitigation. New videos stay Esri-free.

### 23.10 10:00 MSK Scheduled check (vidIQ + Metricool TikTok; 15 vidIQ credits, no outlier search: that runs in the evening check)
YouTube (user_videos, newest 25): all public; nothing private/scheduled on YouTube. Metricool queue intact: 23.10 Chile 10:00, Australia 14:00, Hormuz long 15:00 (YouTube only), Time zones 16:00; 24.10 Turkey v2 14:00 (24.10 10:00 slot is EMPTY: Diomede moved to 02.11); 25.10 Point Roberts, France-Brazil; 26.10 Peñón (10:00, un-drafted) and South Africa; 27.10 Llívia, Bir Tawil; 28.10 NW Angle; 02.11 Diomede. Nothing from 29.10 except Diomede on 02.11.
Views (median baseline 1,245): Egypt 1,345 at ~23 h (+119 since 22:00; passed the median, best of the new batch), Bolivia 335 (+83 in 12 h, weak), Baarle 740, Pheasant 1,165 (flat), $100B Short 1,198, Aral 2,205, Libya 1,608, Russia 1,187, gold 1,028. Long videos: 3 / 49 / 37 views.
Analytics 20-23.10 (lagged, directional): Aral 2,113 views, 54% engaged, 63% avg viewed; $100B 1,096, 36%, 66%, 1 sub; Russia 1,072, 53%, 53%; gold 483, 45%, 59%. Traffic: Shorts feed 4,668 of ~5,017 (93%): engaged 48%, avg viewed 60.8% (baseline 52% / 62%: flat); search 213 (4%); subscribers gained in the period: 1.
TikTok (15-23.10, same column inference as before): views Egypt copy 294 (10 likes; was DATA MISSING), Bolivia 277, Baarle 305, Pheasant 277, $100B 293, gold 265, Aral 282, Libya 375, Russia 284; leaders still Hannibal 549, Madagascar 507, GTA slogan 467. Median of the copies ~284: no video at 3x (needs ~850). Daily views flat ~570-580 on 21-22.10 after 1,000-1,750 on 18-20.10. New followers in the daily rows: 0-1. Still DATA MISSING: Tequesta (0), GTA ep2/real-places (3/0).
Metadata: no clear errors found, nothing changed. Reminder: tomorrow's Turkey v2 (myth hook) is the first test of the outlier hook patterns; read it at 24 h on 25.10 and compare against Egypt (best YouTube) and the 284 TikTok median.
Next: (1) fill the empty 24.10 10:00 slot and the 29.10+ batch (Esri-free, myth/ratio hooks, loop endings) once the user confirms; (2) re-read Chile/Australia/Hormuz/Time zones after they publish today; (3) Peñón goes out 26.10 with Esri (user decision), add it to esri_delete_before_ypp.md after.
Monetisation (main goal): subscribers +1 in 3 days; views are on a plateau around the 1.2-1.4K ceiling per Short; no step toward the YPP thresholds yet.

### 23.10 22:00 MSK Scheduled check (vidIQ + Metricool; 20 vidIQ credits incl. 5 for the outlier search)
PUBLISHING FAILURE (found this run): in Metricool, Australia (23.10 14:00, YouTube+TikTok), Hormuz long (15:00, YouTube) and Time zones (16:00, YouTube+TikTok) have status ERROR on both networks: "You have reached your Metricool account limit." Only Chile (10:00) published (YouTube kclVOcCkPyA, TikTok 7699755083449257229). That is why the three are absent from the newest-14 vidIQ list. Cause is a Metricool plan/post-count limit (plan details are not exposed by getBrandSettings: NOT VERIFIED which limit). Everything from 24.10 (Turkey v2, Point Roberts, France-Brazil, Peñón, South Africa, Llívia, Bir Tawil, NW Angle, Diomede 02.11) is still PENDING and is expected to fail the same way until the limit is cleared. Nothing was re-posted by hand (would duplicate once the limit lifts, and changes the publishing path: needs the owner's word). Final files are still on disk (/home/claude/v28, v60, v62) if a direct upload is chosen.
Side note: Time zones and Hormuz long descriptions in Metricool still say "Copernicus Sentinel data (2023-2025)" while the on-screen credit says 2023-2026; align the text before they publish.
YouTube (user_videos newest 14): Chile 105 views / 2 likes at ~15 h (07:03Z, weak start; Chile hook is a statement, not a myth/ratio). Egypt 1,416 / 16 (best of the new batch), Bolivia 447 / 20, Baarle 746, Pheasant 1,167, $100B Short 1,215, gold 1,029, Aral 2,214, Russia 1,191, Libya 1,607, coin 1,308. Long videos 3 / 49 / 37. Analytics 21-23.10 (top_videos, traffic_sources) returned no rows (lag): no baseline comparison this run.
TikTok (Metricool 17-23.10): no new rows vs the morning check; copies of Chile/Australia/Time zones: DATA MISSING (Australia and Time zones never published). Median ~284, no video at 3x.
Outliers (vidIQ TikTok+Instagram, 5 credits): repeating techniques (not copied): quiz/countdown overlays, a counter in the hook ("She had 38 babies"), myth/question text equal to the first spoken words, 9-41 s loop-friendly map graphics, "what if" 3D, small accounts with 100-400x scores. Consistent with the Turkey v2 myth hook now in the queue.
Metadata: no clear errors found, nothing changed.
Next: (1) owner checks the Metricool plan/limit (or tells me to upload directly via vidIQ); (2) after the limit clears: re-schedule Australia/Hormuz/Time zones into free slots (24.10 10:00 is empty) and fix the credit year in two descriptions; (3) new batch from 29.10 only after the queue actually publishes.
Monetisation (main goal): publishing is the bottleneck right now: 3 of 4 planned posts for 23.10 did not go out; views per Short on the plateau 1.2-1.4K, subscribers +1 in 3 days.

### 23.10 23:16 MSK Failed posts re-scheduled (Metricool limit still NOT confirmed lifted)
Metricool accepted the updates and set status PENDING (not a proof that the limit is gone; the real test is the first publish): Time zones -> 24.10 10:00 (the empty slot; YouTube+TikTok), Hormuz long -> 24.10 16:00 (YouTube only), Australia -> 29.10 10:00. Descriptions of Time zones and Hormuz long now say Copernicus 2023-2026 (matches the on-screen credit). Check at 24.10 10:30 MSK: if Time zones shows ERROR again, the plan limit is still in force and the owner must fix the plan; do not re-upload by hand without the owner's word. Queue now: 24.10 10:00 Time zones, 14:00 Turkey v2, 16:00 Hormuz long; 25.10 Point Roberts, France-Brazil; 26.10 Peñón, South Africa; 27.10 Llívia, Bir Tawil; 28.10 NW Angle; 29.10 Australia; 02.11 Diomede.

### 23.10 ~23:40 MSK Thumbnails (user: "Загружай красивые кликабельные обложки")
Checked the current thumbnails of the 4 long videos: Panama (custom, "WATER DROPPING"), No.1 company (custom), GTA Vice City vs Miami (custom, uses a real Miami satellite crop: Esri question, see esri_delete_before_ypp.md) and "Could You Spend $100 Billion?" (QPkO6HzLpmA): auto frame with small text, the weakest. Made a new cover from the film's own graphic (the $100B bill stack that reaches ~110 km, past the 100 km space line; text "$100 BILLION REACHES SPACE", 1280x720, 143 KB, no stock or AI imagery, no paid generation) and uploaded it with vidiq_update_video_thumbnail (5 credits; status updated). Source: map_shorts/thumbnails/spend100b_long_C.jpg (+ .py). NOT VERIFIED: how it renders on YouTube and its CTR; read impressions CTR in Studio after 48 h. Shorts were not touched: a custom thumbnail set through the API does not show in the Shorts feed. Hormuz long: covers A ("1/5 OF WORLD OIL STUCK") and B ("THE BACKUP ROAD") already exist in map_shorts/hormuz_bypass/ (AI-generated, labelled in the description); upload one after the video publishes (A/B test in Studio). vidIQ credits this step: 10.

### 24.10 10:00 MSK Scheduled check (vidIQ + Metricool; 15 vidIQ credits, no outlier search: evening only)
LIMIT CONFIRMED STILL ACTIVE: Time zones (re-scheduled for 24.10 10:00) went to ERROR again on both networks at 10:00: "You have reached your Metricool account limit." Nothing published today so far. Queue behind it (Turkey v2 14:00, Hormuz long 16:00, 25-28.10 Shorts, Australia 29.10, Diomede 02.11) will fail the same way. Owner action needed (Metricool plan/limit, or manual upload in Studio, or wait for 1 Nov if the cap is monthly: NOT VERIFIED which).
YouTube (user_videos newest 12): nothing new since Chile (23.10 07:03Z). Chile 109 views / 2 likes at ~27 h (was 105 at 15 h: dead; statement hook, no ratio/myth). Egypt 1,437 / 16 (best of the batch), Bolivia 502 / 23, Baarle 748, Pheasant 1,186, $100B Short 1,231, gold 1,030, Aral 2,232, Russia 1,191, Libya 1,608, coin 1,309. Long: $100B 3 views (new cover uploaded 23.10, read CTR after 48 h).
Analytics 21-24.10 (lagged, directional; only 8 videos with data): Pheasant 1,146 views / 538 engaged (63% avg viewed), Baarle 698 / 245 (91% avg viewed: high retention, low engaged share), gold 538 / 267 (79%, 3 subs: the only subscriber source besides Aral 1), Libya 196, coin 148. Traffic: Shorts feed 2,738 of 2,964 (92%), engaged 45%, avg viewed 69.7% (baseline 52% / 62%: viewed share up, engaged share down); search 150 (5%); subscribers gained in the period: 4 total (3 from the gold cube, 1 Aral).
TikTok (Metricool 17-24.10): same rows as 23.10 (latest day 22.10: 571 views, 1 new follower): no new data; copies of Chile and everything after 22.10 are DATA MISSING. Median ~284, no video at 3x.
Metadata: nothing changed (no clear errors).
Monetisation: publishing blocked; 4 subscribers in 4 days (gold cube = the best subscriber converter: "what if" scale format with 3D).

### 24.10 17:00 MSK Checkpoint 4 (Mode 4 review, 21-24.10 batch: E1 control, E2 first test; 10 vidIQ credits)
Data (vidIQ user_videos 24.10 ~17:00 MSK; baseline median 4-15.10 = 1,245): Pheasant 1,195 (3 days; was 1,158 at 22.10 22:00: flat), Baarle 748 (724 -> 748), Bolivia 516 (24 h: ~330; 3 days 516), Egypt 1,443 (the only one above the median, +16%), Chile 113 at ~34 h (105 at 15 h: dead). Median of the four measurable 21-22.10 Shorts = ~970, below 1,245; none near 3x. Canberra and Diomede have NOT published (Metricool account limit; Canberra moved to 29.10, Diomede to 02.11), so E2 (myth/ratio hook, Turkey v2) is UNTESTED: Turkey v2 14:00 and Time zones 10:00 and Hormuz long 16:00 all ERROR (limit). Audience retention for Egypt: empty (analytics lag), NOT VERIFIED. Analytics 21-24.10 earlier: Pheasant 63% avg viewed, 47% engaged; Baarle 91% avg viewed but only 35% engaged (many swipe-aways in the first seconds: weak frame 0, consistent with the E1 hypothesis); gold cube 3 of the 4 new subscribers.
Verdict: E1 (first-frame/density) = NO measurable uplift over the baseline in this batch (3 of 4 below the median); not refuted either (n=4, mixed topics). E2 = not run.
Counter-hypotheses checked: (a) publish hour: Chile and Pheasant both went at 10:00 MSK, 113 vs 1,195, so the hour is not the cause; (b) topic: the Pacific War pair (Bolivia 516, Chile 113) is the weakest, Egypt's ratio ("95% live on 5%") the strongest: the hook type and topic dominate, not the hour; (c) series fatigue: 4 border/country Shorts in 3 days with the same visual look; (d) NEW risk: Chile and Canberra are the first Esri-free renders (Blue Marble/Sentinel look flatter than Esri); Egypt/Bolivia/Pheasant/Baarle used Esri. n=1, so NOT a conclusion, but the Esri-free look may cost swipe retention: test on the next ratio-hook video in the Esri-free look before drawing any conclusion; (e) metadata confound: Chile's YouTube title is now "This country is just a line 💀 #geography #chile #shorts" with extra tags, and the $100B long is now titled "The Reality Of Having $100 Billion: It's Not What You Think": neither was changed by me; someone changed them in Studio/vidIQ after publishing (when: unknown). I did not touch them. Chile's low result therefore cannot be tied to the original title.
Keep: ratio/number hooks in the title (Egypt), 3D "what if" scale videos (gold cube = best subscriber converter), 40-65 s map Shorts, AI/credit labelling. Change: frame 0 of border Shorts (a visual hook, not a flat map), vary topics (not 4 borders in a row), put the number in the first 1.5 s. Stop: statement-only hooks with no contrast ("This country is over 4,000 km long"), topic pairs from the same history thread back to back. Next experiment: the myth hook (Turkey v2) as soon as publishing works, then compare against Egypt (1,443) and the TikTok median 284. Next video: a "what if" 3D scale Short or a ratio-title map Short.
Proposed topics for the 29.10+ batch (each needs a source check and the authenticity gate before production): (1) "90% of Canadians live near the US border" style population-concentration map (ratio hook, check the exact figure); (2) a 3D "what if" scale video (all the world's water in one ball, or all the ice melted: sea-level number); (3) "Africa is bigger than China + India + USA + Europe" style size comparison on a map (own graphic, check the area figures); (4) Baikal holds ~20% of the world's unfrozen fresh water (check); (5) "Why does the Nile flow north" myth-rebuttal hook. Waiting for the owner's go before any production.
Blocker (unchanged): Metricool account limit; queue stalled since 23.10 14:00. Monetisation: 4 subscribers in 4 days; blocked publishing is the main drag.

### 24.10 22:00 MSK Scheduled check (vidIQ + Metricool + outlier search; 10 vidIQ credits)
PUBLISHING: nothing went out today. Time zones (10:00), Turkey v2 (14:00), Hormuz long (16:00) = ERROR "Metricool account limit" (both networks). Still pending: 25.10 Point Roberts 10:00, France-Brazil 14:00 (expected to fail the same way), 26-28.10 Shorts, Australia 29.10, Diomede 02.11. Owner action needed (plan limit); no manual upload without the owner's word.
YouTube (user_videos newest 8): Chile 213 views / 8 likes (was 113 at 17:00 MSK: +100 in ~5 h; its title is now "This country is just a line 💀 #geography #chile #shorts" and tags were extended by someone other than me: a weak signal that a punchier title helps, n=1, change time unknown), Egypt 1,462, Bolivia 520, Baarle 751, Pheasant 1,197, $100B Short 1,236, gold 1,031. $100B long 4 views (title changed by someone to "The Reality Of Having $100 Billion: It's Not What You Think"; new cover from 23.10). No analytics report this run (lagged; saved credits).
TikTok (Metricool 18-24.10; column mapping inferred): Chile copy now has data: 286 views, 7 likes (47 s). Views by copy: Madagascar 593 (15 likes, TikTok leader), Hannibal 549 (20), GTA slogan 467, Libya 376, Baarle 319, Egypt 298, Bolivia 282, Chile 286, Pheasant 279, Aral 286, Russia 284, $100B 293, gold 266. Median ~284; nothing at 3x (needs ~850). Engagement per 1k views: Hannibal 36, gold 57 earlier, Libya 40; shares: only Russia 1; comments: none new. Avg watch 9-19 s on 40-85 s videos. Daily views: 21.10 598, 22.10 580, 23.10 286 (partial); no day after 23.10 in the data. DATA MISSING: all days after 23.10, Tequesta (0), GTA ep2/real-places.
Outliers (vidIQ TikTok + Instagram, last 7 days, 5 credits). Repeating techniques (2+ videos each, content not copied): (1) hypothetical "what if" map simulations of 70-117 s with fast cuts/zooms, SFX and music (Mexico takes over the Americas 696K = 11.8x; "oldest country wins" 969K = 7.8x; IG 3D "jump 2x" 797K = 12.7x): the same family as our gold-cube "what if" video that converts subscribers best; (2) frame-0 text that is a question and equals the first spoken words ("What did the Romans call your country?" 2.4M = 21.9x; "What Country Is This? Level: Very Easy" 4M = 29.7x on IG) with a countdown for the viewer to guess; (3) a rapid zoom from the globe to the subject in the first 2 s ("And this is Madagascar", 972K = 8.3x; an obscure-island Google Earth zoom 2.1M = 24.5x); (4) loop-friendly endings; (5) short 23 s map-manipulation clip (1M = 29.5x) next to 68-117 s explainers: duration is not the lever, hook and escalation are. Small accounts (5-36K followers) hit 8-30x their median, so no channel-size ceiling. Note for us: Madagascar is also our TikTok leader (593).
Metadata: nothing changed. The Chile and $100B long title/tag edits were made by someone else; I left them.
Next steps: (1) owner resolves the Metricool limit; (2) next batch (after the go): a "what if" map/3D escalation video and a guess-the-country countdown Short, each with the question as frame-0 text equal to the first spoken words; (3) read Chile's new title effect again at 48 h.
Monetisation: publishing blocked since 23.10 14:00; 4 subscribers in 4 days; best subscriber format = "what if" 3D scale.

### 24.10 22:30 MSK Zernio connected and first test post (owner approved: key provided, "делай")
Zernio (API key kept outside the repo) is connected: YouTube mr.buck000 and TikTok mr.buck222 (TikTok linked by the owner after the test). Plan Usage-Based, uploads unlimited, spend 0 cents after the first post (price per post NOT VERIFIED). Test publish: Time zones (audited PASS 22.10, same file, size matches) to YouTube via POST /posts, publishNow: https://www.youtube.com/watch?v=CErOWpPs-Io. vidIQ read-back (5 credits): title, description (credit year 2023-2026, AI voice line), tags match the intended package. NOT VERIFIED: AI-content flag on YouTube and Shorts classification (duration still processing). The old Metricool post for Time zones stays in ERROR (past date, cannot re-fire). Details: map_shorts/zernio_notes.md. Queue in Metricool (25.10 onward) is still scheduled there and will fail on the limit: to be moved to Zernio only with the owner's go; set each Metricool copy to draft first to avoid double posts.

### 24.10 23:40 MSK Queue moved from Metricool to Zernio (owner approved)
11 posts scheduled in Zernio (table in map_shorts/zernio_notes.md): 25.10 Point Roberts 10:00, Turkey v2 14:00 (myth hook, first E2 test), Hormuz long 16:00 (YouTube only); 26.10 Peñón 10:00, South Africa 14:00; 27.10 Llívia, Bir Tawil; 28.10 NW Angle, France-Brazil; 29.10 Australia; 02.11 Diomede. AI flags set on both networks (YouTube containsSyntheticMedia, TikTok video_made_with_ai). Metricool copies set to draft (nothing deleted). Zernio spend after 12 posts: 0 cents (unit price still not verified).
Peñón had no authenticity audit: run today (map_shorts/week_2026_10_25/audits/velez_authenticity_audit_2026_10_24.md): PASS with accepted risks. Open items for the owner: "1930" is stated flatly in voice and on a card while sources say 1930 or 1934 (fix = re-voice one line, paid, owner's go); Esri licence before YPP; blurry zoom at ~21 s. A "music and SFX are synthesised" line was added to the Peñón description.
Note: Hormuz cover (A or B) and the thumbnails of other videos are not set through Zernio; upload with vidiq_update_video_thumbnail after the video is public.

### 25.10 00:25 MSK New Short: Australia continent vs Greenland island (owner: "делай ролик строго по референсу")
Built on the DNA of GeoGlobeTales xGmyqt_Ild0 (Caspian, 1.32M): name-flip hook with on-screen strike-through (ISLAND -> CONTINENT) in 3 s, globe push-in, scale facts with a true-size slide of Greenland on a Mercator map (great-circle rotation), 3.5x counter, coast-to-coast measure, complication "no official rule", contrast pair (Australian vs North American Plate, PB2002 boundaries), second question (why Greenland looks huge -> Mercator 1569) and a loop ending on the opening globe frame. New engine70 (globe / flat / Mercator modes, mask fills on the globe), original synth bed + one SFX per event. 62.9 s, -14.3 LUFS, visual events 15/10/7/12/11/10 per 10 s. Voice Lumean 0.45 RUB (owner approved). AI clips: only prompts written (ai_prompts.md), not generated (owner asked for prompts). Audit PASS (authenticity_audit_2026_10_25.md). Scheduled in Zernio 29.10 14:00 MSK (YT+TT, AI flags on). Measure vs Egypt 1,462 and the TikTok median 284.
