import json, os, sys, time, urllib.request, csv, re
from script10 import LINES, CONT
KEY = open(".lumean_key").read().strip()
BASE = "https://api.lumean.app/api/public"
def api(m, p, b=None):
    r = urllib.request.Request(BASE + p, method=m, data=json.dumps(b).encode() if b is not None else None,
        headers={"X-API-KEY": KEY, "Accept": "application/json", "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(r, timeout=90))
    if not d.get("success"): raise RuntimeError(d)
    return d["data"]
tpl = next(t["id"] for t in api("GET", "/templates") if t["service_key"] == "elevenlabs")
override = {"tts_settings": {"model_id": "eleven_multilingual_v2", "voice_id": "cCYjmrGZaI86GUJ7F2Nn",
    "public_owner_id": "fd99b11504e8c1aac6e847ea61616cd450db4e2b1b8aaa196c35d58c85fd9f28",
    "language_code": "en", "advanced_voice_settings": True,
    "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True, "speed": 1.05}}}
parts = []
for i, l in enumerate(LINES):
    parts.append(l)
    if i < len(LINES) - 1:
        parts.append("{{pause=0.25}}" if (i + 1) in CONT else "{{pause=0.45}}")
text = " ".join(parts)
body = {"template_id": tpl, "input_text": text, "config_override": override, "name": "italy ww2 v2"}
pv = api("POST", "/orders/chunks/preview", {k: body[k] for k in ("template_id", "input_text")})
print("cost RUB", pv["summary"]["cost_display"]["amounts"]["rub"]["amount_formatted"]); sys.stdout.flush()
if len(sys.argv) > 1 and sys.argv[1] == "go":
    o = api("POST", "/orders", body)
    while o["status"] not in ("completed", "result_delivered", "failed", "cancelled", "compensated", "partially_completed"):
        time.sleep(5); o = api("GET", f"/orders/{o['id']}")
    print(o["status"], o["id"])
    res = o["result"]
    os.makedirs("lumean", exist_ok=True)
    for p in res["files"] + res["service_files"]:
        if p.endswith((".mp3", "alignment.csv", "result.json", ".srt")):
            u = api("POST", "/storage/url", {"path": p})["url"]
            urllib.request.urlretrieve(u, "lumean/" + os.path.basename(p))
    print(os.listdir("lumean"))
