"""Take 2, piece T2a RETAKE v2 (owner 05.11 "Да"): first = A3 edit, LAST = pose P2 (same composition, different pose), living room in the prompt. ORIGINAL NOTE: Take 2, piece T2a (owner "да, запускай T2a"): Kling 4.0 i2v 720p 12 s = $1.74; first = last = A3 edit, no keyframes; lines "Every night at ten, I dine here. In public. Anyone dressed properly may come in. ...Lower. Lower. Good. Marcel, show them." Earlier note on piece 2: Take 1, piece 2: ONE pinned generation, Kling 4.0 i2v 720p 15 s = $2.18. Lines: "They call me the Sun King. Yes... I'm that handsome. Some of you write that I eat too much. I read it. Of course, that's not true." (27 words; the last two sentences of Take 1 go to piece 3). Pins: first = A3 edit, keyframe_1 (5 s) = anchor E7 blissful, keyframe_2 (10 s) = anchor E6 annoyed, last = anchor E2 smug. One call, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/pilot_frames/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. The same king in every frame, always the face and look of @first_frame: the same face, the same age, tall white-grey powdered wig, thin dark waxed moustache with curled tips, beauty mark, scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded dining hall with the long table, ladies on stools and standing courtiers, the same framing and the same room all the time. At the end, 12 s, he is exactly as in @last_frame (his head tilted a little to his right, a pleased smug closed-mouth smile, the ringed hand stretched out toward the table as if presenting the feast); the camera, the room and the framing of @last_frame are the same as in @first_frame, only his pose differs. Realistic live action, real skin texture, no beauty filter. "
"0-4 s: he starts in the pose of @first_frame, then lowers his hand and speaks calmly and grandly, chin up: \"Every night at ten, I dine here. In public.\" "
"4-6.5 s: \"Anyone dressed properly may come in.\" In the background behind him a courtier in a plain wig bows only slightly, barely lowering his head, almost standing straight. "
"6.5-9 s: the king notices, slowly turns his head toward the courtier behind him (his body stays in place, his face stays the same), raises one eyebrow and says: \"...Lower.\" the courtier bows a little more; \"Lower.\" the courtier bows deeply; \"Good.\" "
"9-11 s: the king turns his face back to the lens and says, with a small gesture of one ringed hand to his side: \"Marcel, show them.\" "
"11-12 s: he tilts his head a little to his right and holds the pleased smug pose of @last_frame, hand toward the table, mouth closed. "
"THE ROOM IS ALIVE, all through the clip: behind him the standing courtiers are not statues, they shift their weight, turn their heads to one another and whisper behind a hand; the seated ladies on the stools fan themselves with folding fans and whisper to each other; a servant in livery crosses slowly behind the table carrying a dish; the candle flames flicker. The background people keep their places and their faces, only small natural movements. "
"Acting limits: heavy eyelids stay, no wide-open eyes, no broad grin, no lean toward the lens, the face stays at a medium distance. "
"Camera: filmed by himself on a phone held in one hand at arm's length: gentle hand-held sway and small roll only, small re-centring jerks. NO fast pans, NO whip pans, NO fast swings of the camera, NO sudden zoom, no gimbal, no dolly or flying camera; the room behind him stays in the same place and the framing stays the same. "
"Sound: only diegetic, low murmur of a large hall, cutlery on gold, candle flicker, fabric; no music at all. No text or captions, no modern objects, no tall wigs on anyone but the king, only one king in the frame (no second face, no double).")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "T1_keyframe_edit_768.jpg", RAW + "anchors/POSE_P2_pleased_768.jpg"],
        "duration": 12, "resolution": "720p"}
open(H0 + "take2_T2a_v2_prompt.txt", "w").write(prompt)
r = apipod.submit("videos", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
open(H0 + "pilot_frames/TAKE2_T2a_v2.task_id", "w").write(tid)
res = apipod.wait("videos", tid, timeout=2400, every=10)
open(H0 + "pilot_frames/TAKE2_T2a_v2.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
u = find(d.get("result") or d)
if u: apipod.download(u, H0 + "pilot_frames/TAKE2_T2a_v2.mp4"); print("saved")
