"""C07 first frame (29.10, owner "Да"): take 3 is a HARD CUT into the court scene; redrawn with the generated king.
Refs: [0] identity = frames/C06_last.jpg (the generated king, brown wig, gown), [1] composition = frames/C07.jpg (storyboard: low floor angle, hand sweeping in from the top). Nano Banana 2.1, 2K, about $0.04. PAID."""
import json, re, sys, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}


def host(path):
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": path.split("/")[-1], "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
    return d["publicUrl"]


def find(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u:
            return u


PROMPT = ("Vertical 9:16 photo taken with a phone lying on a polished parquet floor and looking up, ultra-wide phone lens, strong perspective, very low angle, slightly rolled, in a gilded Versailles state bedchamber with a canopied bed on the left, tall windows and a crystal chandelier above. "
          "The man from the FIRST reference image, EXACTLY the same face (same pale skin, light eyes, long nose, thin upturned moustache, same age), now wearing a tall white-grey powdered full-bottomed wig with long curls over his shoulders, the same gold embroidered silk dressing gown over a white lace shirt, white stockings and black buckled shoes, "
          "stands full length in the middle of the frame with his ringed hand raised, a smug look down at the lens. "
          "A man's hand sweeps into the frame from the top edge, out of focus, as if re-aiming the phone. Behind him in the distance the double doors are opening and courtiers in period dress are entering. "
          "Composition like the SECOND reference image. Warm window and candle light. Photorealistic, real skin texture. No text, no modern objects.")
body = {"model": "nano-banana-2.1", "prompt": PROMPT, "aspect_ratio": "9:16", "quality": "2K", "image_urls": [host("frames/C06_last.jpg"), host("frames/C07.jpg")]}
r = apipod.submit("images", body); print(r)
tid = r["data"]["task_id"]; open("frames/C07_v2.jpg.task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=400, every=4)
open("frames/C07_v2.jpg.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
print("cost", (res.get("data") or {}).get("usage", {}).get("cost"))
apipod.download(find(res.get("data") or {}), "frames/C07_v2.jpg"); print("saved")
