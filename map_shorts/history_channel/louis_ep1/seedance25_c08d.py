"""C08 via the DRAFT route (owner 29.10 "Да"): image-only Seedance 2.5 draft keeps the exact first frame. Draft 480p, 8 s, about $0.78; the final (720p about $1.76 if the draft route accepts 720p, else 1080p about $4.34) is a SEPARATE yes.
First frame = frames/C08_first_draft.jpg (the last frame of the C07 take: face close, hand on the wig). Camera = CAMERA_BASE + the C08 beats of camera_plan_ep1.md. No phone visible in his hand (the first direct take drew one).
Usage: python3 seedance25_c08d.py show | draft | final <draft_task_id> [720p|1080p]
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
               "Never a smooth gimbal move, never a zoom, never a dolly or flying camera: every move comes from his arm and body, the phone always within arm's reach. The filming phone is never visible in the picture, and his hands hold nothing. ")
prompt = (CAMERA_BASE +
          "Continue this exact shot without any cut, from this exact frame: the same vain French king in the tall grey-white powdered wig, white powdered face with pink rouge, gold embroidered silk dressing gown and white lace jabot, in the gilded state bedchamber; courtiers behind him keep bowing. "
          "0-2 s: he lowers his hand from the wig, eases the phone back a little so the room and the bowing court show behind him, sweeps a contemptuous look over the court, then looks back at the lens and speaks, bored and scornful: \"All these people, and nobody may speak before me.\" "
          "2-5 s: without noticing, he brings the phone closer and closer, so that his face slowly fills the whole frame and the top of the tall wig is cut off by the upper edge; his expression turns tender and adoring: \"I love listening.\" "
          "5-8 s: with the phone very close, he snorts a laugh at his own joke and says, amused: \"To myself, mostly.\" The phone jolts and tilts a little with the laugh. "
          "Lips clearly moving with every word. Same face, wig, makeup and costume as the first frame. Natural blinking, real skin texture, photorealistic. No music.")
body = {"model": "seedance-2.5-draft", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C08_first_draft.jpg", "image/jpeg")],
        "duration": 8, "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
if mode == "final":
    body = {"model": "seedance-2.5-draft", "draft_task_id": sys.argv[2], "resolution": (sys.argv[3] if len(sys.argv) > 3 else "1080p")}
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode in ("draft", "final"):
    tag = "seedance25_c08d_" + mode
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
