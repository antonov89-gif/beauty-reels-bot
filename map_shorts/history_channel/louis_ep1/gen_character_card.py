"""Generic character-card generator (Marcel was done by gen_marcel_card.py + gen_marcel_sheet.py; same method).
Characters: chef (Maitre Benoit). Nano Banana 2.1, 2K, about $0.04 per image. PAID: runs only after the owner's yes.
Usage: python3 gen_character_card.py chef front            (1 image from text + a palace style reference, $0.04)
       python3 gen_character_card.py chef three_quarter    (from cook_front.jpg)
       python3 gen_character_card.py chef sheet [ids]      (the 16 angles/emotions from cook_front.jpg + cook_three_quarter.jpg, about $0.64)"""
import json, re, sys, threading, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip(); H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
CH = {"chef": dict(dir="chef_card/", prefix="cook",
    face="a large broad-shouldered man of about 45 with a round, ruddy, sweaty face, a bulbous nose, thick dark bushy eyebrows, small bright blue eyes, a double chin, flushed cheeks, no moustache and no beard, skin shining with sweat",
    dress="a plain soft rounded white linen cap sitting low on the head, with no pleats and not tall, a white linen apron over a cream shirt with the sleeves rolled to the elbows, a white cloth knotted at the neck; no gold, no red, no wig",
    place="a plain warm stone palace kitchen corridor with copper pots hanging on the wall")}
BASE = "Vertical 9:16 photo, soft even natural light, photorealistic, real skin texture with visible pores. No text. "
ANG = {"a1_left34": "Head and shoulders, turned three-quarters to HIS left, looking at the lens, neutral.", "a2_right34": "Head and shoulders, turned three-quarters to HIS right, looking at the lens, neutral.",
       "a3_profile_left": "Head and shoulders in strict profile facing the left of the frame, the bulbous nose and double chin clearly visible, neutral.", "a4_profile_right": "Head and shoulders in strict profile facing the right of the frame, neutral.",
       "a5_back": "Seen from behind, head and shoulders: the back of the tall white cap, the knotted cloth, broad shoulders, head slightly turned.", "a6_from_below": "Low camera angle looking up at him, head and shoulders, he looks down at the lens, nervous.",
       "a7_from_above": "High camera angle looking down at him, head and shoulders, he looks up at the lens, eager.", "a8_bow_side": "Upper body seen from the side, carrying a huge copper pot with both arms, leaning with the weight, face turned to the lens.",
       "e1_neutral": "Close front portrait, head and shoulders, neutral, looking at the lens.", "e2_nervous_smile": "Close front portrait, head and shoulders, a nervous broad smile with clenched teeth.",
       "e3_panicked": "Close front portrait, head and shoulders, panicked, eyes wide, mouth open, sweat on the forehead.", "e4_proud": "Close front portrait, head and shoulders, proud, chin up, a satisfied smile.",
       "e5_wiping": "Close front portrait, head and shoulders, wiping his forehead with the white cloth, exhausted.", "e6_apologetic": "Close front portrait, head and shoulders, apologetic, eyebrows raised, lips pressed.",
       "e7_delighted": "Close front portrait, head and shoulders, delighted, a big happy grin.", "e8_shocked": "Close front portrait, head and shoulders, shocked, frozen, eyes huge."}
urls = {}


def host(path):
    if path not in urls:
        d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": path.split("/")[-1], "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
        urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
        urls[path] = d["publicUrl"]
    return urls[path]


def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u


def gen(c, name, scene, refs, extra=""):
    ch = CH[c]; body = {"model": "nano-banana-2.1", "prompt": BASE + scene + f" {ch['face'].capitalize()}, wearing {ch['dress']}, in {ch['place']}. " + extra, "aspect_ratio": "9:16", "quality": "2K", "image_urls": [host(r) for r in refs]}
    r = apipod.submit("images", body)
    if "data" not in r: print(name, "SUBMIT FAILED", str(r)[:300]); return
    tid = r["data"]["task_id"]; out = H0 + ch["dir"] + name + ".jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=400, every=4)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {})
    if u: apipod.download(u, out)
    print(name, "cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")


c, step = sys.argv[1], sys.argv[2]; ch = CH[c]; P = ch["prefix"]; D = H0 + ch["dir"]
SAME = " EXACTLY the same man as in the FIRST (and SECOND) reference image: the same face, eyes, brows, nose, chins, skin and age; do not change them. "
if step == "front":
    gen(c, P + "_front", "Close front portrait, shoulders and head, looking straight into the lens with an eager, nervous smile.", [H0 + "chef_card/cook_front_v2_thumb.jpg"],
        " The reference image shows exactly the right FACE and the right kitchen, apron and neck cloth: keep exactly the same man, face, skin, sweat, cap, apron and kitchen, but (1) NO thumb, finger or hand anywhere in the frame (his arms hang down out of sight, nothing in the foreground), and (2) a clearly visible heavy double chin and fuller jowls, as a well-fed cook.")
elif step == "three_quarter":
    gen(c, P + "_three_quarter", "Three-quarter view from the waist up, carrying a large copper pot with both hands, glancing at the lens with a nervous smile.", [D + P + "_front.jpg"], SAME)
else:
    ids = sys.argv[3:] or list(ANG); sem = threading.Semaphore(4)

    def run(k):
        with sem: gen(c, "sheet_" + k, ANG[k], [D + P + "_front.jpg", D + P + "_three_quarter.jpg"], SAME)
    ts = [threading.Thread(target=run, args=(k,)) for k in ids]; [t.start() for t in ts]; [t.join() for t in ts]
