import apipod, json, concurrent.futures as cf, sys
U = {"s1": "037b4fd0-8a51-4e50-a2b2-37167dc5a003", "s2": "cc0e7e8c-787d-4d32-9a85-04be3b503e18", "s3": "2612943c-87cd-405f-a956-1f74a130448d",
     "s4": "c97eb857-73c1-41df-a307-6a8513eb10c7", "s5": "e3508f92-5b28-4aed-9e19-42e426cece8f", "s6": "7689e62a-0a7b-4b31-8b56-0572187c701d",
     "s7a": "5540da4a-a871-44e5-8622-f8e71233d6c6", "s7b": "b34bd023-c3cb-4ecf-a082-be5505c69e59", "s8": "f75f5225-5e78-4478-ab11-e9f4f31dd2ff"}
BASE = "3D game-engine render in the same style as the first frame (not Pixar, not photoreal), same character and environment, smooth physically plausible motion, no camera shake, no text. "
P = {
 "s1": "Nugget flicks the small gold ring upward with his thumb; the ring spins in the air and falls into the glowing crucible below; molten gold splashes up; Nugget reacts with a wide-open mouth and raised eyebrows. Camera: slow steady push-in.",
 "s2": "Thick streams of gold rings, coins and small gold bars flow in arcs from the globe into the funnel; molten gold pours into the crucible and glows brighter; Nugget stares up with an amazed open-mouth face. Camera: slow pull-back and a gentle tilt up revealing the whole globe.",
 "s3": "The giant gold cube stays perfectly still; a bright reflection sweeps across its polished surface; tiny Nugget raises both arms in amazement. Camera: slow rise from a low angle to eye level, cube stays centred.",
 "s4": "A few birds fly up from the lawn; tiny Nugget at the foot of the gold cube spreads his arms; the Eiffel Tower and the cube stay perfectly still. Camera: smooth crane pull-back and rise until the whole tower is visible.",
 "s5": "The drill spins and bores into the rock; the conveyor belt carries gold nuggets up and pours them onto the gold cube; Nugget watches with a surprised face. Camera: slow push-in toward the cube.",
 "s6": "The gold cube grows outward just slightly from the ghost outline, only a little bigger; tiny Nugget scratches his head in confusion. Camera: slow gentle push-in.",
 "s7a": "The gold cube slices into countless tiny glittering gold cubes that lift off as a swarm and spread over the crowd of colourful mannequins, who raise their arms. Camera: big smooth pull-back and rise over the swarm.",
 "s7b": "The tiny gold cube sparkles next to the larger white sugar cube on the palm; Nugget's face behind opens into a wide surprised grin. Camera: slow push-in macro, hand stays steady.",
 "s8": "A pigeon dives in, snatches the tiny gold crumb from Nugget's fingers and flies off; Nugget's smile drops into a shocked open-mouth stare. Camera: steady medium shot, no whip pans.",
}
def run(k):
    url = f"https://s.apipod.ai/images/2026/10/14/{U[k]}.jpg"
    r = apipod.submit("videos", {"model": "veo3-1-fast", "prompt": BASE + P[k], "image_urls": [url], "aspect_ratio": "9:16"})
    if "data" not in r: return k, r
    w = apipod.wait("videos", r["data"]["task_id"], timeout=1500, every=10)
    d = w.get("data", {})
    if d.get("status") != "completed": return k, w
    res = d["result"][0]; apipod.download(res, f"v_{k}.mp4"); return k, d["usage"]["cost"], res
ks = sys.argv[1:] or list(U)
with cf.ThreadPoolExecutor(3) as ex:
    for r in ex.map(run, ks): print(r, flush=True)
