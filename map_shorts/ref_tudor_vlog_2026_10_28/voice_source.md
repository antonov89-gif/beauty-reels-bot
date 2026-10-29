# Where does the Elizabeth channel's voice come from? (28-29.10.2026)
Answer: NOT PUBLIC. The creator does not name the voice or the tools. What is known and what we measured:

## Public facts (web, 29.10)
- Creator: the About link points to cosminacreates.shop ("CosminaCreates", prices in GBP). TikTok account @cosminacreates posts the same Elizabeth I series (labelled AI-generated) and other "history to present" characters.
- The shop sells: "Elizabeth I - AI Workflow" GBP 59, "AI Character Development - For AI Beginners" GBP 59, "AI Beginner Guide" GBP 29, "Ultimate AI Masterclass" GBP 249, Bundle Vol 1-3 GBP 99, "1:1 AI Mentorship" GBP 799, consulting via a contact form. The page names no tool and says nothing about voices or lip sync. The Elizabeth workflow e-book is the one place that would document the method.
- Hashtags on her TikTok captions (search snippets, not read on the page): #higgsfield (Queen Victoria post) and #magnificai (Elizabeth I post). Possible tools: Higgsfield (video and voice platform) and Magnific (upscaling). Not attribution; the third-party guide alici.ai itself says its tool list is "recommendation-only".
- The Chloe VS History article (aitopics) names no tools or voices either.

## Our measurement of Vlog 1 audio (owner's mp4, 128 s; scripts in the session, results here)
- Voice pitch (median f0) in the three long takes: 176 / 174 / 171 Hz, i.e. the SAME voice in three different framings and rooms (a native generator voice usually drifts between clips; this one does not). Low female pitch. The later shots mix in other sounds (banquet, the servant's cry, laughter): 148 / 277 / 159 Hz.
- Room-noise floor in pauses differs per take (-57 to -49 dB): an ambience per shot (generated natively or layered per shot).
- Bandwidth about 14-16 kHz (AAC 128k re-encode): no information on the source.
- Loudness -15.4 LUFS, true peak -1.1 dBFS.
Reading (STRONG INFERENCE, not proof): one fixed voice (a voice reference or a TTS/clone) with per-shot ambience; whether the voice is a human actress, a clone or a synthetic voice cannot be told from these numbers.

## Ways to find out for sure
1. Buy "Elizabeth I - AI Workflow" (GBP 59, about $75): needs the owner's decision.
2. Ask the creator through the contact on the channel's About page / her shop's "Hire Cosmina" form.
3. Test it ourselves: Higgsfield has audio-reference video models (Seedance 2.0, Grok Video 1.5, MiniMax H3) and voice tools (Eleven v4, Seed Audio, Qwen TTS with reference-element voices). Our Higgsfield account shows 0.1 credits, so it needs a top-up; APIpod has Seedance 2.0 r2v `audio_urls` and Kling 4.0 r2v `voices` (see model_choice.md).
