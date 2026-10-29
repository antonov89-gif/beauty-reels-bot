"""TTS with the LOCKED history-channel voice (voice_lock.json): one Lumean order per group of clip lines.
Usage: python3 tts_locked.py preview|go GROUP=C06,C07,... [GROUP=...]
Applies the lock's accent prefix and TTS-only respelling; the lines file keeps normal spelling. Output: tts_ep1/<first>-<last>.mp3
The key is read from .lumean_key (never printed, never committed)."""
import json, os, re, sys, time, urllib.request

KEYFILES = ["/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/.lumean_key", "/home/user/beauty-reels-bot/.lumean_key", "/home/claude/v51/.lumean_key", "/home/claude/v34/.lumean_key"]
KEY = next(open(p).read().strip() for p in KEYFILES if os.path.exists(p))
BASE = "https://api.lumean.app/api/public"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tts_ep1") + "/"
os.makedirs(OUT, exist_ok=True)


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


lock = json.load(open(os.path.join(HERE, "voice_lock.json")))
lines = json.load(open(os.path.join(HERE, "lines_ep1_emotion.json")))["lines"]


def tts_text(ids):
    t = lock["accent"]["text_prefix"] + " ".join(lines[c] for c in ids)
    for x, y in lock["accent"]["respelling_tts_only"]:
        t = re.sub(x, y, t)
    return t


mode = sys.argv[1]
groups = [a.split("=", 1)[1].split(",") for a in sys.argv[2:]]
tpl = next(t["id"] for t in api("GET", "/templates") if t["service_key"] == "elevenlabs")
ts = {"model_id": lock["model_id"], "voice_id": lock["voice_id"], "public_owner_id": lock["public_owner_id"], "language_code": lock["language_code"],
      "advanced_voice_settings": True, "voice_settings": lock["voice_settings"]}
orders = {}
for ids in groups:
    name = ids[0] + "-" + ids[-1]
    body = {"template_id": tpl, "input_text": tts_text(ids), "config_override": {"tts_settings": ts}, "name": "louis ep1 locked v3 " + name}
    pv = api("POST", "/orders/chunks/preview", {k: body[k] for k in ("template_id", "input_text")})
    print(name, len(body["input_text"]), "chars, cost RUB", pv["summary"]["cost_display"]["amounts"]["rub"]["amount_formatted"], flush=True)
    if mode == "go":
        orders[name] = api("POST", "/orders", body)["id"]
for name, oid in orders.items():
    while True:
        o = api("GET", f"/orders/{oid}")
        if o["status"] in ("completed", "result_delivered", "partially_completed"):
            for p in o["result"]["files"]:
                if p.endswith(".mp3"):
                    urllib.request.urlretrieve(api("POST", "/storage/url", {"path": p})["url"], OUT + name + ".mp3")
            print(name, o["status"], flush=True); break
        if o["status"] in ("failed", "cancelled", "compensated"):
            print(name, "FAILED", o["status"], flush=True); break
        time.sleep(5)
