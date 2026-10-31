"""Ep.2 set master v4: HAUGHTY face from the owner's C08 frame (owner 31.10 'Лицо не надменное, плохое качество'; yes to $0.12). Earlier: v3 FACE FIX (owner 31.10 'Это ужас, переделай и проверь': v1/v2 faces were older, heavier, one eye droopy). Refs: face master first (owner 31.10: bigger wig, same face). Nano Banana Pro 4K 9:16 (about $0.12). PAID: runs after the owner's 'Сделай'.
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
prompt = ("Vertical 9:16 phone selfie photo, ultra-wide front camera look, hand-held, photorealistic, a real photograph with fine film grain, NOT retouched: matte powdered skin with visible pores, fine lines and natural unevenness, no skin smoothing, no beauty filter, no waxy or plastic look. No text, no modern objects. "
          "The man is the SAME man as in the FIRST reference image (the left panel C08): same face, same grey eyes, the same upturned waxed moustache, the same beauty spot beside the mouth. Copy his HAUGHTY expression exactly: heavy upper eyelids, a disdainful gaze looking DOWN his nose at the lens, chin tilted slightly back, one eyebrow a little raised, lips closed in a contemptuous half-smile; not smiling warmly, eyes NOT wide open. Both eyes symmetrical. "
          "His wig is the tall grey-white wavy pompadour with rolled curls above the ears from the FIRST reference image, with the long curls over both shoulders down to the chest as in the SECOND reference image (the right panel C09). White court powder and a light pink flush on the cheeks as in the first reference. "
          "He wears a scarlet velvet coat embroidered with gold suns, a white lace cravat with a white linen napkin tucked in. "
          "Composition, room and crowd like the THIRD reference image: he sits at the head of a very long dining table with a white cloth, gold plates and candelabra in a gilded antechamber of Versailles at night, his arm holding the phone at arm's length, a standing crowd of courtiers in plain simple wigs behind the table, ladies seated at the sides, painted ceiling, black windows, warm candlelight only. Only the king wears a tall wig and scarlet.")
refs = [host_file("louis_ep2/frames/owner_C08_panel.jpg"), host_file("louis_ep2/frames/owner_C09_panel.jpg"), host_file("louis_ep2/frames/master_table_v3_1440.jpg")]
r = apipod.submit("images", {"model": "nano-banana-pro", "prompt": prompt, "aspect_ratio": "9:16", "quality": "4K", "image_urls": refs})
if "data" not in r: print("SUBMIT FAILED", r); sys.exit(1)
tid = r["data"]["task_id"]; out = "louis_ep2/frames/master_table_v4_4k.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=600, every=5)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
u = find(res.get("data") or {})
if u: apipod.download(u, out)
print("cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")
