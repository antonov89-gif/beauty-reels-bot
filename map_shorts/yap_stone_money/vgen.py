import apipod, json, sys, time, base64, io, concurrent.futures as cf
from PIL import Image
U = json.load(open("kf/urls.json"))
def src(k):
    if k in U: return U[k]
    im = Image.open(f"kf/{k}.jpg").convert("RGB").resize((768, 1376)); b = io.BytesIO(); im.save(b, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
TAIL = " Keep the same low-budget Daz/Blender explainer 3D look, smooth steady camera, no cuts, no text, no letters, no numbers, no extra people."
P = {
 "K1": "The three sailors lean in and push hard; the heavy stone disk slowly rolls up onto the bamboo raft, the raft dips and splashes in the turquoise water, the canoe sail flutters in the wind; one man wipes his forehead; slow push-in.",
 "K2": "The man keeps pointing out of the open door towards the sea and nods proudly; the cashier slowly turns her head to look at the sea, then back at him, raises one eyebrow and slowly nods with a serious face; palm trees sway outside; gentle push-in.",
}
def run(k):
    body = {"model": "grok-imagine-1.5-fast", "prompt": P[k] + TAIL, "image_urls": [src(k)], "aspect_ratio": "9:16", "duration": 6}
    for a in range(30):
        r = apipod.submit("videos", body)
        if "data" in r: break
        if r.get("http_error") == 429: time.sleep(30); continue
        return k, "submit_err", str(r)[:300]
    w = apipod.wait("videos", r["data"]["task_id"], timeout=900, every=10); d = w.get("data", {})
    if d.get("status") == "completed":
        apipod.download(d["result"][0], f"clips/{k}.mp4"); return k, d.get("usage"), d["result"][0]
    return k, "failed", str(d or w)[:300]
ks = sys.argv[1:] or list(P)
with cf.ThreadPoolExecutor(4) as ex:
    for x in ex.map(run, ks): print(*x, flush=True)
