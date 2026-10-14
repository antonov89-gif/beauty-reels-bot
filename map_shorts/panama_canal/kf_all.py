import apipod, json, sys, concurrent.futures as cf
REF = "https://s.apipod.ai/images/2026/10/14/b7543b2b-3587-4db4-9544-daf2f635fa2f.jpg"
BASE = ("Cinematic documentary realism, as if filmed for a premium travel and engineering documentary: real-world location in Panama, {light}, warm saturated colour grade, "
 "high contrast with deep slightly crushed blacks, glossy clean surfaces, gentle film grain, anamorphic-like wide framing, physically plausible water, ships with correct real-world scale and proportions, "
 "modern ships with plain hulls (no readable names, no logos), lush green rainforest. 16:9 horizontal, subject clearly separated from the background. No text, no letters, no logos. ")
ARCH = ("Authentic-looking archival photograph from the early 20th century, warm sepia monochrome, soft film grain, slight vignette, dust and scratches, period-correct clothing and machinery, "
 "documentary realism, 16:9 horizontal wide framing. No text, no letters, no captions. ")
HERO = ("The hero ship is the same giant container ship as in the reference image: dark blue hull, red bottom paint, white superstructure, mixed-colour containers, no name on the hull. ")
SUN, MID, SET = "golden-hour sunrise light", "bright tropical midday light with soft clouds", "golden sunset light with long warm shadows"
K = {
"A02": (SUN, 1, "Low tracking shot from the water alongside the bow of the hero container ship cutting through calm sea, white spray and wake at the bow, the hull towering above the camera, Caribbean coast behind."),
"A03": (SUN, 1, "Low angle inside a modern concrete lock chamber of the new Agua Clara locks: a massive steel rolling lock gate, taller than a ten-story building, closing behind the stern of the hero container ship, wet concrete walls."),
"A04": (MID, 1, "Clean 3D cutaway visualisation with photoreal materials: a modern canal lock chamber shown in cross-section, the hero container ship floating inside, water entering through large culverts and openings in the chamber floor, technical X-ray style see-through concrete walls, neutral dark background."),
"A05": (MID, 0, "Size comparison on a flat neutral grey plain: a long concrete canal lock chamber stood upright on its end like a tower beside the Eiffel Tower in Paris, the upright chamber clearly taller than the Eiffel Tower, tiny people at the base for scale, clear sky, wide static shot."),
"A06": (SUN, 1, "Close low angle inside a lock chamber: water surging up from openings in the chamber floor, foamy white turbulence, the dark blue hull of the hero container ship rising beside the wet concrete wall."),
"A07": (None, 0, "Panama, 1880s: French canal excavation in tropical jungle, steam excavators and hundreds of workers with shovels and wheelbarrows in a muddy trench, palm trees, smoke."),
"A08": (None, 0, "Panama, 1880s: workers in straw hats beside a narrow-gauge railway carrying wagons of earth out of a deep muddy cut, heavy tropical humidity, makeshift wooden huts."),
"A09": (None, 0, "Panama, around 1910: American excavation of the Culebra Cut, huge steam shovels loading rock into lines of railway dump cars on terraced cliff walls, hundreds of workers."),
"A10": (None, 0, "Panama, around 1912: a massive landslide of mud and rock collapsing into the excavated canal cut, buried railway tracks and an overturned steam shovel, workers looking on from the terrace above."),
"A11": (None, 0, "Panama, August 1914: an early 20th-century steamship with a tall funnel passing through a newly built concrete canal lock, flags and bunting, a crowd of people in hats standing on the lock wall."),
"A12": (SUN, 1, "Close tracking shot at sea: a small orange pilot boat running alongside the towering hull of the hero container ship, a canal pilot in a reflective vest climbing a rope ladder up the side of the hull."),
"A13": (SUN, 1, "Aerial view: two red tugboats pushing at the stern of the hero container ship as it enters a modern lock, white churned water, lock walls and rainforest around."),
"A14": (MID, 0, "Side view along an old concrete lock wall of the original Panama Canal locks: silver electric towing locomotives on rails pulling a container ship on taut steel cables, ship hull filling the right side of the frame."),
"A15": (None, 0, "Studio product shot on a dark wooden table with dramatic warm rim light: a tall neat stack of US dollar banknotes growing next to a detailed scale model of a dark blue container ship with mixed-colour containers, black background, shallow depth of field, cinematic realism. 16:9 horizontal. No text, no letters, no logos."),
"A16": (None, 0, "Close-up of a wooden auction gavel striking a sound block on a desk in a port office, through the big window behind it a giant container ship is blurred in warm afternoon light, shallow depth of field, cinematic realism. 16:9 horizontal. No text, no letters, no logos."),
"A17": (None, 0, "Panama, 1928: a lone swimmer crossing calm canal water inside a concrete lock chamber, small rowing boat following him, spectators in hats watching from the edge of the lock wall."),
"A18": (MID, 0, "High aerial drone view of the modern Panama Canal Agua Clara locks: three stepped lock chambers with large rectangular water-saving basins beside them, geometric pools of water, dense rainforest around, a container ship inside a chamber."),
"A19": (MID, 1, "Aerial follow shot: the hero container ship gliding across Gatun Lake between small round islands covered in dense green rainforest, light mist on the water, calm reflective lake."),
"A20": (None, 0, "Heavy tropical rain falling on dense green rainforest and on the surface of a calm lake in Panama, close-up of rain drops hitting the water, grey sky, lush wet leaves, cinematic documentary realism, deep blacks, gentle film grain. 16:9 horizontal. No text, no letters, no logos."),
"A21": (MID, 1, "Drone glide: the hero container ship passing through the Culebra Cut, a deep narrow channel carved between tall terraced rock and grass cliffs, rainforest on top."),
"A22": (MID, 0, "Drought at a tropical lake in Panama: exposed dry shoreline of cracked brown mud far below a green rainforest edge, old tree stumps sticking out of the mud, low water far away, harsh light."),
"A23": (MID, 0, "High aerial view: dozens of container ships and tankers waiting at anchor in a long line to the hazy horizon off the coast of Panama, the sea glittering, lots of empty water between them."),
"A24": (SET, 1, "Aerial slow rise above the modern Cocolí locks on the Pacific side: the hero container ship inside a lock chamber while the water level drops, wet chamber walls exposed, rainforest and hills around."),
"A25": (SET, 1, "Tracking shot alongside the hero container ship sailing under the large green steel arch of the Bridge of the Americas, the Panama City skyline in the distance."),
"A26": (SET, 1, "Medium shot: a canal pilot in a reflective vest climbing down a rope ladder on the hull of the hero container ship to a small orange pilot boat waiting below on the water."),
"A27": (SET, 1, "Wide shot from behind and above: the hero container ship sailing away into a golden Pacific sunset, shimmering golden water, distant islands, clear horizon."),
}
def run(k):
    light, ref, p = K[k]
    if light is None: prompt = (ARCH + p) if k in ("A07","A08","A09","A10","A11","A17") else p
    else: prompt = BASE.format(light=light) + (HERO if ref else "") + p
    body = {"model": "nano-banana-2.1", "prompt": prompt, "aspect_ratio": "16:9", "quality": "1K"}
    if ref: body["image_urls"] = [REF]
    for attempt in range(2):
        r = apipod.submit("images", body)
        if "data" not in r: print(k, r); continue
        w = apipod.wait("images", r["data"]["task_id"])
        if w.get("data", {}).get("status") == "completed":
            u = w["data"]["result"][0]; apipod.download(u, f"keyframes/{k}.jpg")
            return k, w["data"].get("usage", {}).get("cost"), u
        print(k, "failed", w.get("data", w))
    return k, None, None
ks = sys.argv[1:] or list(K)
res = {}
with cf.ThreadPoolExecutor(8) as ex:
    for k, c, u in ex.map(run, ks):
        print(k, c, u); sys.stdout.flush(); res[k] = u
json.dump(res, open("keyframes/urls_%s.json" % ("all" if not sys.argv[1:] else "_".join(ks)), "w"), indent=1)
