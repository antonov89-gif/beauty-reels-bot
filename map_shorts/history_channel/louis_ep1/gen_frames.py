"""Run frames_louis.F through APIpod (Nano Banana 2.1, 1K, $0.02 each), several at a time. Usage: python3 gen_frames.py [id id ...] (default: all missing)
Reference images are hosted on Zernio media once per run. Task ids and statuses are saved first; a failed download is retried from the saved status (no new charge)."""
import json
import os
import sys
import threading
import urllib.request

sys.path.insert(0, "/home/claude/v51")
import apipod
from frames_louis import F, STYLE

CARD = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_card/"
OUT = "frames/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
urls = {}


def host(name):
    if name not in urls:
        d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": name, "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
        urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(CARD + name, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
        urls[name] = d["publicUrl"]
    return urls[name]


def find(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u:
            return u


cost = {}


def one(fid):
    refs, scene = F[fid]
    out = OUT + fid + ".jpg"
    body = {"model": "nano-banana-2.1", "prompt": "Keep exactly the same man, face, wig and costume as in the reference images. " + STYLE + " " + scene, "aspect_ratio": "9:16", "quality": "1K", "image_urls": [host(r) for r in refs]}
    r = apipod.submit("images", body)
    if "data" not in r:
        print(fid, "SUBMIT FAILED", r); return
    tid = r["data"]["task_id"]; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=400, every=4); open(out + ".status.json", "w").write(json.dumps(res, indent=1))
    cost[fid] = (res.get("data") or {}).get("usage", {}).get("cost")
    u = find(res.get("data") or {})
    for a in range(3):
        try:
            apipod.download(u, out); break
        except Exception as e:
            print(fid, "download retry", a, e)
    print(fid, "done", cost[fid], os.path.getsize(out) if os.path.exists(out) else 0)


ids = sys.argv[1:] or [i for i in F if not (os.path.exists(OUT + i + ".jpg") and os.path.getsize(OUT + i + ".jpg") > 1000)]
sem = threading.Semaphore(5)


def run(i):
    with sem:
        one(i)


ts = [threading.Thread(target=run, args=(i,)) for i in ids]
[t.start() for t in ts]; [t.join() for t in ts]
print("total", round(sum(v or 0 for v in cost.values()), 3), "for", len(ids))
