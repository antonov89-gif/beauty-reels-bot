# Zernio publishing (replaces Metricool while its account limit blocks posts)
- API: https://zernio.com/api/v1, header `Authorization: Bearer $(cat .zernio_key)`. The key sits in `.zernio_key` in the repo root (gitignored, chmod 600; never print or commit it). The container is ephemeral: if the file is gone, ask the owner for the key again or store it as an environment secret (ZERNIO_API_KEY).
- Profile "Default" id 6add13029d77da1e129d50ba. Accounts: YouTube mr.buck000 (accountId 6add13efdae3320d1b3875af), TikTok mr.buck222 (connected 24.10; accountId: read it from GET /accounts).
- Plan: Usage-Based, uploads unlimited (-1). After the first post: spend 0 cents. Price per post/account NOT VERIFIED; check GET /usage-stats after each batch.
- Post: POST /posts with `content`, `mediaItems:[{type:"video",url:<public HTTPS mp4>}]`, `platforms:[{platform, accountId, platformSpecificData}]`, `publishNow:true` or `scheduledFor` (ISO, with offset or `timezone`).
- YouTube `platformSpecificData` that worked: title, tags, visibility "public", madeForKids false, containsSyntheticMedia true (AI disclosure), category "27" (Education).
- Media URL source: the Metricool cloudfront files (static.metricool.com/planner/...) are public and work.
- Test 24.10 22:26 MSK: Time zones Short published, https://www.youtube.com/watch?v=CErOWpPs-Io (title/description/tags read back by vidIQ: match). NOT VERIFIED: that YouTube shows the AI flag and classifies it as a Short (duration was not processed yet).
- Do not double-publish: Metricool posts for the same video must be set to draft before a Zernio publish.

## Queue moved to Zernio (24.10 ~23:40 MSK, owner: "да, публикуй пока в зернио, потом когда обновятся лимиты обратно")
TikTok settings that Zernio accepts (top-level `tiktokSettings`): privacy_level, allow_comment/duet/stitch, content_preview_confirmed true, express_consent_given true, video_made_with_ai true. TikTok caption = `platforms[].customContent` (title + hashtags); the long text goes to YouTube. Times in MSK (+03:00).
| MSK slot | Video | Platforms |
|---|---|---|
| 25.10 10:00 | Point Roberts | YT+TT |
| 25.10 14:00 | Turkey v2 (myth hook, E2 test) | YT+TT |
| 25.10 16:00 | Hormuz long | YT |
| 26.10 10:00 | Peñón de Vélez (Esri, audited 24.10) | YT+TT |
| 26.10 14:00 | South Africa | YT+TT |
| 27.10 10:00 | Llívia | YT+TT |
| 27.10 14:00 | Bir Tawil | YT+TT |
| 28.10 10:00 | NW Angle | YT+TT |
| 28.10 14:00 | France-Brazil | YT+TT |
| 29.10 10:00 | Australia | YT+TT |
| 02.11 10:00 | Diomede | YT+TT |
The Metricool copies of all 11 were set to DRAFT (not deleted) so nothing posts twice. When the Metricool limit is lifted: re-schedule from the drafts only for videos NOT already published through Zernio. The Hormuz Metricool draft holds only a placeholder text; the full package is in map_shorts/hormuz_bypass/publication.md and in Zernio.
