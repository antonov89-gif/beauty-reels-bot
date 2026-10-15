import apipod, json, sys, time, concurrent.futures as cf
STYLE = ("Hyper-detailed screenshot from a modern next-gen open-world action video game set in the fictional sunny backcountry of Florida: "
 "in-engine real-time render, NOT a photograph, harsh bright sun, deep blue sky with towering clouds, saturated warm colours, glossy wet mud and chrome, "
 "very dense environmental detail (cypress and pine trees, palm trees, mud splashes, flags, banners without readable words, coolers, litter), "
 "cinematic depth of field, slight bloom and lens flare, characteristic 2025 AAA game lighting and skin shading, generic anonymous people only, faces small or turned away. "
 "Vertical 9:16 composition, strong foreground subject and leading lines. No logos, no readable text, no brand names, no HUD, no watermark. ")
K = {
"M1": "Hook frame: a giant lifted monster truck with oversized tyres launching through a huge muddy pit, brown mud spraying in a big wave toward the camera, a cheering crowd covered in mud behind a rope line, flags and a forest edge in the background, low angle.",
"M2": "A muddy off-road park: a quad ATV and a swamp buggy racing side by side through a wide brown mud pit, mud flying, riders in helmets and goggles, tall pines behind, bright midday sun.",
"M3": "A wild outdoor party: a crowd of anonymous young people covered head to toe in brown mud laughing and dancing beside lifted trucks, coolers, string lights and flags, a forest edge behind, golden afternoon light, handheld camera feel.",
"M4": "Aerial view of a huge sprawling muddy off-road park in flat green Florida countryside: many brown mud pits and winding dirt tracks, hundreds of parked trucks and tents and campers, a pine forest border, a small lake, bright sun.",
"M5": "A rusty lifted pickup truck sliding sideways through a deep mud bog at golden hour, a huge fan of mud spray lit by low sun, spectators on a dirt berm, cypress trees and Spanish moss, dramatic light rays.",
"M6": "Dusk at a muddy trail park: a line of lifted trucks with bright headlights parked in the mud, a big bonfire, people in muddy clothes sitting on tailgates, purple and orange sky, fireflies, string lights.",
"M7": "Ending frame: a lone muddy truck parked at the edge of a swamp road at sunset, an airboat fan silhouette and cypress trees in the distance, a hand-painted flag on a pole, pink and orange sky, calm mood.",
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
if __name__ == "__main__":
    res = {}
    try: res = json.load(open("kf/urls.json"))
    except Exception: pass
    with cf.ThreadPoolExecutor(4) as ex:
        for k, c, u in ex.map(run, sys.argv[1:] or list(K)): print(k, c, u); res[k] = u
    json.dump(res, open("kf/urls.json", "w"), indent=1)
