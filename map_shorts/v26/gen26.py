import ws302, base64, concurrent.futures as cf
ST = ", photorealistic, shot on a real camera like travel vlog B-roll, natural daylight, realistic people, vertical 9:16, no text, no logos, no readable signs"
J = {
 "ai_checkout": ("close-up of a hand using a laptop trackpad on a cruise booking checkout page with a price total, blurred numbers, home desk", "The hand scrolls down and clicks, the price on screen jumps up, slow push-in."),
 "ai_bill": (None, "The couple scans the long printed bill, the man raises his eyebrows, the woman laughs nervously, camera slowly pushes in."),
 "ai_steward": ("a cruise cabin steward in a white uniform folding a towel animal on a neatly made cruise cabin bed, porthole light", "The steward finishes the towel elephant and smiles, gentle dolly forward."),
 "ai_cocktails": ("two colourful tropical cocktails clinking at a cruise ship pool deck bar, blue ocean behind, bright sun", "Two hands clink the cocktails, ice moves, camera racks focus to the ocean."),
 "ai_wifi": ("a young woman on a cruise ship balcony holding her phone and frowning at a slow loading screen, open ocean behind", "She lifts the phone higher searching for signal and sighs, slow orbit."),
 "ai_tender": ("tourists in sunhats stepping from a big white cruise ship into a small tender boat heading to a tropical island", "The tender boat pulls away toward the island, camera follows from behind."),
 "ai_hotel": ("view from a hotel room window at dawn of a huge cruise ship docked at the port, a suitcase by the window", "Morning light rises, the curtains move slightly, slow push toward the window."),
 "ai_shock": ("a man sitting on a cruise cabin bed looking at his phone with the final onboard bill, surprised face, balcony behind", "He scrolls, his eyes widen, he looks up at the camera in disbelief, slow push-in."),
}
def b64(f): return "data:image/jpeg;base64," + base64.b64encode(open(f, "rb").read()).decode()
def go(k):
    p, mv = J[k]
    if p:
        r = ws302.run("bytedance/seedream-v4.5", {"prompt": p + ST, "size": "1080*1920"}, out=f"{k}.jpg")
        if r.get("status") != "completed": return k, "img " + str(r)[:200]
    else:
        import shutil; shutil.copy("test.jpg", f"{k}.jpg")
    r = ws302.run("kwaivgi/kling-v3-turbo-pro/image-to-video", {"image": b64(f"{k}.jpg"), "prompt": mv, "duration": 3}, out=f"{k}.mp4")
    return k, r.get("status") or str(r)[:200]
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(go, J): print(r, flush=True)
