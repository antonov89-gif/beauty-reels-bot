"""Ep.2 king sheet TEST (owner 04.11 'Делаю тест'): picture a1 at 4K on two models, reference R1 (A3 white wig) via the public raw GitHub URL. PAID: about $0.05 + up to $0.12. One call per model, no retries."""
import json, re, sys, threading
sys.path.insert(0, "/home/claude/v51")
import apipod
REF = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/R1_king_card_A3_white_wig.jpg"
md = open("king_sheet_prompts.md").read()
prompt = md.split("## A1 ")[1].split("Prompt:\n")[1].split("\n## ")[0].strip()
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
def run(tag, body):
    r = apipod.submit("images", body)
    if "data" not in r: print(tag, "SUBMIT FAILED", json.dumps(r)[:300]); return
    tid = r["data"]["task_id"]; out = f"sheet/a1_{tag}.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=600, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {})
    if u: apipod.download(u, out)
    print(tag, "cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL", (res.get("data") or {}).get("status"))
jobs = {"nb21_4k": {"model": "nano-banana-2.1", "prompt": prompt, "aspect_ratio": "9:16", "quality": "4K", "image_urls": [REF]},
        "gpt25_sunburst_lite_4k": {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high", "image_urls": [REF]}}
ts = [threading.Thread(target=run, args=(k, v)) for k, v in jobs.items()]
[t.start() for t in ts]; [t.join() for t in ts]
