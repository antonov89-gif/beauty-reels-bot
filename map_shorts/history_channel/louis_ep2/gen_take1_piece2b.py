"""Take 1, piece 2 RETAKE b (owner 05.11 "да, повторяй кусок 2"): first = last = A3 edit, no keyframes (the pin rule: same composition at both ends). ORIGINAL NOTE: Take 1, piece 2: ONE pinned generation, Kling 4.0 i2v 720p 15 s = $2.18. Lines: "They call me the Sun King. Yes... I'm that handsome. Some of you write that I eat too much. I read it. Of course, that's not true." (27 words; the last two sentences of Take 1 go to piece 3). Pins: first = A3 edit, keyframe_1 (5 s) = anchor E7 blissful, keyframe_2 (10 s) = anchor E6 annoyed, last = anchor E2 smug. One call, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/pilot_frames/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. The same king in every frame, always the face and look of @first_frame: the same face, the same age, tall white-grey powdered wig, thin dark waxed moustache with curled tips, beauty mark, scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded dining hall with the long table, ladies on stools and standing courtiers, the same framing and the same room all the time. At the end, 15 s, he is exactly as in @last_frame (the smug pause with a ringed hand at a curl of the wig). Realistic live action, real skin texture, no beauty filter. "
"0-3 s: he starts in the pose of @first_frame (a ringed hand at a curl of his wig), chin up, drawling: \"They call me the Sun King.\" "
"3-6 s: delighted with himself, he touches a curl of his wig and says: \"Yes... I'm that handsome.\" then a long satisfied sigh with closed eyes, mouth closed. "
"6-10 s: he opens his eyes, the smile fades, he looks offended and says: \"Some of you write that I eat too much.\" "
"10-11.5 s: a cold pause, eyebrows up, a frown, lips pressed: \"I read it.\" then he sniffs through his nose. "
"11.5-14 s: he waves the idea away with the back of one ringed hand, chin up: \"Of course, that's not true.\" "
"14-15 s: he settles back into the pose of @last_frame. "
"Acting limits: heavy eyelids stay, no wide-open eyes, no broad grin, no lean toward the lens, the face stays at a medium distance. "
"Camera: filmed by himself on a phone held in one hand at arm's length: gentle hand-held sway and small roll only, small re-centring jerks. NO fast pans, NO whip pans, NO fast swings of the camera, NO sudden zoom, no gimbal, no dolly or flying camera; the room behind him stays in the same place and the framing stays the same. "
"Sound: only diegetic, low murmur of a large hall, cutlery on gold, candle flicker, fabric; no music at all. No text or captions, no modern objects, no tall wigs on anyone but the king, only one king in the frame (no second face, no double).")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "T1_keyframe_edit_768.jpg", RAW + "T1_keyframe_edit_768.jpg"],
        "duration": 15, "resolution": "720p"}
open(H0 + "take1_piece2b_prompt.txt", "w").write(prompt)
r = apipod.submit("videos", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
open(H0 + "pilot_frames/TAKE1_piece2b.task_id", "w").write(tid)
res = apipod.wait("videos", tid, timeout=2400, every=10)
open(H0 + "pilot_frames/TAKE1_piece2b.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
u = find(d.get("result") or d)
if u: apipod.download(u, H0 + "pilot_frames/TAKE1_piece2b.mp4"); print("saved")
