"""T1c (chain clip 3), Kling 4.0 i2v 720p 8 s, @first_frame = last frame of T1b (owner 04.11 "да"). Price $0.145/s x 8 = $1.16. One call, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/pilot_frames/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. The same king from @first_frame for the whole clip: the same face, the same age, the same tall white-grey powdered wig, the same thin waxed moustache and beauty mark, the same scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded dining hall with the long table, the seated ladies and the standing courtiers behind him. Realistic live action, real skin texture, no beauty filter. "
"0-2 s: he opens his eyes, the smug smile fades, he leans toward the lens, offended: \"Some of you write that I eat too much.\" "
"2-4 s: a short pause, eyebrows up, cold: \"I read it.\" "
"4-6 s: he sniffs loudly through his nose and waves it away with the back of his ringed hand. "
"6-8 s: chin up again, looking down his nose into the lens, dismissive: \"Of course, that's not true.\" "
"Filmed by himself on a phone held in one hand at arm's length, clumsy with it: constant natural hand-held sway and small roll, the framing drifts and he re-centres with small jerks. Never a smooth gimbal move, never a zoom, never a dolly or flying camera. "
"Sound: only diegetic, low murmur of a large hall, cutlery on gold, candle flicker, fabric; no music at all. No text or captions, no modern objects, no phone visible in the frame, no tall wigs on anyone but the king.")
body = {"model": "kling-4.0-i2v", "prompt": prompt, "image_urls": [RAW + "T1b_last.jpg"], "duration": 8, "resolution": "720p"}
open(H0 + "t1c_kling40_prompt.txt", "w").write(prompt)
r = apipod.submit("videos", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
open(H0 + "pilot_frames/T1c_kling40.task_id", "w").write(tid)
res = apipod.wait("videos", tid, timeout=1800, every=10)
open(H0 + "pilot_frames/T1c_kling40.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
u = find(d.get("result") or d)
if u: apipod.download(u, H0 + "pilot_frames/T1c_kling40.mp4"); print("saved")
