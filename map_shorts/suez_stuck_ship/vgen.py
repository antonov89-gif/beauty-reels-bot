import apipod, json, sys, time, concurrent.futures as cf
U = json.load(open("kf/urls.json"))
TAIL = " Keep the same semi-realistic 3D explainer look, smooth steady camera, no cuts, no text, no letters, no numbers, no logos, no extra people."
P = {
 "K1": "Slow drone push-in toward the stuck ship, dust blows across the canal, the tiny excavator moves slightly, haze drifts.",
 "K2": "The tugboats strain on their ropes, water churns, the excavator digs and the sand pipe pumps, workers wave; the huge ship does not move.",
 "K3": "Slow camera tilt up from the engineer to the glowing moon, the water in the canal rises slowly and quietly, the engineer lifts a hand.",
 "K4": "The tugboats push and pull together, the bow slowly swings loose from the bank, spray and foam, smooth camera.",
 "K5": "Smooth slow aerial flight along the queue of ships, the first ship begins to move forward, small waves.",
 "K6": "The man bows deeper, the official takes the toy tugboat with both hands and smiles slightly, a light breeze moves the flags.",
}
def run(k):
    body = {"model": "grok-imagine-1.5-fast", "prompt": P[k] + TAIL, "image_urls": [U[k]], "aspect_ratio": "9:16", "duration": 6}
    r = {}
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
