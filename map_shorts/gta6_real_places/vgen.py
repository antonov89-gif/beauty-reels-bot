import apipod, json, sys, concurrent.futures as cf
U = json.load(open("kf/urls.json"))
TAIL = " Smooth realistic motion, no cuts, no text, no logos."
P = {
 "G01": "The pink convertible stays parked while pedestrians in swimwear walk past, neon tubes glow and flicker, palm trees sway in the breeze, the police helicopter slowly crosses the sky, waves roll on the beach, slow forward camera push down the avenue.",
 "G04": "The hero in the foreground slowly turns his head to look at the run-down motel, a gust of wind lifts dust and sand across the cracked lot, palm trees sway, sunlight flickers, the sea shimmers in the background, slow forward camera glide.",
 "G05": "The loaded sugarcane truck drives toward the camera on the dusty road leaving a dust cloud, thick white steam keeps pouring from the refinery smokestacks, distant field smoke drifts, the man in the foreground walks forward, slow camera push in.",
 "G06": "Sun rays flicker through the pine trees, mist drifts over the river valley, leaves and ferns sway, the muddy pickup rolls slowly forward along the trail, the people by the cabin move, slow forward camera glide down the muddy road.",
 "G07": "The man on the rooftop looks toward the glowing skyline, helicopters cross the pink sunset sky, city lights flicker on, palm leaves sway, ocean glitters, slow camera push forward past the motorbike.",
}
def run(k):
    body = {"model": "grok-imagine-1.5-fast", "prompt": P[k] + TAIL, "image_urls": [U[k]], "aspect_ratio": "9:16", "duration": 6}
    r = apipod.submit("videos", body)
    if "data" not in r: return k, "submit_err", r
    w = apipod.wait("videos", r["data"]["task_id"], timeout=900, every=10); d = w.get("data", {})
    if d.get("status") == "completed":
        apipod.download(d["result"][0], f"clips/{k}.mp4"); return k, d.get("usage"), d["result"][0]
    return k, "failed", d or w
with cf.ThreadPoolExecutor(4) as ex:
    for x in ex.map(run, sys.argv[1:] or list(P)): print(*x)
