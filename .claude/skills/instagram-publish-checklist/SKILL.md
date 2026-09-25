---
name: instagram-publish-checklist
description: Pre-flight checklist before calling publish_draft_to_instagram or InstagramPublishingAgent in beauty-reels-bot. Use before any real (non-mock) Instagram publish, or when a publish fails/behaves unexpectedly.
disable-model-invocation: true
---

# Instagram Publish Checklist

`InstagramPublishingAgent` in `reels_mvp.py` only works correctly in one of
two modes — fully mocked, or fully real. A half-configured state (real
token + local file path, or missing token treated as real) is the
recurring failure this checklist exists to catch; it was already the root
cause of one bug this session (`"MOCK_ACCESS_TOKEN"` vs the actual default
`"MOCK_INSTAGRAM_TOKEN"` string mismatch, fixed in commit `bbb805e`).

## Before calling publish_draft_to_instagram, verify:

1. **Token mode is unambiguous.**
   ```bash
   python3 -c "import os; print(repr(os.environ.get('INSTAGRAM_ACCESS_TOKEN')))"
   ```
   - Unset or literally `MOCK_INSTAGRAM_TOKEN` → mock mode, any `media_url`
     is fine, nothing hits the real Graph API.
   - Any other value → real mode, and the checks below are mandatory.

2. **In real mode, `media_url` must be a public HTTPS URL**, not a local
   filesystem path. Instagram's Graph API fetches the video itself; it
   cannot read a path on this machine. `publish_draft_to_instagram`
   already raises on this, but verify the render's output actually got
   uploaded somewhere public (S3, a CDN, a public HTTP endpoint) before
   calling it — the render step only produces a local file.

3. **Token has the right permissions and isn't expired** — a real Graph
   API token needs `instagram_content_publish` and an Instagram
   Professional account linked to a Facebook Page. An expired or
   under-scoped token fails at `create_reels_container`, not earlier.

4. **Check container status before assuming success** — Reels publishing
   is async: `create_reels_container` returning an ID does not mean the
   video is live. Poll `check_container_status` until `FINISHED` before
   reporting the publish as done.

## If a publish fails

Read the actual Graph API error body (not just the HTTP status) — Meta's
error messages usually name the exact missing scope or malformed field.
Don't guess-fix; the mock-token bug above was only found by reproducing
the failure and reading the real error, not by assumption.
