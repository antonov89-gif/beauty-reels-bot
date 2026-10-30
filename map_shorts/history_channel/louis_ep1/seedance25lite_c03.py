"""C03 remake on Seedance 2.5 LITE i2v (owner "да делай" 30.10: 720p, 8 s, $0.15/s = $1.20 by the APIpod pricing page). First frame = the LAST frame of the new Lite C02 (frames/C03_first_lite.jpg), so the join C02 -> C03 stays continuous. Short line: "The doctor. The surgeon. Nobody came to see them. [pause] Everyone came for me. Naturally." Usage: python3 seedance25lite_c03.py show | go"""
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


prompt = ("Continue this exact shot without any cut: a vertical hand-held phone selfie video, front camera of a smartphone, the same vain French king in the same short curled brown night wig and gold embroidered silk dressing gown, reclining on the pillows of his canopied state bed, holding the phone himself at arm's length, his face first very close to the lens and then easing back to a medium selfie. "
          "The phone is hand-held and clumsy: constant natural sway, small roll, the framing drifts and he re-centres it with small jerks; never a smooth move, never a zoom. Far behind him in the room stand two men who have come in: a royal doctor in a long black robe and a small red cap, and a surgeon in a plain dark coat with a leather case; they wait politely and stay in the background. "
          "He glances at them over his shoulder with heavy bored eyelids, looks away, then turns his eyes back to the lens, dry and bored, and says, unhurried, lips clearly moving with every word: \"The doctor.\" (short pause) \"The surgeon.\" (short pause) \"Nobody came to see them.\" "
          "Then a real pause of about one second: he smiles to himself, silent, savouring it. Then, smug and pleased with a small nod: \"Everyone came for me.\" Then, soft and satisfied, slowly: \"Naturally.\" Then a silent pleased smile at the lens. "
          "Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. "
          "Sound: recorded by the phone's own microphone: his voice close, a soft rustle of silk and lace, a faint creak of the parquet and quiet footsteps far behind, a quiet palace room. No music.")
body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C03_first_lite.jpg", "image/jpeg")],
        "duration": 8, "resolution": "720p", "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25lite_c03"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
