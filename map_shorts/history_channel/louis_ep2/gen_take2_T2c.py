"""Take 2, piece T2c (grape beat). Kling 4.0 i2v 720p 12 s = $1.74 (0.145 x 12). first = T2c start still (camera on the king's right, beige wig, grape at the mouth), last = T2c end still v2 (same composition, grape eaten, eyes into the lens; owner exception 05.11 for its 4K quality). Lines: "People ask me why I eat in front of everyone. They want to see their king. [eats the grape] Even with his mouth full." Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. The same king in every frame, always the face and look of @first_frame: the same face, the same age, the tall powdered wig of the same colour, thin dark waxed moustache with curled tips, beauty mark, light rouge, scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded hall, the same framing and the same camera side all the time. At the end, 12 s, the frame is exactly as @last_frame (the grape eaten, his mouth closed and chewing, the ringed hand resting on the edge of the gold dish, his eyes turned straight into the phone lens with heavy lids and one eyebrow slightly raised, smug); the camera, the room and the framing of @last_frame are the same as in @first_frame, only his pose differs. Realistic live action, real skin texture, no beauty filter. "
"0-1 s: he looks at the grape between his ringed fingers with bored haughty heavy lids, mouth closed. "
"1-5 s: without looking at the lens he says slowly and drily: \"People ask me why I eat in front of everyone.\" a small pause, he turns the grape a little between his fingers. "
"5-7.5 s: \"They want to see their king.\" he lifts the grape to his mouth, one eyebrow goes up. "
"7.5-9 s: he puts the grape in his mouth and slowly chews with his lips closed, his eyes slide sideways into the phone lens; a silent beat. "
"9-11 s: still chewing, mouth almost closed, muffled, calm and arrogant: \"Even with his mouth full.\" "
"11-12 s: he swallows, lowers the hand to the edge of the dish and holds the smug look into the lens of @last_frame, mouth closed. "
"THE ROOM IS ALIVE, all through the clip: behind him the standing courtiers are not statues, they shift their weight and turn their heads to one another; the ladies in gowns raise folding fans beside their faces and whisper to each other; a servant in livery walks slowly across behind with a dish, towards the right edge; the candle flames flicker. The background people keep their faces, only small natural movements. "
"Phone mistake once: at about 4 s the blurred edge of the page's sky-blue sleeve at the lower left slides a little further into the frame for a second, and the focus hunts for half a second, then settles. "
"Acting limits: heavy eyelids stay, no wide-open eyes, no broad grin, no lean toward the lens, the face stays at the same distance. "
"Camera: filmed by Marcel the page on a phone held in one hand, close to the king's side: gentle hand-held sway, small roll and small re-centring jerks, a slight push-in while he chews. NO fast pans, NO whip pans, NO sudden zoom, no gimbal, no dolly or flying camera; the room stays in the same place and the framing stays the same. "
"Sound: only diegetic, low murmur of a large hall, cutlery on gold, candle flicker, fabric; no music at all. No text or captions, no modern objects, only one king in the frame (no second face, no double).")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "T2c_start_4k.jpg", RAW + "T2c_end_v2_4k.jpg"],
        "duration": 12, "resolution": "720p"}
open(H0 + "take2_T2c_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE2_T2c.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE2_T2c.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE2_T2c.mp4"); print("saved")
