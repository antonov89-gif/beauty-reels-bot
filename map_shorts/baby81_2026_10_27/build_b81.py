"""'Three Mothers Claimed the Same Baby' (fiction, stories channel): Veo clips + our graphics (tag 12, memory bubble with a torn glowing outline, DNA UI)
+ white 1-3 word captions at ~78 % height + own soft bed (pad + music-box lullaby) and light SFX. AI never writes text.
Clips /home/claude/v88/clips, voice /home/claude/v88/lumean, timing /home/claude/v88/timing.json. Output /home/claude/v88/b81_final.mp4"""
import csv
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import script_b81
import sb_overlay_b81 as sb

V, W = Path("/home/claude/v88/clips"), Path("/home/claude/v88")
T = json.load(open(W / "timing.json")); ST, D, TW = T["starts"], T["D"], T["T"]
END = ST[-1] + D[-1] + 2.0                       # 2 s quiet landing after the last word
FPS, WD, HT = 24, 1080, 1920
wt = lambda l, w: ST[l] + TW[l][w]                # noqa: E731  absolute time of word w in line l

# (out_start, out_end, clip, src_in, src_out); src_out None = 1:1 speed
EDL = [
    (0.0,        ST[1],      "c01",  0.0, None),   # 1 baby on the shore
    (ST[1],      wt(1, 6),   "c02",  0.0, None),   # 2 the nurse carries him in
    (wt(1, 6),   ST[2],      "c03",  0.0, None),   # 2 the wristband, the cot (tag 12 here)
    (ST[2],      ST[3],      "c05",  0.0, None),   # 3 three families
    (ST[3],      ST[4],      "c04",  0.0, None),   # 4 no papers (+ memory bubble)
    (ST[4],      ST[6], "c06b", 0.0, None),   # 5-6 the question, two mothers talk
    (ST[6],      wt(7, 3),   "c07b", 0.4, None),   # 7 the third mother hums, the baby calms
    (wt(7, 3),   ST[8],      "c08b", 0.0, None),   # 8 the baby looks at her
    (ST[8],      wt(8, 3),   "c07",  0.0, None),   # 9 swab
    (wt(8, 3),   ST[9],      "c08",  0.0, None),   # 9 DNA bands + MATCH
    (ST[9],      wt(9, 5),   "c10",  0.0, None),   # 10 her face
    (wt(9, 5),   END,        "c11",  0.0, None),   # 10 the hug, quiet hold
]
PUSH = {"c06b": 0.14}
# overlays on their own layer: (kind, t0, t1)
OVL = [
    ("tag12", wt(1, 10), ST[2]),
    ("dna", wt(8, 3) + 0.2, ST[9] - 0.1),
]
BUBBLE = (wt(3, 6), ST[4] - 0.2)                 # "The flood had taken everything"


def clip_len(c):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(V / f"{c}.mp4")],
                                capture_output=True, text=True).stdout)


def build_base(out):
    inputs, chains = [], []
    for i, (a, b, c, s0, s1) in enumerate(EDL):
        inputs += ["-i", str(V / f"{c}.mp4")]
        d = b - a
        have = clip_len(c) - s0
        if d <= have + 1e-3:                                   # 1:1 speed
            f = f"[{i}:v]trim=start={s0}:duration={d + 0.05:.3f},setpts=PTS-STARTPTS"
        else:                                                  # slow down to fit, never more than needed
            k = d / have
            assert k < 1.6, (c, d, have)
            f = f"[{i}:v]trim=start={s0},setpts=(PTS-STARTPTS)*{k:.4f}"
        f += f",scale={WD}:{HT}:force_original_aspect_ratio=increase:flags=lanczos,crop={WD}:{HT},setsar=1,fps={FPS},trim=duration={d:.4f},setpts=PTS-STARTPTS"
        if c in PUSH:                                          # slow push on a wide, static clip (keeps the camera alive)
            nn = int(d * FPS) + 2
            f += f",scale=2160:3840,zoompan=z='1+{PUSH[c]}*on/{nn}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={WD}x{HT}:fps={FPS}"
        f += ",eq=contrast=1.04:saturation=1.05"
        chains.append(f + f"[v{i}]")
    cat = "".join(f"[v{i}]" for i in range(len(EDL))) + f"concat=n={len(EDL)}:v=1:a=0[vid]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + [cat]), "-map", "[vid]", "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(out)], check=True)


