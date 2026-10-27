"""Iraq Short: premium 3D keyframe clips (Veo 3.1) + our graphics (banner, rotated stamps, chips from sb_overlay) + 2-4 word captions with the
active word yellow + own synth bed and SFX. Clips /home/claude/v86/clips, voice /home/claude/v86/lumean, timing /home/claude/v86/timing.json.
Output /home/claude/v86/iq_final.mp4"""
import csv
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/ai_lifeboat_2026_10_25"); sys.path.insert(0, str(Path(__file__).parent))
import script_iq
import sb_overlay as ov
from music_lb import music

V, W = Path("/home/claude/v86/clips"), Path("/home/claude/v86")
T = json.load(open(W / "timing.json")); ST, D, TW = T["starts"], T["D"], T["T"]
END = ST[-1] + D[-1] + 1.2
FPS, WD, HT = 24, 1080, 1920
wt = lambda l, w: ST[l] + TW[l][w]          # noqa: E731  absolute time of word w in line l

# (out_start, out_end, clip, src_in, src_out, push_in, saturation)
EDL = [
    (0.0,        ST[1],     "c01", 0.0, 5.0, False, 1.10),    # hook: fly-in to the 58 km coast
    (ST[1],      ST[2],     "c02", 0.0, 3.5, False, 1.10),    # 46 million people: city lights
    (ST[2],      ST[3],     "c03", 0.5, 3.8, False, 1.10),    # Iran / Kuwait
    (ST[3],      ST[4],     "c04", 0.0, 6.6, False, 1.10),    # the channel to Umm Qasr
    (ST[4],      ST[5],     "c05", 0.0, 5.0, False, 1.10),    # border in the middle, deep water near Kuwait
    (ST[5],      wt(5, 8),  "c06", 0.0, 3.6, False, 1.10),    # "Wait, a channel is still a channel": tanker in the lane
    (wt(5, 8),   ST[7],     "c07", 0.0, 8.0, False, 1.10),    # ports on the channel (stretched slightly: ~8 s)
    (ST[7],      ST[8],     "c08", 0.0, 8.0, False, 1.10),    # the gate closes
    (ST[8],      END,       "c09", 0.0, 8.0, False, 1.10),    # sunset pull-back, question
]
# overlays: (kind, text, y, t0, t1)
OVL = [
    ("banner", "ONE 58 KM DOOR?!", 0, 0.05, ST[1]),
    ("chip", "≈ 90% OF OIL EXPORTS", 1180, wt(0, 0) + 0.4, ST[1]),
    ("chip", "46,000,000 PEOPLE", 330, ST[1] + 0.05, ST[2]),
    ("stamp", "TINY DOOR", 760, wt(1, 4), ST[2] + 0.2),
    ("chip", "IRAN  ·  IRAQ  ·  KUWAIT", 330, ST[2] + 0.05, ST[3]),
    ("chip", "UMM QASR: ONE WAY OUT", 330, ST[3] + 0.3, ST[4]),
    ("chip", "BORDER: THE MIDDLE", 300, ST[4] + 0.1, ST[5]),
    ("chip", "DEEP WATER: KUWAIT SIDE", 410, wt(4, 8), ST[5]),
    ("stamp", "WAIT…", 700, ST[5] + 0.1, wt(5, 8)),
    ("chip", "KUWAIT: MUBARAK AL-KABEER PORT", 300, wt(5, 11), ST[7]),
    ("chip", "IRAQ: GRAND FAW PORT", 410, wt(6, 9), ST[7]),
    ("stamp", "CHOKE POINT?", 700, wt(7, 5), wt(7, 5) + 2.6),
    ("chip", "2023: COURT STRIKES DOWN DEAL LAW", 1180, wt(7, 12), ST[8]),
    ("banner", "SMART MOVE OR CHOKEHOLD?", 0, wt(8, 10), END),
]


def build_base(out):
    inputs, chains = [], []
    for i, (a, b, c, s0, s1, push, sat) in enumerate(EDL):
        inputs += ["-i", str(V / f"{c}.mp4")]
        d = b - a; k = d / (s1 - s0)
        f = (f"[{i}:v]trim={s0}:{s1},setpts=PTS-STARTPTS,scale={WD}:{HT}:force_original_aspect_ratio=increase,crop={WD}:{HT},setsar=1,"
             f"setpts={k:.4f}*PTS,fps={FPS},trim=duration={d:.4f}")
        f += f",eq=contrast=1.05:saturation={sat}"
        chains.append(f + f"[v{i}]")
    cat = "".join(f"[v{i}]" for i in range(len(EDL))) + f"concat=n={len(EDL)}:v=1:a=0[vid]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + [cat]), "-map", "[vid]", "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(out)], check=True)


def overlay_pngs():
    paths = []
    for k, (kind, txt, y, a, b) in enumerate(OVL):
        im = Image.new("RGBA", (WD, HT), (0, 0, 0, 0))
        if kind == "banner":
            ov.banner(im, txt)
        elif kind == "chip":
            ov.chip(im, txt, y)
        else:
            ov.stamp(im, txt, y)
        p = W / f"ovl_{k:02d}.png"; im.save(p); paths.append(p)
    return paths


