import apipod, json, sys, time, concurrent.futures as cf
U = json.load(open("kf/urls.json"))
TAIL = " Keep the same low-budget Daz/Blender explainer 3D look, smooth steady camera, no cuts, no text, no letters, no numbers, no extra people."
P = {
 "S1": "Slow push-in from orbit toward the Atlantic Ocean on the globe; the glowing orange seam pulses; the Americas and Europe-Africa slowly slide a little further apart; clouds drift; stars twinkle.",
 "S2a": "The two rock slabs slowly move apart, glowing magma rises into the widening gap and cools into dark new rock at the top, small bubbles rise through the water; camera slowly dollies sideways along the seam.",
 "S2b": "Macro shot: the man's fingernail visibly grows a little longer next to the yellow ruler while the thin crack in the stone block opens only a tiny bit; gentle slow push-in.",
 "S3a": "The caravel sails forward along the giant yellow measuring tape, waves splash at its bow, the sails flutter, the tape stretches to the horizon; camera tracks alongside the ship.",
 "S3b": "The giant measuring tape slides out a few more meters along the road while the man walks beside it pointing; the city bus rolls in slowly and stops next to the tape; camera slowly pulls back to show both.",
 "S4a": "The glowing crack spreads and zigzags further through the supercontinent, steam rises along it, the landmass starts to split into pieces; the globe rotates very slowly.",
 "S4b": "The continents drift slowly apart toward their modern positions while the blue Atlantic Ocean widens between them along the glowing seam; continuous slow pull-back from the globe.",
 "S5": "The fissure between the rock walls slowly widens, the man's legs spread further apart, he wobbles and waves his arms for balance with a surprised face; camera slowly cranes up revealing the long rift valley.",
 "S6": "The man grins at the camera, his index fingernail along the ruler grows comically longer past the end of the ruler, he gives a proud thumbs-up and raises his eyebrows; slow push-in to his smug face.",
}
def run(k):
    body = {"model": "grok-imagine-1.5-fast", "prompt": P[k] + TAIL, "image_urls": [U[k]], "aspect_ratio": "9:16", "duration": 6}
    for a in range(30):
        r = apipod.submit("videos", body)
        if "data" in r: break
        if r.get("http_error") == 429: time.sleep(30); continue
        return k, "submit_err", r
    w = apipod.wait("videos", r["data"]["task_id"], timeout=900, every=10); d = w.get("data", {})
    if d.get("status") == "completed":
        apipod.download(d["result"][0], f"clips/{k}.mp4"); return k, d.get("usage"), d["result"][0]
    return k, "failed", d or w
with cf.ThreadPoolExecutor(4) as ex:
    for x in ex.map(run, sys.argv[1:] or list(P)): print(*x)
