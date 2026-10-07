import ws, base64, concurrent.futures as cf
def b64(f): return "data:image/jpeg;base64," + base64.b64encode(open(f, "rb").read()).decode()
REF, CHR = b64("ref_crop.jpg"), b64("r_nb2.jpg")
STY = ("Image 1 is a STYLE reference only: recreate exactly its 3D CGI render style (Daz/Blender-like character model look, smooth skin shading, simple plain materials, soft flat lighting, slightly low-detail video-game cutscene look). Do not copy its people or room. ")
CHN = "Image 2 shows the main character: keep exactly the same man, face, keffiyeh and teal tunic. "
END = " Vertical 9:16. No text, no captions."
J = {  # key: (uses character, scene, motion)
 "c_intro": (1, "The shepherd man stands on a sandy hill above the blue Dead Sea, a few white goats behind him, one brown goat wandering away on the left.", "He turns his head toward the brown goat that is wandering away and frowns; the goat trots off; slow push-in camera."),
 "c_goat": (0, "A brown goat walking along the edge of a sandy cliff above the blue Dead Sea, a few white goats far behind, wide shot.", "The brown goat walks away along the cliff edge, camera tracks it from behind."),
 "c_climb": (1, "The shepherd man climbs a steep sandy cliff trail high above the blue Dead Sea, low angle wide shot.", "He climbs the narrow cliff trail upward, hand on the rock, slow upward crane camera."),
 "c_search": (1, "The shepherd man peers around a rock ledge on a high cliff, hand shading his eyes, a black cave opening next to him.", "He leans out and scans left and right, then shrugs; camera orbits slowly around him."),
 "c_throw": (1, "The shepherd man stands at a cliff face holding a fist-sized rock, a dark cave opening in front of him, low angle.", "He winds up and throws the rock into the dark cave; the camera follows the rock into the darkness."),
 "c_shatter": (0, "Inside a dark cave, a clay jar shattering, pieces flying, dust and a beam of daylight.", "The clay jar bursts into pieces in slow motion, dust rises, camera pushes in."),
 "c_jars": (1, "The shepherd man holds a burning torch inside a dark cave; rows of tall ancient clay jars with lids stand on the floor in the torch light.", "Camera glides forward over the jars; the man's eyes widen in awe."),
 "c_pull": (1, "Close-up: the shepherd man's hands pull an old rolled parchment scroll out of a clay jar in a cave, his amazed face above.", "The hands slowly lift the scroll out of the jar, dust falls, camera tilts up to the man's amazed face."),
 "c_unroll": (0, "An ancient parchment scroll with Hebrew letters unrolling on a plain wooden table.", "The scroll unrolls slowly toward the camera, slow push-in."),
 "c_priceless": (0, "An ancient scroll displayed in a glass museum case under a spotlight in a plain museum hall.", "Slow cinematic orbit around the glass case."),
 "c_end": (0, "A brown goat peeking out from behind a big rock on a sandy hill near the blue Dead Sea; a shepherd man in a teal tunic walks away far in the background.", "The brown goat pops its head out from behind the rock, looks at the camera and blinks; camera slowly pushes in."),
}
IMG = {"i_scale": "A brass balance scale on a plain wooden table: an old parchment scroll on the left pan, three small gold coins on the right pan.",
       "i_caves": "A tall sandy cliff face in the Dead Sea desert with many dark cave openings, bright daylight, wide vertical shot."}
def mk(k, scene, chr_):
    imgs = [REF, CHR] if chr_ else [REF]
    p = STY + (CHN if chr_ else "") + "Scene: " + scene + END
    r = ws.run("google/nano-banana-2/edit", {"images": imgs, "prompt": p, "aspect_ratio": "9:16"}, out=f"{k}.jpg")
    return r.get("status") == "completed"
def vid(k):
    c, scene, mv = J[k]
    if not mk(k, scene, c): return k, "img-fail"
    r = ws.run("kwaivgi/kling-v3-turbo-pro/image-to-video", {"image": b64(f"{k}.jpg"), "prompt": mv, "duration": 3}, out=f"{k}.mp4", timeout=900)
    return k, r.get("status")
with cf.ThreadPoolExecutor(6) as ex:
    fs = [ex.submit(vid, k) for k in J] + [ex.submit(lambda k=k, s=s: (k, mk(k, s, 0)), ) for k, s in IMG.items()]
    for f in fs: print(f.result(), flush=True)
print("balance", ws.balance())
