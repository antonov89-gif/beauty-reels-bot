"""One ep.1 clip on Veo 3.1 via APIpod (owner 29.10: "сразу финальную" + "which model is cheaper": Veo 3.1 quality 1080p is about $0.8+ per 8-s clip vs Seedance 2.5 1080p $0.542/s).
Image-to-video from a first frame (image_urls[0]); 8 s fixed; Veo's own voice is only a lip-timing guide, our locked voice replaces it (build_clip.py).
Usage: python3 veo_clip.py <CID> <first_frame.jpg> "<prompt>" [veo3-1-quality] [1080p]
Signed result URLs carry a provider credential: they are stripped before anything is saved."""
import json, re, sys, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
CID, FRAME, PROMPT = sys.argv[1:4]; MODEL = sys.argv[4] if len(sys.argv) > 4 else "veo3-1-quality"; RES = sys.argv[5] if len(sys.argv) > 5 else "1080p"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip(); H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": FRAME.split("/")[-1], "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(FRAME, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
r = apipod.submit("videos", {"model": MODEL, "prompt": PROMPT, "image_urls": [d["publicUrl"]], "aspect_ratio": "9:16", "resolution": RES}); print(r)
tag = f"frames/veo_{CID.lower()}"; tid = r["data"]["task_id"]; open(tag + ".task_id", "w").write(tid)
res = apipod.wait("videos", tid, timeout=1200, every=8)
open(tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))


def find(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u:
            return u


data = res.get("data") or {}; print("status", data.get("status"), "usage", data.get("usage"), data.get("error"))
u = find(data.get("result") or data)
if u: apipod.download(u, tag + ".mp4"); print("saved", tag + ".mp4")
