import os, sys, time, urllib.request, json
sys.path.insert(0, "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad")
from lumean_api import api
sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/walk_it_01_alaska_patagonia"); import script as script
tpl = next(t["id"] for t in api("GET", "/templates") if t["service_key"] == "elevenlabs")
override = {"tts_settings": {"model_id": "eleven_multilingual_v2", "voice_id": "cCYjmrGZaI86GUJ7F2Nn", "public_owner_id": "fd99b11504e8c1aac6e847ea61616cd450db4e2b1b8aaa196c35d58c85fd9f28",
    "language_code": "en", "advanced_voice_settings": True,
    "voice_settings": {"stability": 0.55, "similarity_boost": 0.8, "style": 0.2, "use_speaker_boost": True, "speed": 1.08}}}
NAME = "walk it 01 v1"
text = " {{pause=0.3}} ".join(script.LINES)
# reuse an existing order with this name (protects against a double charge after a proxy reset)
oid = None
try:
    for o in api("GET", "/orders"):
        if isinstance(o, dict) and o.get("name") == NAME: oid = o["id"]; print("found existing order", flush=True); break
except Exception as e:
    print("list orders failed", e, flush=True)
if not oid:
    oid = api("POST", "/orders", {"template_id": tpl, "input_text": text, "config_override": override, "name": NAME})["id"]
    print("submitted", flush=True)
open("/home/claude/v83/wk/order_id.txt", "w").write(str(oid))
while True:
    time.sleep(6)
    try:
        o = api("GET", f"/orders/{oid}")
    except Exception as e:
        print("poll error", e, flush=True); continue
    if o["status"] in ("completed", "result_delivered", "partially_completed"):
        d = "/home/claude/v83/wk/lumean"; os.makedirs(d, exist_ok=True)
        res = o["result"]
        for p in res["files"] + res["service_files"]:
            if p.endswith((".mp3", "alignment.csv", "result.json", ".srt")):
                u = api("POST", "/storage/url", {"path": p})["url"]
                urllib.request.urlretrieve(u, d + "/" + os.path.basename(p))
        print("done", o["status"], sorted(os.listdir(d)), "cost", o.get("cost") or o.get("price"), flush=True); break
    if o["status"] in ("failed", "cancelled", "compensated"):
        print("FAILED", o["status"], flush=True); break
