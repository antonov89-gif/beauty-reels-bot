import apipod, json, sys, time, os, concurrent.futures as cf
STYLE = ("Semi-realistic high-end 3D nature-explainer render, NOT a photograph, NOT cartoon, NOT Pixar: detailed fur with soft shading, slightly stylised clean look, "
 "saturated natural colours, flat clear blue sky, simple readable environments, shallow depth of field, soft grounded shadows. "
 "No text, no letters, no numbers, no logos, no watermark. Vertical 9:16, free space above for captions. ")
K = {
"K1": "Two cliff edges with a deep blue sea channel between them, seen from a slight height. Left cliff: an adult male lion with a full mane and a zebra standing together on grey rock, savanna grass. Right cliff: a ring-tailed lemur and a fossa (slender reddish-brown cat-like animal with a long tail and small rounded ears) on mossy green rock with tropical leaves. Symmetric composition, the channel in the centre, open sky above.",
"K2": "Dark navy starfield with a soft glowing Earth horizon at the bottom. Two land masses in shaded relief: the east coast of Africa on the left and the island of Madagascar on the right, separated by a narrow ocean channel with a thin glowing line over it. Top-down map-style diagram view, thin glowing lines, no labels.",
"K3": "Madagascar rainforest and dry baobab alley: a green chameleon on a branch in the foreground, a sifaka lemur clinging to a tree trunk, a tenrec on the ground, baobab trees in the background, warm morning light.",
"K4": "A small raft made of tree branches and leaves floating on a calm turquoise ocean at sunrise, a ring-tailed lemur sitting on it holding on, the green coast of Africa far behind, golden light.",
"K5": "Close-up of a fossa (slender reddish-brown cat-like animal with a long tail and small rounded ears) walking along a thick tree branch toward the camera, green jungle blurred behind, a few lemurs tiny in the far background.",
"K6": "A ring-tailed lemur wearing small sunglasses sitting on a raft shaped like a deck chair, floating on the sea at sunset; on the far shore a big male lion waves a paw sadly; warm pink sky.",
}
U = json.load(open("kf/urls.json")) if os.path.exists("kf/urls.json") else {}
def run(k):
    body = {"model": "nano-banana-2.1", "prompt": STYLE + K[k], "aspect_ratio": "9:16", "quality": "2K"}
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
