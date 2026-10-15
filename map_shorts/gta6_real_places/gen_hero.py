import apipod
STYLE = ("Hyper-detailed screenshot from a modern next-gen open-world action video game set in a fictional sunny version of Miami, Florida: "
 "in-engine real-time render, NOT a photograph, harsh bright Florida sun, saturated warm colours, glossy surfaces, dense environmental detail, "
 "cinematic depth of field, slight bloom and lens flare, 2025 AAA game lighting and realistic skin shading, generic anonymous character. "
 "Vertical 9:16, strong foreground subject. No logos, no readable text, no brand names, no HUD, no watermark. ")
P = ("Hero poster shot: a tanned young woman with a platinum blonde bob and large black sunglasses, white crop top and gold chain, sitting on the folded roof of a shiny pink 1980s convertible, "
     "smiling confidently at the camera, medium shot from slightly below, golden-hour sun behind her creating a warm rim light and lens flare, tall palm trees, pastel art deco hotels with neon tubes along a beachfront avenue, "
     "hot orange and pink sunset sky, turquoise ocean in the distance. The subject is in the lower two thirds of the frame; the top fifth is open sky for a title.")
r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + P, "aspect_ratio": "9:16", "quality": "2K"})
print(r)
w = apipod.wait("images", r["data"]["task_id"]); d = w.get("data", {})
print(d.get("status"), d.get("usage"), d.get("result"), d.get("error"))
if d.get("status") == "completed": apipod.download(d["result"][0], "hero.jpg")
