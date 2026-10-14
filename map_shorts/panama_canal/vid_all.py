import apipod, json, glob, sys, time, os, concurrent.futures as cf
U = {"A01": "https://s.apipod.ai/images/2026/10/14/b7543b2b-3587-4db4-9544-daf2f635fa2f.jpg"}
for f in sorted(glob.glob("keyframes/urls_*.json"), key=os.path.getmtime):
    U.update({k: v for k, v in json.load(open(f)).items() if v})
TAIL = " Realistic physics, real-world scale, smooth steady cinematic camera, no cuts, no text, no letters, no logos, no people talking. Ambient natural sound only, no music, no voice."
ARCH = " Keep it a sepia archival early-20th-century film look with flicker and grain; subtle period-film motion."
M = {
"A01": "Slow aerial drone push-in toward the giant container ship in the foreground; the line of waiting ships stays at anchor; sunrise light glitters on gently moving water, haze drifts.",
"A02": "Low tracking shot moving alongside the bow as the container ship cuts forward through the sea, white spray and foam curling off the bow, water rushing past the camera.",
"A03": "The enormous steel rolling gate slowly slides sideways across the lock chamber, closing behind the container ship; water churns at its base; camera slowly tilts up along the gate.",
"A04": "Slow orbit around the cutaway lock; water surges in through the floor culverts and the chamber fills, lifting the container ship steadily upward.",
"A05": "Very slow wide push-in toward the upright concrete lock chamber standing beside the Eiffel Tower; clouds drift slowly; tiny people walk at the base.",
"A06": "Close low angle: water boils up violently from the chamber floor openings, white turbulence spreading, the dark blue hull rises slowly beside the wet concrete wall.",
"A07": "Slow pan across the excavation site; workers dig and swing shovels, steam excavators puff black smoke." + ARCH,
"A08": "Slow pan following the railway wagons of earth being pushed along the track; workers shovel mud." + ARCH,
"A09": "Steam shovels swing and dump rock into the railway dump cars; a train slowly moves; smoke rises; slow pan." + ARCH,
"A10": "Mud and rocks keep sliding down the slope in a slow landslide around the overturned steam shovel, workers on the terrace step back." + ARCH,
"A11": "The steamship glides slowly forward through the lock, flags flutter, the crowd on the wall waves hats; slow pan following the ship." + ARCH,
"A12": "Tracking shot: the orange pilot boat runs alongside the huge moving hull; the pilot climbs steadily up the rope ladder; spray from the boat's bow.",
"A13": "Slow aerial descent as two tugboats push at the stern, churning white water, while the container ship moves slowly into the lock.",
"A14": "Side tracking shot: the silver towing locomotives roll slowly along their rails on the lock wall, steel cables taut, the ship hull gliding forward beside them.",
"A15": "Slow push-in; bundles of dollar banknotes keep stacking higher one by one beside the model container ship; warm light flickers on the paper.",
"A16": "The hand lifts the wooden gavel and strikes the sound block once firmly; papers jump slightly; the ship stays blurred in the window behind.",
"A17": "The lone swimmer swims steadily across the lock water, the small rowing boat follows, spectators lean and watch; slow pan." + ARCH,
"A18": "Slow high drone glide over the locks and the water-saving basins; a ship sits in a chamber; the water shimmers; clouds' shadows move over the rainforest.",
"A19": "Slow aerial follow shot as the container ship glides forward between the green islands, its wake spreading on the calm lake, mist drifts.",
"A20": "Heavy rain pours down; countless drops splash on the lake surface; leaves shake under the rain; slow push-in toward the water.",
"A21": "Slow drone glide following the container ship as it moves forward through the narrow cut between the terraced cliffs, a tug escorting it.",
"A22": "Slow pull-back revealing more of the cracked dry lake bed and the stumps; dust drifts in the hot wind; ships far away on the low water.",
"A23": "Slow aerial pull-back and rise revealing even more ships waiting at anchor to the hazy horizon; water glitters.",
"A24": "Slow aerial rise above the lock as the water level visibly drops and the container ship lowers inside the chamber, wet walls being exposed.",
"A25": "Tracking shot alongside as the container ship sails forward and passes under the green steel arch bridge, city skyline in the distance, sunset glow.",
"A26": "The pilot climbs down the last rungs of the rope ladder and steps onto the orange pilot boat, which then peels away from the moving hull.",
"A27": "Slow push-out as the container ship sails away into the golden sunset, its wake trailing, water shimmering.",
}
def run(k):
    if os.path.exists(f"clips/{k}.mp4"): return k, "exists", None
    body = {"model": "veo3-1-fast", "prompt": M[k] + TAIL, "image_urls": [U[k]], "aspect_ratio": "16:9"}
    for a in range(30):
        r = apipod.submit("videos", body)
        if "data" in r: break
        if r.get("http_error") == 429: time.sleep(30); continue
        return k, "submit_err", r
    else: return k, "gave_up", None
    w = apipod.wait("videos", r["data"]["task_id"], timeout=1500, every=15)
    d = w.get("data", {})
    if d.get("status") == "completed":
        apipod.download(d["result"][0], f"clips/{k}.mp4"); return k, d.get("usage", {}).get("cost"), d["result"][0]
    return k, "failed", d or w
ks = sys.argv[1:] or list(M)
with cf.ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, ks): print(*res); sys.stdout.flush()
