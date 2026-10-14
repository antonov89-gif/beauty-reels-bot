import apipod
STYLE = ("Clearly a 3D render in the look of a low-budget educational 'what if' explainer animation made in Daz Studio / Blender with game-engine assets, NOT a photograph, NOT Pixar, NOT cartoon, NOT hyper-realistic: "
 "characters have realistic human proportions and a realistic head size, normal-sized eyes, smooth airbrushed plastic-looking skin with soft shading and almost no pores, simple solid-clump hair mesh, slightly uncanny early-2010s game cutscene look, expressive exaggerated facial animation; "
 "simple matte clothing textures; simplified environment with flat saturated blue sky and simple even lighting with soft shadows. "
 "No text, no letters, no numbers, no logos. Vertical 9:16, free space above for captions. ")
P = ("Scene: Thingvellir-style rift valley in Iceland: two long walls of dark grey basalt rock with patches of green moss, between them a narrow straight fissure in the ground with crystal-clear blue water at the bottom, no lava, no fire. "
     "Max, a man about 30 with short brown hair and light stubble, red hoodie, blue jeans, brown hiking boots, stands with one boot on each edge of the fissure, legs spread wide, arms out for balance, surprised face with raised eyebrows and open mouth, looking down into the gap. "
     "Medium-wide shot from slightly above, the fissure leading toward the horizon, flat blue sky.")
r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + P, "aspect_ratio": "9:16", "quality": "2K"})
w = apipod.wait("images", r["data"]["task_id"]); u = w["data"]["result"][0]; apipod.download(u, "test_S5_v2.jpg"); print(w["data"].get("usage"), u)
