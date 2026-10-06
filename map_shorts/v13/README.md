# v13 — long-form 16:9 "The No.1 company of every country" (¿Y si? style)

Map cards (teal water, cream land, flag + country top-left, red pin on the HQ, white company plate, number badge)
alternate with Pexels stock footage (ids in `clips13.json`, download `https://www.pexels.com/download/video/<id>/`).
Small burned-in phrase subtitles + SRT.

Voice: `tts_kokoro.py` (free, offline) or `tts_lumean.py go` + `timing_from_align.py` (ElevenLabs via Lumean,
needs `.lumean_key`). Then `engine13.py prep` -> 4 x `engine13.py video A B cK.mp4` -> `audio13.py` -> mux.
