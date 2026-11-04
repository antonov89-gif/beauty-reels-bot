"""T1 pilot RETAKE, Kling 4.0 i2v 720p 11s from F01a, with the @first_frame tag fixed (owner 04.11 "да" after the tag-bug explanation). Price: $0.145/s x 11 = $1.595 (same as the first try). One yes = this one call. Usage: python3 gen_t1_kling40_v2.py show | go."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/pilot_frames/"
CAMERA = ("Filmed by himself on a phone held in one hand at arm's length, and he is clumsy with it: constant natural hand-held sway and small roll, the framing drifts, his face slides off-centre and he re-centres it with small jerks, at moments the phone comes too close and the horizon tilts. "
          "Never a smooth gimbal move, never a zoom, never a dolly or flying camera: every move comes from his arm and body. ")
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. Keep exactly the same king throughout: tall white-grey powdered wig, heavy-lidded haughty eyes, thin waxed moustache, beauty mark beside the mouth, light rouge, scarlet velvet coat with gold suns, lace cravat, jewelled rings. Realistic live action, real skin texture, no beauty filter. "
          "0-3 s: @first_frame stays, the phone too close and out of focus, his own scarlet sleeve and fist covering the top half; a muffled voice, the king mumbles: \"Is it... is it on?\" while his thumb taps the screen and the sleeve slides off the lens. "
          "3-5 s: he pulls the phone back to arm's length and sees himself; surprise turns into pleasure: \"Ah. There I am.\" "
          "5-7 s: a small clearing of the throat, he sits up straight at the head of the long table, chin up, heavy lids, the crowd of courtiers in plain wigs behind him in warm candlelight. "
          "7-11 s: he looks straight into the lens, grand and formal, with natural lip movement: \"Bonjour. I am Louis, King of France.\" then a tiny proud nod. "
          + CAMERA +
          "Sound: only diegetic, low murmur of a large hall, cutlery on gold, candle flicker, fabric; no music at all. No text or captions, no modern objects, no tall wigs on anyone but the king.")
body = {"model": "kling-4.0-i2v", "prompt": prompt, "image_urls": [RAW + "F01a_v1_owner.jpg"], "duration": 11, "resolution": "720p"}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:90] + "...") for k, v in body.items()}, indent=1))
if mode == "show":
    open(H0 + "t1_kling40_v2_prompt.txt", "w").write(prompt)
if mode == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/T1_kling40_v2.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "pilot_frames/T1_kling40_v2.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/T1_kling40_v2.mp4"); print("saved")
