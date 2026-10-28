"""One Nano Banana 2.1 character-card frame via APIpod ($0.02 at 1K). Optional reference image (the approved face) keeps the identity.
Usage: python3 gen_card.py <out.jpg> "<prompt>" [ref.jpg]
The reference is hosted on Zernio media (public URL), as in iraq_door/sb_ai.py. The task id is saved before waiting."""
import json
import sys
import urllib.request

sys.path.insert(0, "/home/claude/v51")
import apipod

STYLE = ("Photorealistic vertical 9:16 character reference frame of a living human actor in 17th-century French court dress, cinema camera, 50mm lens, "
         "soft natural window light with warm candle fill, true-to-life skin texture, fabric, lace and gold embroidery, neutral gilded-wall background, "
         "no text, no logos, no watermark, no modern objects.")
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
