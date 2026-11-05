"""Take 3, piece T3a (soup, setup S6 low from the table). Kling 4.0 i2v 720p 10 s = $1.45 (0.145 x 10). first = T3a start still, last = T3a end still (same composition, different pose). Lines: "Four rounds. First, soup. [slurps] My sister-in-law says I eat four bowls. [a servant puts down one more] ...She can't count." Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. The same king in every frame, always the face and look of @first_frame: the same face, the same age, the tall silver-grey powdered wig, thin dark waxed moustache with curled tips, beauty mark, light rouge, scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded hall, the same very low camera position looking up from the table, the same big silver soup bowl in the foreground, the same framing all the time. At the end, 10 s, the frame is exactly as @last_frame (the spoon lowered toward the bowl in his ringed hand, wet lips, mouth closed, a flat deadpan look straight into the phone lens, a second silver bowl already standing on the table at the right); the camera, the room and the framing of @last_frame are the same as in @first_frame, only his pose and the servant differ. Realistic live action, real skin texture, no beauty filter. "
"0-1 s: the spoon hovers above the bowl, steam rises, he looks at the soup and then at the lens with a smug half-smile. "
"1-3.5 s: he says calmly and grandly: \"Four rounds. First, soup.\" "
"3.5-5 s: he dips the spoon, lifts it to his lips and slurps the soup noisily, then lowers the spoon; a silent beat, his flat look into the lens. "
"5-7.5 s: dry and offended: \"My sister-in-law says I eat four bowls.\" at about 6.5 s the servant's gloved hand puts one more silver bowl down at the right edge and draws back. "
"7.5-9 s: a pause with the flat deadpan look, one eyebrow slightly raised, then quietly and drily: \"...She can't count.\" "
"9-10 s: silence after the joke: he holds the deadpan look into the lens, mouth closed, not speaking. "
"THE ROOM IS ALIVE, all through the clip: behind him the standing courtiers shift their weight and turn their heads to one another; the ladies on stools whisper to each other behind folding fans; steam rises from the bowls; the candle flames flicker; the servant is busy at the right edge. The background people keep their faces, only small natural movements. "
"Phone mistake once: at about 5 s his own blurred thumb slides a little further over the lower left of the lens for a second and the focus hunts for half a second, then settles. "
"Acting limits: heavy eyelids stay, no wide-open eyes, no broad grin, no lean toward the lens, the face stays natural and undistorted. "
"Camera: filmed by himself on a phone held in one hand just above the tablecloth, looking up: gentle hand-held sway, small roll and small re-centring jerks, a slight push-in toward the bowl and the face while he speaks. NO fast pans, NO whip pans, NO sudden zoom, no gimbal, no dolly or flying camera; the room stays in the same place and the framing stays the same. "
"Sound: only diegetic, low murmur of a large hall, a spoon on silver, the slurp, cutlery on gold, candle flicker, fabric; no music at all. No text or captions, no modern objects, only one king in the frame (no second face, no double).")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "T3a_start_4k.jpg", RAW + "T3a_end_4k.jpg"],
        "duration": 10, "resolution": "720p"}
open(H0 + "take3_T3a_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE3_T3a.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE3_T3a.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE3_T3a.mp4"); print("saved")
