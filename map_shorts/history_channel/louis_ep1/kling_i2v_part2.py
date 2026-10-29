"""C01 part 2 (speech): Kling 4.0 image-to-video, first frame = the last frame of part 1 v2, the king speaks the opener; the generated audio is muted and replaced by the locked voice.
Usage: python3 kling_i2v_part2.py estimate | go (PAID, owner said yes on 29.10, about $1.96 at 1080p, 9 s). Task id and status are saved before/after waiting."""
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


prompt = ("Raw hand-held phone footage, ultra-wide lens, held by a page who stands still beside the bed: only tiny natural hand micro-shake, the camera does not move, no zoom. "
          "@first_frame: a vain French king in a short dark curled night wig and a gold silk dressing gown, propped on the pillows of his canopied state bed, courtiers in the background. "
          "He speaks English straight into the lens with a smug, haughty, drawling, arrogant manner, clear natural lip movement, timed like this: "
          "0.0-1.7 s, irritated and sharp: \"Marcel, not the ceiling.\" 1.7-2.3 s: \"Me.\" tapping his chest with one finger. 2.3-3.1 s, satisfied as the phone steadies: \"Good.\" "
          "3.3-5.2 s, smug and drawling: \"Welcome to Versailles.\" 5.2-7.1 s, delighted with himself, chin up: \"Yes, I'm that handsome.\" 7.1-8.4 s, sneering, one eyebrow up: \"Try not to faint.\" "
          "8.4-9.0 s: silent smirk. Keep his face, wig, moustache and gown exactly as in @first_frame, natural blinking, real skin. Room tone only, absolutely no music.")
body = {"model": "kling-4.0-i2v", "prompt": prompt, "image_urls": [host(H0 + "frames/C01_part2_first.jpg")], "duration": 9, "resolution": "1080p"}
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:700])
if sys.argv[1:] == ["go"]:
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "frames/kling_i2v_part2.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1500, every=10); open(H0 + "frames/kling_i2v_part2.status.json", "w").write(json.dumps(res, indent=1))
    print(json.dumps(res)[:800])
    u = find(res.get("data") or {}); print("url", u)
    if u: apipod.download(u, H0 + "frames/kling_i2v_part2.mp4")
