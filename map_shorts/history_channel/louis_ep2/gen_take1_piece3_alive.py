"""TEST: Take 1 piece 3 with a LIVING ROOM (owner 05.11 "1": background life in the generation, one 8 s clip): Kling 4.0 i2v 720p 8 s = $1.16; first = last = A3 edit, no keyframes; lines "Every day I feast in front of the court. Today... before your eyes." Earlier note on piece 2: Take 1, piece 2: ONE pinned generation, Kling 4.0 i2v 720p 15 s = $2.18. Lines: "They call me the Sun King. Yes... I'm that handsome. Some of you write that I eat too much. I read it. Of course, that's not true." (27 words; the last two sentences of Take 1 go to piece 3). Pins: first = A3 edit, keyframe_1 (5 s) = anchor E7 blissful, keyframe_2 (10 s) = anchor E6 annoyed, last = anchor E2 smug. One call, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/pilot_frames/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. The same king in every frame, always the face and look of @first_frame: the same face, the same age, tall white-grey powdered wig, thin dark waxed moustache with curled tips, beauty mark, scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded dining hall with the long table, ladies on stools and standing courtiers. At the end, 8 s, he is exactly as in @last_frame (the smug pause with a ringed hand at a curl of the wig). Realistic live action, real skin texture, no beauty filter. "
"0-3 s: he starts in the pose of @first_frame, lowers his hand from the wig and makes a small, slow, proud gesture toward the long table and the court behind him, chin up: \"Every day I feast in front of the court.\" "
"3-5 s: a short theatrical pause, one eyebrow slightly raised, a sly half-smile: \"Today...\" "
"5-7.5 s: he points one ringed finger toward the viewer from where he is (no lean toward the lens) and says: \"before your eyes.\" "
"7.5-8 s: he returns to the pose of @last_frame, smug, mouth closed. "
"THE ROOM IS ALIVE, all through the clip: behind him the standing courtiers are not statues, they shift their weight from foot to foot, turn their heads to one another and whisper behind a hand, one nods, one adjusts his cuff; the seated ladies on the stools fan themselves with folding fans, turn to each other and whisper, one looks at the king; a servant in livery crosses slowly behind the table carrying a dish; the candle flames flicker and the chandeliers glitter. The background people keep their places and their faces, only small natural movements. "
"Acting limits for the king: heavy eyelids stay, no wide-open eyes, no broad grin, no lean toward the lens, the face stays at a medium distance. "
"Camera: filmed by himself on a phone held in one hand at arm's length: a gentle hand-held sway, a small roll and slow drift, so the whole room moves a little, small re-centring jerks. NO fast pans, NO whip pans, NO sudden zoom, no gimbal, no dolly or flying camera. "
"Sound: only diegetic, low murmur of a large hall, cutlery on gold, candle flicker, fabric; no music at all. No text or captions, no modern objects, no tall wigs on anyone but the king, only one king in the frame (no second face, no double).")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "T1_keyframe_edit_768.jpg", RAW + "T1_keyframe_edit_768.jpg"],
        "duration": 8, "resolution": "720p"}
open(H0 + "take1_piece3_alive_prompt.txt", "w").write(prompt)
r = apipod.submit("videos", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
open(H0 + "pilot_frames/TAKE1_piece3_alive.task_id", "w").write(tid)
res = apipod.wait("videos", tid, timeout=2400, every=10)
open(H0 + "pilot_frames/TAKE1_piece3_alive.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
u = find(d.get("result") or d)
if u: apipod.download(u, H0 + "pilot_frames/TAKE1_piece3_alive.mp4"); print("saved")
