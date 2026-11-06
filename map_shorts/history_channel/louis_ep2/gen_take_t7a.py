"""Take 7 piece 7a I was wondering what else to show you (setup S16, three-quarter right): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 10 s = $1.45 (0.145 x 10). first = t7a_start_4k, last = t7a_end_4k. Lines (script 7.3): LOUIS (OWNER): "[leans back, thinks, looks around the hall] So... I was wondering what else to show you here. [pause, a short laugh] Ha. Probably... nothing." Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"the same king in every frame, always the face and look of the reference: "
"the same face, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, the candlelight must not tint it), the scarlet velvet coat with a gold sun, lace cravat, leaning back in the candlelit gilded hall, filmed by his own hand-held phone held below eye level so that the hall behind him is visible. "
"At the end, 10 s, the frame is exactly as @last_frame (a short dry laugh, the eyes on the lens); "
"the king and the room are in the same place in both frames. "
"Realistic live action, real skin texture, no beauty filter. "
"0-2.5 s: "
"he leans back, looks slowly around the hall from right to left, thoughtful, the lips pursed; "
"2.5-5.5 s: "
"he brings his eyes to the lens: "
"\"So... "
"I was wondering what else to show you here.\" with a small frown and a tilt of the head to the right; "
"at 4 s a lady at the back right closes her fan; "
"5.5-7 s: "
"the silent beat of one and a half seconds: "
"he looks around the hall again and the corners of his mouth rise; "
"the camera keeps moving; "
"7-8.5 s: "
"a short dry laugh: "
"\"Ha.\" with a small shoulder shake; "
"8.5-10 s: "
"\"Probably... "
"nothing.\" lightly, with a shrug of one shoulder, settling into the pose of @last_frame. "
"CAMERA SCORE in absolute amounts (his own hand-held phone; "
"the king and the room stay in place while the frame moves; "
"his face is at 40 percent of the width, so every move keeps his face and wig inside the frame, the free margin is about 30 percent on each side): "
"every 2 seconds the frame shifts by 8 to 10 percent of its width: "
"0-2 s a slow swing to the right by 10 percent following his gaze and a roll easing by 3 degrees; "
"2-4 s a swing back to the left by 9 percent with a push-in of 5 percent; "
"4-6 s a sag down by 5 percent and a lift; "
"at about 5 s (the allowed window is 3 to 7 s) the phone tilts up to the ceiling for half a second and comes back; "
"6-8 s a drift to the right by 8 percent; "
"at about 8.5 s (the allowed window is 6.5 to 9.5 s) his own pink thumb slips into the lower left corner covering the lower left 20 percent of the frame width (never more than 25 percent) for 0.6 s and never his face; "
"8-10 s a small push-in and settle to the framing of @last_frame. "
"POSE SCORE as verbs: "
"lean, scan, frown, tilt, glance, smirk, laugh, shrug; "
"the head moves about half of its own width (about 15 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; "
"never a hold longer than 2 seconds. "
"THE ROOM IS ALIVE: "
"candle flames flicker; "
"at 1 s a servant in livery far behind crosses from left to right; "
"at 3 s a courtier at the right edge of the table turns to his neighbour; "
"at 4 s the lady at the back right closes her fan; "
"at 7 s a courtier shifts his weight. "
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
        "image_urls": [RAW + "t7a_start_4k.jpg", RAW + "t7a_end_4k.jpg"],
        "duration": 10, "resolution": "720p"}
open(H0 + "take_t7a_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t7a.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t7a.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t7a.mp4"); print("saved")
