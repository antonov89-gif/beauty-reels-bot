import apipod
STYLE = ("Bright stylised 3D animation still in the look of a polished viral science-explainer Short (game-engine CG, like Zack D. Films): "
 "clear readable shapes, expressive glossy materials, soft shadows, clean daylight, saturated colours, clear horizon, simulation feel, "
 "main subject clearly separated from the background. Characters have big expressive faces, slightly exaggerated reactions, smooth airbrushed skin and simple hair meshes; NOT photorealistic, NOT Pixar. "
 "Vertical 9:16 composition with free space in the top third. No text, no letters, no numbers, no logos, no watermark. ")
P = ("Iceland rift valley with mossy black lava rocks and a small waterfall in the distance under a clear blue sky. A long glowing orange crack runs straight through the valley floor toward the horizon. "
     "Max, a man about 30 with short brown hair, light stubble, a red hoodie, blue jeans and brown hiking boots, stands with one boot on each side of the crack, legs spread wide, arms flung out for balance, "
     "eyebrows raised in comic surprise, looking down at the crack. Wide shot from slightly above, the crack leading the eye.")
r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + P, "aspect_ratio": "9:16", "quality": "2K"})
w = apipod.wait("images", r["data"]["task_id"]); u = w["data"]["result"][0]; apipod.download(u, "test_S5.jpg"); print(w["data"].get("usage"), u)
