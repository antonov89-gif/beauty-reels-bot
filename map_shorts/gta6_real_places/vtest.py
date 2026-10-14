import apipod, json, sys, concurrent.futures as cf
U = json.load(open("kf/urls.json"))["G00"]
P = ("Cinematic open-world game footage: the purple sports car keeps drifting toward the camera with tyre smoke swirling, neon signs flicker and glow, palm trees sway, "
     "police lights flash in the distance, pedestrians run away at the sides, slow push-in camera. Smooth realistic motion, no cuts, no text, no logos.")
T = {
 "lite": {"model": "veo3-1-lite", "prompt": P, "image_urls": [U], "aspect_ratio": "9:16"},
 "grok": {"model": "grok-imagine-1.5-fast", "prompt": P, "image_urls": [U], "aspect_ratio": "9:16", "duration": 6},
}
def run(k):
    r = apipod.submit("videos", T[k])
    if "data" not in r: return k, "submit_err", r
    w = apipod.wait("videos", r["data"]["task_id"], timeout=900, every=10); d = w.get("data", {})
    if d.get("status") == "completed":
        apipod.download(d["result"][0], f"clips/test_{k}.mp4"); return k, d.get("usage"), d["result"][0]
    return k, "failed", d or w
with cf.ThreadPoolExecutor(2) as ex:
    for x in ex.map(run, sys.argv[1:] or list(T)): print(*x)
