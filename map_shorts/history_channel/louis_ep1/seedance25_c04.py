"""C04 (owner 29.10 "Да", about $5.2 with the new first frame: draft 480p about $0.78, then 1080p final about $4.34 only after the owner sees the draft).
HARD CUT to the wig table (script): first frame = frames/C04_first.jpg (redrawn with the C01-C03 king by gen_c04_frame.py, cropped to 1080x1920).
Same method as C01 v4: Seedance 2.5 Draft IMAGE-ONLY, phone propped on the table by him. 8 s (our C04 voice is 6.8 s).
Our locked voice is aligned to the model's speech afterwards; the model's own audio is dropped.
Usage: python3 seedance25_c04.py show | draft | final <draft_task_id>
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


prompt = ("Continue this exact shot: a vertical phone video from a phone propped on a wooden dressing table, low table-height angle, the phone does not move at all (no zoom, no camera travel). "
          "The same vain French king in the short curled brown night wig and the gold embroidered silk dressing gown leans over the table and lifts the long dark curly full-bottomed wig toward the lens with his ringed hand, then speaks straight into the lens, lips clearly moving with every word: "
          "\"Now, the wig. My hair started falling out at seventeen. I took it personally, so I got a wig.\" "
          "Brisk on 'Now, the wig', a mock-tragic sigh on 'falling out', his free hand on his chest, lower lip pushed out, brow knit with wounded pride, then he lifts his chin with dry resolve on 'so I got a wig' and shakes the dark wig slightly. "
          "Natural blinking, real skin texture, photorealistic. No music.")
body = {"model": "seedance-2.5-draft", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C04_first.jpg", "image/jpeg")],
        "duration": 8, "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
if mode == "final":
    body = {"model": "seedance-2.5-draft", "draft_task_id": sys.argv[2], "resolution": "1080p"}
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode in ("draft", "final"):
    tag = "seedance25_c04_" + mode
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
