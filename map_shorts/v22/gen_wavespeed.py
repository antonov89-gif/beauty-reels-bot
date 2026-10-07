import ws, base64, concurrent.futures as cf, sys
CH = "a 12-year-old Bedouin shepherd boy in 1947 with a white headscarf, teal robe, big brown eyes"
ST = ", stylized 3D animated feature film look, bright saturated daylight, glossy materials, shallow depth of field, vertical 9:16, no text"
J = {
 "c_climb": (f"{CH}, climbing a steep sandy cliff trail high above the Dead Sea, seen from below, wide shot, small figure on huge cliff", "He climbs the narrow cliff trail upward, hand on the rock, slow upward crane camera."),
 "c_search": (f"{CH}, peering around a rock ledge on a high cliff, hand over eyes searching, a black cave opening nearby", "He leans out and scans left and right, shrugs, camera orbits slowly around him."),
 "c_throw": (f"{CH}, standing at a cliff face holding a rock, a dark cave opening in front of him, low angle", "He winds up and throws the rock into the dark cave; the camera follows the rock into the darkness."),
 "c_shatter": ("inside a dark cave, a clay jar shattering with pieces flying, dust and golden light rays" , "The clay jar bursts into pieces in slow motion, dust rises, camera pushes in."),
 "c_jars": (f"{CH}, holding a torch in a dark cave, rows of ancient clay jars glowing with warm golden light on the floor", "Camera glides forward over the jars as golden light pulses; the boy's eyes widen in awe."),
 "c_pull": (f"close-up of the boy's hands pulling an ancient parchment scroll out of a clay jar, golden glow", "The hands slowly lift the scroll out of the jar, golden dust sparkles, camera tilts up to the boy's amazed face."),
 "c_unroll": ("an ancient parchment scroll with Hebrew letters unrolling on a wooden table, golden glow, dust particles", "The scroll unrolls slowly toward the camera, sparkles drift, slow push-in."),
 "c_priceless": ("an ancient scroll displayed in a glass museum case under a golden spotlight in a dark elegant museum hall, sparkles", "Slow cinematic orbit around the glass case, light sparkles, dust motes."),
 "c_end": (f"a brown goat peeking out from behind a rock on a sandy hill near the Dead Sea, the shepherd boy walking far away in the background", "The brown goat pops its head out from behind the rock, looks at the camera and blinks; camera slowly pushes in."),
}
IMG = {
 "i_scale": ("a golden balance scale: on the left pan an ancient scroll, on the right pan three small gold coins, wooden table, warm studio light" ),
 "i_caves": ("a tall sandy cliff face in the Dead Sea desert with many dark cave openings, golden sunlight, wide vertical shot"),
}
def img(k, p):
    r = ws.run("bytedance/seedream-v4.5", {"prompt": p + ST, "size": "1080*1920"}, out=f"{k}.jpg"); return k, r.get("status")
def vid(k):
    p, mv = J[k]
    a = ws.run("bytedance/seedream-v4.5", {"prompt": p + ST, "size": "1080*1920"}, out=f"{k}.jpg")
    if a.get("status") != "completed": return k, "img-fail"
    im = "data:image/jpeg;base64," + base64.b64encode(open(f"{k}.jpg", "rb").read()).decode()
    r = ws.run("kwaivgi/kling-v3-turbo-pro/image-to-video", {"image": im, "prompt": mv, "duration": 3}, out=f"{k}.mp4", timeout=900)
    return k, r.get("status")
if __name__ == "__main__":
    with cf.ThreadPoolExecutor(6) as ex:
        fs = [ex.submit(vid, k) for k in J] + [ex.submit(img, k, p) for k, p in IMG.items()]
        for f in fs: print(f.result(), flush=True)
    print("balance", ws.balance())
