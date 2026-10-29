"""v6 (owner 29.10: "делай как референс: камера близко к лицу и ходит в руке"): C07, C09, C10 redrawn as CLOSE hand-held selfies (face and shoulders large, his arm holding the phone), the gags kept in the background; C12-C15 v5 stay.
Based on v5 of the hard-cut first frames (owner 29.10: "Нет, нужен такой парик" = the tall grey powdered wig of the old storyboard C08/C09). Face from the face master, face larger, smug half-smile, no rouge.
Refs, in this order: face_front_talking.jpg, face_three_quarter.jpg, tall_wig_ref.jpg (the wig only, cropped from the old C09 frame, face masked grey; owner 29.10 "На с09"), then the storyboard frame as the COMPOSITION reference.
Nano Banana 2.1, 2K, about $0.04 each (7 = about $0.28). PAID: runs only after the owner's yes. Usage: python3 gen_frames_v6.py [ids]"""
import json, re, sys, threading, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
FM = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_card/face_master_v3/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip(); H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
FACE = ("a man of about 35 with a pale complexion, light grey-hazel eyes, a long straight nose, a narrow face, a thin upturned waxed moustache, arched brows and a small dark beauty spot beside the mouth")
KEEP = ("He has EXACTLY the same face as the man in the FIRST and SECOND reference images (same eyes, nose, moustache, age about 35 and skin): do not make him older, no heavy makeup, no pink rouge, no powdered cheeks. "
        "Expression: a smug, self-satisfied half-smile, relaxed, not stern, not tired. Only the wig and clothes change as described.")
BASE = "Vertical 9:16 phone photo, ultra-wide front camera look, hand-held, soft natural light, photorealistic, real skin texture with visible pores. No text, no modern objects. "
WHITE = ("the tall grey-white powdered wig from the THIRD reference image: a high wavy crown standing up above the head, rows of rolled curls at the sides, and long grey curls falling over the shoulders to the chest")
GOLD = "a gold embroidered silk dressing gown over a white lace shirt"
RED = "a scarlet velvet coat embroidered with gold suns, a white lace jabot and lace cuffs, rings on his fingers"
SC = {
 "C07": f"Close hand-held selfie, phone held at arm's length slightly above, his face and shoulders filling the upper half of the frame, his arm visible at the lower edge. {FACE.capitalize()}, wearing {WHITE} and {GOLD}, smug half-smile at the lens. Behind him in the gilded state bedchamber the double doors are opening and courtiers in period dress are entering, small and a little out of focus.",
 "C09": f"Close hand-held selfie, phone at arm's length, his face and shoulders large in the frame, his arm visible at the lower edge. {FACE.capitalize()}, wearing {WHITE} and {GOLD}, smug, one eyebrow raised. Behind him in the gilded bedchamber a row of courtiers make deep courtly bows, and one courtier is reaching for his plumed hat that has fallen on the parquet floor.",
 "C10": f"Close hand-held selfie from slightly above, his face large in the upper part of the frame; he lifts one leg so that his black buckled shoe with a bright red heel and a white silk stocking comes up into the lower part of the frame next to the lens. {FACE.capitalize()}, wearing {WHITE} and {GOLD}, a proud, teasing look. Gilded bedchamber with a canopied bed behind.",
}
urls = {}


def host(path):
    if path not in urls:
        n = path.split("/")[-1]
        d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": n, "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
        urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
        urls[path] = d["publicUrl"]
    return urls[path]


def find(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u:
            return u


def one(fid):
    refs = [host(FM + "face_front_talking.jpg"), host(FM + "face_three_quarter.jpg"), host(FM + "tall_wig_ref.jpg"), host("frames/" + fid + ".jpg")]
    body = {"model": "nano-banana-2.1", "prompt": BASE + SC[fid] + " The room and the other people like the FOURTH reference image (not its camera distance); ignore the wig and the face in the fourth image. " + KEEP, "aspect_ratio": "9:16", "quality": "2K", "image_urls": refs}
    r = apipod.submit("images", body)
    if "data" not in r: print(fid, "SUBMIT FAILED", r); return
    tid = r["data"]["task_id"]; out = f"frames/{fid}_v6.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=400, every=4)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {})
    if u: apipod.download(u, out)
    print(fid, "cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")


ids = sys.argv[1:] or list(SC)
sem = threading.Semaphore(4)


def run(i):
    with sem: one(i)


ts = [threading.Thread(target=run, args=(i,)) for i in ids]
[t.start() for t in ts]; [t.join() for t in ts]
