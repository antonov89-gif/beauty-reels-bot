"""Marcel the page: the FULL character card (owner 30.10: "карточка Марселя со всех ракурсов и эмоций, чтобы лицо не менялось при генерациях").
16 images, Nano Banana 2.1, 2K, about $0.04 each = about $0.64. PAID: runs only after the owner's yes.
Every image uses marcel_front.jpg and marcel_three_quarter.jpg as the face references (in this order) plus the locked descriptor block; neutral grey-beige studio-like palace wall light so the face is the only variable.
8 angles: left 3/4, right 3/4, profile left, profile right, back of the head, from below, from above, bow seen from the side. 8 emotions (close front): neutral, worried, alarmed, apologetic, eager, timid, terrified, relieved smile.
Usage: python3 gen_marcel_sheet.py [ids]  (default all 16)"""
import json, re, sys, threading, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
MC = "/home/user/beauty-reels-bot/map_shorts/history_channel/marcel_card/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip(); H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
FACE = ("a slim young man of about 18 with a round, open, slightly freckled face, a short snub nose, large dark brown eyes with a worried look, thick straight dark eyebrows, a small chin, ears that stick out a little, no moustache, a smooth boyish complexion with a natural light flush")
LIVERY = ("a plain short white-powdered wig tied at the nape with a black ribbon, a sky-blue wool coat with plain silver braid on the cuffs and small silver buttons, a white linen cravat; no gold, no red")
KEEP = "EXACTLY the same young man as in the FIRST and SECOND reference images: the same face, eyes, brows, nose, ears, freckles and age; do not change them. "
BASE = "Vertical 9:16 photo, soft even natural light in a pale gilded palace corridor with a plain warm-grey wall behind him, photorealistic, real skin texture with visible pores. No text, no hands over the face. "
SC = {
 "a1_left34": "Head and shoulders, turned three-quarters to HIS left (we see his right cheek), looking at the lens, neutral.",
 "a2_right34": "Head and shoulders, turned three-quarters to HIS right (we see his left cheek), looking at the lens, neutral.",
 "a3_profile_left": "Head and shoulders in strict profile facing the left of the frame, the snub nose and the sticking-out ear clearly visible, neutral.",
 "a4_profile_right": "Head and shoulders in strict profile facing the right of the frame, the snub nose and the sticking-out ear clearly visible, neutral.",
 "a5_back": "Seen from behind, head and shoulders: the back of the powdered wig with the black ribbon at the nape, the blue coat, one ear visible, head slightly turned.",
 "a6_from_below": "Low camera angle looking up at him, head and shoulders, he looks down at the lens with a worried look.",
 "a7_from_above": "High camera angle looking down at him, head and shoulders, he looks up at the lens with big eyes.",
 "a8_bow_side": "Upper body seen from the side, bowing deeply from the waist, face turned toward the lens, anxious.",
 "e1_neutral": "Close front portrait, head and shoulders, neutral calm face, looking at the lens.",
 "e2_worried": "Close front portrait, head and shoulders, a worried frown, eyebrows pulled together, lips pressed.",
 "e3_alarmed": "Close front portrait, head and shoulders, alarmed, eyes wide, mouth open to cry out.",
 "e4_apologetic": "Close front portrait, head and shoulders, apologetic, head slightly lowered, eyes looking up from under the brows, a small wince.",
 "e5_eager": "Close front portrait, head and shoulders, eager and out of breath, eyebrows raised, mouth slightly open as if announcing something.",
 "e6_timid": "Close front portrait, head and shoulders, timid, eyes lowered, trying to speak, lips slightly parted.",
 "e7_terrified": "Close front portrait, head and shoulders, terrified, eyes very wide, mouth tight, a flinch as if someone shouted his name.",
 "e8_relieved": "Close front portrait, head and shoulders, relieved, a shy small smile, shoulders relaxed.",
}
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


def one(k):
    refs = [host(MC + "marcel_front.jpg"), host(MC + "marcel_three_quarter.jpg")]
    body = {"model": "nano-banana-2.1", "prompt": BASE + SC[k] + f" {FACE.capitalize()}, wearing {LIVERY}. " + KEEP, "aspect_ratio": "9:16", "quality": "2K", "image_urls": refs}
    r = apipod.submit("images", body)
    if "data" not in r: print(k, "SUBMIT FAILED", str(r)[:300]); return
    tid = r["data"]["task_id"]; out = MC + f"sheet_{k}.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=400, every=4)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {})
    if u: apipod.download(u, out)
    print(k, "cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")


ids = sys.argv[1:] or list(SC)
sem = threading.Semaphore(4)


def run(i):
    with sem: one(i)


ts = [threading.Thread(target=run, args=(i,)) for i in ids]
[t.start() for t in ts]; [t.join() for t in ts]
