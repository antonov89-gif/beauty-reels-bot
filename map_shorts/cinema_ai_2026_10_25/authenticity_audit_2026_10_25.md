# Authenticity audit: "Cinema" AI animation Short (25.10.2026)

File checked: /home/claude/v71/cinema_final.mp4 (1080x1920, 8.1 s, 10.8 MB; -15.5 LUFS, peak -1.5 dBFS; model audio normalised). Frames every 0.5 s plus full-size frames at 4.6 s and 7.2 s read.

| Section | Finding |
|---|---|
| Claims | No factual claims in the video. Title and description say it is an AI-generated animation and not real footage. |
| Footage | Not footage: 100% AI-generated (Veo 3.1 Fast text-to-video via WaveSpeed, prompt in gen_cinema.py), 720p upscaled to 1080x1920. Very photorealistic by the owner's brief; the realism makes the labelling the main safeguard. |
| AI shots | Whole video is AI. On screen for the whole clip: "AI-GENERATED ANIMATION" (top) and "Not real footage · Veo 3.1 Fast" (bottom). Description states the same and that no real people or event are shown. YouTube containsSyntheticMedia true, TikTok video_made_with_ai true. |
| AI inventions | Audience = generic silhouettes seen from behind (no identifiable face, no real person); a phone screen in the left foreground shows a generic picture; no readable text, logos or brand names visible in the frames checked; the ship is a generic wooden galleon (not a copyrighted character: the reference's One Piece ship was NOT requested). |
| People/logos | None identifiable. |
| Sound | Model-generated audio (orchestral swell, water, crowd). Source: Veo built-in audio (licence/Content ID behaviour NOT VERIFIED: Google states generated content is usable per its terms; no copyrighted track was requested; risk LOW-MODERATE for Content ID matches on the orchestral swell). |
| Imagery/data | No third-party imagery. Veo/WaveSpeed terms for commercial use of outputs: NOT VERIFIED (read before relying on monetisation). |
| Platform policy | AI-only, off-niche content for a geography channel: risk for the YPP review (inauthentic/mass-produced content, unclear channel purpose). Mitigation: one-off, clearly labelled, not a series. Removal risk LOW (labelled), monetisation risk MODERATE. |
| Metadata/flags | publication.md; flags to be read back from Zernio after scheduling. |

Verdict: PASS with accepted risks (PARTLY: audio licence and commercial terms NOT VERIFIED; off-niche). Open items for the owner: (1) publish as a one-off, not a series; (2) the title must keep "AI" (a title that implies real footage would turn this into a BLOCK).


## Version 2 (humpback whale, replaces the ship clip in the schedule)
File checked: /home/claude/v71/cinema2_final.mp4 (1080x1920, 8.0 s, 12.8 MB; -13.6 LUFS, peak -1.4 dBFS; no black frames or freezes). Frames every 0.5 s plus full-size frames at 1.0, 4.0 and 7.3 s read.
| Section | Finding |
|---|---|
| AI shots | 100% AI (Veo 3.1 Lite text-to-video). Labels "AI-GENERATED ANIMATION" (top) and "Not real footage · Veo 3.1 Lite" (bottom) on the whole clip; description and flags (YouTube containsSyntheticMedia true, TikTok video_made_with_ai true) read back from Zernio. |
| AI inventions / people | One AI-generated young man (face visible, laughing), AI audience silhouettes; he is not a real person and does not resemble a named person as far as can be judged (NOT VERIFIED: an AI face can resemble a real one by chance; no name or claim attached). No readable text or logos found in the frames checked (a phone and a plastic bottle without a legible label). The whale is a generic humpback; the whale stays on the screen and the foam floods the room (the model did not make it leave the screen). |
| Sound | Veo built-in audio (water, crowd). Licence/Content ID behaviour and Veo/WaveSpeed commercial terms NOT VERIFIED. |
| Platform policy | Same as version 1: AI-only and off-niche; one-off, clearly labelled. Removal risk LOW, monetisation risk MODERATE. |
Verdict: PASS with accepted risks (unchanged).
