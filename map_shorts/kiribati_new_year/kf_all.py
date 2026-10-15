import apipod, json, sys, time, os, concurrent.futures as cf
STYLE = ("Clearly a 3D render in the look of a low-budget educational explainer animation made in Daz Studio / Blender with game-engine assets, NOT a photograph, NOT Pixar, NOT cartoon, NOT hyper-realistic: "
 "characters have realistic human proportions and a realistic head size, normal-sized eyes, smooth airbrushed plastic-looking skin with soft shading, simple solid-clump hair mesh, slightly uncanny early-2010s game cutscene look, expressive facial animation; "
 "simple matte clothing textures; simplified environment with flat saturated blue sky or dusk and simple even lighting with soft shadows. No text, no letters, no numbers, no logos. Vertical 9:16, free space above for captions. ")
K = {
"K1": "A beach party at dusk in the tropics: a long table with food and drinks, balloons and party hats, an oversized clock with no numbers showing almost twelve o'clock on a wooden post, a Pacific islander family of five in red and yellow party hats about to cheer, palm trees, string lights, calm sea behind. Table-level camera.",
"K2": "Navy starfield with a soft glowing Earth horizon at the bottom: a top-down map-style view of the central Pacific with small green island groups scattered in a long chain; a thin glowing yellow line cuts vertically through the middle of the chain; the islands to the left of the line are bright, the islands to the right are dim. Thin glowing lines, no labels.",
"K3": "Split composition by a vertical glowing yellow line in the centre: on the left a Pacific islander official in a short-sleeve shirt in a sunlit office holding a phone with a paper desk calendar; on the right an identical office in softer evening light with another official holding a phone and a paper desk calendar showing a different page; both look puzzled. No readable text.",
"K4": "Navy starfield diagram of the central Pacific island chain with a thin glowing yellow line bending eastward around all the islands, a big blank white calendar page fluttering and tearing away above the eastern islands. Thin glowing lines, no labels.",
"K5": "Sunrise over a calm Pacific beach: a cheering crowd of islanders and tourists in sunglasses and party hats, a small firework bursting over the sea at dawn, a low coconut palm island on the horizon, warm orange and pink sky.",
"K6": "A beach party table with an untouched cake, a family of four in red and yellow party hats around it looking disappointed, on a wooden post behind them an empty hook with a torn calendar page, a man in a flowered shirt shrugging with raised palms, dusk light, string lights.",
}
U = json.load(open("kf/urls.json")) if os.path.exists("kf/urls.json") else {}
def run(k):
    body = {"model": "nano-banana-2.1", "prompt": STYLE + K[k], "aspect_ratio": "9:16", "quality": "1K"}
    r = {}
    for a in range(20):
        r = apipod.submit("images", body)
        if "data" in r: break
        time.sleep(20)
    w = apipod.wait("images", r["data"]["task_id"]); d = w.get("data", {})
    if d.get("status") != "completed": return k, None, d
    apipod.download(d["result"][0], f"kf/{k}.jpg"); U[k] = d["result"][0]; json.dump(U, open("kf/urls.json", "w"), indent=1)
    return k, d.get("usage"), d["result"][0]
todo = [k for k in (sys.argv[1:] or list(K)) if k not in U or not os.path.exists(f"kf/{k}.jpg")]
with cf.ThreadPoolExecutor(3) as ex:
    for r in ex.map(run, todo): print(r)
