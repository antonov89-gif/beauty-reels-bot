import ws302, base64, concurrent.futures as cf
def b64(f): return "data:image/jpeg;base64," + base64.b64encode(open(f, "rb").read()).decode()
REF = b64("/home/claude/v21/ws2/ref_crop.jpg")
STY = ("Image 1 is a STYLE reference only: recreate its 3D CGI render style (smooth skin shading, simple materials, bright daylight, video-game cutscene look). Do not copy its people or room. ")
J = {
 "thumb_c": "Scene: a funny split composition. Top half: aerial view of a tiny round coral atoll in deep blue ocean. Bottom half: a cheerful Polynesian family of eight standing close together on the white beach, all wearing the same bright red T-shirts and the same white name tag stickers, all smiling at the camera, one man in front holds a bouquet. Strong saturated colors, clean empty ocean area at the top for text. Vertical 9:16, no text, no letters.",
 "thumb_a": "Scene: a tiny round coral atoll seen from a low drone angle in a vast deep-blue ocean, turquoise lagoon, palm trees. On the white beach stands a crowd of about twelve Polynesian islanders of all ages, all smiling and waving at the camera, every person wearing an identical white name tag sticker on the chest. Lower half of the frame is empty open ocean (space for text). Vertical 9:16, no text, no letters.",
 "thumb_b": "Scene: close-up of a young Polynesian man on a tropical beach looking shocked at the camera, holding a bouquet of flowers; behind him a big crowd of smiling islanders who all look alike and all wear identical name tag stickers. Palm trees, turquoise lagoon, bright sun. Top third of the frame is clear blue sky (space for text). Vertical 9:16, no text, no letters.",
}
def go(k):
    r = ws302.run("bytedance/seedream-v4.5/edit", {"images": [REF], "prompt": STY + J[k], "size": "1080*1920"}, out=f"{k}.jpg")
    return k, r.get("status"), r.get("error")
with cf.ThreadPoolExecutor(2) as ex:
    for r in ex.map(go, ["thumb_c"]): print(r, flush=True)
