import apipod
STYLE = ("Cinematic documentary realism, as if filmed for a premium travel and engineering documentary: real-world location in Panama, golden-hour sunrise light, warm saturated colour grade, "
 "high contrast with deep slightly crushed blacks, glossy clean surfaces, gentle film grain, anamorphic-like wide framing, physically plausible water, ships with correct real-world scale and proportions, "
 "modern container ships with plain hulls (no readable names, no logos), lush green rainforest coast. 16:9 horizontal, subject clearly separated from the background. No text, no letters, no logos. ")
P = ("Aerial shot at sunrise off the green Caribbean coast of Panama: in the foreground a giant modern container ship with a dark blue hull, red bottom paint, white bridge at the stern and mixed-colour containers, "
     "behind it a long line of other container ships and tankers waiting at anchor stretching toward the horizon, calm sea with golden reflections, light haze, rainforest hills on the coast.")
r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + P, "aspect_ratio": "16:9", "quality": "2K"})
w = apipod.wait("images", r["data"]["task_id"]); u = w["data"]["result"][0]; apipod.download(u, "test_A01.jpg"); print(w["data"]["usage"], u)
