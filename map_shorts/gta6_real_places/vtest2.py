import apipod, json, sys, concurrent.futures as cf
U = json.load(open("kf/urls.json"))
P = {
 "G03": "The airboat keeps skimming forward across the marsh with spray and a V-shaped wake behind it, its caged fan spinning, the alligator in the foreground water slowly glides and turns its head, "
        "grass and lily pads sway, mist drifts in golden light, gentle forward camera move. Smooth realistic motion, no cuts, no text, no logos.",
 "G02": "The red pickup truck drives away along the long bridge toward the horizon, the fishing boat rocks on the turquoise sea, clouds drift, sun flare shimmers on the water, "
        "slow forward camera glide over the bridge. Smooth realistic motion, no cuts, no text, no logos.",
}
def run(k):
    body = {"model": "grok-imagine-1.5-fast", "prompt": P[k], "image_urls": [U[k]], "aspect_ratio": "9:16", "duration": 6}
    r = apipod.submit("videos", body)
    if "data" not in r: return k, "submit_err", r
    w = apipod.wait("videos", r["data"]["task_id"], timeout=900, every=10); d = w.get("data", {})
    if d.get("status") == "completed":
        apipod.download(d["result"][0], f"clips/test_grok_{k}.mp4"); return k, d.get("usage"), d["result"][0]
    return k, "failed", d or w
with cf.ThreadPoolExecutor(2) as ex:
    for x in ex.map(run, sys.argv[1:] or list(P)): print(*x)
