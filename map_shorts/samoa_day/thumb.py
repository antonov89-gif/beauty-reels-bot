import apipod, json
exec(open("kf_test2.py").read().split("P = (")[0].replace("import apipod", ""))
U = json.load(open("kf/urls.json"))
P = ("Mia is the same woman as in reference image 1: Samoan woman about 30, long dark hair, red floral shirt. "
     "YouTube Shorts cover, bold simple composition: in the lower half Mia in a medium close-up with a shocked face (wide eyes, open mouth), holding her phone; "
     "in the upper half behind her a giant blank paper calendar page (no text, no numbers) tearing in half and flying away over a turquoise tropical sea with two small green islands and palm trees; "
     "strong contrast, saturated colours, empty space at the very top for a title.")
r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + P, "aspect_ratio": "9:16", "quality": "2K", "image_urls": [U["S5"]]})
w = apipod.wait("images", r["data"]["task_id"]); u = w["data"]["result"][0]; apipod.download(u, "thumb_base.jpg"); print(w["data"].get("usage"), u)
