"""C01 part 1 (0-3 s): Kling 4.0 image-to-video, first frame = the ceiling, last frame = the C01 king frame, ONE continuous tilt, no speech.
Usage: python3 kling_i2v_part1_v2.py estimate | go (PAID, owner said yes on 29.10, about $0.65 at 1080p). Task id and status are saved before/after waiting."""
import json, sys, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep1/"
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


prompt = ("Raw hand-held phone footage, ultra-wide lens. The page stands STILL beside the bed and only ROTATES the phone: a pure tilt from pointing up to pointing at the king, like turning a phone in the hand. "
          "The camera position never changes: no dolly, no zoom, no forward movement, no flying; the king, the bed and the canopy keep exactly the same size in the frame the whole time, they only slide through the frame as the phone pitches down. "
          "It starts on @first_frame: the painted gilded ceiling, the canopy edge and the top of the king's wig at the bottom edge, a white plume at the right edge, small natural hand shake. "
          "Then ONE continuous downward tilt, no cut: motion blur, a hint of rolling-shutter wobble, the exposure drops from the bright ceiling to the warm bed, the autofocus hunts, and the phone lands on @last_frame with a small overshoot and settle: the king in the bed looking straight into the lens. "
          "No speech, no music, only room tone and fabric rustle.")
body = {"model": "kling-4.0-i2v", "prompt": prompt, "image_urls": [host(H0 + "frames/C01_ceiling2.jpg"), host(H0 + "frames/C01.jpg")], "duration": 3, "resolution": "1080p"}
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:700])
if sys.argv[1:] == ["go"]:
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "frames/kling_i2v_part1_v2.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1500, every=10); open(H0 + "frames/kling_i2v_part1_v2.status.json", "w").write(json.dumps(res, indent=1))
    print(json.dumps(res)[:800])
    u = find(res.get("data") or {}); print("url", u)
    if u: apipod.download(u, H0 + "frames/kling_i2v_part1_v2.mp4")
