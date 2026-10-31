"""Dub voice for episode 1 in another language with the SAME locked voice (voice_lock.json: ElevenLabs v4 "The Young Heir" via Lumean), one Lumean order per language.
Lines: lines_ep1_dub.json (<lang> -> clip -> line). Clips are joined with a 2-s pause so the result can be split per clip later (split_dub.py). FR: native French, no accent tag; ES/RU: "[thick French accent]" prefix.
Usage: python3 tts_dub.py preview|go fr|es|ru  -> tts_ep1/dub_<lang>.mp3. "preview" is free (price only); "go" places a PAID order: only after the owner's yes with the price.
The key is read from .lumean_key (never printed, never committed)."""
import json, os, sys, time, urllib.request
KEYFILES = ["/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/.lumean_key", "/home/user/beauty-reels-bot/.lumean_key", "/home/claude/v51/.lumean_key"]
KEY = next(open(p).read().strip() for p in KEYFILES if os.path.exists(p))
BASE = "https://api.lumean.app/api/public"; HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "tts_ep1") + "/"
CLIPS = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C12", "C13", "C14", "C15"]


def api(m, p, b=None):
    r = urllib.request.Request(BASE + p, method=m, data=json.dumps(b).encode() if b is not None else None, headers={"X-API-KEY": KEY, "Accept": "application/json", "Content-Type": "application/json"})
    for a in range(4):
        try:
            d = json.load(urllib.request.urlopen(r, timeout=120)); break
        except urllib.error.HTTPError as e:
            print("HTTP", e.code, e.read().decode()[:600], flush=True); raise
        except Exception:
            if a == 3: raise
            time.sleep(2 * 2 ** a)
    if not d.get("success"): raise RuntimeError(d)
    return d["data"]


mode, lang = sys.argv[1], sys.argv[2]
lock = json.load(open(os.path.join(HERE, "voice_lock.json"))); lines = json.load(open(os.path.join(HERE, "lines_ep1_dub.json")))[lang]
prefix = "" if lang == "fr" else lock["accent"]["text_prefix"]
text = prefix + " {{pause=2.0}} ".join(lines[c] for c in CLIPS)
tpl = next(t["id"] for t in api("GET", "/templates") if t["service_key"] == "elevenlabs")
ts = {"model_id": lock["model_id"], "voice_id": lock["voice_id"], "public_owner_id": lock["public_owner_id"], "language_code": lang,
      "advanced_voice_settings": True, "voice_settings": lock["voice_settings"]}
body = {"template_id": tpl, "input_text": text, "config_override": {"tts_settings": ts}, "name": f"louis ep1 dub {lang}"}
pv = api("POST", "/orders/chunks/preview", {k: body[k] for k in ("template_id", "input_text")})
print(lang, len(text), "chars, cost RUB", pv["summary"]["cost_display"]["amounts"]["rub"]["amount_formatted"], flush=True)
if mode == "go":
    oid = api("POST", "/orders", body)["id"]
    while True:
        o = api("GET", f"/orders/{oid}")
        if o["status"] in ("completed", "result_delivered", "partially_completed"):
            for p in o["result"]["files"]:
                if p.endswith(".mp3"): urllib.request.urlretrieve(api("POST", "/storage/url", {"path": p})["url"], OUT + f"dub_{lang}.mp3")
            print(lang, o["status"], flush=True); break
        if o["status"] in ("failed", "cancelled", "compensated"):
            print(lang, "FAILED", o["status"], flush=True); break
        time.sleep(5)
