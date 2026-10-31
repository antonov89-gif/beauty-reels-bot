"""Ep.2 set master v3: FACE FIX (owner 31.10 'Это ужас, переделай и проверь': v1/v2 faces were older, heavier, one eye droopy). Refs: face master first (owner 31.10: bigger wig, same face). Nano Banana Pro 4K 9:16 (about $0.12). PAID: runs after the owner's 'Сделай'.
Refs: master_table_4k.jpg (scene, face, coat: keep), tall_wig_ref.jpg (the wig). Output louis_ep2/frames/master_table_v2_4k.jpg (+ .task_id, .status.json)."""
import json, re, sys, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
FM = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_card/face_master_v3/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip(); H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
FACE = "a man of about 35 with a pale complexion, light grey-hazel eyes, a long straight nose, a narrow face, a thin upturned waxed moustache, arched brows and a small dark beauty spot beside the mouth"
def host(path):
    n = path.split("/")[-1]
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": n, "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
    return d["publicUrl"]
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
def host_file(path):
    n = path.split("/")[-1]
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": n, "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
    return d["publicUrl"]
prompt = ("Vertical 9:16 phone selfie photo, ultra-wide front camera look, hand-held, photorealistic, real skin texture with visible pores, no text, no modern objects. "
          "The man's face must be EXACTLY the face of the man in the FIRST and SECOND reference images: a young man of about 30 to 33, a narrow face with a lean jaw and no jowls, smooth forehead with no wrinkles, a long straight nose, "
          "BOTH eyes wide open, bright, symmetrical, light grey-hazel, looking straight into the lens, arched brows, a thin upturned waxed moustache, a small dark beauty spot beside the mouth. Alert, confident expression with a small smug smile of the mouth only: no heavy eyelids, no sleepy or squinting eye, no bags under the eyes. "
          "He wears the tall powdered grey-white wig from the THIRD reference image (towering swept-up front, rolled curls above the ears, long curls over both shoulders), pale white court powder on the face with a light natural pink flush on the cheeks, "
          "a scarlet velvet coat embroidered with gold suns, a white lace cravat with a white linen napkin tucked into it. "
          "Composition, room and crowd like the FOURTH reference image: he sits at the head of a very long dining table with a white cloth, gold plates and candelabra in a gilded antechamber of Versailles at night, his arm holding the phone at arm's length, a standing crowd of courtiers in plain simple wigs behind the table, ladies seated at the sides, painted ceiling, black windows, warm candlelight only. Only the king wears a tall wig and scarlet.")
refs = [host_file(FM + "face_front_talking.jpg"), host_file(FM + "face_three_quarter.jpg"), host_file(FM + "tall_wig_ref.jpg"), host_file("louis_ep2/frames/master_table_v2_1440.jpg")]
r = apipod.submit("images", {"model": "nano-banana-pro", "prompt": prompt, "aspect_ratio": "9:16", "quality": "4K", "image_urls": refs})
if "data" not in r: print("SUBMIT FAILED", r); sys.exit(1)
tid = r["data"]["task_id"]; out = "louis_ep2/frames/master_table_v3_4k.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=600, every=5)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
u = find(res.get("data") or {})
if u: apipod.download(u, out)
print("cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")
