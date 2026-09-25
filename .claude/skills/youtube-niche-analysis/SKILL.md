---
name: youtube-niche-analysis
description: Full-depth analysis of a YouTube channel and its niche — viewer psychology, good/bad competitors, and content-gap opportunities the channel could exploit before competitors do. Use whenever asked to analyze a YouTube channel, scout a niche for a new channel, do competitor research, or find "what's missing" content opportunities. Uses the Nexlev and vidIQ MCP servers.
---

# YouTube Channel & Niche Analysis

Turns "analyze this channel/niche" into a repeatable pipeline instead of an
ad-hoc one-off each time. Built for scouting new channel ideas and content
gaps in this project's niche (beauty/UGC reels) but works for any niche.

## Inputs needed from the user

- A channel URL or @handle (or a niche description if there's no anchor
  channel yet — start at step 2 in that case).

## Pipeline

### 1. Resolve the anchor channel
```
mcp__Nexlev__channel_resolver(input=<url or @handle>)
```
Get the 24-char `UC...` channelId — every other tool needs it.

### 2. Niche overview (async — poll it)
```
mcp__Nexlev__get_niche_overview(channelId=..., async=true)
```
Poll `get_niche_overview_status` with the returned jobId every ~5s until
`completed`. This is the core deliverable: niche positioning, similar
competitors with VPH/outlier scores, market opportunity signals.

### 3. Baseline channel metrics
```
mcp__Nexlev__get_channel_analytics(channelId=...)
mcp__Nexlev__check_channel_monetization(channelId=...)
mcp__Nexlev__check_faceless_channel(channelId=...)
```

### 4. Find the channel's own outlier (viral) videos
```
mcp__Nexlev__youtube_channel_outliers(channel_id=..., min_outlier_threshold=2.0)
```
These are the videos that worked far better than the channel's average —
the strongest signal for what resonates with ITS specific audience.

### 5. Viewer psychology — read the actual comments, don't guess
For the anchor channel's top 2-3 outlier videos AND top 2-3 videos from
the niche overview's competitors:
```
mcp__Nexlev__youtube_video_comments(video_id=..., sort_by="top")
# or mcp__vidq__vidiq_video_comments for channel-wide comment sweeps
mcp__Nexlev__get_video_transcript(videoId=...)
```
Read for: what hook/promise made people watch, what they praise, what
they complain is missing, recurring questions (= unmet content demand),
emotional register (aspirational? reassuring? shock/curiosity?).

### 6. Identify good vs. bad competitors
From the niche overview's competitor list, pull metrics side-by-side:
```
mcp__Nexlev__get_batch_channel_metrics_v2(channelIds=[...up to 10], async=true)
```
Poll `get_batch_channel_metrics_status`. Classify:
- **Good competitor** = high outlier score, RPM > $8, consistent upload
  cadence, monetized, growing (recent channelCreatedAfter / upload dates).
- **Bad competitor** (i.e., weak, exploitable) = stagnant uploads, low
  avg views relative to subscriber count, no monetization, generic
  unoriginal format — these are the openings, not the models to copy.

### 7. Broaden the niche scan for whitespace
```
mcp__Nexlev__search_niche_finder_channels(query=<niche topic>, minOutlierScore=2, ...)
# or search_shorts_niche_finder_channels for Shorts-specific niches
```
Look for topic clusters (via `topicTags`) that show up in the semantic
search but are UNDER-represented among the actual top competitors found
in step 6 — that gap is the opportunity.

### 8. (Optional) What competitors monetize beyond ads
```
mcp__Nexlev__get_channel_promotions(query="channelProfile", channelId=...)
```
Reveals if top competitors are selling courses/products the anchor
channel isn't — a content-gap signal that's also a revenue signal.

### 9. Only if text tools can't answer a visual question
```
mcp__Nexlev__watch_youtube_video_and_ask(...)
```
Expensive — last resort per the tool's own guidance. Use only for
questions text (transcript/comments/metadata) genuinely can't answer,
e.g. editing style, on-screen graphics, thumbnail composition.

## Output format

Deliver as a structured report, not a wall of tool output:

1. **Channel & niche snapshot** — size, monetization, format, RPM tier.
2. **Viewer psychology** — 3-5 bullet points grounded in actual comment
   quotes/transcript evidence, not generic assumptions.
3. **Good competitors** (2-4) — why they're strong, what to learn from.
4. **Bad/weak competitors** (2-4) — why they're exploitable.
5. **Content gap opportunities** — specific video/content ideas that (a)
   no strong competitor is doing, (b) the comment/transcript evidence
   suggests real audience demand for, (c) fit the anchor channel's
   existing format. Rank by estimated view potential, not novelty alone.

## Notes

- Always resolve channel URLs through `channel_resolver` first — never
  guess or hand-parse a channelId from a URL.
- Async tools (`get_niche_overview`, `get_batch_channel_metrics_v2`)
  must be polled, not treated as instant — don't report "no data" before
  the job actually completes or fails.
- Ground every psychology/gap claim in a specific comment, transcript
  line, or metric — this skill exists to replace guessing with evidence.
