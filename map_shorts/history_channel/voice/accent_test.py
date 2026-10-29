"""French-accent voice test for the history channel (owner 29.10: the king must have a French accent).
Same lines as the ep.1 emotion test (C01-C05, tagged, from lines_ep1_emotion.json), ElevenLabs via Lumean.
Usage: python3 accent_test.py preview [names]   (free: price only)
       python3 accent_test.py go [names]        (PAID: one Lumean order per name, about 0.23-0.4 RUB each; needs the owner's yes)
The key is read from .lumean_key (never printed, never committed)."""
import json, os, sys, time, urllib.request

KEYFILES = ["/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/.lumean_key", "/home/user/beauty-reels-bot/.lumean_key", "/home/claude/v51/.lumean_key", "/home/claude/v34/.lumean_key"]
KEY = next(open(p).read().strip() for p in KEYFILES if os.path.exists(p))
BASE = "https://api.lumean.app/api/public"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audition_accent") + "/"
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


cand = {v["name"].split(" - ")[0].split()[0].lower(): v for v in json.load(open(os.path.join(HERE, "french_candidates.json")))}
VOICES = {  # name: (voice_id, public_owner_id, text prefix)
    "heir_tag": ("AqRCwHAjbeFmvSwJvHll", "779d91788b0d9e364d32e0a0e4273ec722b92887fa710d82f50b2d034a9fb97b", "[strong French accent] "),
}
for k in ("marcel", "antonin", "cyril", "jamie", "nicolas", "henri"):
    v = cand[k]
    VOICES[k] = (v["voice_id"], v["public_owner_id"], "")
lines = json.load(open(os.path.join(HERE, "lines_ep1_emotion.json")))["lines"]
BODY = " ".join(lines[c] for c in ("C01", "C02", "C03", "C04", "C05"))
MODEL = os.environ.get("EL_MODEL", "eleven_v4")
tpl = next(t["id"] for t in api("GET", "/templates") if t["service_key"] == "elevenlabs")
mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
names = sys.argv[2:] or list(VOICES)
orders = {}
for n in names:
    vid, owner, pre = VOICES[n]
    text = pre + BODY
    ts = {"model_id": MODEL, "voice_id": vid, "language_code": "en", "advanced_voice_settings": True, "public_owner_id": owner,
          "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.5, "use_speaker_boost": True, "speed": 0.95}}
    body = {"template_id": tpl, "input_text": text, "config_override": {"tts_settings": ts}, "name": "louis accent test " + n + "_" + MODEL}
    pv = api("POST", "/orders/chunks/preview", {k: body[k] for k in ("template_id", "input_text")})
    print(n, len(text), "chars, cost RUB", pv["summary"]["cost_display"]["amounts"]["rub"]["amount_formatted"], flush=True)
    if mode == "go":
        orders[n] = api("POST", "/orders", body)["id"]
if mode == "go":
    for n, oid in orders.items():
        while True:
            o = api("GET", f"/orders/{oid}")
            if o["status"] in ("completed", "result_delivered", "partially_completed"):
                for p in o["result"]["files"]:
                    if p.endswith(".mp3"):
                        urllib.request.urlretrieve(api("POST", "/storage/url", {"path": p})["url"], OUT + n + "_" + MODEL + ".mp3")
                print(n, o["status"], flush=True); break
            if o["status"] in ("failed", "cancelled", "compensated"):
                print(n, "FAILED", o["status"], flush=True); break
            time.sleep(5)
