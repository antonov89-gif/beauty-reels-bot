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

## 3. Experiment cards
**E1 — Visual density.** HYPOTHESIS: ≥ 10 events/10 s and no pause > 2.5 s lower the swipe share. EVIDENCE: pace vs views above (correlation only). VARIABLE: number of pop-ups, zooms, highlights. CONTROL: batch 21–24.10 (6–7.7 events/10 s). METRIC: median of 24 h / 72 h views vs control, vidIQ relative retention. WINDOW: 7 Shorts per variant. LIMITATIONS: different topics, compare medians. RESULT: — . NEXT DECISION: — .

**E2 — Answer on frame 0.** HYPOTHESIS: a number or contrast visible at 0.0 s lowers swipes vs a title over satellite imagery. CONTROL: Shorts 18–20.10 (pop-in hooks). TEST: batch 21–24.10. METRIC: median of 24 h views vs the 18–20.10 Shorts and vs the channel median ≈1.2k; vidIQ relative retention in the first quarter (baseline 0.46–0.6). RESULT: — .

**E3 — Niche title convention.** VARIABLE: "number-contrast + #geography #map" vs our style. METRIC: search share (vidIQ traffic_sources), 24 h views. LIMITATIONS: no A/B for Shorts, sequential only. RESULT: — .

**E4 — GTA series.** HYPOTHESIS: GTA Shorts reach another audience and don't hurt geography. METRIC: 24 h views of 4 GTA Shorts 18–20.10 vs geography Shorts on the same days. DECISION 20.10: if GTA median < 50% of geography median, no new GTA until 19.11. RESULT: — .

## 4. Principles (confirmed / rejected)
| Date | Principle | Evidence | Confidence |
|---|---|---|---|
| 17.10 | Daily views follow uploads: no upload → views drop ~40× (7.10: 4,376 vs 11.10: 100) | V daily | FACT (pattern), cause HYPOTHESIS |
| 17.10 | Peak window 10–16 MSK | user observation + Metricool best time | ESTIMATE |

## 5. Decision journal
| Date | Hypothesis | Change | Result | Conclusion |
|---|---|---|---|---|
| 17.10 | First 3 s are the main leak (44.4% swipe) | 7 new Shorts rebuilt with key visual on frame 0 | pending (21–24.10) | |
