"""C01 start frame: the painted ceiling seen by Marcel's phone (owner 29.10: the clip starts on the ceiling). Nano Banana 2.1, 2K, about $0.04. PAID: run only after the owner's yes."""
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


PROMPT = ("Vertical 9:16 phone photo taken by someone pointing a phone straight up at the ceiling of the King's state bedchamber at Versailles, around 1685: "
          "a gilded baroque ceiling with painted panels (an allegorical sky with clouds and putti), heavy carved gilt mouldings, cream and gold. "
          "At the very bottom edge the top of the gold brocade bed canopy with its fringe enters the frame at an angle. "
          "The tip of a white ostrich plume, very close to the lens and softly out of focus, intrudes from the lower left corner. "
          "Horizon rolled about 8 degrees, slight motion blur from a hand-held phone, bright window light washing the gilding, highlights slightly blown, "
          "real phone-camera look: ultra-wide distortion at the edges, fine sensor noise in the shadows. Same room, gilding and colours as the reference image. "
          "No people, no faces, no hands, no text, no lamps, no modern objects.")
body = {"model": "nano-banana-2.1", "prompt": PROMPT, "aspect_ratio": "9:16", "quality": "2K", "image_urls": [host("frames/C01.jpg")]}
r = apipod.submit("images", body); print(r)
tid = r["data"]["task_id"]; open("frames/C01_ceiling.jpg.task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=400, every=4); open("frames/C01_ceiling.jpg.status.json", "w").write(json.dumps(res, indent=1))
print("cost", (res.get("data") or {}).get("usage", {}).get("cost"))
apipod.download(find(res.get("data") or {}), "frames/C01_ceiling.jpg"); print("saved")
