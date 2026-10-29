"""C05 redo (owner 29.10 "Да, 2"): the Veo take had a different face; Seedance 2.5 i2v DIRECT 1080p (no draft), 8 s, about $4.34 ($0.542/s, APIpod pricing page).
First frame = frames/C05_first.jpg (last frame of C04 final), so C04 -> C05 has no visible cut.
Usage: python3 seedance25_c05.py show | go
Signed result URLs carry a provider credential: they are stripped before anything is saved."""
import json, re, subprocess, sys, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}


def host(path, ctype):
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": path.split("/")[-1], "contentType": ctype}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": ctype}), timeout=120)
    return d["publicUrl"]


def find(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u:
            return u


prompt = ("Continue this exact shot without any cut: a vertical phone video from a phone resting on a wooden dressing table in a gilded palace room; the phone stays perfectly still, no zoom, no camera movement. "
          "The same proud French king stays in the same place and pose, leaning over the table behind the white wig stands, holding the long dark curly wig beside his face; his clothes stay exactly as in the first frame (short curled brown wig, gold embroidered silk robe, white lace shirt). "
          "He gently strokes the dark wig, closes his eyes for a moment with a contented sigh, then opens them, lifts his chin and gives the lens a calm, haughty, self-satisfied half-smile, without laughing, and says calmly, lips clearly moving with every word: "
          "\"It makes me look taller, they say. I wouldn't know. I never look down.\" "
          "Then he keeps the proud look in silence. Same face as the first frame. Natural blinking, real skin texture, photorealistic. No music.")
body = {"model": "seedance-2.5-i2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C05_first.jpg", "image/jpeg")],
        "duration": 8, "resolution": "1080p", "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25_c05_1080"
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
