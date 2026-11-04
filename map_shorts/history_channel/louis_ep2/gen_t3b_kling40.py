"""T3b pilot, Kling 4.0 i2v 720p 8 s from F03b (owner 04.11 "д"). Price: $0.145/s x 8 = $1.16. One call, no retries. Usage: python3 gen_t3b_kling40.py go. Key: /home/claude/.apipod_key (never printed)."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/pilot_frames/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. Keep exactly the same king throughout (tall white-grey powdered wig, heavy-lidded haughty eyes, thin waxed moustache, beauty mark beside the mouth, light rouge, scarlet velvet coat with gold suns, lace cravat, jewelled rings) and the same blue-sleeved hand of Marcel the page. Realistic live action, real skin texture, no beauty filter. "
"0-2 s: servants carry a whole roast pheasant and a roast partridge past; the king, holding a roast leg in his bare fingers, closes his eyes for a moment and breathes in the smell, then says tenderly \"Ah. Here they are. A whole pheasant. And a partridge.\" "
"2-5 s: Marcel's hand with a thin silver fork comes into the lens from the bottom right, close to the camera, focus hunting between the fork and the king's face; the king looks at the fork with disdain: \"What is that.\" "
"5-8 s: he pushes the fork away with two ringed fingers without looking at Marcel and says slowly \"Someone taught the peasants to use a fork. I've untaught them.\" Then he takes a bite of the leg, chewing, with a smug look. "
"Filmed by himself on a phone held in one hand at arm's length, clumsy with it: constant natural hand-held sway and small roll, the framing drifts, his face slides off-centre and he re-centres it with small jerks. Never a smooth gimbal move, never a zoom, never a dolly or flying camera. "
"Sound: only diegetic, low murmur of a large hall, cutlery on gold, candle flicker, fabric; no music at all. No text or captions, no modern objects, no tall wigs on anyone but the king, a fork is clearly a fork, not a knife.")
body = {"model": "kling-4.0-i2v", "prompt": prompt, "image_urls": [RAW + "F03b_v1_owner.jpg"], "duration": 8, "resolution": "720p"}
open(H0 + "t3b_kling40_prompt.txt", "w").write(prompt)
r = apipod.submit("videos", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
open(H0 + "pilot_frames/T3b_kling40.task_id", "w").write(tid)
res = apipod.wait("videos", tid, timeout=1800, every=10)
open(H0 + "pilot_frames/T3b_kling40.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
u = find(d.get("result") or d)
if u: apipod.download(u, H0 + "pilot_frames/T3b_kling40.mp4"); print("saved")
