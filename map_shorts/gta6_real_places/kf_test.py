import apipod
STYLE = ("Hyper-detailed screenshot from a modern next-gen open-world crime action video game set in a fictional sunny version of Miami, Florida: "
 "in-engine real-time render, NOT a photograph, harsh bright Florida sun, deep blue sky, saturated warm colours, glossy wet-looking surfaces, "
 "very dense environmental detail (palm trees, neon signs without readable words, parked classic and modern cars, litter, graffiti, flags), "
 "cinematic depth of field, slight bloom and lens flare, characteristic 2025 AAA game lighting and skin shading, generic anonymous pedestrians only. "
 "Vertical 9:16 composition, strong foreground subject and leading lines. No logos, no readable text, no brand names, no HUD, no watermark. ")
P = ("Vice City style beach strip at golden afternoon: art deco hotels with pastel facades and glowing neon tubes along a palm-lined beachfront avenue, "
     "a shiny lowered pink 1980s convertible parked in the foreground, a few tourists in swimwear and sunglasses walking past, the turquoise ocean and white sand on the right, "
     "a police helicopter in the sky.")
r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + P, "aspect_ratio": "9:16", "quality": "2K"})
w = apipod.wait("images", r["data"]["task_id"]); u = w["data"]["result"][0]; apipod.download(u, "test_vice.jpg"); print(w["data"].get("usage"), u)
