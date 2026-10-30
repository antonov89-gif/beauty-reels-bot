"""C09 v8 (owner 30.10 "Да": the page Marcel from his card is in the row of bowing courtiers, other courtiers in simple plain wigs). Based on v7 (owner 29.10: fixes after the frame check + "он не умеет держать телефон, покажи это зрителям": C07 jabot, C10 red heel only, C14 a different setup, C09/C13/C15 deliberately badly framed). v6.1 (owner 29.10: makeup standard "C10 more powder, C09 less" = one medium powder level for all frames). v6 (owner 29.10: "делай как референс: камера близко к лицу и ходит в руке"): C07, C09, C10 redrawn as CLOSE hand-held selfies (face and shoulders large, his arm holding the phone), the gags kept in the background; C12-C15 v5 stay.
Based on v5 of the hard-cut first frames (owner 29.10: "Нет, нужен такой парик" = the tall grey powdered wig of the old storyboard C08/C09). Face from the face master, face larger, smug half-smile, no rouge.
Refs, in this order: face_front_talking.jpg, face_three_quarter.jpg, tall_wig_ref.jpg (the wig only, cropped from the old C09 frame, face masked grey; owner 29.10 "На с09"), then the storyboard frame as the COMPOSITION reference.
Nano Banana 2.1, 2K, about $0.04 each (7 = about $0.28). PAID: runs only after the owner's yes. Usage: python3 gen_frames_v6.py [ids]"""
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
SC = {"C09": (f"Badly framed hand-held selfie, as if he cannot hold a phone: his face has slid to the LEFT edge of the frame and is cut by it (only the right half of his face and part of the tall wig visible), the horizon tilted about 12 degrees. {FACE.capitalize()}, wearing {WHITE} and {GOLD} with a lace jabot, smug, one eyebrow raised. "
      "Behind him in the gilded bedchamber a row of courtiers in simple plain grey wigs and plain dark coats makes deep courtly bows; in the middle of the row, clearly visible and small, a slim young page in a SKY-BLUE coat with silver braid and a small white wig with a black ribbon (his face is shown in the SIXTH and SEVENTH reference images) bows and glances up in alarm; a black plumed hat lies on the parquet floor in front of the row.")}
urls = {}


def host(path):
    if path not in urls:
        n = path.split("/")[-1]
        d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": n, "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
        urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
        urls[path] = d["publicUrl"]
    return urls[path]


def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u


MC = "/home/user/beauty-reels-bot/map_shorts/history_channel/marcel_card/"
fid = "C09"
refs = [host(FM + "face_front_talking.jpg"), host(FM + "face_three_quarter.jpg"), host(FM + "tall_wig_ref.jpg"), host("frames/C09_first_v7.jpg"), host(FM + "makeup_ref_C09v6.jpg"), host(MC + "marcel_front.jpg"), host(MC + "marcel_three_quarter.jpg")]
body = {"model": "nano-banana-2.1", "prompt": BASE + SC[fid] + " The room like the FOURTH reference image (not its camera distance); ignore the wig and the face in the fourth image. The KING's face is the FIRST and SECOND reference images; the small page's face is the SIXTH and SEVENTH: do not mix the two faces. " + KEEP, "aspect_ratio": "9:16", "quality": "2K", "image_urls": refs}
r = apipod.submit("images", body)
if "data" not in r: sys.exit("SUBMIT FAILED " + str(r)[:300])
tid = r["data"]["task_id"]; out = "frames/C09_v8.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=400, every=4)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
u = find(res.get("data") or {})
if u: apipod.download(u, out)
print(fid, "cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")
