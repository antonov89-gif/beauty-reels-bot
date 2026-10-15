import apipod, json, sys, time, os, concurrent.futures as cf
STYLE = ("Semi-realistic high-end 3D explainer render, NOT a photograph, NOT cartoon, NOT Pixar: smooth clean materials, simple readable environments, soft grounded shadows, shallow depth of field. ")
TAIL = " Generic ship with no names, no logos, no readable letters. Vertical 9:16, free space above for captions."
K = {
"K1": "A gigantic dark-blue container ship stacked high with colourful containers, wedged diagonally across a narrow desert canal, the bow stuck in the sandy bank, the stern touching the opposite bank, sandstorm haze in a yellow sky, a tiny yellow excavator on the bank for scale. High aerial view.",
"K2": "Wide shot of four small orange tugboats pulling with taut ropes on the bow of a huge stuck container ship, a yellow excavator digging the sand bank at the bow, a dredger with a pipe pumping sand, workers in orange safety vests and white helmets on the bank, warm daylight.",
"K3": "Dusk at a desert canal: an enormous glowing supermoon low in the sky, a huge container ship in the dark water below, in the foreground an engineer in a white helmet and orange vest standing on the bank looking up at the moon, wet marks on the bank showing the water rising.",
"K4": "At high tide about fourteen small orange tugboats pushing and pulling a huge container ship from all sides, the bow swinging free of the sandy bank, white spray, golden evening light, high angle.",
"K5": "Aerial view along a straight desert canal: a very long queue of container ships and tankers on the water stretching to the horizon behind one freed ship, calm blue water, sand banks, clear sky.",
"K6": "A man in a dark suit bowing and offering a toy-sized orange tugboat on a small velvet cushion to a canal official in a white uniform with gold shoulder boards, the canal and a huge container ship behind them, friendly mood, sunny day.",
}
Q = os.environ.get("QUALITY", "1K")
U = json.load(open("kf/urls.json")) if os.path.exists("kf/urls.json") else {}
def run(k):
    body = {"model": "nano-banana-2.1", "prompt": STYLE + K[k] + TAIL, "aspect_ratio": "9:16", "quality": Q}
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
