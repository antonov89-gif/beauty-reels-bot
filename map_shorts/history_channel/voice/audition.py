"""Voice audition for the history channel's one-voice rule (owner 28.10: ONE voice on all videos; nasty, arrogant, haughty).
ElevenLabs v3 through Lumean (pay-as-you-go, min 500 billable chars per order). Voices = the ids already used by the account's Lumean templates.
Usage: python3 audition.py preview | go. The key is read from .lumean_key (never printed, never committed)."""
import json
import os
import sys
import time
import urllib.request

KEYFILES = ["/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/.lumean_key", "/home/user/beauty-reels-bot/.lumean_key", "/home/claude/v51/.lumean_key", "/home/claude/v34/.lumean_key"]
def _ok(k):
    try:
        urllib.request.urlopen(urllib.request.Request("https://api.lumean.app/api/public/templates", headers={"X-API-KEY": k, "Accept": "application/json"}), timeout=30)
        return True
    except Exception:
        return False


KEY = next(k for k in (open(p).read().strip() for p in KEYFILES if os.path.exists(p)) if _ok(k))
BASE = "https://api.lumean.app/api/public"


def api(m, p, b=None):
    r = urllib.request.Request(BASE + p, method=m, data=json.dumps(b).encode() if b is not None else None, headers={"X-API-KEY": KEY, "Accept": "application/json", "Content-Type": "application/json"})
    for a in range(4):
        try:
            d = json.load(urllib.request.urlopen(r, timeout=120)); break
        except urllib.error.HTTPError:
            raise
        except Exception:
            if a == 3:
                raise
            time.sleep(2 * 2 ** a)
    if not d.get("success"):
        raise RuntimeError(d)
    return d["data"]


VOICES = {  # name: (voice_id, public_owner_id or None)
    "arthur": ("3nMIMZ7RlGwsq1WLgxY3", None),
    "george": ("jaJPMbicLce0HUswUo6w", None),
    "jon": ("MFZUKuGQUsGJPQjTS4wC", "b45c1524a1"),
    "adam": ("eGSd0uV8dNQnZuEEX9lu", None),
    "david": ("cCYjmrGZaI86GUJ7F2Nn", "fd99b11504e8c1aac6e847ea61616cd450db4e2b1b8aaa196c35d58c85fd9f28"),
    "std": ("O25OBJSCm417f6WHn13t", "64cbc624eb"),
}
TEXT = ("[smug] Marcel, down! [haughty] Bow. Lower. Good. Welcome to Versailles. [admiringly] Yes, I am that handsome. [sneering] Try not to faint. "
        "[smug] A hundred people watch me wake up. The French call it the lever. I call it a premiere. [admiringly] Look at me. Magnificent. [arrogant] The sun is never late.")
OUT = "/home/user/beauty-reels-bot/map_shorts/history_channel/voice/audition/"
os.makedirs(OUT, exist_ok=True)
tpl = next(t["id"] for t in api("GET", "/templates") if t["service_key"] == "elevenlabs")
mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
names = sys.argv[2:] or list(VOICES)
orders = {}
for n in names:
    vid, owner = VOICES[n]
    ts = {"model_id": "eleven_v3", "voice_id": vid, "language_code": "en", "advanced_voice_settings": True,
          "voice_settings": {"stability": 0.3, "similarity_boost": 0.75, "style": 0.5, "use_speaker_boost": True, "speed": 0.95}}
    if owner and len(owner) > 20:
        ts["public_owner_id"] = owner
    body = {"template_id": tpl, "input_text": TEXT, "config_override": {"tts_settings": ts}, "name": "louis voice audition " + n}
    pv = api("POST", "/orders/chunks/preview", {k: body[k] for k in ("template_id", "input_text")})
    print(n, "cost RUB", pv["summary"]["cost_display"]["amounts"]["rub"]["amount_formatted"], flush=True)
    if mode == "go":
        oid = None
        for o in api("GET", "/orders"):
            if isinstance(o, dict) and o.get("name") == body["name"]:
                oid = o["id"]; break
        if not oid:
            oid = api("POST", "/orders", body)["id"]
        orders[n] = oid
if mode == "go":
    for n, oid in orders.items():
        while True:
            o = api("GET", f"/orders/{oid}")
            if o["status"] in ("completed", "result_delivered", "partially_completed"):
                for p in o["result"]["files"]:
                    if p.endswith(".mp3"):
                        urllib.request.urlretrieve(api("POST", "/storage/url", {"path": p})["url"], OUT + n + ".mp3")
                print(n, o["status"], os.listdir(OUT), flush=True); break
            if o["status"] in ("failed", "cancelled", "compensated"):
                print(n, "FAILED", o["status"], flush=True); break
            time.sleep(5)
