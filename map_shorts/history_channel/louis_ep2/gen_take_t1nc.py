"""Take 1 NEW piece 1c: Some of you write that I eat too much ... before your eyes (setup S2b, chest height from his left, diagonal along the table): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 16 s = $2.32 (0.145 x 16). first = t1nc_start_4k, last = t1nc_end_4k. Lines (script 7.3): LOUIS: "[a satisfied sigh] Some of you write that I eat too much. I read it. [sniffs] Of course, that's not true. Every day I feast in front of the court. Today... before your eyes." Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes.
BRIEF: briefs/brief_t1nc.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"the same king in every frame, always the face and look of the reference: "
"the same face, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, the candlelight must not tint it), the scarlet velvet coat with a gold sun, lace cravat, the candlelit gilded hall behind him, his own hand-held phone at chest height from his left side looking diagonally along the long table. "
"At the end, 16 s, the frame is exactly as @last_frame (a grand smug look into the lens). "
"Realistic live action, real skin texture, no beauty filter. "
"0-1.5 s: "
"a satisfied sigh, the heavy lids lowering; "
"1.5-4 s: "
"he reads the comments with a wounded look, glancing back over his shoulder: "
"\"Some of you write that I eat too much.\" with a tilt of the head; "
"at 3 s a courtier at the right leans to his neighbour; "
"4-6 s: "
"\"I read it.\" a slow blink; "
"then he sniffs, haughty; "
"6-8 s: "
"a quiet beat of two seconds: "
"he lets it hang, then waves a hand dismissively without looking; "
"the camera keeps moving; "
"8-10.5 s: "
"\"Of course, that's not true.\" the chin rising, a dry smile; "
"10.5-13.5 s: "
"\"Every day I feast in front of the court.\" the head sweeping slowly to look down the table at the court and back; "
"at 12 s the lady with the fan at the right fans herself; "
"13.5-15 s: "
"\"Today... "
"before your eyes.\" the eyes on the lens; "
"15-16 s: "
"a silent tail of one second, a smug closed smile, settling into the pose of @last_frame. "
"CAMERA SCORE in absolute amounts (his own hand-held phone; "
"the king and the room stay in place while the frame moves; "
"his face is at 35 percent of the width and his wig at about 70 percent, so every move keeps the whole wig inside the frame, the free margin is about 14 percent on each side): "
"every 2 seconds the frame shifts by 5 to 7 percent of its width: "
"0-2 s a slow drift to the right by 5 percent and a push-in of 4 percent; "
"2-4 s a sway to the left by 6 percent with the roll easing by 3 degrees; "
"4-6 s a dip and a lift by 4 percent; "
"at about 5 s (the allowed window is 3 to 7 s) the whole picture blurs for 0.5 s, then snaps sharp; "
"6-8 s a drift to the right by 6 percent; "
"8-10 s a push-in of 5 percent and a sway left; "
"at about 9 s (the allowed window is 7 to 12 s) his own pink thumb slips into the lower right corner covering the lower right 15 percent of the frame width (never more than 20 percent) for 0.7 s and never his face; "
"10-13 s the sweep of the head with the frame following by 7 percent to the right and back; "
"13-16 s a small push-back of 6 percent and settle to the framing of @last_frame. "
"POSE SCORE as verbs with times: "
"0-1.5 s sigh; "
"1.5-4 s read, glance, tilt; "
"4-6 s blink, sniff; "
"6-8 s wave; "
"8-10.5 s lift, smile; "
"10.5-13.5 s sweep, return; "
"13.5-16 s smile; "
"the head moves about half of its own width (about 17 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre. "
"THE ROOM IS ALIVE: "
"candle flames flicker; "
"at 1 s a servant in livery far behind carries a dish from the right edge to the centre; "
"at 3 s the courtier at the right leans to his neighbour; "
"at 7 s a lady at the right lowers her fan; "
"at 12 s the lady with the fan fans herself. "
"Acting limits: "
"heavy eyelids stay except in the laugh beats, no wide-open eyes for the king, the face stays natural, hands have five natural fingers. "
"No whip pans and no zoom lens, all moves by hand; "
"no gimbal, no dolly or flying camera. "
"Sound: "
"only diegetic, low murmur of a large hall, fabric, cutlery, candle flicker, breath; "
"no music at all. "
"No text or captions, no modern objects, no clear glass or crystal glass anywhere, only one king in the frame (no second king, no double). "
)

body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "t1nc_start_4k.jpg", RAW + "t1nc_end_4k.jpg"],
        "duration": 16, "resolution": "720p"}
open(H0 + "take_t1nc_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t1nc.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t1nc.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t1nc.mp4"); print("saved")
