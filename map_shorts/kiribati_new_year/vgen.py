import apipod, json, sys, time, concurrent.futures as cf
U = json.load(open("kf/urls.json"))
TAIL = " Keep the same low-budget Daz/Blender explainer 3D look, smooth steady camera, no cuts, no text, no letters, no numbers, no extra people."
P = {
 "K1": "The oversized clock hand ticks to twelve, the family starts to cheer and raise their arms, then a big blank white calendar page drops from above and covers the scene; smooth camera.",
 "K2": "Slow orbit around the island chain, the glowing yellow line pulses softly, the islands on one side stay brighter than the other.",
 "K3": "The left official says hello into the phone and waves, the right official shakes his head and checks his calendar, both look at their calendars; the glowing line pulses.",
 "K4": "The glowing yellow line slowly bends eastward around all the islands, the blank white calendar page flutters and tears away to the right.",
 "K5": "Slow push-in, the sun rises slightly, the crowd cheers and raises their hands, a small firework bursts over the sea.",
 "K6": "Slow push-in, the girl's smile falls into a pout, the candle flames flicker, the man shrugs with raised palms.",
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
