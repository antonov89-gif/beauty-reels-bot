"""One image-to-video clip through APIpod, model-specific bodies (schemas from docs.apipod.ai, 27.10.2026).
Usage: python3 gen_clip_multi.py <model> <frame.jpg> <out.mp4> "<motion prompt>" [duration]
models: veo3-1-quality (8 s fixed, 720p), kling-4.0-i2v (duration 3-30, 720p), seedance-2.0-i2v (duration 4-15, 720p, 9:16, native audio on).
The frame is hosted on Zernio media (public URL). The task id is saved before waiting."""
import json
import sys
import urllib.request

sys.path.insert(0, "/home/claude/v51")
import apipod

model, frame, out, motion = sys.argv[1:5]
dur = int(sys.argv[5]) if len(sys.argv) > 5 else 5
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}


def zc(path, body):
    return json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1" + path, data=json.dumps(body).encode(), headers=H, method="POST"), timeout=60))


d = zc("/media/presign", {"filename": frame.split("/")[-1], "contentType": "image/jpeg"})
urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(frame, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
url = d["publicUrl"]; print("frame url", url)
body = {"model": model, "prompt": motion, "image_urls": [url]}
if model == "veo3-1-quality":
    body.update(aspect_ratio="9:16", resolution="720p")
elif model == "kling-4.0-i2v":
    body.update(duration=dur, resolution="720p")
elif model == "seedance-2.0-i2v":
    body.update(duration=dur, resolution="720p", aspect_ratio="9:16", generate_audio=True)
else:
    raise SystemExit("unknown model " + model)
r = apipod.submit("videos", body)
print(r)
tid = r["data"]["task_id"]; open(out + ".task_id", "w").write(tid)
res = apipod.wait("videos", tid, timeout=1200, every=8); open(out + ".status.json", "w").write(json.dumps(res, indent=1)); print(json.dumps(res)[:600])


def find(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u:
            return u


u = find(res.get("data") or {}); print("url", u)
apipod.download(u, out)
