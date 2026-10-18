---
name: youtube-growth-engine
description: Use for any audit, growth analysis, pre-publish check or post-publish review of the Mr. Buck YouTube channel (@Mr.Buck000) and its TikTok copy. Applies YOUTUBE GROWTH INTELLIGENCE ENGINE V3.0 PRO: 4 modes, 15 modules, Judge A/B, counter-hypotheses, experiment cards, priority scoring, dashboards and the Growth Learning Log.
---

# YouTube Growth Intelligence Engine V3.0 PRO — Mr. Buck

The full prompt is `map_shorts/prompts/youtube_growth_engine_v3_pro.md`. Read it before each audit and follow it verbatim. This file only adds the channel specifics and the working rules.

## Channel
- YouTube: @Mr.Buck000, channel ID `UCFphFU69Tgz3LyHoZzODdWw`. TikTok: mr.buck222.
- Format: faceless English geography "why…?" Shorts on an animated satellite map (engine `map_shorts/week_2026_10_21/engine/`). Audience: US, India, Philippines. 99.9% of watch time comes from non-subscribers.
- Goal: as many views as possible. Shorts feed = 88% of traffic, so the first 3 seconds (stayed vs swiped) are the main lever.
- Baseline (Studio, 28 days to 17.10.2026): stayed 55.6% / swiped 44.4%; best Short 2,302 views; median ≈1.2k. Full audit: `map_shorts/audit_v2_2026-10-17.md`.

## Which mode
- No mode given → MODE 2 DEEP AUDIT.
- New Short rendered, before scheduling → MODE 3 PRE-PUBLISH: Module 10 (stages A–D), 11 (risk 1–5 per group), 12 (QC + script-to-video table), Judge A/B, consensus, then verdict READY / REVISE / REWORK / INSUFFICIENT DATA. Watch the actual file (extract stills at 0.0 s, 1 s, 3 s and each scene; check loudness), never judge by title only.
- 24–72 h after publishing, or on a monitoring run → MODE 4 CONTINUOUS OPTIMIZATION: compare with the log, update the experiment cards.
- "quick" → MODE 1.

## Tools (check which are really connected; never pretend)
- vidIQ: `vidiq_channel_analytics` (top_videos, traffic_sources, shorts_vs_longform_split, audience_geography, audience_retention, daily), `vidiq_video_stats`, `vidiq_watch_shortform_content` (10 credits) + `vidiq_job_poll`, `vidiq_outliers`, `vidiq_update_video`.
- Nexlev: `search_shorts_niche_finder_channels`, `faceless_outliers_videos`, `youtube_channel_shorts`; `watch_youtube_video_and_ask` is 1/day on the free plan.
- Metricool: `getScheduledPosts`, `createScheduledPost` / `updateScheduledPost`, `getBestTimeToPostByNetwork`.
- Do not ask the user for Studio screenshots (decided 18.10.2026: the user works without them). The per-video stayed/swiped share is unavailable, so use these proxies: views at 24 h and 72 h vs the channel median (vidIQ `vidiq_video_stats` / `top_videos`), relative retention and the first-quarter drop (vidIQ `audience_retention`), likes and comments per 1k views. Screenshots the user sends on their own are a bonus.

## Honesty rules
- Tag every significant claim FACT / HYPOTHESIS / ESTIMATE / DATA MISSING, with source, date and sample size.
- Never invent CTR, retention, revenue, impressions or demographics. Never promise a view count.
- Shorts views count every start, so compare 24 h / 72 h views and retention against the channel median, not single videos.
- Consecutive uploads are not an A/B test: compare medians of batches, one main variable per experiment.

## Standing production rules (from the audits)
- Frame 0 already shows the key visual and a number or contrast; the hook line is ≤ 1.5 s; ≥ 10 visual events per 10 s, no static pause > 2.5 s.
- Publish window 10–16 MSK, Shorts duplicated to TikTok (isAigc true, madeForKids false).
- Ask before any paid generation and name the cost. No copyrighted music, no leaks; hedge unconfirmed facts; label AI visuals "AI CONCEPT · NOT GAME FOOTAGE"; disclose AI voice and image sources in the description.
- Never print or commit API keys; never put video files in the repository.
- Voice-over must sound like a real person: follow `map_shorts/prompts/voiceover_naturalness_rules.md` (write for the ear, natural delivery settings, transcribe-and-check, light mix chain). The AI-voice disclosure stays in every description and platform toggle.

## Growth Learning Log (Module 15)
- File: `map_shorts/growth_log.md`. After every publish batch or audit, add the results and the extracted principle there and commit it. Do not claim something is saved unless the commit exists.
- Experiment cards E1–E4 live in the log; update RESULT and NEXT DECISION when the observation window closes.

## Answer format
Follow section IX of the prompt (Executive summary → 12 points), in Russian, plain language. End every audit with: keep / change / stop / experiment / next video and why / first action now.
