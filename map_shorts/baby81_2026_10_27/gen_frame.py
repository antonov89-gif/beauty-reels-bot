"""One Nano Banana 2.1 frame via APIpod ($0.02 at 1K). Usage: python3 gen_frame.py <out.jpg> "<prompt>" [quality]"""
import sys, time
sys.path.insert(0, "/home/claude/v51")
import apipod
STYLE = open("/home/user/beauty-reels-bot/map_shorts/prompts/style_zackd_3d_render.md").read().split("STYLE v2 instead of the photoreal prefix:\n")[1].split("\n")[0]
out, scene = sys.argv[1], sys.argv[2]; q = sys.argv[3] if len(sys.argv) > 3 else "1K"
r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + " " + scene, "aspect_ratio": "9:16", "quality": q})
print(r)
tid = r["data"]["task_id"]
open(out + ".task_id", "w").write(tid)   # never lose a paid task id
res = apipod.wait("images", tid, timeout=300, every=4)
import json; open(out + ".status.json", "w").write(json.dumps(res, indent=1)); print(json.dumps(res)[:700])
d = res.get("data") or {}
def find_url(x):
    if isinstance(x, str) and x.startswith("http"): return x
    if isinstance(x, dict):
        for v in x.values():
            u = find_url(v)
            if u: return u
    if isinstance(x, list):
        for v in x:
            u = find_url(v)
            if u: return u
url = find_url(d)
print("url", url)
apipod.download(url, out)
