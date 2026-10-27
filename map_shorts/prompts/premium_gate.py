"""Premium gate for a finished Short (run BEFORE showing it to the owner; results go into reference_check.md / the authenticity audit).
Usage: python3 premium_gate.py <video.mp4> [--timing timing.json] [--out report.md] [--sheet sheet.jpg] [--clip]
Checks (each row PASS / WARN / FAIL; anything not run is NOT VERIFIED, never PASS):
  spec         1080x1920, 24-30 fps, an audio stream, audio and video lengths within 0.35 s
  loudness     EBU R128 integrated -15.5..-12.5 LUFS, true peak <= -1.0 dBTP
  frames       first frame not dark (hook readable), no black frames, no frozen stretch > 1.5 s except the last 1.5 s
  drift        AI colour drift: inside one shot (between detected cuts) the colour histogram moves away from the shot's first frame
               (a country changing colour, layers vanishing; measured on a 14x8 grid so a local change is caught). Flags are REVIEW items: look at the sheet and cut before the time shown (a sunset or a camera flight also flags).
  bed          music bed audible in the gaps of the voice (needs --timing with starts and D): gap level -34..(speech - 6) dB
  --clip       treat the file as a raw AI clip (one shot): no cut detection, drift is measured over the whole clip
Not covered (always NOT VERIFIED here): factual claims, text overlap on screen, text safe zone, AI labels, licences. Those stay in the authenticity audit.
Calibrated on the 9 Iraq Short clips (27.10.2026): the pink-Iraq clip c07, the vanishing-layers clip c04 and the sunset c09 are flagged; c01-c03, c05, c06, c08 are not."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

W, H = 160, 284


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(v):
    j = json.loads(run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", v]).stdout)
    vs = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    au = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    num, den = (vs["r_frame_rate"].split("/") if vs else ("0", "1"))
    return dict(w=int(vs["width"]), h=int(vs["height"]), fps=float(num) / float(den or 1), vdur=float(vs.get("duration") or j["format"]["duration"]),
                adur=float(au.get("duration") or j["format"]["duration"]) if au else None, dur=float(j["format"]["duration"]))


def frames(v, fps):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-vf", f"fps={fps},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def loudness(v):
    e = run(["ffmpeg", "-hide_banner", "-i", v, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    I = re.findall(r"I:\s+(-?[0-9.]+) LUFS", e)
    P = re.findall(r"Peak:\s+(-?[0-9.]+) dBFS", e)
    return (float(I[-1]) if I else None), (float(P[-1]) if P else None)


def hist(f):
    h = np.concatenate([np.histogram(f[..., c], bins=8, range=(0, 256))[0] for c in range(3)]).astype(np.float64)
    return h / h.sum() * 3


def hdist(a, b):
    return float(0.5 * np.abs(a - b).sum() / 3)


def luma(f):
    return float((0.3 * f[..., 0] + 0.59 * f[..., 1] + 0.11 * f[..., 2]).mean())


def cells(f):
    gh, gw = 14, 8
    return f[:H // gh * gh, :W // gw * gw].astype(np.float32).reshape(gh, H // gh, gw, W // gw, 3).mean(axis=(1, 3))


def drift(fr, fps, one_shot):
    """Return (cuts, flags). Cut = frame difference above 0.11 (mean abs / 255). Drift = the share of grid cells (14x8) whose mean colour moved
    by more than 70/255 from the shot's first frame, above 0.30 and still there at the end of the shot (calibrated on 9 Iraq clips: the pink-Iraq clip
    0.39, vanishing layers 0.62, a sunset 0.32 = review; stable clips 0.15-0.24)."""
    d = np.array([np.abs(fr[i].astype(np.int16) - fr[i - 1].astype(np.int16)).mean() / 255 for i in range(1, len(fr))])
    cuts = [] if one_shot else [i + 1 for i, x in enumerate(d) if x > 0.11]
    bounds = [0] + cuts + [len(fr)]
    flags = []
    for a, b in zip(bounds, bounds[1:]):
        if (b - a) / fps < 1.2:
            continue
        c0 = cells(fr[a])
        sh = [float((np.abs(cells(fr[k]) - c0).max(axis=-1) > 70).mean()) for k in range(a, b)]
        mx = max(sh)
        if mx > 0.30 and sh[-1] > 0.6 * mx:
            first = next(i for i, x in enumerate(sh) if x > 0.10)
            flags.append(dict(t_start=round(a / fps, 2), t_end=round(b / fps, 2), drift_from=round((a + first) / fps, 2), max=round(mx, 2)))
    return [round(c / fps, 2) for c in cuts], flags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--timing"); ap.add_argument("--out"); ap.add_argument("--sheet"); ap.add_argument("--clip", action="store_true")
    a = ap.parse_args()
    v = a.video; rows = []
    add = lambda name, st, msg: rows.append((name, st, msg))                      # noqa: E731
    p = probe(v)
    ok = p["w"] == 1080 and p["h"] == 1920 and 23.5 <= p["fps"] <= 30.5
    add("spec", "PASS" if ok else "FAIL", f'{p["w"]}x{p["h"]} @ {p["fps"]:.2f} fps, {p["dur"]:.2f} s')
    if p["adur"] is None:
        add("audio", "WARN" if a.clip else "FAIL", "no audio stream")
    else:
        dd = abs(p["adur"] - p["vdur"])
        add("audio length", "PASS" if dd <= 0.35 else "WARN", f'audio {p["adur"]:.2f} s vs video {p["vdur"]:.2f} s (diff {dd:.2f})')
        I, P = loudness(v)
        okl = I is not None and -15.5 <= I <= -12.5 and P is not None and P <= -1.0
        add("loudness", "PASS" if okl else "FAIL", f"{I} LUFS, true peak {P} dBTP")
    fps = 8
    fr = frames(v, fps)
    if len(fr) < 4:
        add("frames", "FAIL", "could not read frames")
    else:
        l0, ln = luma(fr[0]), luma(fr[-1])
        add("first frame", "PASS" if l0 > 35 else "WARN", f"mean luma {l0:.0f} (a dark frame 0 hurts the hook)")
        add("last frame", "PASS" if ln > 25 else "WARN", f"mean luma {ln:.0f}")
        blk = [i / fps for i, f in enumerate(fr) if luma(f) < 8]
        add("black frames", "PASS" if len(blk) / len(fr) < 0.02 else "FAIL", f"{len(blk)} of {len(fr)}" + (f", first at {blk[0]:.1f} s" if blk else ""))
        dif = np.array([np.abs(fr[i].astype(np.int16) - fr[i - 1].astype(np.int16)).mean() / 255 for i in range(1, len(fr))])
        frozen, run_ = [], 0
        for i, x in enumerate(dif):
            run_ = run_ + 1 if x < 0.002 else 0
            if run_ >= int(1.5 * fps) and (i + 1) / fps < len(fr) / fps - 1.5:
                frozen.append(round((i + 1) / fps, 1)); run_ = 0
        add("frozen stretch", "PASS" if not frozen else "WARN", "none" if not frozen else f"frozen > 1.5 s around {frozen} s")
        cuts, flags = drift(fr, fps, a.clip)
        add("cuts", "PASS", f"{len(cuts)} detected" + (f": {cuts}" if cuts else "") + f" ({len(cuts) / (len(fr) / fps) * 10:.1f} per 10 s)" if not a.clip else "single clip")
        add("colour drift", "PASS" if not flags else "WARN", "none detected" if not flags else
            "REVIEW " + "; ".join(f'shot {f["t_start"]}-{f["t_end"]} s: colours move from {f["drift_from"]} s (max {f["max"]})' for f in flags))
        if a.sheet:
            n = int(p["dur"]) + 1
            run(["ffmpeg", "-v", "error", "-y", "-i", v, "-vf", f"fps=1,scale=180:-1,tile={min(14, n)}x{-(-n // 14)}", "-frames:v", "1", a.sheet])
            add("contact sheet", "PASS", a.sheet)
    if a.timing:
        t = json.load(open(a.timing)); st, d = t["starts"], t["D"]
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
        x = np.frombuffer(raw, np.float32); sr = 16000
        db = lambda y: 20 * np.log10(np.sqrt(np.mean(y ** 2)) + 1e-9)             # noqa: E731
        sp = db(np.concatenate([x[int(s * sr):int((s + dd) * sr)] for s, dd in zip(st, d)]))
        gaps = [db(x[int((s + dd + 0.05) * sr):int((n - 0.05) * sr)]) for s, dd, n in zip(st, d, st[1:]) if n - (s + dd) > 0.25]
        bad = [round(float(g), 1) for g in gaps if not (-34 <= g <= sp - 6)]
        add("music bed", "PASS" if not bad else "WARN", f"speech {sp:.1f} dB, gaps {[round(float(g), 1) for g in gaps]}" + (f"; outside -34..{sp - 6:.0f}: {bad}" if bad else ""))
    else:
        add("music bed", "NOT VERIFIED", "pass --timing to measure")
    for nv in ("facts / claims", "text overlap and safe zone", "AI label and flags", "licences"):
        add(nv, "NOT VERIFIED", "not covered by this script: see the authenticity audit")
    verdict = "FAIL" if any(r[1] == "FAIL" for r in rows) else ("REVIEW" if any(r[1] == "WARN" for r in rows) else "PASS (script checks only)")
    md = f"# Premium gate: {Path(v).name}\n| Check | Status | Detail |\n|--|--|--|\n" + "\n".join(f"| {n} | {s} | {m} |" for n, s, m in rows) + f"\n\nVerdict: **{verdict}**\n"
    print(md)
    if a.out:
        Path(a.out).write_text(md)
    sys.exit(1 if verdict == "FAIL" else 0)


if __name__ == "__main__":
    main()
