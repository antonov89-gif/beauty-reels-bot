"""Builds gen_take_<key>_seedance.py (Seedance 2.5 Lite i2v, 720p, 9:16, audio off, first + last frame pins) from the Kling script gen_take_<key>.py of the same piece. Usage: python3 make_seedance_script.py t4bA [first_image] [last_image]  (images default to <key>_start_4k.jpg / <key>_end_4k.jpg in refs/; piece B starts from t4bA_end_4k.jpg)"""
import re, json, sys
key = sys.argv[1]; H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
first = sys.argv[2] if len(sys.argv) > 2 else key + "_start_4k.jpg"; last = sys.argv[3] if len(sys.argv) > 3 else key + "_end_4k.jpg"
src = open(H0 + "gen_take_%s.py" % key).read()
sec = int(re.search(r'"duration":\s*(\d+)', src).group(1)); brief = re.search(r'BRIEF:\s*(\S+)', src).group(1)
m = re.search(r'prompt = \((.*?)\)\n', src, re.S)
t = "".join(json.loads(x) for x in re.findall(r'("(?:[^"\\]|\\.)*")', m.group(1)))
t = t.replace("@first_frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. ", "The first frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. ")
t = t.replace("as @first_frame:", "as in the first frame:").replace("@last_frame", "the last frame").replace("@first_frame", "the first frame")
assert "@" not in t
out = '"""Take %s CLIP on Seedance 2.5 LITE i2v (owner 07.11: Seedance 2.5 Lite): image_urls[0] = first frame, [1] = last-frame constraint (APIpod spec seedance--2-5-lite-image-to-video), 720p only, %d s, $0.15/s = $%.2f, audio off (the model audio is always muted). Same prompt as gen_take_%s.py (Kling) with the tag wording changed. One call, no retries without a new yes. Run: python3 gen_take_%s_seedance.py go\nBRIEF: %s\n"""\n' % (key, sec, 0.15 * sec, key, key, brief)
out += 'import json, re, sys\nsys.path.insert(0, "/home/claude/v51")\nimport apipod\nH0 = "%s"\nRAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"\nprompt = (\n' % H0
for c in re.split(r'(?<=[.;:]) ', t): out += '    ' + json.dumps(c + ' ') + '\n'
out += ')\nbody = {"model": "seedance-2.5-lite-i2v", "prompt": prompt, "image_urls": [RAW + "%s", RAW + "%s"],\n        "duration": %d, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": False}\n' % (first, last, sec)
out += '''open(H0 + "take_%s_seedance_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_%s_seedance.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_%s_seedance.status.json", "w").write(re.sub(r'(https://[^"?]+)\\\\?[^"]*', r'\\\\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_%s_seedance.mp4"); print("saved")
''' % (key, key, key, key)
open(H0 + "gen_take_%s_seedance.py" % key, "w").write(out); print(key, len(t), "chars", sec, "s")
