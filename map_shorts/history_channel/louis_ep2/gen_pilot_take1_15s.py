"""PILOT: first 15 s of Take 1 as ONE pinned generation (owner 05.11 "да, делай пилот"). Kling 4.0 i2v 720p 15 s = $0.145 x 15 = $2.18. Pins: first = A3 edit, keyframe_1 (5 s) = anchor E2, keyframe_2 (10 s) = anchor E1, last = A3 edit. One call, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/pilot_frames/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. The same king in every frame, always the face and look of @first_frame: the same face, the same age, tall white-grey powdered wig, thin dark waxed moustache with curled tips, beauty mark, scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded dining hall with the long table, ladies on stools and standing courtiers. "
"Around 5 s he is exactly as in @keyframe_1 (smug half-smile, mouth closed, a pause after clearing his throat). Around 10 s he is exactly as in @keyframe_2 (looking straight into the lens, haughty, heavy lids, mouth closed, a pause). At the end, 15 s, he is exactly as in @last_frame (the smug pause with a ringed hand at a curl of the wig). Realistic live action, real skin texture, no beauty filter. "
"0-3 s: he fumbles with the phone: the phone swings too close to his face, big and out of focus, a muffled voice: \"Is it... is it on?\" while his thumb taps the screen. "
"3-4.5 s: he pulls the phone back to arm's length, sees himself, pleased: \"Ah. There I am.\" "
"4.5-5.5 s: he clears his throat and settles into the pose of @keyframe_1. "
"5.5-8.5 s: calm and grand, looking down his nose into the lens: \"Bonjour. I am Louis, King of France.\" "
"8.5-10.5 s: a proud sweep of one ringed hand toward the hall behind him: \"Welcome to Versailles.\" then the pause of @keyframe_2. "
"10.5-14 s: \"And this is my channel.\" with a small nod, then he returns to the pose of @last_frame. "
"Acting limits: heavy eyelids stay, no wide-open eyes, no broad grin, no lean toward the lens, the face stays at a medium distance after 3 s. "
"Filmed by himself on a phone held in one hand at arm's length, clumsy with it: natural hand-held sway and small roll, the framing drifts and he re-centres with small jerks. Never a smooth gimbal move, never a zoom, never a dolly or flying camera. "
"Sound: only diegetic, low murmur of a large hall, cutlery on gold, candle flicker, fabric; no music at all. No text or captions, no modern objects, no tall wigs on anyone but the king.")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "T1_keyframe_edit_768.jpg", RAW + "T1_keyframe_edit_768.jpg"],
        "keyframe_urls": [RAW + "anchors/ANCHOR_E2_smug_1080.jpg", RAW + "anchors/ANCHOR_E1_haughty_1080.jpg"],
        "duration": 15, "resolution": "720p"}
open(H0 + "pilot_take1_15s_prompt.txt", "w").write(prompt)
r = apipod.submit("videos", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
open(H0 + "pilot_frames/PILOT_take1_15s.task_id", "w").write(tid)
res = apipod.wait("videos", tid, timeout=2400, every=10)
open(H0 + "pilot_frames/PILOT_take1_15s.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
u = find(d.get("result") or d)
if u: apipod.download(u, H0 + "pilot_frames/PILOT_take1_15s.mp4"); print("saved")
