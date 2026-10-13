import ws302, base64, concurrent.futures as cf
def b64(f): return "data:image/jpeg;base64," + base64.b64encode(open(f, "rb").read()).decode()
STY = "Cinematic photorealistic documentary still, shot on a drone or 35mm cinema camera, natural light, fine film grain, realistic scale. Wide 16:9. No text, no letters, no logos, no flags, no readable signs. "
J = {
 "ai_hook": ("Low aerial view over a very narrow sea strait at sunrise between dry rocky mountain coasts, a long line of large oil tankers and container ships queued in the channel, golden haze, deep blue water.",
             "Fast low drone flight forward over the water toward the queue of tankers, slight camera tilt up, sunrise light."),
 "ai_closed": ("Several large oil tankers anchored and motionless in a calm hazy sea at dusk, empty shipping lane between them, distant hazy coastline, ominous orange-grey sky.",
               "Slow drone orbit around the anchored tankers, the ships stay still, gentle swell, dusk light fading."),
 "ai_sailor": ("A tired merchant sailor in an orange work overall stands alone at the railing on the deck of a large tanker at dusk, looking at the horizon, hazy sea, lonely mood, medium shot from behind and to the side.",
               "Slow push-in toward the sailor, wind moves his overall, he lowers his head, the sea glitters behind."),
 "ai_fujairah": ("Aerial view of a busy oil port on a coast with jagged brown mountains behind: rows of white cylindrical oil storage tanks, a long jetty with tankers moored, ships waiting offshore in a blue sea, bright morning.",
                 "Slow drone glide along the coast past the storage tanks toward the jetty and moored tankers."),
 "ai_pipe": ("Aerial view of a large above-ground steel oil pipeline running straight across golden sand dunes toward rugged brown mountains on the horizon, low warm sun, long shadows.",
             "Drone flies forward fast and low along the pipeline toward the mountains, dunes rushing below."),
 "ai_train": ("A long freight train with shipping containers emerging from a tunnel portal in rugged bare brown rocky mountains, desert valley, clear sky, harsh midday sun, aerial three-quarter view.",
              "The train moves out of the tunnel toward the camera, drone slowly pulls back and rises revealing the mountains."),
 "ai_final": ("A huge fully loaded container ship leaving a modern port with tall cranes at sunset, heading out into the open sea, warm orange sky, calm water with a long wake, aerial view from behind the ship.",
              "Drone follows behind the container ship as it sails out to the open sea, slowly rising, sunset glow."),
}
def go(k):
    p, mv = J[k]
    r = ws302.run("bytedance/seedream-v4.5", {"prompt": STY + p, "size": "2560*1440"}, out=f"{k}.jpg")
    if r.get("status") != "completed": return k, "img", str(r)[:200]
    r = ws302.run("minimax/hailuo-2.3/fast", {"image": b64(f"{k}.jpg"), "prompt": mv, "duration": 6}, out=f"{k}.mp4")
    return k, r.get("status"), str(r.get("error"))[:200]
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(go, J): print(r, flush=True)
