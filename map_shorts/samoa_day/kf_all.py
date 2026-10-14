import apipod, json, sys, time, concurrent.futures as cf
exec(open("kf_test2.py").read().split("P = (")[0].replace("import apipod", ""))
SPACE = "Space/diagram shot in the same low-budget explainer 3D style: dark navy starfield background, simple stylised Earth globe with flat green-brown land, deep blue ocean and soft white clouds, clean simple shading. NO people. "
MIA = "Mia is the same woman as in reference image 1: Samoan woman about 30, long dark hair, red floral shirt, same Daz-style CG face. "
K = {
 "S5": ("Night bedroom in a simple tropical island house, palm leaves outside the open window, soft moonlight; Mia, a Samoan woman about 30 with long dark hair and a red floral shirt, lies in bed under a light sheet, smiling sleepily, reaching to switch off a bedside lamp; a phone on the nightstand.", None),
 "S1": ("Interior of an 1890s wooden trading post on a tropical island: a big paper wall calendar with completely blank pages (no text, no numbers) hangs on the wooden wall; a man's hand tears off the top page and an identical blank page is underneath; shelves with jars, sacks and a kerosene lamp; warm daylight from a window with palm trees.", None),
 "S2": ("1890s harbour on a tropical Pacific island: a two-masted wooden trading schooner moored at a wooden jetty, palm trees and green mountains; in the foreground a close medium shot of only hands, arms and torsos (faces out of frame): a trader in a white 1890s shirt and waistcoat hands a large brass mantel clock to the hands of a Samoan chief wearing a woven traditional fine mat over his shoulders.", None),
 "S3": (SPACE + "The globe is centred on the South Pacific: New Zealand and Australia at the lower left, the small Samoan islands in the middle; a thin glowing yellow line runs from north to south just to the east of Samoa; glowing dotted routes of a small cargo ship and a small plane go from New Zealand and Australia to Samoa.", None),
 "S4": ("NO people. Stylised top-down 3D map of the tropical Pacific Ocean with small green Samoan islands; a thin glowing yellow line bends around the islands; above the islands a giant blank paper calendar page (no text, no numbers) is being torn off and flies away in the wind over the ocean; flat saturated colours.", None),
 "S6": (MIA + "Bright tropical living room in the morning: Mia holds a birthday cake with lit candles and looks with a confused, disappointed face at a wall calendar where one square has been torn out, leaving an empty hole; her friend, a smiling Samoan man about 30 in a blue shirt, shrugs beside her; flat bright colours.", "S5"),
}
def run(k, ref=None):
    p, _ = K[k]
    body = {"model": "nano-banana-2.1", "prompt": STYLE + p, "aspect_ratio": "9:16", "quality": "2K"}
    if ref: body["image_urls"] = [ref]
    for a in range(20):
        r = apipod.submit("images", body)
        if "data" in r: break
        time.sleep(20)
    w = apipod.wait("images", r["data"]["task_id"]); d = w.get("data", {})
    if d.get("status") != "completed": return k, None, d
    apipod.download(d["result"][0], f"kf/{k}.jpg"); return k, d.get("usage"), d["result"][0]
res = {}
k, c, u = run("S5"); print(k, c, u); res["S5"] = u
with cf.ThreadPoolExecutor(4) as ex:
    futs = [ex.submit(run, kk, u if K[kk][1] == "S5" else None) for kk in ["S1", "S2", "S3", "S4", "S6"]]
    for f in futs:
        kk, c2, u2 = f.result(); print(kk, c2, u2); res[kk] = u2
json.dump(res, open("kf/urls.json", "w"), indent=1)
