"""C01 start frame v2 (29.10): the SAME camera position as the C01 frame, pitched up 60 degrees (rotation only), so a tilt between the two frames cannot make the camera fly. Nano Banana 2.1, 2K, about $0.04. PAID: run only after the owner's yes."""
import json, sys, urllib.request
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


PROMPT = ("Same room and EXACTLY the same camera position as the reference photo (the phone has not moved, it is held at the same spot, the same height, the same distance from the bed), "
          "but the phone is now tilted straight up by about 60 degrees, pure rotation. Vertical 9:16 hand-held phone photo: the painted gilded baroque ceiling with its carved gilt mouldings fills most of the frame. "
          "At the bottom edge, at the SAME scale as in the reference photo, the front edge of the gold brocade bed canopy with its fringe and, just below it, the very top of the king's curled dark wig entering the frame. "
          "The tip of a white ostrich plume, soft and out of focus, at the right edge as in the reference. Ultra-wide phone lens, slight roll, slight motion blur, bright window light on the gilding. "
          "Same gilding, colours and canopy as the reference. No other people, no hands, no text, no modern objects.")
body = {"model": "nano-banana-2.1", "prompt": PROMPT, "aspect_ratio": "9:16", "quality": "2K", "image_urls": [host("frames/C01.jpg")]}
r = apipod.submit("images", body); print(r)
tid = r["data"]["task_id"]; open("frames/C01_ceiling2.jpg.task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=400, every=4); open("frames/C01_ceiling2.jpg.status.json", "w").write(json.dumps(res, indent=1))
print("cost", (res.get("data") or {}).get("usage", {}).get("cost"))
apipod.download(find(res.get("data") or {}), "frames/C01_ceiling2.jpg"); print("saved")