def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def build_ass(path):
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,66,&H00FFFFFF,&H000000FF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,1,5,4,2,60,60,400,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ch = [(r["char"], float(r["start"]), float(r["end"])) for r in csv.DictReader(open(W / "lumean/alignment.csv"))]
    words, cur, s0, pb = [], "", None, 0
    for c, a, b in ch:
        if c == " ":
            if cur:
                words.append((cur, s0, pb)); cur, s0 = "", None
            continue
        if s0 is None:
            s0 = a
        cur += c; pb = b
    if cur:
        words.append((cur, s0, pb))
    groups, pos = [], 0
    for ln in script_iq.LINES:
        lw = words[pos:pos + len(ln.split())]; pos += len(ln.split()); k = 0
        while k < len(lw):
            n = 4 if len(lw) - k == 4 else (3 if len(lw) - k > 4 else len(lw) - k)
            groups.append(lw[k:k + n]); k += n
    rep = {"Forty-six": "46", "fifty-eight": "58", "ninety": "90", "twenty-three,": "2023,"}
    ev = []
    for gi, g in enumerate(groups):
        nxt = groups[gi + 1][0][1] if gi + 1 < len(groups) else END
        for wi, w in enumerate(g):
            a = w[1]; b = g[wi + 1][1] if wi + 1 < len(g) else min(nxt, g[-1][2] + 0.3)
            txt = " ".join(("{\\c&H00D6FF&}" + rep.get(x[0], x[0]) + "{\\c&HFFFFFF&}") if j == wi else rep.get(x[0], x[0]) for j, x in enumerate(g))
            ev.append(f"Dialogue: 1,{ts(a)},{ts(b)},Cap,,0,0,0,,{txt}")
    Path(path).write_text(hdr + "\n".join(ev), encoding="utf-8")


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, "same")


def sfx_track(n, sr):
    rng = np.random.default_rng(86); out = np.zeros(n)

    def place(s, t, g=1.0):
        i = int(t * sr)
        if 0 <= i < n:
            e = min(n, i + len(s)); out[i:e] += s[:e - i] * g
    tt = lambda d: np.arange(int(d * sr)) / sr          # noqa: E731
    def whoosh(d=0.5):
        t = tt(d); f = np.cumsum(np.interp(t, [0, d], [250, 2400])) / sr
        return lp(np.sin(2 * np.pi * f) * rng.normal(0, 1, len(t)) * np.sin(np.pi * t / d) ** 2, 6) * 0.3
    def pop():
        t = tt(0.12); return np.sin(2 * np.pi * (480 + 900 * np.exp(-t * 40)) * t) * np.exp(-t * 35) * 0.45
    def slam():
        t = tt(0.6); return (np.sin(2 * np.pi * (45 + 90 * np.exp(-t * 16)) * t) * np.exp(-t * 6) * 0.9 + lp(rng.normal(0, 1, len(t)), 4) * np.exp(-t * 22) * 0.35)
    for a, *_ in EDL[1:]:
        place(whoosh(), a - 0.12, 0.6)
    for kind, _, _, a, _ in OVL:
        place(slam() if kind == "stamp" else pop(), a, 0.8 if kind == "stamp" else 0.5)
    return out


def write_wav(x, path):
    x = np.clip(x / max(1e-9, np.abs(x).max()) * 0.9, -1, 1); w = wave.open(str(path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()


if __name__ == "__main__":
    for a, b, c, s0, s1, *_ in EDL:
        assert b > a and s1 <= 8.0, (c, a, b)
    build_base(W / "iq_base.mp4"); build_ass(W / "iq.ass")
    sr = 44100; n = int(END * sr) + sr
    bed = music(END, ST, TW, dark=(ST[7], ST[8]), stings=[(1, 4), (7, 5), (8, 10)])[:n]
    bed = np.pad(bed, (0, max(0, n - len(bed))))
    write_wav(bed * 0.62 + sfx_track(n, sr), W / "bed.wav")
    pngs = overlay_pngs()
    inputs = ["-i", str(W / "iq_base.mp4"), "-i", str(W / "lumean/result.mp3"), "-i", str(W / "bed.wav")]
    for p in pngs:
        inputs += ["-loop", "1", "-t", f"{END:.2f}", "-i", str(p)]
    fc, last = [], "0:v"
    for k, (kind, _, _, a, b) in enumerate(OVL):
        fc.append(f"[{3 + k}:v]format=rgba,fade=in:st={a:.2f}:d=0.16:alpha=1,fade=out:st={b - 0.15:.2f}:d=0.15:alpha=1[o{k}]")
        fc.append(f"[{last}][o{k}]overlay=enable='between(t,{a:.2f},{b:.2f})':shortest=1[v{k}]"); last = f"v{k}"
    fc.append(f"[{last}]ass={W / 'iq.ass'}[v]")
    fc.append("[1:a]aresample=44100,asplit[vo][sc];[2:a]volume=0.62[bed];[bed][sc]sidechaincompress=threshold=0.06:ratio=3:attack=20:release=300[duck];"
              "[vo][duck]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-t", f"{END:.2f}",
                    "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", str(W / "iq_final.mp4")], check=True)
    print("done", round(END, 2), "s")
