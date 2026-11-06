"""Take 7 piece 7b he stands, the crowd bows, bye, subscribe (setup S14, low swing up): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 14 s = $2.03 (0.145 x 14). first = t7b_start_4k, last = t7b_end_4k. Lines (script 7.3): LOUIS (OWNER): "[stands up, the crowd bows] That's all. Bye. I'm busy. [beat, points at the lens] ...And you: subscribe to my stunning channel. And like. [pause, a lazy wave of the hand, he looks away, bored] Or... whatever." Hard cut on "Or... whatever." to the end card. Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"the same king in every frame, always the face and look of the reference: "
"the same face, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, the candlelight must not tint it), the scarlet velvet coat with a gold sun, lace cravat, rising from his gilded armchair in the candlelit gilded hall, filmed by his own hand-held phone held low and swinging up with him; "
"the courtiers and ladies behind him bow. "
"At the end, 14 s, the frame is exactly as @last_frame (he stands, a lazy wave, looking away bored, the crowd bowing deeply); "
"the king and the room are in the same place in both frames. "
"Realistic live action, real skin texture, no beauty filter. "
"0-2.5 s: "
"he rises from the armchair, the camera rising with him; "
"behind him the courtiers begin to bow, one lady at the left curtsies; "
"2.5-5.5 s: "
"\"That's all. "
"Bye. "
"I'm busy.\" he says with a bored sigh, looking down at the lens from above; "
"at 4 s a courtier on the right bows lowest of all; "
"5.5-7.5 s: "
"the silent beat of one and a half seconds: "
"he lets the bowing crowd hold, glancing over them with satisfaction; "
"the camera keeps moving; "
"7.5-9.5 s: "
"he points a finger at the lens, with a small lift of the eyebrow: "
"\"...And you:\" 9.5-12 s: "
"\"subscribe to my stunning channel. "
"And like.\" he nods slowly, smug; "
"12-14 s: "
"a silent pause, a lazy wave of the hand, he looks away to the side, bored: "
"\"Or... "
"whatever.\" and the frame settles to the pose of @last_frame. "
"CAMERA SCORE in absolute amounts (his own hand-held phone; "
"the king and the room stay in place while the frame moves; "
"his face is at 44 percent of the width, so every move keeps his face and wig inside the frame, the free margin is about 28 percent on each side): "
"every 2 seconds the frame shifts by 8 to 10 percent of its width: "
"0-2 s a swing up with his rising of 10 percent with the roll easing by 4 degrees; "
"2-4 s a drift to the right by 9 percent and a push-in of 5 percent; "
"4-6 s a sway to the left by 8 percent; "
"at about 6 s (the allowed window is 4 to 8 s) the focus hunts for half a second; "
"6-8 s a push-in of 6 percent as he points; "
"8-10 s a drift to the right by 8 percent; "
"at about 10 s (the allowed window is 8 to 12 s) his own pink thumb slips into the lower right corner covering the lower right 20 percent of the frame width (never more than 25 percent) for 0.7 s and never his face; "
"10-12 s a sag and a lift; "
"12-14 s a sway to the left by 8 percent and settle to the framing of @last_frame. "
"POSE SCORE as verbs: "
"rise, sigh, glance, point, nod, wave, look away; "
"the head moves about half of its own width (about 20 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; "
"never a hold longer than 2 seconds. "
"THE ROOM IS ALIVE: "
"candle flames flicker; "
"at 1 s the lady at the left curtsies; "
"at 3 s the courtiers on both sides dip their heads; "
"at 4 s a courtier on the right bows lowest; "
"at 6 s a servant behind the crowd lowers his tray; "
"at 11 s a child page at the right peeks up and is pushed down by a hand. "
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
        "image_urls": [RAW + "t7b_start_4k.jpg", RAW + "t7b_end_4k.jpg"],
        "duration": 14, "resolution": "720p"}
open(H0 + "take_t7b_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t7b.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t7b.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t7b.mp4"); print("saved")
