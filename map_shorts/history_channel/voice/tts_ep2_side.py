"""Ep.2 side voices (AI voices, disclosed): Marcel = shortlist voice 1 (Edward, French young), the cupbearer = shortlist voice 4 (Christopher, British narration).
Usage: python3 tts_ep2_side.py preview|go. Lines from lines_ep2_emotion.json ("marcel", "cupbearer"), joined with 2-s pauses. Output tts_ep2/marcel.mp3, tts_ep2/cupbearer.mp3. PAID on 'go'."""
import json, os, sys, time, urllib.request
mode = sys.argv[1]
sys.argv = ["x", "none"]; __file__ = os.path.abspath("tts_locked.py")
exec(open("tts_locked.py").read().split("lock = json.load")[0])
OUT = os.path.join(HERE, "tts_ep2") + "/"
L = json.load(open(os.path.join(HERE, "lines_ep2_emotion.json")))
sl = json.load(open(os.path.join(HERE, "page_voice_shortlist.json")))
tpl = next(t["id"] for t in api("GET", "/templates") if t["service_key"] == "elevenlabs")
for name, num, lines in (("marcel", 1, L["marcel"]), ("cupbearer", 4, L["cupbearer"])):
    row = next(r for r in sl if r[0] == num)
    text = " {{pause=2.0}} ".join(lines.values())
    ts = {"model_id": "eleven_v4", "voice_id": row[5], "public_owner_id": row[6], "language_code": "en", "advanced_voice_settings": True,
          "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.5, "use_speaker_boost": True, "speed": 1.0}}
    body = {"template_id": tpl, "input_text": text, "config_override": {"tts_settings": ts}, "name": "louis ep2 " + name}
    pv = api("POST", "/orders/chunks/preview", {k: body[k] for k in ("template_id", "input_text")})
    print(name, row[1], len(text), "chars, RUB", pv["summary"]["cost_display"]["amounts"]["rub"]["amount_formatted"], flush=True)
    if mode == "go":
        oid = api("POST", "/orders", body)["id"]
        while True:
            o = api("GET", f"/orders/{oid}")
            if o["status"] in ("completed", "result_delivered", "partially_completed"):
                for p in o["result"]["files"]:
                    if p.endswith(".mp3"): urllib.request.urlretrieve(api("POST", "/storage/url", {"path": p})["url"], OUT + name + ".mp3")
                print(name, o["status"], flush=True); break
            if o["status"] in ("failed", "cancelled", "compensated"): print(name, "FAILED", o["status"], flush=True); break
            time.sleep(4)
