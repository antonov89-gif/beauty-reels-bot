"""Take 5 piece 5b Marcel films the laden table and the king eating (no words): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 5 s = $0.72 (0.145 x 5). first = t5b_start_4k, last = t5b_end_4k. Lines (script 7.3): [Marcel films the laden table and the king eating, about 4 s, no words: chewing, a happy hum, the murmur of the crowd] Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"the same king in every frame, always the face and look of the reference: "
"the same face, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, the candlelight must not tint it), the scarlet velvet coat with a gold sun, lace cravat, far at the top behind the laden table in the first frame; "
"filmed by Marcel on a hand-held phone in the candlelit gilded hall. "
"At the end, 5 s, the frame is exactly as @last_frame (the camera has tilted up and moved in on the sharp, chewing king). "
"Realistic live action, real skin texture. "
"No spoken words: "
"only chewing, his happy hum and the murmur of the crowd. "
"0-2 s: "
"the camera drifts over the heaped dishes, sharp in the foreground, the king chews at the far end; "
"at 1.2 s a servant at the right edge passes with a covered dish and leaves the frame; "
"2-4 s: "
"the camera tilts up and pushes in; "
"at about 1.8 s the whole picture blurs for 0.5 s, then snaps sharp on the king; "
"he chews with relish, closes his eyes in bliss and hums; "
"4-5 s: "
"the frame settles on the king as in @last_frame, a satisfied small nod while chewing; "
"behind him on the right the lady with the fan fans herself and a courtier watches him eat. "
"CAMERA SCORE in absolute amounts: "
"0-2 s a drift to the right by 8 percent and the roll easing from 7 degrees right to 4 degrees left; "
"2-4 s a clear tilt UP of 20 degrees with a push-in that grows the king from the small far figure to the large subject of @last_frame, and a re-aim to the right by 6 percent; "
"at about 3 s (the allowed window is 2.5 to 3.6 s) Marcel's sky-blue braided sleeve brushes the lower left of the lens, covering at most 15 percent of the width, gone by 3.6 s; "
"4-5 s a small sway and settle to the framing of @last_frame. "
"POSE SCORE as verbs with times: "
"0-2 s chew, swallow; "
"2-4 s chew, close the eyes, hum, roll the head about half its width to the left; "
"4-5 s nod, chew; "
"THE ROOM IS ALIVE: "
"candle flames flicker; "
"at 1.2 s the servant passes with a covered dish; "
"at 3 s the lady with the fan turns her head toward the king; "
"at 4 s a courtier behind him on the right shifts his weight. "
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
        "image_urls": [RAW + "t5b_start_4k.jpg", RAW + "t5b_end_4k.jpg"],
        "duration": 5, "resolution": "720p"}
open(H0 + "take_t5b_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t5b.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t5b.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t5b.mp4"); print("saved")
