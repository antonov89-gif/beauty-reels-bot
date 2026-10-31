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
| 29.10 10:00 | Australia's capital (Canberra) | YT+TT |
| 02.11 10:00 | Diomede | YT+TT |
The Metricool copies of all 11 were set to DRAFT (not deleted) so nothing posts twice. When the Metricool limit is lifted: re-schedule from the drafts only for videos NOT already published through Zernio. The Hormuz Metricool draft holds only a placeholder text; the full package is in map_shorts/hormuz_bypass/publication.md and in Zernio.
| 25.10 06:00 | Australia vs Greenland (new, engine70, audited PASS 25.10; moved from 29.10 at the owner's request) | YT+TT |
Own uploads: POST /media/presign -> PUT the file to uploadUrl -> use publicUrl (media.zernio.com/temp/...). Zernio moves the file from temp/ to media/ when the post is created (seen 25.10).
| 29.10 14:00 | Dahala Khagrabari (text+music, 16.9 s, audited PASS 25.10; moved from 10:00 on 25.10, slot clash with Canberra) | YT+TT |
| (draft) | AI cinema animation v2: humpback whale, rejected by the owner, draft until v3 | YT+TT |

## History channel accounts (31.10, owner: "на zernio нужно создать аккаунт тик ток")
- Tried: POST /profiles ("History POV - Louis XIV (NOT Mr. Buck)") and GET /connect/tiktok: both refused 402 PAYMENT_REQUIRED "Add a payment method to connect more than 2 accounts" (free_tier_account_limit 2, current 2 = Mr. Buck YouTube + TikTok, has_payment_method false). Nothing was created, nothing charged.
- Zernio pricing (zernio.com/pricing, read 31.10): accounts 1-2 free, accounts 3-10 $6/month each, no per-post charge. History channel TikTok = account 3 ($6/mo); its YouTube = account 4 (another $6/mo).
- Owner's steps: (1) create the TikTok account in the TikTok app (a Zernio connect only links an existing account); (2) add a payment method: https://zernio.com/dashboard/billing?add_payment_method=1 ; (3) tell Claude: it creates the separate profile and sends the TikTok authUrl (GET /connect/tiktok?profileId=...), the owner logs in and approves; (4) GET /accounts confirms; the history videos then post ONLY to that profile's accounts, never to Mr. Buck.
