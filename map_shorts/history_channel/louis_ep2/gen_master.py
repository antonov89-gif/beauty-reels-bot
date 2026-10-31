"""Ep.2 set master frame: Nano Banana Pro 4K 9:16 (about $0.12). PAID: runs only after the owner's yes (31.10 'Да да').
Refs in order: face_front_talking.jpg, face_three_quarter.jpg, tall_wig_ref.jpg, makeup_ref_C09v6.jpg. Output louis_ep2/frames/master_table_4k.jpg (+ .task_id, .status.json)."""
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
prompt = ("Vertical 9:16 phone selfie photo, ultra-wide front camera look, hand-held, slightly underexposed, real skin texture with visible pores, photorealistic, no text, no modern objects. "
          f"{FACE.capitalize()}, exactly the same face as the man in the FIRST and SECOND reference images (same eyes, nose, moustache, age about 35; do not make him older). "
          "He wears the tall white-powdered wig from the THIRD reference image, the heavy white-pink court makeup and rouged cheeks like the FOURTH reference image, a scarlet velvet coat embroidered with gold suns, a white lace cravat with a white napkin tucked into it. "
          "He sits at the head of a very long dining table with a white cloth, gold plates, candelabra with lit candles, in a gilded antechamber of Versailles at night, painted ceiling at the top edge, tall black windows. "
          "His own arm holds the phone at arm's length, his face fills the lower middle of the frame with a smug half-smile, looking into the lens. "
          "Behind him and along the table a standing crowd of courtiers in plain simple wigs and dark period clothes watches him eat, and in the front row sit four or five ladies on folding stools. "
          "Warm candlelight only, deep soft shadows, no daylight. Only the king wears a tall wig and scarlet; everybody else is plain.")
refs = [host(FM + n) for n in ("face_front_talking.jpg", "face_three_quarter.jpg", "tall_wig_ref.jpg", "makeup_ref_C09v6.jpg")]
r = apipod.submit("images", {"model": "nano-banana-pro", "prompt": prompt, "aspect_ratio": "9:16", "quality": "4K", "image_urls": refs})
if "data" not in r: print("SUBMIT FAILED", r); sys.exit(1)
tid = r["data"]["task_id"]; out = "louis_ep2/frames/master_table_4k.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=600, every=5)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
u = find(res.get("data") or {})
if u: apipod.download(u, out)
print("cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")
