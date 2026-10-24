# Zernio publishing (replaces Metricool while its account limit blocks posts)
- API: https://zernio.com/api/v1, header `Authorization: Bearer <key>`. The key is NOT stored in the repo (kept outside git; never print or commit it).
- Profile "Default" id 6add13029d77da1e129d50ba. Accounts: YouTube mr.buck000 (accountId 6add13efdae3320d1b3875af), TikTok mr.buck222 (connected 24.10; accountId: read it from GET /accounts).
- Plan: Usage-Based, uploads unlimited (-1). After the first post: spend 0 cents. Price per post/account NOT VERIFIED; check GET /usage-stats after each batch.
- Post: POST /posts with `content`, `mediaItems:[{type:"video",url:<public HTTPS mp4>}]`, `platforms:[{platform, accountId, platformSpecificData}]`, `publishNow:true` or `scheduledFor` (ISO, with offset or `timezone`).
- YouTube `platformSpecificData` that worked: title, tags, visibility "public", madeForKids false, containsSyntheticMedia true (AI disclosure), category "27" (Education).
- Media URL source: the Metricool cloudfront files (static.metricool.com/planner/...) are public and work.
- Test 24.10 22:26 MSK: Time zones Short published, https://www.youtube.com/watch?v=CErOWpPs-Io (title/description/tags read back by vidIQ: match). NOT VERIFIED: that YouTube shows the AI flag and classifies it as a Short (duration was not processed yet).
- Do not double-publish: Metricool posts for the same video must be set to draft before a Zernio publish.
