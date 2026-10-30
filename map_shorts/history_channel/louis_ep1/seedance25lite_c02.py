"""C02 remake on Seedance 2.5 LITE i2v (720p, 9 s, $0.15/s = $1.35 by the APIpod pricing page; usage.cost is checked after). First frame = C02_first.jpg = the last frame of C01, so the join C01 -> C02 must stay invisible: Lite keeps the first frame only approximately (diff 5.8-7.2 in the C04/C05 pilots), the join is checked on frames before it is used; if it jumps, C02 goes to the draft route (about $5.8). Short line: "A hundred people watch me wake up. [pause] I call it... opening night." Usage: python3 seedance25lite_c02.py show | go"""
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


prompt = ("Continue this exact shot without any cut: a vertical hand-held phone selfie video, front camera of a smartphone, the same vain French king in the same short curled brown night wig and gold embroidered silk dressing gown, reclining on the pillows of his canopied state bed, holding the phone himself at arm's length; courtiers move quietly in the background. "
          "The phone is hand-held and clumsy: constant natural sway, small roll, the framing drifts and he re-centres it with small jerks; never a smooth move, never a zoom. "
          "With his free ringed hand he touches and adjusts one curl of his wig, then leans a little toward the lens as if sharing a secret, eyes sparkling, and says, unhurried, lips clearly moving with every word, proud and conspiratorial: \"A hundred people watch me wake up.\" "
          "Then a real pause of about one second: he looks at the lens, savouring it, silent. Then, with a tiny head tilt and a soft laugh: \"I call it... opening night.\" Then a silent pleased smile at the lens. "
          "Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. "
          "Sound: recorded by the phone's own microphone: his voice close, a soft rustle of silk and lace, faint murmur of courtiers far behind, a quiet palace room. No music.")
body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C02_first.jpg", "image/jpeg")],
        "duration": 9, "resolution": "720p", "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25lite_c02"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
