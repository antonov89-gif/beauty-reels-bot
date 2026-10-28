"""Character card v2 (owner 28.10: more hype and extravagant, documentary look like the Elizabeth channel). Same CLI as gen_card.py."""
import json
import sys
import urllib.request

sys.path.insert(0, "/home/claude/v51")
import apipod

STYLE = ("Raw documentary-style vertical 9:16 frame, as if filmed on a phone front camera by a vlogger inside Versailles: ultra-wide lens with slight perspective distortion, handheld, "
         "natural window light with candle glow, hyper-real skin with visible pores, powder and fine lines, true-to-life heavy fabric, gold embroidery, lace and jewels, "
         "17th-century French court, no text, no logos, no watermark, no modern objects.")
out, scene = sys.argv[1], sys.argv[2]
body = {"model": "nano-banana-2.1", "prompt": STYLE + " " + scene, "aspect_ratio": "9:16", "quality": "1K"}
if len(sys.argv) > 3:
    K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip()
    H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
    ref = sys.argv[3]
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": ref.split("/")[-1], "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(ref, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
    body["image_urls"] = [d["publicUrl"]]
    body["prompt"] = "Keep exactly the same man, face and wig as in the reference image. " + body["prompt"]
r = apipod.submit("images", body)
print(r)
tid = r["data"]["task_id"]
open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=300, every=4)
open(out + ".status.json", "w").write(json.dumps(res, indent=1))
print(json.dumps(res)[:400])


def find(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u:
            return u


u = find(res.get("data") or {})
print("url", u)
apipod.download(u, out)
