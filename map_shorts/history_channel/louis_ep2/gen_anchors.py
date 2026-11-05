"""Ep.2 anchors (owner 04.11 "1, делай якоря"): each emotion tile EDITED into the dinner hall. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, only image_urls = the tile. 6 calls x about $0.12 = $0.72, no retries (a failed one needs a new yes)."""
import json, re, sys, threading
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
NAMES = {"E1": "haughty", "E2": "smug", "E3": "laugh", "E6": "annoyed", "E7": "blissful", "E8": "startled"}
def prompt(n):
    return ("Edit the photo: keep the man, his face, his exact expression, his head angle, his tall white-grey wig, his scarlet velvet coat with gold suns, lace cravat and cuffs EXACTLY as they are (do not redraw or change his face, age, skin, eyes or moustache; do not change the expression). "
            "Change only the setting and the framing: show him from the chest up as a hand-held phone selfie at arm's length, sitting at the head of a very long dining table with a white cloth, gold plates and candelabra with lit candles in a gilded antechamber of Versailles at night, warm candlelight only; behind him a standing crowd of courtiers in plain simple wigs and dark period clothes, in the front row four or five ladies seated on folding stools. Fine film grain, real skin texture. "
            "No text, no logos, no modern objects, no extra fingers, no blond or cream wig, no clown makeup.")
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
def run(n):
    body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt(n), "aspect_ratio": "9:16", "resolution": "4K", "quality": "high", "image_urls": [RAW + f"K_{n}_up.jpg"]}
    r = apipod.submit("images", body)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: print(n, "NOT SUBMITTED", json.dumps(r)[:300]); return
    out = H0 + f"pilot_frames/anchors/ANCHOR_{n}_{NAMES[n]}_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; u = find(d)
    if u: apipod.download(u, out)
    print(n, NAMES[n], d.get("status"), "cost", (d.get("usage") or {}).get("cost"), "saved" if u else "NO URL")
import sys as _s
ONLY = _s.argv[1:] or list(NAMES)
ts = [threading.Thread(target=run, args=(n,)) for n in ONLY]
[t.start() for t in ts]; [t.join() for t in ts]
