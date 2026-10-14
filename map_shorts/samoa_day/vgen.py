import apipod, json, sys, time, base64, io, concurrent.futures as cf
from PIL import Image
U = json.load(open("kf/urls.json"))
def src(k):
    if k in U: return U[k]
    im = Image.open(f"kf/{k}.jpg").convert("RGB").resize((768, 1376)); b = io.BytesIO(); im.save(b, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
TAIL = " Keep the same low-budget Daz/Blender explainer 3D look, smooth steady camera, no cuts, no text, no letters, no numbers, no extra people."
P = {
 "S1": "The man lifts the blank top sheet of the wall calendar and lets it fall, an identical blank sheet is underneath; he blinks, puzzled, and scratches his head; dust floats in the warm window light; slow push-in.",
 "S2": "The trader's hands give the brass clock to the chief's hands, the clock's pendulum swings; the schooner rocks gently at the jetty, palm trees sway, small waves; camera slowly tracks along the jetty.",
 "S3": "The globe slowly rotates; a small cargo ship and a small plane travel along the glowing dotted routes from New Zealand and Australia toward the small Samoan islands; the yellow line glows; slow orbit.",
 "S4": "The glowing yellow line slowly bends around the green islands while the big blank calendar page flutters, tears free and flies away over the blue ocean; camera follows the page.",
 "S5": "The woman switches off the bedside lamp and the room darkens to moonlight, she lies down and closes her eyes, then warm morning light floods in, she wakes up, grabs her phone and stares at it with a shocked face.",
 "S6": "The woman holding the birthday cake looks at the calendar hole, her face falls into a disappointed pout, the candle flames flicker; the man beside her shrugs apologetically with raised palms; slow push-in.",
}
def run(k):
    body = {"model": "grok-imagine-1.5-fast", "prompt": P[k] + TAIL, "image_urls": [src(k)], "aspect_ratio": "9:16", "duration": 6}
    for a in range(30):
        r = apipod.submit("videos", body)
        if "data" in r: break
        if r.get("http_error") == 429: time.sleep(30); continue
        return k, "submit_err", str(r)[:300]
    w = apipod.wait("videos", r["data"]["task_id"], timeout=900, every=10); d = w.get("data", {})
    if d.get("status") == "completed":
        apipod.download(d["result"][0], f"clips/{k}.mp4"); return k, d.get("usage"), d["result"][0]
    return k, "failed", str(d or w)[:300]
ks = sys.argv[1:] or list(P)
with cf.ThreadPoolExecutor(4) as ex:
    for x in ex.map(run, ks): print(*x, flush=True)