# ---------- our graphics ----------
def layer_png(kind, path):
    im = Image.new("RGBA", (WD, HT), (0, 0, 0, 0))
    if kind == "tag12":
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); cx, cy, r = 210, 560, 135
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 235), outline=(255, 214, 0, 255), width=10)
        d.text((cx, cy + 6), "12", font=ImageFont.truetype(sb.MB, 170), fill=(20, 30, 60, 255), anchor="mm")
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.2))); im.alpha_composite(lay)
    else:
        sb.dna(im)
    im.save(path)


def bubble_assets():
    """Inner video (slow push on the wave frame, masked by the torn outline) and the glowing ring PNG."""
    cx, cy, rx, ry = 690, 215, 290, 205
    pts = sb.torn_mask(cx, cy, rx, ry)
    m = Image.new("L", (WD, HT), 0); ImageDraw.Draw(m).polygon(pts, fill=255); m.save(W / "bub_mask.png")
    ring = Image.new("RGBA", (WD, HT), (0, 0, 0, 0))
    g = Image.new("RGBA", (WD, HT), (0, 0, 0, 0)); ImageDraw.Draw(g).line(pts + [pts[0]], fill=(255, 255, 255, 255), width=14, joint="curve")
    ring.alpha_composite(g.filter(ImageFilter.GaussianBlur(12)))
    ImageDraw.Draw(ring).line(pts + [pts[0]], fill=(255, 255, 255, 255), width=8, joint="curve")
    ring.save(W / "bub_ring.png")
    d = BUBBLE[1] - BUBBLE[0]; n = int(d * FPS) + 2
    wave = Image.open(W / "frames/s04b.jpg").convert("RGB").resize((WD, HT))
    cw, ch = int(rx * 2.7), int(ry * 2.7)                      # a landscape window of the wave frame (house + wave), centred on the bubble
    bx, by, kw = 540, int(HT * 0.57), 1000
    kh = int(kw * ch / cw)
    box = wave.crop((bx - kw // 2, by - kh // 2, bx + kw // 2, by + kh // 2)).resize((cw, ch))
    src = Image.new("RGB", (WD, HT), (0, 0, 0)); src.paste(box, (cx - cw // 2, cy - ch // 2)); src.save(W / "bub_src.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "bub_src.png"), "-vf",
                    f"scale=2160:3840,zoompan=z='1.0+0.12*on/{n}':x='{2 * cx}*(1-1/zoom)':y='{2 * cy}*(1-1/zoom)':d={n}:s={WD}x{HT}:fps={FPS}",
                    "-frames:v", str(n), "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(W / "bub_inner.mp4")], check=True)


# ---------- captions: white 1-3 words, ~78 % height, same look as the approved storyboard ----------
def caption_png(txt, path):
    im = Image.new("RGBA", (WD, HT), (0, 0, 0, 0)); sb.caption(im, txt); im.save(path)


def caption_list():
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
    for ln in script_b81.LINES:
        lw = words[pos:pos + len(ln.split())]; pos += len(ln.split())
        clauses, cur_ = [], []
        for w in lw:                                            # break at punctuation, then balance each clause into 1-3 word groups
            cur_.append(w)
            if w[0][-1] in ".,:?!;":
                clauses.append(cur_); cur_ = []
        if cur_:
            clauses.append(cur_)
        for cl in clauses:
            k = -(-len(cl) // 3); base, extra = divmod(len(cl), k); i = 0
            for j in range(k):
                m = base + (1 if j < extra else 0); groups.append(cl[i:i + m]); i += m
    rep = {"twelve": "12", "twelve.": "12."}
    lines, t = [], 0.0
    (W / "caps").mkdir(exist_ok=True)
    Image.new("RGBA", (WD, HT), (0, 0, 0, 0)).save(W / "caps/blank.png")
    for gi, g in enumerate(groups):
        a = g[0][1]; nxt = groups[gi + 1][0][1] if gi + 1 < len(groups) else END
        b = min(nxt, g[-1][2] + 0.35) if gi + 1 < len(groups) else g[-1][2] + 0.6
        if a > t + 1e-3:
            lines.append(("blank.png", a - t))
        p = W / f"caps/c{gi:02d}.png"
        caption_png(" ".join(rep.get(x[0], x[0]) for x in g), p)
        lines.append((p.name, b - a)); t = b
    if END > t:
        lines.append(("blank.png", END - t))
    with open(W / "caps/list.txt", "w") as f:
        for name, d in lines:
            f.write(f"file '{W / 'caps' / name}'\nduration {d:.3f}\n")
        f.write(f"file '{W / 'caps' / 'blank.png'}'\n")


# ---------- audio: own soft bed + lullaby + light SFX ----------
SR = 44100


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tone(f, d, kind="pad"):
    t = np.arange(int(d * SR)) / SR
    if kind == "box":                                   # music box: sine + 2nd/4th partials, fast decay
        y = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 4 * f * t)
        return y * np.exp(-t * 3.2) * (1 - np.exp(-t * 400))
    y = sum(np.sin(2 * np.pi * f * (1 + dt) * t) for dt in (-0.003, 0, 0.003))
    a = np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.2)
    return y * a / 3


def soft_bed(total):
    n = int(total * SR) + SR; out = np.zeros(n)
    prog = [(45, 57, 60, 64), (41, 53, 57, 60), (48, 55, 60, 64), (43, 55, 59, 62)]     # Am F C G (low root + triad), 4 s per chord
    bar = 4.0
    for b in range(int(total // bar) + 1):
        for m in prog[b % 4]:
            s = tone(hz(m), bar + 1.2); i = int(b * bar * SR); e = min(n, i + len(s)); out[i:e] += s[:e - i] * (0.16 if m < 50 else 0.07)
    # music-box lullaby (own melody, A minor pentatonic), starts when the third mother hums and returns softly at the end
    mel = [(69, 1), (72, 1), (76, 1.5), (74, .5), (72, 1), (69, 1), (67, 1.5), (69, .5), (72, 1), (74, 1), (76, 1.5), (72, .5), (69, 3)]
    def play(t0, g):
        t = t0
        for m, ln in mel:
            s = tone(hz(m), ln * 0.9 + 1.0, "box"); i = int(t * SR)
            if i < n:
                e = min(n, i + len(s)); out[i:e] += s[:e - i] * g
            t += ln * 0.9
    play(ST[6] - 0.2, 0.22)
    play(ST[9] + 0.4, 0.17)
    # long fade-in at the start and a slow fade-out at the very end
    x = out[:int(total * SR)]
    x *= np.minimum(1, np.arange(len(x)) / (SR * 1.5)) * np.minimum(1, (len(x) - np.arange(len(x))) / (SR * 1.5))
    return np.pad(x, (0, n - len(x)))


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, "same")


def sfx_track(n):
    rng = np.random.default_rng(88); out = np.zeros(n)

    def place(s, t, g):
        i = int(t * SR)
        if 0 <= i < n:
            e = min(n, i + len(s)); out[i:e] += s[:e - i] * g

    def whoosh(d=0.5):
        t = np.arange(int(d * SR)) / SR; f = np.cumsum(np.interp(t, [0, d], [250, 1800])) / SR
        return lp(np.sin(2 * np.pi * f) * rng.normal(0, 1, len(t)) * np.sin(np.pi * t / d) ** 2, 6) * 0.22
    def pop():
        t = np.arange(int(0.14 * SR)) / SR; return np.sin(2 * np.pi * (520 + 900 * np.exp(-t * 40)) * t) * np.exp(-t * 32) * 0.4
    def ding():
        t = np.arange(int(1.0 * SR)) / SR; return (np.sin(2 * np.pi * 988 * t) + 0.5 * np.sin(2 * np.pi * 1318 * t)) * np.exp(-t * 4) * 0.3
    for a, *_ in EDL[1:]:
        place(whoosh(), a - 0.12, 0.5)
    place(pop(), wt(1, 11), 0.7)
    place(ding(), OVL[1][1] + 0.5, 0.7)
    return out


def write_wav(x, path):
    x = np.clip(x, -1, 1); w = wave.open(str(path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()


if __name__ == "__main__":
    for a, b, c, *_ in EDL:
        assert b > a and (V / f"{c}.mp4").exists(), (c, a, b)
    build_base(W / "b81_base.mp4")
    bubble_assets(); caption_list()
    for kind, a, b in OVL:
        layer_png(kind, W / f"ovl_{kind}.png")
    n = int(END * SR) + SR
    bed = soft_bed(END)
    vx = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(W / "lumean/result.mp3"), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768.0
    vr = np.sqrt(np.mean(vx[np.abs(vx) > 0.01] ** 2))                    # speech rms
    br = np.sqrt(np.mean(bed[np.abs(bed) > 1e-4] ** 2))
    mix = bed * (vr * 10 ** (-13 / 20) / br) + sfx_track(n)[:len(bed)] * vr * 0.35   # bed about 13 dB under the voice, light SFX
    write_wav(mix, W / "bed_b81.wav")
    bd = BUBBLE[1] - BUBBLE[0]
    inputs = ["-i", str(W / "b81_base.mp4"), "-i", str(W / "lumean/result.mp3"), "-i", str(W / "bed_b81.wav"),
              "-f", "concat", "-safe", "0", "-i", str(W / "caps/list.txt"),
              "-i", str(W / "bub_inner.mp4"), "-loop", "1", "-t", f"{bd:.2f}", "-i", str(W / "bub_mask.png"), "-loop", "1", "-t", f"{bd:.2f}", "-i", str(W / "bub_ring.png")]
    for kind, a, b in OVL:
        inputs += ["-loop", "1", "-t", f"{END:.2f}", "-i", str(W / f"ovl_{kind}.png")]
    fc = []
    # memory bubble: masked inner video + glowing ring, popping in and out
    fc.append(f"[4:v]trim=duration={bd:.2f},setpts=PTS-STARTPTS[bi];[5:v]format=gray[bm];[bi][bm]alphamerge,format=rgba,fade=in:st=0:d=0.3:alpha=1,fade=out:st={bd - 0.3:.2f}:d=0.3:alpha=1,setpts=PTS+{BUBBLE[0]:.2f}/TB[bub]")
    fc.append(f"[6:v]format=rgba,fade=in:st=0:d=0.3:alpha=1,fade=out:st={bd - 0.3:.2f}:d=0.3:alpha=1,setpts=PTS+{BUBBLE[0]:.2f}/TB[ring]")
    fc.append(f"[0:v][bub]overlay=enable='between(t,{BUBBLE[0]:.2f},{BUBBLE[1]:.2f})':eof_action=pass[b1];[b1][ring]overlay=enable='between(t,{BUBBLE[0]:.2f},{BUBBLE[1]:.2f})':eof_action=pass[b2]")
    last = "b2"
    for k, (kind, a, b) in enumerate(OVL):
        idx = 7 + k
        fc.append(f"[{idx}:v]format=rgba,fade=in:st={a:.2f}:d=0.2:alpha=1,fade=out:st={b - 0.2:.2f}:d=0.2:alpha=1[o{k}]")
        fc.append(f"[{last}][o{k}]overlay=enable='between(t,{a:.2f},{b:.2f})':shortest=1[v{k}]"); last = f"v{k}"
    fc.append(f"[3:v]fps={FPS},format=rgba[cap];[{last}][cap]overlay=shortest=0:eof_action=pass[v]")
    fc.append("[1:a]aresample=44100,asplit[vo][sc];[2:a]volume=1.0[bed];[bed][sc]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=400[duck];"
              "[vo][duck]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,apad=whole_dur=" + f"{END:.2f}" + "[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-t", f"{END:.2f}",
                    "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", str(W / "b81_final.mp4")], check=True)
    print("done", round(END, 2), "s")
