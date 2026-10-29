"""C03 (owner 29.10 "Да", about $5.1: draft 480p about $0.78, then 1080p final about $4.34 only after the owner sees the draft).
Same method as C01 v4: Seedance 2.5 Draft IMAGE-ONLY, first frame = the LAST frame of C02 (seedance25_c02_final.mp4), so C02 -> C03 has no visible cut; he keeps filming himself (selfie). 8 s (our C03 voice is 6.5 s).
Our locked voice is aligned to the model's speech afterwards; the model's own audio is dropped.
Usage: python3 seedance25_c03.py show | draft | final <draft_task_id>
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


prompt = ("Continue this exact shot without any cut: a vertical hand-held phone selfie video, ultra-wide front camera, the same vain French king in the same short curled brown night wig and gold embroidered silk dressing gown, reclining on the pillows of his canopied state bed, holding the phone himself at arm's length. "
          "The phone stays steady with only tiny natural hand micro-shake; the camera does not zoom and does not travel. Behind him two men step up to the bedside and wait: a royal doctor in a long black robe and black skullcap, and a surgeon in a plain dark coat with a leather case. "
          "He glances at them over his shoulder with heavy bored eyelids, looks away, then his eyes shine back at the lens with a pleased smile, and he speaks straight into the lens, lips clearly moving with every word, dry and smug: "
          "\"The doctor's here, the surgeon's here, and nobody came to see them. Everyone came to see me. Naturally.\" "
          "A satisfied breath before 'Naturally', said slowly with a smug little nod, then a silent pleased smile. The two men stay politely in the background. Natural blinking, real skin texture, photorealistic. No music.")
body = {"model": "seedance-2.5-draft", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C03_first.jpg", "image/jpeg")],
        "duration": 8, "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
if mode == "final":
    body = {"model": "seedance-2.5-draft", "draft_task_id": sys.argv[2], "resolution": "1080p"}
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode in ("draft", "final"):
    tag = "seedance25_c03_" + mode
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
