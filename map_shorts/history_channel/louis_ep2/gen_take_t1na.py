"""Take 1 NEW piece 1a: Is it on / Ah there I am / Bonjour / Welcome to Versailles (setup S1, extreme low selfie): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 12 s = $1.74 (0.145 x 12). first = t1na_start_4k, last = t1na_end_4k. Lines (script 7.3): LOUIS: "[phone too close, muffled] Is it... is it on? [pulls it back, sees himself, pleased] Ah. There I am. [clears throat] Bonjour. I am Louis, King of France. Welcome to Versailles." Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"the same king in every frame, always the face and look of the reference: "
"the same face, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, the candlelight must not tint it), the scarlet velvet coat with a gold sun, lace cravat, filmed on his own hand-held phone from far too close and low, then pulled back; "
"the painted ceiling and gilded cornice of the candlelit palace hall behind and above him. "
"At the end, 12 s, the frame is exactly as @last_frame (the phone pulled back, he looks pleased into the lens); "
"the king and the room are in the same place in both frames. "
"Realistic live action, real skin texture, no beauty filter. "
"0-2.5 s: "
"his face huge and low in the lens, squinting at the screen with a frown, muffled: "
"\"Is it... "
"is it on?\" the thumb at the lower right corner fumbles over the screen; "
"2.5-4.5 s: "
"he pulls the phone back and sees himself; "
"the picture drifts up and down as the focus hunts for half a second; "
"his face brightens: "
"\"Ah. "
"There I am.\" 4.5-6 s: "
"a silent beat of one and a half seconds: "
"he admires himself, smoothing his moustache with one finger; "
"the camera keeps moving; "
"6-8 s: "
"he clears his throat: "
"\"Hm-hm.\" and straightens: "
"\"Bonjour.\" 8-12 s: "
"\"I am Louis, King of France. "
"Welcome to Versailles.\" the chin rising, the eyes on the lens, settling into the pose of @last_frame. "
"CAMERA SCORE in absolute amounts (his own hand-held phone; "
"the king and the room stay in place while the frame moves; "
"the face is at 80 percent of the width at the start and 56 percent at the end, so every move keeps the face and wig inside the frame): "
"every 2 seconds the frame shifts by 8 to 10 percent of its width: "
"0-2 s a fumbling drift to the left by 9 percent with the roll swinging 4 degrees; "
"2-4 s the pull-back of about 25 percent of the face size with a drift to the right by 9 percent; "
"at about 3 s the focus hunts for half a second; "
"4-6 s a sway to the left by 8 percent and a dip; "
"6-8 s a push-in of 5 percent and a re-centring jerk; "
"at about 7 s (the allowed window is 5 to 9 s) the phone tilts up to the painted ceiling for half a second and comes back; "
"8-10 s a drift to the right by 8 percent; "
"10-12 s a small sag and settle to the framing of @last_frame. "
"POSE SCORE as verbs: "
"squint, frown, pull back, brighten, smooth the moustache, clear the throat, straighten, lift the chin; "
"the head moves about half of its own width in each 2-second window, alternating left and right and ending near the centre; "
"never a hold longer than 2 seconds. "
"THE ROOM IS ALIVE: "
"candle flames flicker and painted clouds on the ceiling catch the light; "
"at the lower edge at 5 s the head of a courtier in a plain wig passes behind him from right to left; "
"at 9 s a tiny servant's shoulder in livery at the left edge. "
"Acting limits: "
"heavy eyelids stay except in the laugh beats, no wide-open eyes for the king, the face stays natural, hands have five natural fingers. "
"No whip pans and no zoom lens, all moves by hand; "
"no gimbal, no dolly or flying camera. "
"Sound: "
"only diegetic, low murmur of a large hall, fabric, cutlery, candle flicker, his voice and breath; "
"no music at all. "
"No text or captions, no modern objects, no clear glass or crystal glass anywhere, only one king in the frame (no second king, no double). "
)

body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "t1na_start_4k.jpg", RAW + "t1na_end_4k.jpg"],
        "duration": 12, "resolution": "720p"}
open(H0 + "take_t1na_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t1na.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t1na.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t1na.mp4"); print("saved")
