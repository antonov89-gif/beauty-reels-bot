---
name: authenticity-check
description: MANDATORY gate for EVERY video of the Mr. Buck channel (YouTube, TikTok, Instagram copies; Shorts and long videos) before it is delivered to the user, uploaded or scheduled. Verifies claims, footage identity, AI labelling, people/logos, music and imagery licences, credits, platform flags and platform-policy risk. Run it also on a video the user hands over, and on every re-render.
---

# Authenticity check (mandatory, every video)

Rule from the user (22.10.2026): "проверка обязательно на все ролики". No video is delivered as final, uploaded, scheduled or published until this check has been run on the FINAL file and its verdict is PASS or FIXED. A re-render after any change re-runs the affected items. Do not skip it because the video is "just a Short", "already checked" or the user is in a hurry; if a check cannot be done, say so and mark it NOT VERIFIED (never PASS).

Reply to the user in Russian, briefly: verdict, what was fixed, what is open. Write the full audit to `map_shorts/<project>/authenticity_audit_<date>.md` and commit it.

## Method
Look at the real final file, not at the plan: extract stills (0 s, 1 s, every cut, last frame), watch the AI shots at full size, run ffmpeg (cuts, freezes, black, loudness), read the publication package and the scheduled Metricool post. Source of truth for every fact is a page or dataset you actually opened or searched; say which.

## Checklist
1. **Claims (on-screen text, voice, title, description, thumbnail).** Every number, superlative and causal claim: source + verdict VERIFIED / PARTLY / NOT VERIFIED. Wording must not be stronger than the source (e.g. "average" vs "highest point", "usually" vs "always"). Disputed figures: show only what is agreed, or write "reportedly". A hook that overstates a fact is a FIX, not a pass.
2. **Footage identity.** Each real clip: page title/metadata matches what we say it shows (place, date, event). Visually compare with a map/satellite frame if the title is vague; if still unsure, describe it generically ("Lofoten islands", not a named village). Stock footage must be illustrative where the place is not certain, and the description says so.
3. **AI content.** List every AI element (voice, image, video, music). Each AI visual of a REAL place or event is flagged: on-screen label "AI-GENERATED SHOT" (or similar) during the shot, a line in the description, and the platform flag ON (YouTube isAiGeneratedContent, TikTok isAigc, Instagram AI label). AI voice: disclosed in the description and flags. AI must never be presented as real footage, a real photo, a real person or a real event. Note what the AI invented (buildings, people, text) and check it does not contradict the real place.
4. **People, faces, logos, brands, trademarks.** None identifiable without a release (Pexels and similar licences forbid it); remove or crop. No real person's voice or likeness cloned. No fake news-style footage of real events.
5. **Music and sound.** Source + licence for every track and effect (own synthesis, Mixkit/Pixabay/etc., licensed). No copyrighted or trending music in the file (the user may add trending sound inside TikTok). Read the licence text when the platform allows it; if only a summary was found, mark PARTLY and name the Content ID risk.
6. **Imagery and data licences + credits.** Pexels/Wikimedia/NASA/Esri/Natural Earth/terrain data: licence, required credit text, link. CC BY/BY-SA need author, title, licence, link and "changes were made". Esri World Imagery: attribution on screen and in the description. Checked 22.10 (`map_shorts/esri_licence_check_2026_10_22.md`): NOT VERIFIED and a real risk once the channel is monetised (Esri's static-map terms name "commercial monetization" as needing Esri's permission; video is not addressed; the channel is not monetised today). Mark PARTLY in every audit and remind the user of the pending permission request.
7. **Platform policy.** YouTube inauthentic/reused content (a montage of stock clips with only music and cropping is a risk; value must be added: own graphics, research, commentary), spam/misleading metadata, made-for-kids not set, altered-or-synthetic disclosure. TikTok: AIGC label, no unoriginal-content reposts. Rate monetisation risk and removal risk LOW / MODERATE / HIGH.
8. **Metadata and flags.** Title, description, tags, hashtags match the video (no misleading tags like another place); credits block present; AI flags set in the Metricool post (read it back with getScheduledPosts); privacy/schedule correct.
9. **Technical honesty.** The video does what the package says (duration, language, "no voice" etc.); cover/thumbnail is a frame or an honestly labelled AI image and not a different place.

## Verdict
- **PASS**: all items VERIFIED or PARTLY with a stated, accepted risk.
- **FIXED**: problems found and corrected, file re-rendered and re-checked.
- **BLOCK**: something false, unlabelled AI, unlicensed material or an identifiable person remains. Do not upload or schedule; tell the user what is needed.
Open items that only the user can decide (hook wording, licence reading, money) go in one short list.

## Audit file template
Title, date, file checked (size, duration), then sections: Claims | Footage | AI shots | People/logos | Sound | Imagery/data | Platform policy | Metadata/flags | Verdict | Open items. Past examples: `map_shorts/lofoten_2026_10_22/authenticity_audit_2026_10_22.md`.
