"""One Veo 3.1 clip from a start frame via APIpod. Usage: python3 gen_clip.py <frame.jpg> <out.mp4> "<motion prompt>" [model veo3-1-fast] [resolution 720p]
Frame is hosted on Zernio media (public URL). Task id and status are saved before download."""
import sys, json, urllib.request
sys.path.insert(0, "/home/claude/v51"); import apipod
frame, out, motion = sys.argv[1], sys.argv[2], sys.argv[3]
model = sys.argv[4] if len(sys.argv) > 4 else "veo3-1-fast"; res = sys.argv[5] if len(sys.argv) > 5 else "720p"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip(); H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
def zc(path, body):
    return json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1" + path, data=json.dumps(body).encode(), headers=H, method="POST"), timeout=60))
d = zc("/media/presign", {"filename": frame.split("/")[-1], "contentType": "image/jpeg"})
urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(frame, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
url = d["publicUrl"]; print("frame url", url)
r = apipod.submit("videos", {"model": model, "prompt": motion, "image_urls": [url], "aspect_ratio": "9:16", "resolution": res})
print(r); tid = r["data"]["task_id"]; open(out + ".task_id", "w").write(tid)
res_ = apipod.wait("videos", tid, timeout=900, every=8); open(out + ".status.json", "w").write(json.dumps(res_, indent=1)); print(json.dumps(res_)[:600])
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    if isinstance(x, (dict, list)):
        for v in (x.values() if isinstance(x, dict) else x):
            u = find(v)
            if u: return u
u = find(res_.get("data") or {}); print("url", u)
apipod.download(u, out)
