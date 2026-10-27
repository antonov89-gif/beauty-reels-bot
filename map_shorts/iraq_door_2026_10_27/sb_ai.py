"""Premium 3D restyle of the storyboard base frames with Nano Banana 2.1 edit (APIpod, $0.02 per 1K image).
The base frame (accurate Esri-free map + Natural Earth borders) is the layout reference; the model re-renders it as a tilted 3D documentary map
and adds the shot's 3D props. Text is never generated (our own graphics are composited later).
Usage: python3 sb_ai.py s01 s03 ... -> /home/claude/v86/ai/sNN.jpg ; runs 2 at a time (rate limit)."""
import json
import subprocess
import sys
import urllib.request

sys.path.insert(0, "/home/claude/v51")
import apipod  # noqa: E402

STYLE = ("Use the input image as the exact map layout. Re-render it as a premium cinematic 3D map shot from a high-end geography documentary: "
         "camera tilted about 35 degrees looking north, raised terrain relief with soft shadows, the red-highlighted country as a slightly raised "
         "glossy red layer with a glowing edge, crisp white borders, deep turquoise water with subtle realistic ripples and specular light, "
         "warm golden-hour light, gentle atmospheric haze at the horizon, depth of field, ultra detailed, 9:16 vertical. "
         "Keep coastlines, borders, rivers and the glowing lines exactly where they are in the input. "
         "No text, no letters, no numbers, no labels, no logos, no watermark. ")
PROPS = {
    "s01": "Add one detailed 3D crude oil supertanker leaving the tiny yellow-glowing coastline at the head of the gulf, small compared with the country.",
    "s02": "Add a dense miniature crowd of tiny stylised 3D people standing across the red country (no faces, generic), the coastline still glowing yellow.",
    "s03": "Add small 3D flag-free country markers: a glowing pin on the yellow coastline; the neighbours on the left (purple) and right (blue) slightly darker.",
    "s04": "Add 3D container cranes and an oil terminal at the yellow pin; the cyan glowing channel is a narrow water lane leading out to sea.",
    "s05": "Show the white dashed line as a floating 3D dashed border in the middle of the channel and the cyan lane as a glowing deep-water route nearer the purple side.",
    "s06": "Add a large 3D crude oil tanker sailing exactly ON the glowing cyan line (the deep-water lane), its hull centred on that line in open water, bow pointing toward the open sea at the lower right, white wake behind it.",
    "s07": "Add big modern 3D port cranes and docks at the purple pin (on the island) and a second port under construction with cranes at the red pin across the water.",
    "s08": "Add a giant translucent 3D steel gate half-closing across the cyan channel between the two ports, dramatic lighting.",
    "s09": "Add the oil supertanker small at the head of the gulf, and a dramatic sunset sky over the whole region.",
}


def upload(path):
    K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip()
    H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
    req = urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": path.split("/")[-1], "contentType": "image/jpeg"}).encode(),
                                 headers=H, method="POST")
    d = json.load(urllib.request.urlopen(req, timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
    return d["publicUrl"]


def find(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    if isinstance(x, (dict, list)):
        for v in (x.values() if isinstance(x, dict) else x):
            u = find(v)
            if u:
                return u


def one(s):
    url = upload(f"/home/claude/v86/base/{s}.jpg")
    r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + PROPS[s], "aspect_ratio": "9:16", "quality": "1K", "image_urls": [url]})
    tid = (r.get("data") or {}).get("task_id")
    if not tid:
        return s, "SUBMIT FAIL " + json.dumps(r)[:200]
    open(f"/home/claude/v86/ai/{s}.task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=400, every=4)
    u = find(res.get("data") or {})
    if not u:
        return s, "FAIL " + json.dumps(res)[:200]
    apipod.download(u, f"/home/claude/v86/ai/{s}.jpg")
    return s, "ok"


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--one":
        print(*one(sys.argv[2]), flush=True)
        sys.exit()
    ids = sys.argv[1:]
    for k in range(0, len(ids), 2):
        ps = [subprocess.Popen([sys.executable, __file__, "--one", s]) for s in ids[k:k + 2]]
        for p in ps:
            p.wait()
