"""C06 (reference manner, owner 29.10 "делай как референс"): Seedance 2.5 draft route (keeps the exact first frame), 9 s (our C06 voice is 7.4 s). Draft about $0.88; the 1080p final about $4.88 is a SEPARATE yes.
First frame = frames/C06_first.jpg (last frame of the C05 take). The camera becomes hand-held: he picks the phone up from the table.
Same method as C01 v4: Seedance 2.5 Draft IMAGE-ONLY, 
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


prompt = ("Continue this exact shot without any cut, one continuous hand-held phone video: the same vain French king at the wig table in the gilded room picks the phone up from the table with his free hand, so the view lifts and sways naturally like a real phone in a hand, and holds it at arm's length as a selfie, close, ultra-wide front camera with real wide-angle distortion, constant gentle hand-held sway and small roll, no zoom, the phone always within arm's reach. "
          "Same face, same short curled brown wig, same gold embroidered silk robe and white lace shirt as the first frame. He takes the white powdered wig from its stand and pushes it right into the lens so the white curls fill the frame for a moment, then pulls it back, looks at it, sniffs with mock disdain and speaks straight into the lens, lips clearly moving with every word, savouring each word, theatrical and prophetic: "
          "\"White, grey, a little powder. One day, everybody will wear this. I'm just early.\" "
          "A modest lowered gaze and a sly smile on 'I'm just early', a small chuckle. Natural blinking, real skin texture, photorealistic. No music.")
body = {"model": "seedance-2.5-draft", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C06_first.jpg", "image/jpeg")],
        "duration": 9, "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
if mode == "final":
    body = {"model": "seedance-2.5-draft", "draft_task_id": sys.argv[2], "resolution": "1080p"}
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode in ("draft", "final"):
    tag = "seedance25_c06_" + mode
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
