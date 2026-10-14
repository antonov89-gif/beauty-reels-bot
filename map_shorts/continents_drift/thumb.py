import apipod
exec(open("kf_test2.py").read().split("P = (")[0].replace("import apipod", ""))
MAX = "https://s.apipod.ai/images/2026/10/14/1bbbce94-59e7-44d0-9d34-0e56fb8dd05b.jpg"
P = ("Max is the same man as in reference image 1: same face, short brown hair, light stubble, red hoodie. "
     "YouTube Shorts cover, bold simple composition: in the lower half Max in a medium close-up with a shocked face (wide eyes, open mouth), pointing up with one hand; "
     "in the upper half behind him a big stylised Earth globe in a dark navy starfield, a bright glowing orange crack splits the Atlantic Ocean down the middle, Europe-Africa and the Americas pulled visibly apart; "
     "strong contrast, saturated colours, empty dark space at the very top for a title.")
r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + P, "aspect_ratio": "9:16", "quality": "2K", "image_urls": [MAX]})
w = apipod.wait("images", r["data"]["task_id"]); u = w["data"]["result"][0]; apipod.download(u, "thumb_base.jpg"); print(w["data"].get("usage"), u)
