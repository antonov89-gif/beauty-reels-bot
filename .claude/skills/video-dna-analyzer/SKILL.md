---
name: video-dna-analyzer
description: Use when the user sends a YouTube (or Shorts/TikTok) link and asks to analyse it ("Разбери по DNA", "анализ ролика", "разбери референс", camera/dynamics/hook breakdown) or wants a new video built from a reference. Forensic reverse engineering by the saved YOUTUBE VIDEO DNA ANALYZER V2.0 prompt.
---

# Video DNA Analyzer (V2.0)

Full prompt: `map_shorts/prompts/video_dna_analyzer_v2.md`. Read it before every analysis and follow all 91 phases; the final answer ends with the 18 blocks of PHASE 91.

## How to run it here
1. **Data (PHASE 0):** vidIQ `vidiq_get_videos_by_ids` (stats, description), Nexlev `get_bulk_video_transcripts` (transcript with timecodes), vidIQ `vidiq_video_comments`, `vidiq_channel_videos` (channel context, outliers), thumbnail via `i.ytimg.com/vi/<id>/maxresdefault.jpg`.
2. **Watching:** vidIQ `vidiq_watch_shortform_content` (10 credits) with a targeted prompt (0–10 s forensics by second, event counts, camera moves, colours/fonts, SFX per 10 s). One general pass plus one style pass is usually enough; Nexlev `watch_youtube_video_and_ask` only if vidIQ fails. The sandbox cannot open youtube.com directly.
3. **Count, do not guess:** visual events per 10 s, cuts, words per minute (transcript words / duration), SFX per 10 s. Tag each claim VERIFIED / STRONG INFERENCE / HYPOTHESIS / UNKNOWN (PHASE 1). Never state retention, CTR or tools used without evidence.
4. **Output:** save the report as `map_shorts/<project>/dna_<videoId>.md` (Russian, short sentences), commit and push. Reply in Russian with the summary and the 18 final blocks condensed.
5. **Transfer:** when a new video is made from the reference, list the fixes to our video that come from the analysis (PHASE 72–75, 88–90) and apply them; copy principles, never phrases, characters, music or graphics (PHASE 89).

Honesty rules of the channel still apply: hedge unconfirmed facts, label AI visuals, no copyrighted music.

## Replication protocol (PHASE 92-96)
When the user asks for a video "по референсу", also run the protocol at the end of `map_shorts/prompts/video_dna_analyzer_v2.md`: (92) double watch, structure pass then frame-by-frame pass; (93) one-sentence "what surprises the viewer" test, reference vs ours; (94) per-second table reference / ours shown BEFORE any generation or paid call; (95) AI-clip checklist from a contact sheet (no burned-in text, no extra characters, natural colours, clean edges) before editing; (96) not-a-copy check recorded in the authenticity audit. Real facts and AI answers only, with date and log.

**Visual accuracy rule:** the visual part of any analysis comes from real frames. YouTube blocks yt-dlp here, so ask the owner for the mp4, run `map_shorts/prompts/frame_forensics.py <video> <out_dir> --dense 10`, open the contact sheets and write the second-by-second table from what is visible. vidIQ/Gemini text is a hypothesis until confirmed; without the file, mark the visual analysis "NOT VERIFIED ON FRAMES".

## Production after the analysis (V5.1)
When a new video is built from the reference, also apply `.claude/skills/youtube-cinematic-dna/` (evidence levels, STYLE_BIBLE + shot deltas, acceptance gates, pilot 2–3 shots, max 2 fixes per shot, status markers). Its mapping and overrides are in `PROJECT_INTEGRATION.md`.
