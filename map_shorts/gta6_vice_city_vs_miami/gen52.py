import apipod, json, re, sys, os, concurrent.futures as cf
src = open("/home/user/beauty-reels-bot/map_shorts/gta6_vice_city_vs_miami/prompts.md").read()
style = src.split("## STYLE LOCK")[1].split("\n", 1)[1].split("\n\n")[0].strip()
FALLBACK = "In-engine screenshot from a 2026 next-gen open-world crime game trailer, photoreal RAGE-like engine look, set in a fictional Vice City (modern Miami, Florida)."
style_safe = FALLBACK + style[style.index(" Ultra-detailed"):]
neg = " Avoid: " + src.split("## NEGATIVE")[1].split("\n", 1)[1].split("\n\n")[0].strip() + "."
frames_part = src.split("## Frames (16:9)")[1].split("## Animation prompts")[0]
anim_part = src.split("## Animation prompts")[1]
F = dict(re.findall(r"- \*\*(V\d+)\*\*: (.+)", frames_part))
A = dict(re.findall(r"- \*\*(V\d+)\*\*: (.+)", anim_part))
SUFFIX = " Rockstar trailer camera, smooth realistic motion, natural physics, no cuts, no text, no logos."
os.makedirs("ai", exist_ok=True)
state = json.load(open("ai/state.json")) if os.path.exists("ai/state.json") else {}
def save(): json.dump(state, open("ai/state.json", "w"), indent=1)
def frame(k):
    for st in (style, style_safe):
        r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": st + " " + F[k] + neg, "aspect_ratio": "16:9", "quality": "2K"})
        if "data" not in r: print(k, "submit err", str(r)[:200]); continue
        w = apipod.wait("images", r["data"]["task_id"], timeout=600, every=5)
        d = w.get("data") or {}
        if d.get("status") == "completed":
            u = d["result"][0]; u = u if isinstance(u, str) else u.get("url")
            apipod.download(u, f"ai/{k}.jpg"); return k, u, st is style_safe
        print(k, "failed", str(w)[:200])
    return k, None, None
def video(k):
    r = apipod.submit("videos", {"model": "veo3-1-fast", "prompt": "Animate this exact frame, keep composition, style and every object. " + A[k] + SUFFIX, "image_urls": [state[k]["img"]], "aspect_ratio": "16:9"})
    if "data" not in r: return k, None, str(r)[:200]
    w = apipod.wait("videos", r["data"]["task_id"], timeout=1500, every=10)
    d = w.get("data") or {}
    if d.get("status") != "completed": return k, None, str(w)[:200]
    u = d["result"][0]; u = u if isinstance(u, str) else u.get("url")
    apipod.download(u, f"ai/{k}.mp4"); return k, u, ""
mode = sys.argv[1]; keys = sys.argv[2:] or sorted(F, key=lambda s: int(s[1:]))
print(len(F), len(A), "keys", keys)
with cf.ThreadPoolExecutor(4) as ex:
    if mode == "frames":
        for k, u, safe in ex.map(frame, keys):
            print(k, "ok" if u else "FAIL", "(safe style)" if safe else ""); 
            if u: state.setdefault(k, {})["img"] = u; save()
    else:
        for k, u, err in ex.map(video, keys):
            print(k, "ok" if u else "FAIL " + err)
            if u: state[k]["vid"] = u; save()
