"""Take 6 the verdict (setup S13, frontal close, slow push-in): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 12 s = $1.74 (0.145 x 12). first = t6_start_4k, last = t6_end_4k. Lines (script 7.3): LOUIS (OWNER): "[wipes his fingers, sits up, glances at the bones on his plate, pushes the plate a little away] So. Do I eat too much? ...No. I eat like a king. [chin up] Don't be afraid of getting fat. Be afraid of being a loser. [haughty laugh]" Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"the same king in every frame, always the face and look of the reference: "
"the same face, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, the candlelight must not tint it), the scarlet velvet coat with a gold sun, lace cravat, the candlelit gilded hall behind him, his own hand-held phone at eye level, frontal and close, slowly pushing in. "
"At the end, 12 s, the frame is exactly as @last_frame (chin up, a haughty laugh, the plate pushed a little away); "
"the king and the room are in the same place in both frames. "
"Realistic live action, real skin texture, no beauty filter. "
"0-2 s: "
"he wipes his fingers on the lace napkin, glances down at the bones on the plate with a complacent smirk, then sits up straighter; "
"2-3.5 s: "
"he pushes the plate a little away with two fingers and looks into the lens: "
"\"So.\" a short pause, then \"Do I eat too much?\" with a raised eyebrow; "
"at 3 s the lady with the fan at the left back turns her head; "
"3.5-5.5 s: "
"the silent beat of one and a half seconds: "
"he lets the question hang, looking at the court with a slow blink, then back; "
"the camera keeps moving; "
"5.5-8 s: "
"\"...No. "
"I eat like a king.\" the chin rising slowly; "
"8-10.5 s: "
"\"Don't be afraid of getting fat. "
"Be afraid of being a loser.\" he says it softly and flatly, the eyes half closed, a small contemptuous head tilt to the left; "
"at 9 s a courtier behind his right shoulder bows his head slightly; "
"10.5-12 s: "
"the haughty laugh, the chin up, settling into the pose of @last_frame. "
"CAMERA SCORE in absolute amounts (his own hand-held phone; "
"the king and the room stay in place while the frame moves; "
"his face is at 56 percent of the width, so every move keeps his face and wig inside the frame, the free margin is about 20 percent on each side): "
"every 2 seconds the frame shifts by 8 to 10 percent of its width: "
"0-2 s a slow push-in of 6 percent and a drift to the left by 8 percent with the roll easing by 3 degrees; "
"2-4 s a sway to the right by 9 percent; "
"4-6 s a sag down by 5 percent and a lift while the roll swings the other way by 4 degrees; "
"at about 5 s (the allowed window is 3 to 7 s) the focus hunts: "
"the picture goes soft for half a second and snaps back sharp; "
"6-8 s a drift to the left by 8 percent with a push-in of 5 percent; "
"at about 9 s (the allowed window is 7 to 11 s) his own pink thumb slips into the lower right corner covering the lower right 20 percent of the frame width (never more than 25 percent) for 0.7 s and never his face; "
"8-10 s a sway to the right; "
"10-12 s a small push-back and the haughty laugh shake of 8 percent, settling to the framing of @last_frame. "
"POSE SCORE as verbs: "
"wipe, glance, sit up, push, lift, blink, tilt, bow, laugh; "
"the head moves about half of its own width (about 20 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; "
"never a hold longer than 2 seconds. "
"THE ROOM IS ALIVE: "
"candle flames flicker; "
"at 3 s the lady with the fan turns her head; "
"at 6 s a servant in livery far behind on the right crosses from right to left; "
"at 9 s the courtier behind his right shoulder bows his head. "
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
        "image_urls": [RAW + "t6_start_4k.jpg", RAW + "t6_end_4k.jpg"],
        "duration": 12, "resolution": "720p"}
open(H0 + "take_t6_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t6.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t6.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t6.mp4"); print("saved")
