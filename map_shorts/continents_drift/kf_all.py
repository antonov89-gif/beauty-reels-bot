import apipod, json, sys, time, concurrent.futures as cf
exec(open("kf_test2.py").read().split("P = (")[0].replace("import apipod", ""))
MAX = "https://s.apipod.ai/images/2026/10/14/1bbbce94-59e7-44d0-9d34-0e56fb8dd05b.jpg"
CHAR = "Max is the same man as in reference image 1: same face, short brown hair, light stubble, red hoodie, blue jeans, brown hiking boots, same Daz-style CG look. "
SPACE = "Space/diagram shot in the same low-budget explainer 3D style: dark navy starfield background, simple stylised Earth globe with flat green-brown continents, deep blue ocean and soft white clouds, clean simple shading. "
K = {
 "S1": (SPACE + "The globe is seen from orbit centred on the Atlantic Ocean, the Americas on the left, Europe and Africa on the right, a thin glowing orange line runs down the middle of the Atlantic from north to south.", False),
 "S2a": ("Clean 3D cutaway cross-section of the deep ocean floor: blue water above, two big grey rock slabs in the middle slightly separated, glowing orange magma rising in the gap and cooling into dark new rock at the top, simple layered rock below, plain dark blue background, simulation feel.", False),
 "S2b": (CHAR + "Close-up of Max's hand resting flat on a light wooden table next to a plain yellow ruler with black tick marks and no numbers; beside the hand a small grey stone block with a thin crack in it; flat light-blue background.", True),
 "S3a": ("A small 15th-century wooden caravel with white sails crosses a calm stylised blue ocean; a giant yellow measuring tape lies flat on the water surface and stretches to the horizon; flat saturated blue sky; simple low-budget 3D look.", False),
 "S3b": (CHAR + "A giant yellow measuring tape lies extended along a flat grey road; a modern plain white-and-blue city bus with no writing is parked right beside it, the bus slightly shorter than the extended tape; Max stands small at the end of the tape pointing at it; flat ground, flat blue sky.", True),
 "S4a": (SPACE + "The globe shows the single supercontinent Pangaea: one big green-brown landmass surrounded by one ocean, a glowing orange crack zigzags through the middle of the landmass.", False),
 "S4b": (SPACE + "The globe shows today's continents spread apart with a wide blue Atlantic Ocean in the middle, a thin glowing orange line along the middle of the Atlantic.", False),
 "S6": (CHAR + "Medium close-up of Max with a smug proud face, holding up one hand next to a plain yellow ruler with no numbers; one of his fingernails is comically long; behind him the same Icelandic rift fissure with dark basalt walls and clear blue water; flat blue sky.", True),
}
def run(k):
    p, ref = K[k]
    body = {"model": "nano-banana-2.1", "prompt": STYLE + p, "aspect_ratio": "9:16", "quality": "2K"}
    if ref: body["image_urls"] = [MAX]
    for a in range(20):
        r = apipod.submit("images", body)
        if "data" in r: break
        time.sleep(20)
    w = apipod.wait("images", r["data"]["task_id"]); d = w.get("data", {})
    if d.get("status") != "completed": return k, None, d
    apipod.download(d["result"][0], f"kf/{k}.jpg"); return k, d.get("usage"), d["result"][0]
res = {"S5": MAX}
with cf.ThreadPoolExecutor(4) as ex:
    for k, c, u in ex.map(run, sys.argv[1:] or list(K)): print(k, c, u); res[k] = u
json.dump(res, open("kf/urls.json", "w"), indent=1)
