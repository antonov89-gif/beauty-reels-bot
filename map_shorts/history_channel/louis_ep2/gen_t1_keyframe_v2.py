"""T1 identity keyframe (owner 04.11 "ок", v2: younger face): GPT Image 2.5 Sunburst Lite, 4K, quality high, 9:16, refs R1 (A3) + K_E1. One call, about $0.12, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Vertical 9:16 hand-held phone photo, ultra-wide front camera look, slightly underexposed, a real photograph with fine film grain, matte skin with pores, photorealistic, no retouching, no beauty filter. "
"The FIRST reference image decides the face; the SECOND reference is a tight crop of the same face: match its age exactly (a man of about 40, firm jawline, no jowls, no bags under the eyes, no heavy cheeks), do not copy its crop or background. "
"Selfie at the head of the long table: the king (the king from the FIRST reference image: exactly the same man and the same costume - his face, heavy-lidded eyes, thin upturned waxed moustache, small beauty mark beside the mouth, light rouge; the tall white-grey powdered wig with a high swept-up front and long curls falling over both shoulders; the scarlet velvet coat embroidered with gold suns, white lace cravat and lace cuffs, jewelled rings; a real documentary photo with visible pores, fine lines and natural matte skin) sits up straight, chin slightly raised, mouth open mid-word as if speaking, haughty and grand. "
"Setting: a very long dining table with a white cloth, gold plates and candelabra with lit candles, in a gilded antechamber of Versailles at night: painted ceiling at the top edge, tall black windows, warm candlelight only, deep soft shadows; behind the table a standing crowd of courtiers in plain simple wigs and dark period clothes (no tall wigs, no scarlet on anyone but the king); in the front row four or five ladies seated on folding stools. "
"No text, no captions, no logos, no interface, no modern objects, no extra fingers, no clown or mime makeup, no white mask face, no smooth plastic skin, no wide-open staring eyes, no dark wig, no blond or cream wig (the wig is always the tall white-grey one).")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg", RAW + "K_A3_face_crop.jpg"]}
r = apipod.submit("images", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted")
out = "pilot_frames/T1_keyframe_gen_v2_4k.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=600, every=5)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
u = find(res.get("data") or {}); d = res.get("data") or {}
print("status", d.get("status"), "usage", d.get("usage"))
if u: apipod.download(u, out); print("saved")
