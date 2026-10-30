"""ElevenLabs Sound Effects via Lumean (owner "да" 30.10 for these 12 calls, about 0.05 RUB each). One order per sound, no retries.
Usage: python3 sfx_order.py preview|go [names...]. Output: sfx/<name>.mp3. Key from .lumean_key (never printed)."""
import json, os, sys, time, urllib.request
sys.argv_saved = list(sys.argv); sys.argv = ["x", "none"]; __file__x = __file__
HERE = os.path.dirname(os.path.abspath(__file__x))
exec(open(os.path.join(HERE, "../voice/tts_locked.py")).read().split("lock = json.load")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.path.join(HERE, "../voice"))))
sys.argv = sys.argv_saved
TPL = "01a174b4-c373-729f-ac36-71ce6314d758"
TAIL = " Recorded on the built-in microphone of a smartphone, realistic, no speech, no words, no music, no tones, no cinematic impacts."
SFX = {
 "handling_grip": (4, "Close-up phone handling noise: fingers shifting grip and rubbing on the body of a smartphone that is recording, thumb sliding over the microphone, small muffled scrapes and rubs, irregular."),
 "handling_knocks": (4, "A smartphone held in a hand while recording: small muffled knocks and taps of the phone body against a hand and a ring, two or three soft bumps, close and dry."),
 "phone_table": (5, "A smartphone recording itself is put down on an old wooden dressing table with a soft knock, a short pause, then picked up again with fingers rubbing on the phone, close."),
 "room_bedchamber": (10, "Room tone of a large quiet palace bedchamber in the morning, high painted ceiling, faint distant murmur of a few people standing by the walls, occasional soft shuffle of feet on parquet, very subtle."),
 "room_dressing": (10, "Room tone of a small quiet dressing room with a fireplace softly crackling, faint creak of a wooden chair, very subtle, intimate."),
 "room_court": (10, "A large ornate palace hall full of courtiers: low murmur of many quiet voices with no clear words, footsteps on parquet, rustle of heavy fabric, reverberant."),
 "court_enters": (6, "A heavy wooden palace door opens with a creak, several people walk in on a parquet floor, footsteps approaching and stopping, rustle of coats."),
 "silk_close": (4, "Rustle of a heavy silk brocade dressing gown and lace cuffs very close to the microphone as a man moves his arm, soft and detailed."),
 "court_bows": (5, "Several courtiers bowing deeply at once: rustle of heavy coats, swords and fabric, a creak of the wooden floor, quiet."),
 "wig_pat": (3, "A hand patting and touching a large powdered curly wig, soft hair rustle, a tiny puff of powder, close."),
 "wig_on_mic": (3, "Curly wig hair pressed against and rubbing over a phone microphone, muffled close rubbing and scratching."),
 "rings_clink": (3, "Several gold rings on fingers softly clinking together as a hand moves, delicate, close."),
}
mode = sys.argv[1]; names = sys.argv[2:] or list(SFX)
for nm in names:
    d, text = SFX[nm]; body = {"template_id": TPL, "input_text": text + TAIL,
                              "config_override": {"duration_seconds": d, "prompt_influence": 0.45, "loop": False, "output_format": "mp3_44100_192"}, "name": "louis ep1 sfx " + nm}
    pv = api("POST", "/orders/chunks/preview", {k: body[k] for k in ("template_id", "input_text")})
    print(nm, "cost RUB", pv["summary"]["cost_display"]["amounts"]["rub"]["amount_formatted"], flush=True)
    if mode != "go": continue
    oid = api("POST", "/orders", body)["id"]
    while True:
        o = api("GET", f"/orders/{oid}")
        if o["status"] in ("completed", "result_delivered", "partially_completed"):
            for p in o["result"]["files"]:
                if p.endswith(".mp3"): urllib.request.urlretrieve(api("POST", "/storage/url", {"path": p})["url"], os.path.join(HERE, nm + ".mp3"))
            print(nm, o["status"], flush=True); break
        if o["status"] in ("failed", "cancelled", "compensated"): print(nm, "FAILED", o["status"], flush=True); break
        time.sleep(4)
