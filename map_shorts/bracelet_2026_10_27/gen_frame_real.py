"""One Nano Banana 2.1 frame via APIpod ($0.02 at 1K), photoreal macro look (this channel: realistic, not STYLE v2 3D).
Usage: python3 gen_frame_real.py <out.jpg> "<scene prompt>" [quality]"""
import json
import sys
sys.path.insert(0, "/home/claude/v51")
import apipod

STYLE = ("Photorealistic vertical 9:16 documentary macro footage frame, shot on a cinema camera with a 50mm macro lens, shallow depth of field, "
         "natural warm workshop light with soft window fill, true-to-life skin and metal, fine real-world detail, no stylisation, no text, no logos, no watermark.")
out, scene = sys.argv[1], sys.argv[2]; q = sys.argv[3] if len(sys.argv) > 3 else "1K"
r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + " " + scene, "aspect_ratio": "9:16", "quality": q})
print(r)
tid = r["data"]["task_id"]
open(out + ".task_id", "w").write(tid)   # never lose a paid task id
res = apipod.wait("images", tid, timeout=300, every=4)
open(out + ".status.json", "w").write(json.dumps(res, indent=1)); print(json.dumps(res)[:500])


def find_url(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find_url(v)
        if u:
            return u


url = find_url(res.get("data") or {})
print("url", url)
apipod.download(url, out)
