"""C02 (owner 29.10 "да", about $5.8: draft 480p about $0.88, then 1080p final about $4.88 only after the owner sees the draft).
Same method as C01 v4: Seedance 2.5 Draft IMAGE-ONLY, first frame = the LAST frame of the approved C01 (seedance25_p2v4_final.mp4), so C01 -> C02 has no visible cut; he keeps filming himself (selfie). 9 s (our C02 voice is 7.8 s).
Our locked voice is aligned to the model's speech afterwards; the model's own audio is dropped.
Usage: python3 seedance25_c02.py show | draft | final <draft_task_id>
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


prompt = ("Continue this exact shot without any cut: a vertical hand-held phone selfie video, ultra-wide front camera, the same vain French king in the same short curled brown night wig and gold embroidered silk dressing gown, reclining on the pillows of his canopied state bed, holding the phone himself at arm's length; courtiers move quietly in the background. "
          "The phone stays steady with only tiny natural hand micro-shake; the camera does not zoom and does not travel. With his free ringed hand he touches and adjusts one curl of his wig, then leans a little toward the lens as if sharing a secret, eyes sparkling, a tiny head tilt, and speaks straight into the lens, lips clearly moving with every word, proud and conspiratorial: "
          "\"Some mornings, a hundred people watch me wake up. The ceremony is called the rising. I call it opening night.\" "
          "A small satisfied 'hm' before he starts, a soft laugh into 'opening night', then a silent pleased smile at the lens. Natural blinking, real skin texture, photorealistic. No music.")
body = {"model": "seedance-2.5-draft", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C02_first.jpg", "image/jpeg")],
        "duration": 9, "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
if mode == "final":
    body = {"model": "seedance-2.5-draft", "draft_task_id": sys.argv[2], "resolution": "1080p"}
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode in ("draft", "final"):
    tag = "seedance25_c02_" + mode
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
