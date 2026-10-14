import apipod, json, concurrent.futures as cf
REF = "https://s.apipod.ai/images/2026/10/14/b7543b2b-3587-4db4-9544-daf2f635fa2f.jpg"
ST = ("YouTube thumbnail photo, hyper-detailed cinematic documentary realism, very high contrast, vivid saturated colours, crisp focus, dramatic light, "
      "simple bold composition with one clear subject, large empty area on the left third for text. The ship is the same giant container ship as in the reference image: "
      "dark blue hull, red bottom paint, mixed-colour containers, no name. 16:9. No text, no letters, no logos, no numbers. ")
P = {"A": "Extreme low-angle close view of the giant container ship squeezed inside a narrow concrete canal lock chamber in Panama, steel lock gate in the foreground, "
          "only a few meters of water on each side, golden sunrise backlight, rainforest behind, sense of immense scale.",
     "B": "Aerial drone view of a long line of giant container ships waiting at anchor off the green coast of Panama, the hero container ship in front entering the canal channel, "
          "glittering turquoise sea, dramatic golden light, deep blue shadows."}
def run(k):
    r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": ST + P[k], "aspect_ratio": "16:9", "quality": "2K", "image_urls": [REF]})
    w = apipod.wait("images", r["data"]["task_id"]); u = w["data"]["result"][0]; apipod.download(u, f"thumbs/base_{k}.jpg"); return k, w["data"].get("usage"), u
with cf.ThreadPoolExecutor(2) as ex:
    for x in ex.map(run, P): print(*x)
