"""C04 remake PILOT on Seedance 2.5 LITE i2v (owner 30.10 "а": one generation, 720p, 9 s, $0.15/s = about $1.35 by the APIpod pricing page).
Goals of the pilot: quality of the Lite face/skin, whether it starts from our first frame, whether it makes useful sound; the short line (compare_reference_ep1_v2.md).
HARD CUT to the wig table (script): first frame = frames/C04_first.jpg (redrawn with the C01-C03 king by gen_c04_frame.py, cropped to 1080x1920).
Same method as C01 v4: Seedance 2.5 Draft IMAGE-ONLY, phone propped on the table by him. 9 s (our C04 voice is 6.8 s; v2: the 8-s draft skipped 'I took it personally').
Our locked voice is aligned to the model's speech afterwards; the model's own audio is dropped.
Usage: python3 seedance25lite_c04.py show | go
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


prompt = ("A vertical phone video, front camera of a smartphone that is propped loosely against a jar on a wooden dressing table, low table-height angle. "
          "The phone is not fixed: it sways a little and drifts, and when he leans on the table the phone gets nudged and re-settles; never a smooth camera move, never a zoom. "
          "The same vain French king in the short curled brown night wig and the gold embroidered silk dressing gown leans over the table and lifts the long dark curly full-bottomed wig toward the lens with his ringed hand, then speaks straight into the lens, lips clearly moving with every word, unhurried, with real pauses, saying exactly: "
          "\"Now, the wig.\" (a short pause) \"My hair started falling out at seventeen.\" (a full one-second pause: he looks at the wig with wounded pride, says nothing) \"I took it personally.\" "
          "Mock-tragic sigh on 'falling out', free hand on his chest, then a dry, offended lift of the chin on 'I took it personally'. "
          "Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, no glow, not golden everywhere. "
          "Sound: recorded by the phone's own microphone: his voice close, the phone being knocked on the wood when he leans, a soft rustle of the silk gown and the wig hair, a quiet room with a faint crackle of a fireplace. No music.")
body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C04_first.jpg", "image/jpeg")],
        "duration": 9, "resolution": "720p", "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25lite_c04"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
