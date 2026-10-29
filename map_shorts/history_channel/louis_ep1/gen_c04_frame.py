"""C04 first frame (29.10, owner "Да"): the storyboard C04.jpg has a different face, so the frame is redrawn with the king of C01-C03.
Refs: [0] identity = frames/C02_first.jpg (the generated king, same wig and gown), [1] composition = frames/C04.jpg (wig table shot). Nano Banana 2.1, 2K, about $0.04. PAID."""
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


PROMPT = ("Vertical 9:16 photo taken with a phone propped on a wooden dressing table in a gilded Versailles room, ultra-wide phone lens, low table-height angle, slightly rolled. "
          "The man from the FIRST reference image, EXACTLY the same face (same pale skin, light eyes, long nose, thin upturned moustache, same age), the same short curled brown night wig and the same gold embroidered silk dressing gown over a white lace shirt, "
          "leans over the table toward the phone and holds up a long dark curly full-bottomed wig toward the lens with his ringed hand, smug look. "
          "Composition like the SECOND reference image: a white powdered wig and a wooden wig stand in the left foreground, a gilded hand mirror, a powder puff and combs on the table, tall window and wood panelling behind, warm candle and window light. "
          "Photorealistic, real skin texture. No text, no modern objects, no other faces.")
body = {"model": "nano-banana-2.1", "prompt": PROMPT, "aspect_ratio": "9:16", "quality": "2K", "image_urls": [host("frames/C02_first.jpg"), host("frames/C04.jpg")]}
r = apipod.submit("images", body); print(r)
tid = r["data"]["task_id"]; open("frames/C04_v2.jpg.task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=400, every=4)
open("frames/C04_v2.jpg.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
print("cost", (res.get("data") or {}).get("usage", {}).get("cost"))
apipod.download(find(res.get("data") or {}), "frames/C04_v2.jpg"); print("saved")
