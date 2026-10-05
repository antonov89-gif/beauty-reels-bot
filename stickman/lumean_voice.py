"""Voice the SCRIPT of make_video.py through Lumean (ElevenLabs TTS) in one order.

The whole script goes in one order (Lumean bills at least 500 chars per order),
with silent {{pause}} markers between scenes; the result is cut at those pauses
into scene01.wav ... scene10.wav for `make_video.py --voice-dir`.

Usage:  LUMEAN_API_KEY=... python3 lumean_voice.py [--template <uuid>] [--out voice_lumean]
"""
import argparse
import json
import os
import re
import subprocess
import time
import urllib.request

from make_video import SCRIPT

BASE = "https://api.lumean.app/api/public"
PAUSE = 1.2


def api(method, path, body=None):
    req = urllib.request.Request(
        BASE + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"X-API-KEY": os.environ["LUMEAN_API_KEY"], "Accept": "application/json",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    if not d.get("success"):
        raise RuntimeError(d.get("message"))
    return d["data"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", help="TTS template id (default: first elevenlabs template)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "voice_lumean"))
    a = ap.parse_args()

    tpl = a.template or next(t["id"] for t in api("GET", "/templates") if t["service_key"] == "elevenlabs")
    text = f" {{{{pause={PAUSE}}}}} ".join(line for line, _ in SCRIPT)
    cost = api("POST", "/orders/chunks/preview", {"template_id": tpl, "input_text": text})
    print("Cost:", cost["summary"]["cost_display"]["amounts"]["rub"]["amount_formatted"], "RUB")

    order = api("POST", "/orders", {"template_id": tpl, "input_text": text, "name": "stickman voiceover"})
    while order["status"] not in ("completed", "result_delivered", "failed", "cancelled", "compensated"):
        time.sleep(5)
        order = api("GET", f"/orders/{order['id']}")
    if order["status"] in ("failed", "cancelled", "compensated"):
        raise SystemExit(f"Order {order['id']} {order['status']}")

    os.makedirs(a.out, exist_ok=True)
    full = os.path.join(a.out, "full.mp3")
    url = api("POST", "/storage/url", {"path": order["result"]["files"][0]})["url"]
    urllib.request.urlretrieve(url, full)

    log = subprocess.run(["ffmpeg", "-i", full, "-af", "silencedetect=noise=-40dB:d=0.8", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    if len(ss) != len(SCRIPT) - 1:
        raise SystemExit(f"Expected {len(SCRIPT) - 1} pauses, found {len(ss)}; split {full} by hand")
    starts = [0.0] + [e - 0.08 for e in se]
    ends = [s + 0.15 for s in ss] + [None]
    for i, (st, en) in enumerate(zip(starts, ends)):
        cut = ["-ss", str(st)] + (["-to", str(en)] if en else [])
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", full, *cut, "-af", "loudnorm=I=-16:TP=-1.5",
                        "-ar", "44100", "-ac", "1", os.path.join(a.out, f"scene{i + 1:02d}.wav")], check=True)
    print("Done:", a.out, "-> python3 make_video.py --voice-dir", a.out)


if __name__ == "__main__":
    main()
