"""Take 1 NEW piece 1b: And this is my channel / Sun King / handsome (setup S2, table height, rolled): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 10 s = $1.45 (0.145 x 10). first = t1nb_start_4k, last = t1nb_end_4k. Lines (script 7.3): LOUIS: "And this is my channel. They call me the Sun King. Yes... I'm that handsome. [a satisfied sigh]" Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes.
BRIEF: briefs/brief_t1nb.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"the same king in every frame, always the face and look of the reference: "
"the same face, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, the candlelight must not tint it), the scarlet velvet coat with a gold sun, lace cravat, the candlelit gilded hall behind him, his hand-held phone at table height, very close, rolled. "
"At the end, 10 s, the frame is exactly as @last_frame (a long satisfied sigh, the eyes closed, the chin lifted). "
"Realistic live action, real skin texture, no beauty filter. "
"0-2.5 s: "
"a smug sideways look at the lens, then to the viewer's left: "
"\"And this is my channel.\" with a small proud nod; "
"2.5-5 s: "
"\"They call me the Sun King.\" he lifts his chin and rolls his head toward the right; "
"at 3.5 s a courtier behind him leans to his neighbour; "
"5-6.5 s: "
"a silent beat of one and a half seconds: "
"a slow blink under heavy lids, the lips pressed in a knowing smirk; "
"the camera keeps moving; "
"6.5-8.5 s: "
"\"Yes... "
"I'm that handsome.\" with a small shrug of his shoulders, deadpan; "
"8.5-10 s: "
"the satisfied sigh, the eyes closing, the head tipping back, settling into the pose of @last_frame. "
"CAMERA SCORE in absolute amounts (his hand-held phone at table height; "
"the king and the room stay in place while the frame moves; "
"his head with the wig is about 85 percent of the width, so every move keeps the whole wig and face inside the frame, the free margin is about 7 percent on each side): "
"every 2 seconds the frame shifts by 6 to 8 percent of its width, never past the 7 percent margin: "
"0-2 s a slow drift to the right by 6 percent and the roll easing by 3 degrees; "
"2-4 s a push-in of 3 percent and a sway to the left by 6 percent; "
"4-6 s the roll swings back by 5 degrees with a small sag; "
"at about 5 s (the allowed window is 3 to 7 s) the whole picture blurs for 0.5 s, then snaps sharp; "
"6-8 s a drift to the right by 6 percent; "
"at about 7.5 s (the allowed window is 5.5 to 9 s) his own pink thumb slips into the lower left corner covering the lower left 15 percent of the frame width (never more than 20 percent) for 0.7 s and never his face; "
"8-10 s a small push-back and settle to the framing of @last_frame. "
"POSE SCORE as verbs: "
"glance, nod, lift, roll, blink, smirk, shrug, sigh, tip back; "
"the head moves about half of its own width (about 18 percent of the frame width, half of the 37 percent face) in each 2-second window, alternating left and right and ending near the centre; "
"never a hold longer than 2 seconds. "
"THE ROOM IS ALIVE: "
"candle flames flicker; "
"at 1 s a servant in livery far behind crosses from the right edge to the centre; "
"at 3.5 s the courtier behind him leans to his neighbour; "
"at 6 s a lady's fan flutters at the back right. "
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
        "image_urls": [RAW + "t1nb_start_4k.jpg", RAW + "t1nb_end_4k.jpg"],
        "duration": 10, "resolution": "720p"}
open(H0 + "take_t1nb_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t1nb.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t1nb.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t1nb.mp4"); print("saved")
