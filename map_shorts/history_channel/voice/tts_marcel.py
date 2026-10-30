"""Marcel the page voice (marcel_card/README.md): ElevenLabs via Lumean, one order for his short lines. Voice from voice/page_voice_shortlist.json (default 1 = Edward, French, young).
Usage: python3 tts_marcel.py preview|go [voice_number]. Output: tts_ep1/marcel_v<N>.mp3 (all lines with 1.2 s of silence between). Key from .lumean_key (never printed).
Lines: "The court, Sire." (C07) | "Pardon, Sire!" (C09) | "Sire, I only..." (C13). He is a nervous young page: eager, anxious, a step late."""
import json, os, sys, time, urllib.request
mode = sys.argv[1]; num = int(sys.argv[2]) if len(sys.argv) > 2 else 1
sys.argv = ["x", "none"]; __file__ = os.path.abspath("tts_locked.py")
exec(open("tts_locked.py").read().split("lock = json.load")[0])
sl = json.load(open(os.path.join(HERE, "page_voice_shortlist.json")))
row = next(r for r in sl if r[0] == num); vid, owner = row[5], row[6]
text = ("[eager, slightly out of breath, announcing] The court, Sire. {{pause=1.2}} [alarmed, apologetic, panicking] Pardon, Sire! {{pause=1.2}} [timid, trying to explain, trailing off] Sire, I only...")
tpl = next(t["id"] for t in api("GET", "/templates") if t["service_key"] == "elevenlabs")
ts = {"model_id": "eleven_v4", "voice_id": vid, "public_owner_id": owner, "language_code": "en", "advanced_voice_settings": True,
      "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.5, "use_speaker_boost": True, "speed": 1.0}}
body = {"template_id": tpl, "input_text": text, "config_override": {"tts_settings": ts}, "name": f"marcel page v{num}"}
pv = api("POST", "/orders/chunks/preview", {k: body[k] for k in ("template_id", "input_text")})
print("voice", num, row[1], "| cost RUB", pv["summary"]["cost_display"]["amounts"]["rub"]["amount_formatted"], flush=True)
if mode == "go":
    oid = api("POST", "/orders", body)["id"]
    while True:
        o = api("GET", f"/orders/{oid}")
        if o["status"] in ("completed", "result_delivered", "partially_completed"):
            for p in o["result"]["files"]:
                if p.endswith(".mp3"): urllib.request.urlretrieve(api("POST", "/storage/url", {"path": p})["url"], OUT + f"marcel_v{num}.mp3")
            print("done", o["status"]); break
        if o["status"] in ("failed", "cancelled", "compensated"): print("FAILED", o["status"]); break
        time.sleep(4)
