import apipod, json, sys, time, concurrent.futures as cf
exec(open("kf_test.py").read().split("P = (")[0].replace("import apipod",""))
import sys as _s
if "G06" in _s.argv: STYLE = STYLE.replace("set in a fictional sunny version of Miami, Florida", "set in the wild backcountry of a fictional US southern state").replace("palm trees, neon signs without readable words, parked classic and modern cars, litter, graffiti, flags", "trees, rocks, ferns, fallen logs, a muddy trail")
K = {
"G00": "Hook frame: low angle from the asphalt of a neon-lit Vice City style boulevard at dusk, a shiny purple sports car drifting toward the camera with smoke from its tyres, palm trees and art deco hotels glowing pink and cyan behind, police lights flashing in the distance.",
"G02": "Leonida Keys style: a long low concrete bridge running straight over open turquoise sea to the horizon, a lone red pickup truck driving on it, a small fishing boat below, tiny mangrove islands, white clouds, intense midday sun.",
"G03": "Grassrivers style swamp: an airboat with a big caged fan skimming across sawgrass marsh and lily pads, spray behind it, an alligator in the foreground water with its eyes just above the surface, cypress trees and humid haze, golden late-afternoon light.",
"G04": "Port Gellhorn style faded Gulf Coast beach town: a run-down motel with an empty pool, cracked parking lot, rusty pickup trucks, a giant fibreglass shark statue at a closed souvenir shop, white sand beach and calm emerald sea behind, overcast warm light.",
"G05": "Ambrosia style sugar country: a huge old sugar refinery with tall smokestacks pouring white steam, trucks loaded with sugarcane on a dusty road, endless flat green cane fields to the horizon, burning field smoke in the distance, hazy golden sun.",
"G06": "NOT a city, NOT a street, no palm trees, no buildings except one cabin. Wilderness scene in a fictional national park: Mount Kalaga style: a forested mountain ridge with granite outcrops above a misty river valley, a winding dirt road with a muddy off-road truck, pine and oak forest, dramatic morning light rays, a hunting cabin in the foreground.",
"G07": "Ending frame: rooftop of an art deco hotel at sunset overlooking a Miami-like skyline and the ocean, a parked motorbike in the foreground, palm trees, pink and orange sky, helicopters, city lights turning on.",
}
def run(k):
    body = {"model": "nano-banana-2.1", "prompt": STYLE + K[k], "aspect_ratio": "9:16", "quality": "2K"}
    for a in range(20):
        r = apipod.submit("images", body)
        if "data" in r: break
        time.sleep(20)
    w = apipod.wait("images", r["data"]["task_id"]); d = w.get("data", {})
    if d.get("status") != "completed": return k, None, d
    apipod.download(d["result"][0], f"kf/{k}.jpg"); return k, d.get("usage"), d["result"][0]
res = {}
with cf.ThreadPoolExecutor(4) as ex:
    for k, c, u in ex.map(run, sys.argv[1:] or list(K)): print(k, c, u); res[k] = u
json.dump(res, open("kf/urls.json", "w"), indent=1)
