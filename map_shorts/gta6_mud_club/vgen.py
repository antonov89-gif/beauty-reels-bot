import apipod, json, sys, base64, io, concurrent.futures as cf
from PIL import Image
U = json.load(open("kf/urls.json"))
TAIL = " Smooth realistic motion, no cuts, no text, no logos."
P = {
 "M1": "The monster truck lands and throws a huge wave of mud toward the camera, the crowd cheers and waves flags, slow-motion spray, slow forward camera push.",
 "M2": "The quad and the swamp buggy race through the mud pit side by side, mud sprays high, riders lean into the turn, the camera tracks forward low over the mud.",
 "M3": "The muddy crowd dances and laughs, string lights flicker, someone throws mud in the air, golden light flickers through the trees, slow handheld camera drift.",
 "M4": "Slow aerial glide forward over the park, trucks crawl along the dirt tracks, a quad leaves a trail of mud, dust and smoke drift, clouds move.",
 "M5": "The pickup slides sideways through the bog throwing a fan of mud, spectators cheer on the berm, light rays flicker through the Spanish moss, slow camera push in.",
 "M6": "The bonfire flickers, sparks rise, people sit on tailgates and talk, headlights flash, fireflies float, the sky slowly darkens, slow camera glide forward.",
}
def src(k):
    if U.get(k): return U[k]
    im = Image.open(f"kf/{k}.jpg").convert("RGB"); im.thumbnail((1024, 1820)); b = io.BytesIO(); im.save(b, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
def run(k):
    body = {"model": "grok-imagine-1.5-fast", "prompt": P[k] + TAIL, "image_urls": [src(k)], "aspect_ratio": "9:16", "duration": 6}
    r = apipod.submit("videos", body)
    if "data" not in r: return k, "submit_err", str(r)[:300]
    w = apipod.wait("videos", r["data"]["task_id"], timeout=900, every=10); d = w.get("data", {})
    if d.get("status") == "completed":
        open(f"clips/{k}.url", "w").write(d["result"][0]); apipod.download(d["result"][0], f"clips/{k}.mp4"); return k, d.get("usage"), d["result"][0]
    return k, "failed", str(d or w)[:300]
if __name__ == "__main__":
    with cf.ThreadPoolExecutor(3) as ex:
        for x in ex.map(run, sys.argv[1:] or list(P)): print(*x)
