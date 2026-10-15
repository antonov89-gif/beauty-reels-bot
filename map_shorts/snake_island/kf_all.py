import apipod, json, sys, time, os, concurrent.futures as cf
STYLE = ("Semi-realistic high-end 3D nature-explainer render, NOT a photograph, NOT cartoon, NOT Pixar: detailed scales and foliage with soft shading, slightly stylised clean look, saturated natural colours, clear blue sky, simple readable environments, shallow depth of field, soft shadows; "
 "any humans in the low-budget Daz/game-cutscene look with smooth slightly plastic skin and simple matte clothing. No text, no letters, no numbers, no logos, no flags, no readable signs. Vertical 9:16, free space above for captions. ")
K = {
"K1": "Aerial view of a small steep green tropical island with dense rainforest and rocky coast in a deep blue sea, a white lighthouse on the top, a grey patrol boat circling near the shore, bright sun.",
"K2": "Stylised shaded-relief map seen from above: the green coast of Brazil on the left, blue ocean, a small island marked by a soft glow offshore, a thin dotted line between the coast and the island, no labels.",
"K3": "A rocky forest floor completely covered by a carpet of thousands of golden-yellow snakes, exaggerated and dramatic, seen from a low angle, green leaves around.",
"K4": "A few golden-yellow snakes with brown markings resting on leaf litter in a rainforest, in the background a scientist in a khaki shirt and white helmet holding a clipboard, standing at a safe distance, calm mood.",
"K5": "A tropical coastline in bright light: a green land strip connecting the mainland on the left to a small forested island on the right, the sea level slightly below the strip, wide aerial view, calm.",
"K6": "A golden-yellow snake with brown markings resting on a thick branch in a rainforest, looking at a small brown-and-white bird sitting on a branch close by, shallow depth of field, calm mood.",
"K7": "An old white lighthouse on a green rocky island at dusk with a small abandoned keeper's house beside it, dark windows, pink and orange sky, calm sea.",
"K8": "A grey navy boat at a rocky landing on a tropical island, two researchers in white helmets and long boots holding snake hooks stepping onto the rocks, dense green forest behind, sunny.",
"K9": "A dim room with a wooden table: a man in a dark jacket and cap sitting with a stack of cash on the table next to an empty glass terrarium, he looks at the viewer with a sly smile, warm lamp light, generic character.",
"K10": "Macro close-up of the head of a golden-yellow snake with amber eyes on a green leaf, soft focus rainforest background, calm.",
"K11": "A small green tropical island with a lighthouse at golden hour, calm sea, soft pink and orange sky, tiny golden snakes on the rocks of the shore, aerial view.",
"K12": "A golden-yellow snake lounging on a wooden beach deck chair wearing small sunglasses, palm trees and a calm blue sea behind, warm sunlight, comic mood.",
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
