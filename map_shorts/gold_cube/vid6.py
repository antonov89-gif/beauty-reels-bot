import apipod
url = "https://s.apipod.ai/images/2026/10/14/2612943c-87cd-405f-a956-1f74a130448d.jpg"
P = ("3D game-engine render in the same style as the first frame (not Pixar, not photoreal), same character and environment, smooth physically plausible motion, no camera shake, no text. "
     "The giant polished gold cube stays a perfect solid gold cube and slowly expands outward just slightly, becoming a little bigger; tiny Nugget at its foot scratches his head in confusion. "
     "No paint, no liquid, no white outline, no extra objects. Camera: slow gentle push-in.")
r = apipod.submit("videos", {"model": "veo3-1-fast", "prompt": P, "image_urls": [url], "aspect_ratio": "9:16"})
w = apipod.wait("videos", r["data"]["task_id"], timeout=1500, every=10)
d = w["data"]; print(d["status"], d.get("usage"))
apipod.download(d["result"][0], "v_s6b.mp4")
