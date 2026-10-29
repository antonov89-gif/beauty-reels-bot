"""C07 (owner 29.10 "Давай сразу чистовик на 720п"): Seedance 2.5 i2v DIRECT at 720p, 8 s, $0.2205/s = about $1.76 (APIpod pricing page). Hard cut into take 3, so the direct route (which does not keep the exact first frame) is acceptable here.
First frame = frames/C07_first.jpg (C07_v7.jpg cropped to 1080x1920). Camera = CAMERA_BASE + the C07 beats of camera_plan_ep1.md. Addressees per the screenwriter review.
Usage: python3 seedance25_c07.py show | go
Signed result URLs carry a provider credential: they are stripped before anything is saved."""
import json, re, subprocess, sys, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}


def host(path, ctype):
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": path.split("/")[-1], "contentType": ctype}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": ctype}), timeout=120)
    return d["publicUrl"]


def find(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u:
            return u


CAMERA_BASE = ("Filmed by himself on a phone held in one hand at arm's length, and he is clumsy with it: constant natural hand-held sway and small roll, the framing keeps drifting, his face slides off-centre and he re-centres it with small jerks, at moments the phone comes too close, the horizon tilts and is corrected. "
               "Never a smooth gimbal move, never a zoom, never a dolly or flying camera: every move comes from his arm and body, the phone always within arm's reach. ")
prompt = (CAMERA_BASE +
          "Continue from this exact frame: the same vain French king in the tall grey-white powdered wig, white powdered face with pink rouge, gold embroidered silk dressing gown and white lace jabot, in the gilded state bedchamber; courtiers in period dress are entering through the doors far behind him. "
          "0-2 s: the phone wobbles as he settles it, his face a little right of centre. 2-5 s: he turns his head over his shoulder toward the courtiers and commands them, regal and bored: \"Bow. Lower. Good.\" The phone swings with his shoulder, the horizon rolls, the courtiers behind him bow lower and lower, and he gives an approving nod on 'Good'. "
          "5-8 s: he turns back to the lens, re-centres the phone with a jerk so that for a moment it is far too close, backs off, taps his tall wig with a ringed finger and says to the viewer, delighted and arrogant: \"Yes, this is the new wig. Take notes.\" "
          "Lips clearly moving with every word. Same face, wig, makeup and costume as the first frame. Natural blinking, real skin texture, photorealistic. No music.")
body = {"model": "seedance-2.5-i2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C07_first.jpg", "image/jpeg")],
        "duration": 8, "resolution": "720p", "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25_c07_720"
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
