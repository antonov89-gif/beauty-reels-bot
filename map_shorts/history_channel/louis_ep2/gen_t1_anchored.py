"""T1 re-do with anchors (owner 04.11 "Да"): Kling 4.0 i2v 720p 8 s. @first_frame = F01a (the fumble), @keyframe_1 = edit of card A3 (identity), @last_frame = anchor E2 smug. Price $0.145/s x 8 = $1.16. One call, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/pilot_frames/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. @keyframe_1 shows the king's exact face and look: around 4 s he settles for a moment into exactly @keyframe_1 (same face, same age, smug closed-mouth pause, one ringed hand at a curl of the wig). @last_frame shows how the clip ends: he ends exactly as in @last_frame (the same face, the smug half-smile). The same king in every frame: the same face, tall white-grey powdered wig, thin waxed moustache, beauty mark, scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded dining hall with the long table, ladies on stools, standing courtiers. Realistic live action, real skin texture, no beauty filter. "
"0-2 s: the phone is far too close, out of focus, his scarlet sleeve and fist cover the top half; a muffled voice, he mumbles \"Is it... is it on?\" while his thumb taps the screen and the sleeve slides off. "
"2-3.5 s: he pulls the phone back to arm's length and sees himself, pleased: \"Ah. There I am.\" "
"3.5-4.5 s: he settles into the pose of @keyframe_1 and clears his throat, heavy lids, haughty. "
"4.5-8 s: calm and grand, looking down his nose into the lens: \"Bonjour. I am Louis, King of France.\" and he ends in the smug half-smile of @last_frame. "
"Acting limits: heavy eyelids stay, no wide-open eyes, no broad grin, no lean toward the lens, the face stays at a medium distance. "
"Filmed by himself on a phone held in one hand at arm's length, clumsy with it: constant natural hand-held sway and small roll, the framing drifts and he re-centres with small jerks. Never a smooth gimbal move, never a zoom, never a dolly or flying camera. "
"Sound: only diegetic, low murmur of a large hall, cutlery on gold, candle flicker, fabric; no music at all. No text or captions, no modern objects, no tall wigs on anyone but the king.")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "F01a_v1_owner.jpg", RAW + "anchors/ANCHOR_E2_smug_1080.jpg"],
        "keyframe_urls": [RAW + "T1_keyframe_edit_768.jpg"], "duration": 8, "resolution": "720p"}
open(H0 + "t1_anchored_prompt.txt", "w").write(prompt)
r = apipod.submit("videos", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
open(H0 + "pilot_frames/T1_anchored.task_id", "w").write(tid)
res = apipod.wait("videos", tid, timeout=1800, every=10)
open(H0 + "pilot_frames/T1_anchored.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
u = find(d.get("result") or d)
if u: apipod.download(u, H0 + "pilot_frames/T1_anchored.mp4"); print("saved")
