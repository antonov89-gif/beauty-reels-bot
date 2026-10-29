"""v5 of the hard-cut first frames (owner 29.10: "Нет, нужен такой парик" = the tall grey powdered wig of the old storyboard C08/C09). Face from the face master, face larger, smug half-smile, no rouge.
Refs, in this order: face_front_talking.jpg, face_three_quarter.jpg, tall_wig_ref.jpg (the wig only, cropped from the old C09 frame, face masked grey; owner 29.10 "На с09"), then the storyboard frame as the COMPOSITION reference.
Nano Banana 2.1, 2K, about $0.04 each (7 = about $0.28). PAID: runs only after the owner's yes. Usage: python3 gen_frames_v5.py [ids]"""
import json, re, sys, threading, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
FM = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_card/face_master_v3/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip(); H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
FACE = ("a man of about 35 with a pale complexion, light grey-hazel eyes, a long straight nose, a narrow face, a thin upturned waxed moustache, arched brows and a small dark beauty spot beside the mouth")
KEEP = ("He has EXACTLY the same face as the man in the FIRST and SECOND reference images (same eyes, nose, moustache, age about 35 and skin): do not make him older. "
        "Makeup (series standard, owner 29.10: more powder): the heavy period makeup of the FIFTH reference image: the face whitened with pale powder (a matte white-pink complexion), clearly pink rouged cheeks and slightly pink lips, as at the court of Versailles; the face itself (features, age) stays the man of the first two reference images. Expression: a smug, self-satisfied half-smile, relaxed, not stern, not tired. Only the wig and clothes change as described.")
BASE = "Vertical 9:16 phone photo, ultra-wide front camera look, hand-held, soft natural light, photorealistic, real skin texture with visible pores. No text, no modern objects. "
WHITE = ("the tall grey-white powdered wig from the THIRD reference image: a high wavy crown standing up above the head, rows of rolled curls at the sides, and long grey curls falling over the shoulders to the chest")
GOLD = "a gold embroidered silk dressing gown over a white lace shirt"
RED = "a scarlet velvet coat embroidered with gold suns, a white lace jabot and lace cuffs, rings on his fingers"
SC = {
 "C07": f"Low angle from a phone on the polished parquet floor looking up at him, his face clearly visible and well lit, a gilded state bedchamber with a canopied bed on the left, tall windows and a crystal chandelier above. {FACE.capitalize()}, wearing {WHITE} and {GOLD}, white stockings and black buckled shoes, stands full length with a ringed hand raised and a smug look down at the lens. A hand sweeps in from the top edge, out of focus, as if re-aiming the phone. Behind him the double doors open and courtiers in period dress enter.",
 "C09": f"Wide view with dark vignetted corners, camera low, in a gilded bedchamber with a canopied bed. {FACE.capitalize()}, wearing {WHITE} and {GOLD}, stands at the left in the foreground, his face clearly visible and turned to the lens, with a smug face. A row of courtiers in period dress makes deep courtly bows to the right; a plumed hat lies on the parquet floor in the middle.",
 "C10": f"Foreground: a large black buckled shoe with a red heel and a white silk stocking, raised toward the lens, sharp. Behind it, small and in the distance, {FACE}, wearing {WHITE} and {GOLD}, sits in a gilded armchair with a smug raised eyebrow, in a bedchamber with a canopied bed and a tall window.",
 "C12": f"Close backward-walking selfie, his face and shoulders filling the upper half of the frame, in the Hall of Mirrors at Versailles: mirrors and chandeliers on the left, tall arched windows on the right, courtiers trailing behind him. {FACE.capitalize()}, wearing {WHITE} and {RED}, strides toward the lens with a proud look, one ringed hand on his jabot.",
 "C13": f"Close selfie, his face filling about a third of the frame, in front of a tall mirror panel in the Hall of Mirrors, chandeliers and arched windows behind. {FACE.capitalize()}, wearing {WHITE} and {RED}, fingers on his jabot, an annoyed sideways glance; a courtier's face peeks over his shoulder in the background.",
 "C14": f"Medium close-up selfie, his face and chest large in frame, at the Hall of Mirrors threshold, courtiers bowing in the background, a long banquet table far away. {FACE.capitalize()}, wearing {WHITE} and {RED}, straightens a curl of his wig with one ringed hand and looks to the side, about to point at the lens.",
 "C15": f"Close selfie, his face large in frame, at a long banquet table laden with tiered cakes, fruit and candelabra in the Hall of Mirrors. {FACE.capitalize()}, wearing {WHITE} and {RED}, chin lifted with a haughty look down his nose; a gilded hand mirror in the lower right foreground.",
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
    refs = [host(FM + "face_front_talking.jpg"), host(FM + "face_three_quarter.jpg"), host(FM + "tall_wig_ref.jpg"), host("frames/" + fid + ".jpg"), host(FM + "makeup_ref_C09v6.jpg")]
    body = {"model": "nano-banana-2.1", "prompt": BASE + SC[fid] + " Composition (only the room, the camera angle and the other people) like the FOURTH reference image; ignore the wig and the face in the fourth image. " + KEEP, "aspect_ratio": "9:16", "quality": "2K", "image_urls": refs}
    r = apipod.submit("images", body)
    if "data" not in r: print(fid, "SUBMIT FAILED", r); return
    tid = r["data"]["task_id"]; out = f"frames/{fid}_mk.jpg"; open(out + ".task_id", "w").write(tid)
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
