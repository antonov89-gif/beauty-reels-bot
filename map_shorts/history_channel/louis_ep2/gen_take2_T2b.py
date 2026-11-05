"""Take 2 piece T2b (owner 05.11 "Да"): Marcel films. Kling 4.0 i2v 720p 8 s = $1.16; ONLY @first_frame = T2b_start_marcel_v2_768.jpg (no last frame: the tilt up is the move). One call, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/pilot_frames/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. Realistic live action, filmed on a phone held in the hand of a nervous young page: real hand shake all the time, small wobbles and rolls, the framing never stands still. "
"0-2 s: the phone still points down at the page's own black buckled shoes and the parquet, it wobbles; the king's voice is heard off screen: \"Up.\" "
"2-4 s: the page jerks the phone upward, the shoes slide out of the bottom of the frame, motion blur on the move: \"Up, Marcel.\" "
"4-5 s: the phone settles roughly level on the room, a little tilted, still shaking slightly: \"There.\" "
"5-8 s: the page slowly pans along the very long candlelit table: the ladies sitting on the folding stools fan themselves and whisper, the men in plain wigs stand behind them, shift their weight and look toward the head of the table; far away at the head of the table sits the king, small in the frame, in his scarlet coat with gold suns and tall white-grey wig. Off-screen voice: \"The duchesses sit. Everyone else stands.\" "
"The king stays far away and small at the head of the table the whole time (never close to the camera). Same hall, same people, same light as @first_frame. "
"Sound: only diegetic, low murmur of a large hall, rustle of silk, fans, cutlery on gold, footsteps on parquet; no music at all. No text or captions, no modern objects, no second king, no tall wigs on anyone but the king.")
body = {"model": "kling-4.0-i2v", "prompt": prompt, "image_urls": [RAW + "anchors/T2b_start_marcel_v2_768.jpg"], "duration": 8, "resolution": "720p"}
open(H0 + "take2_T2b_prompt.txt", "w").write(prompt)
r = apipod.submit("videos", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
open(H0 + "pilot_frames/TAKE2_T2b.task_id", "w").write(tid)
res = apipod.wait("videos", tid, timeout=1800, every=10)
open(H0 + "pilot_frames/TAKE2_T2b.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
u = find(d.get("result") or d)
if u: apipod.download(u, H0 + "pilot_frames/TAKE2_T2b.mp4"); print("saved")
