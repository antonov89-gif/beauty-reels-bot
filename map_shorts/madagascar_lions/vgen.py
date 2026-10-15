import apipod, json, sys, time, concurrent.futures as cf
U = json.load(open("kf/urls.json"))
TAIL = " Keep the same semi-realistic 3D nature-explainer look, smooth steady camera, no cuts, no text, no letters, no numbers, no extra animals, gentle natural movement."
P = {
 "K1": "Slow push-in. The lion turns its head toward the lemur across the channel, the lemur blinks and tilts its head, grass moves in the wind, small waves in the channel below.",
 "K2": "The island slowly drifts away from the coast, the channel widens, the glowing line stretches and glows brighter. Camera static, smooth.",
 "K3": "Slow camera glide to the right. The chameleon rolls an eye, the sifaka lemur shifts on the trunk, leaves sway.",
 "K4": "The raft rocks gently on small waves, the lemur holds on and looks forward, the sun rises slightly, sparkles on the water.",
 "K5": "The fossa walks calmly along the branch toward the camera, its tail swishes, a small head turn, leaves move.",
 "K6": "The raft glides slowly away, the lemur raises one hand in a friendly wave, the lion on the shore lowers its paw and sighs, soft sunset light.",
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
