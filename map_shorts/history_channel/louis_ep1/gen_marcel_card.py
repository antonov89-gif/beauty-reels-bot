"""Marcel the page: character card images (Nano Banana 2.1, 2K, about $0.04 each, 3 = about $0.12). PAID: runs only after the owner's yes.
No reference photo of Marcel exists yet, so the first image (front) is generated from text alone with the king's frame as a STYLE/LIGHT reference only (a different man); images 2 and 3 use image 1 as the face reference.
Usage: python3 gen_marcel_card.py front | three_quarter | full   (one image per call, one yes per image or one yes for all three)"""
import json, re, sys, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip(); H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
FACE = ("a slim young man of about 18 with a round, open, slightly freckled face, a short snub nose, large dark brown eyes with a worried look, thick straight dark eyebrows, a small chin, ears that stick out a little, no moustache, a smooth boyish complexion with a natural light flush")
LIVERY = ("a plain short white-powdered wig tied at the nape with a black ribbon, a sky-blue wool coat with plain silver braid on the cuffs and a row of small silver buttons, a white linen cravat, white stockings and black buckled shoes; no gold, no red")
BASE = "Vertical 9:16 phone photo, ultra-wide front camera look, soft natural window light in a gilded palace room, photorealistic, real skin texture with visible pores. No text, no modern objects. "
SC = {"front": f"Close front portrait, shoulders and head, looking straight into the lens with a worried, eager look. {FACE.capitalize()}, wearing {LIVERY}.",
      "three_quarter": f"Head and shoulders in a TRUE three-quarter view: the whole head and body turned 45 degrees to HIS left, so we see his right cheek and his right ear fully while the far cheek and far ear are partly hidden, the nose pointing clearly to the side of the frame, his eyes turned back toward the lens with a worried look. {FACE.capitalize()}, wearing {LIVERY}. EXACTLY the same face as the first reference image.",
      "full": f"Full-length standing figure in a gilded palace corridor, holding a large plumed black hat in both hands in front of him, anxious posture. {FACE.capitalize()}, wearing {LIVERY}. EXACTLY the same face as the first reference image."}


def host(path):
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": path.split("/")[-1], "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
    return d["publicUrl"]


def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u


k = sys.argv[1]; refs = []
if k == "front": refs = [host(H0 + "louis_ep1/frames/C07_v7.jpg")]
else: refs = [host(H0 + "marcel_card/marcel_front.jpg")]
extra = " The room, light and period look like the reference image, but he is a DIFFERENT, much younger and plainer man: ignore the face, wig and costume in the reference." if k == "front" else ""
body = {"model": "nano-banana-2.1", "prompt": BASE + SC[k] + extra, "aspect_ratio": "9:16", "quality": "2K", "image_urls": refs}
r = apipod.submit("images", body)
if "data" not in r: sys.exit("SUBMIT FAILED " + json.dumps(r)[:400])
tid = r["data"]["task_id"]; out = H0 + f"marcel_card/marcel_{k}.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=400, every=4)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
u = find(res.get("data") or {})
if u: apipod.download(u, out)
print(k, "cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")
