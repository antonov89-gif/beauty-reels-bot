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
