import apipod, json, sys, time, concurrent.futures as cf
U = json.load(open("kf/urls.json"))
TAIL = " Keep the same semi-realistic 3D nature-explainer look, smooth steady camera, no cuts, no text, no letters, no numbers, no logos, no extra people."
P = {
 "K1": "Slow aerial orbit around the island, the patrol boat circles slowly, waves, birds fly by.",
 "K2": "Slow push toward the glowing island, the dotted line pulses, soft waves on the coast.",
 "K3": "Slow glide over the carpet of snakes, they shift and sway gently.",
 "K4": "The camera slowly pulls back to reveal the scientist writing on his clipboard, a snake lifts its head calmly.",
 "K5": "The sea level slowly rises and covers the green land strip, waves, the island becomes separated.",
 "K6": "The bird hops along the branch then flies away, the snake slowly raises its head and watches.",
 "K7": "Slow push-in, birds fly past the lighthouse, the sky darkens slightly, a light blinks on.",
 "K8": "The boat rocks gently, the two researchers step onto the rocks with their snake hooks.",
 "K9": "Slow push-in, the man taps the cash with his finger and smiles slyly.",
 "K10": "Slow push-in, the snake flicks its tongue and blinks slowly.",
 "K11": "Slow aerial pull-back, the lighthouse light turns on, waves roll in.",
 "K12": "The snake lifts its head, the sunglasses slip down its nose, a palm leaf sways.",
}
def dl(url, path):
    for a in range(5):
        try: apipod.download(url, path); return True
        except Exception as e: time.sleep(3)
    return False
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
        url = d["result"][0]; ok = dl(url, f"clips/{k}.mp4"); open(f"clips/{k}.url", "w").write(url)
        return k, d.get("usage"), url, "downloaded" if ok else "DOWNLOAD FAILED (url saved)"
    return k, "failed", str(d or w)[:300]
ks = sys.argv[1:] or list(P)
with cf.ThreadPoolExecutor(4) as ex:
    for x in ex.map(run, ks): print(*x, flush=True)
