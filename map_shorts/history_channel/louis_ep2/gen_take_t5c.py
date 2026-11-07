"""Take 5 piece 5c Ohh, I wasn't born to work (setup S12, from above): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 12 s = $1.74 (0.145 x 12). first = t5c_start_4k, last = t5c_end_4k. Lines (script 7.3): LOUIS (OWNER): "[leans back, hands on the belly, a long happy sigh] Ohh... I wasn't born to work. I was born for happiness, love, pleasure... and a good rest. [a joyful laugh at his own line]" Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes.
BRIEF: briefs/brief_t5c.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"the same king in every frame, always the face and look of the reference: "
"the same face, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, the candlelight must not tint it), the scarlet velvet coat with a gold sun, lace cravat, in a carved gilded armchair in the candlelit gilded hall, his own hand-held phone held high in front of him and above his face, looking down at it. "
"At the end, 12 s, the frame is exactly as @last_frame (he laughs joyfully, one hand on his chest). "
"Realistic live action, real skin texture, no beauty filter. "
"0-2.5 s: "
"his eyes closed, he lets out a long happy sigh, his chest rising and falling, his fingers drumming softly on his belly: "
"\"Ohh...\" at 3-4 s one hand lifts to smooth the lace cravat; "
"at 5.5 s it returns to the belly; "
"at 7 s the palm turns up in a dreamy gesture; "
"at 9 s both settle; "
"2.5-6 s: "
"he opens his eyes under heavy lids, looks up lazily into the lens and says dreamily: "
"\"I wasn't born to work.\" with a small slow shake of the head; "
"at 4 s he rolls his head to the left to look at the court, then back; "
"6-9 s: "
"\"I was born for happiness, love, pleasure...\" his eyes drift up and away as if remembering, a soft smile; "
"a silent beat of one second after \"pleasure\" at 8 s with a lazy blink; "
"9-10 s: "
"\"...and a good rest.\" he closes his eyes again and sinks deeper into the armchair; "
"10-12 s: "
"a joyful laugh at his own line (two full seconds): "
"the head tips back, the shoulders shake, one hand rises to his chest, settling into the pose of @last_frame. "
"CAMERA SCORE in absolute amounts (his own hand-held phone high above; "
"the king and the room stay in place while the frame moves; "
"his face is at 40 percent of the width and his wig at about 75 percent, so every move keeps the whole wig and face inside the frame, the free margin is about 12 percent on each side): "
"every 2 seconds the frame shifts by 6 to 8 percent of its width: "
"0-2 s a slow drift to the right by 6 percent and a push-in of 4 percent; "
"2-4 s a sway to the left by 7 percent with the roll easing by 3 degrees; "
"at about 3.5 s the whole picture blurs for 0.5 s, then snaps sharp; "
"4-6 s a dip down toward his chin by 5 percent and a lift; "
"6-8 s a drift to the right by 7 percent; "
"at about 7.5 s (the allowed window is 6 to 9 s) his own pink thumb slips into the lower left corner covering the lower left 15 percent of the frame width (never more than 20 percent) for 0.7 s and never his face (phone mistake); "
"8-10 s a small push-back of 5 percent; "
"10-12 s the shake of his laughter by 6 percent and a push-back of 4 percent, then settling to the framing of @last_frame. "
"POSE SCORE as verbs: "
"sigh, drum, open, roll, drift, blink, sink, laugh; "
"the head moves about half of its own width (about 20 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; "
"never a hold longer than 2.5 seconds (the silent beat at 8 s keeps the camera moving). "
"THE ROOM IS ALIVE: "
"candle flames flicker; "
"at 3 s a servant in livery far below on the right crosses from right to centre; "
"at 5 s a courtier's powdered wig and shoulder at the right edge shifts; "
"at 9 s the lady with the fan, small at the lower right, fans faster. "
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
        "image_urls": [RAW + "t5c_start_4k.jpg", RAW + "t5c_end_4k.jpg"],
        "duration": 12, "resolution": "720p"}
open(H0 + "take_t5c_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t5c.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t5c.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t5c.mp4"); print("saved")
