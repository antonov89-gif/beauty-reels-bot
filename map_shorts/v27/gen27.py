import ws302, base64, concurrent.futures as cf
def b64(f): return "data:image/jpeg;base64," + base64.b64encode(open(f, "rb").read()).decode()
REF = b64("/home/claude/v21/ws2/ref_crop.jpg")
STY = ("Image 1 is a STYLE reference only: recreate its 3D CGI render style (Daz/Blender-like characters, smooth skin shading, simple materials, soft flat daylight, video-game cutscene look). Do not copy its people or room. ")
J = {
 "ai_1863": ("Scene: 1860s tropical coral atoll beach with coconut palms and turquoise lagoon. An English carpenter in a white linen shirt, braces and straw hat stands with his Polynesian wife in a simple dress; an outrigger canoe arrives at the shore with two more Polynesian women waving. Vertical 9:16, no text.",
             "The canoe lands, the two women step out and wave, the man turns to the camera with a surprised awkward smile; slow push-in."),
 "ai_date": ("Scene: sunset on a tropical atoll beach. A young Polynesian man in a modern shirt holds a small bouquet of flowers in one hand and unrolls a very long paper family tree scroll with the other; the scroll spills onto the sand. Vertical 9:16, no text.",
             "He unrolls the long family tree scroll, it keeps falling onto the sand, he looks worried at the camera; gentle push-in."),
}
def go(k):
    p, mv = J[k]
    r = ws302.run("bytedance/seedream-v4.5/edit", {"images": [REF], "prompt": STY + p, "size": "1080*1920"}, out=f"{k}.jpg")
    if r.get("status") != "completed": return k, "img " + str(r)[:200]
    r = ws302.run("minimax/hailuo-2.3/fast", {"image": b64(f"{k}.jpg"), "prompt": mv, "duration": 6}, out=f"{k}.mp4")
    return k, r.get("status"), r.get("error")
with cf.ThreadPoolExecutor(2) as ex:
    for r in ex.map(go, J): print(r, flush=True)
