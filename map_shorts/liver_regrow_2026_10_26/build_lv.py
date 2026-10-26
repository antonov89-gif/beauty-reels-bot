"""Liver Short (reference JUni9wxjZcU body-cutaway DNA, frame-verified): blur/zoom joins with a light RGB split on every cut,
own counters (50% -> 100%, WEEK 1 -> 9), SAME SIZE / NOT SAME SHAPE tags, end question, 1-3 word captions, own synth bed.
Clips /home/claude/v80/c*.mp4, voice /home/claude/v81/lumean. Output /home/claude/v81/lv_final.mp4"""
import csv, json, subprocess, sys
from pathlib import Path
import cv2
import numpy as np
sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/ai_lifeboat_2026_10_25"); sys.path.insert(0, str(Path(__file__).parent))
import script_lv
from music_lb import music
V, W = Path("/home/claude/v80"), Path("/home/claude/v81")
T = json.load(open(W / "timing.json")); ST, D = T["starts"], T["D"]
END = ST[-1] + D[-1] + 1.6
FPS, WD, HT = 24, 1080, 1920

def wt(line, word):
    return ST[line] + T["T"][line][word]

# (out_start, out_end, clip, src_in, src_out, push_in); the source span is stretched to fit
EDL = [
    (0.0,       ST[1],     "c01", 0.0, 3.5, False),   # body, liver glows (the clip already pushes in)
    (ST[1],     wt(1, 7),  "c02", 1.0, 3.4, False),   # glowing line, liver splits
    (wt(1, 7),  ST[2],     "c03", 0.0, 1.6, False),   # half goes to someone else
    (ST[2],     ST[3],     "c07", 0.0, 1.3, True),    # what's left: half liver + empty outline (c04 showed a whole liver)
    (ST[3],     wt(3, 6),  "c05", 3.0, 5.3, False),   # dive into lobules
    (wt(3, 6),  ST[4],     "c06", 0.0, 2.0, False),   # a cell splits (cut before the morph at 2.5 s)
    (ST[4],     ST[5],     "c07", 1.0, 4.0, False),   # half grows back into the outline (counters)
    (ST[5],     wt(5, 5),  "c03", 2.5, 4.5, False),   # the half they took travels
    (wt(5, 5),  ST[6],     "c08", 0.0, 4.0, False),   # it grows inside the other person
    (ST[6],     wt(6, 5),  "c07", 5.0, 6.5, True),    # "But here's the weird part"
    (wt(6, 5),  ST[7],     "c09", 0.0, 3.5, False),   # same size, different shape (cut before they merge)
    (ST[7],     END,       "c10", 0.0, 3.5, False),   # pull-back + question
]

def build_base(out):
    inputs, chains = [], []
    for i, (a, b, c, s0, s1, push) in enumerate(EDL):
        inputs += ["-i", str(V / f"{c}.mp4")]
        d = b - a; k = d / (s1 - s0)
        f = (f"[{i}:v]trim={s0}:{s1},setpts=PTS-STARTPTS,scale={WD}:{HT}:force_original_aspect_ratio=increase,crop={WD}:{HT},setsar=1,"
             f"setpts={k:.4f}*PTS,fps={FPS},trim=duration={d:.4f}")
        if push:
            f += f",scale=w='{WD}*(1+0.05*t/{d:.3f})':h='{HT}*(1+0.05*t/{d:.3f})':eval=frame,crop={WD}:{HT}"
        chains.append(f + f"[v{i}]")
    cat = "".join(f"[v{i}]" for i in range(len(EDL))) + f"concat=n={len(EDL)}:v=1:a=0[vid]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + [cat]), "-map", "[vid]", "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(out)], check=True)

def join_fx(img, s):
    """Zoom blur + light RGB split at a join, s in 0..1 (reference uses blur/glitch joins instead of clean cuts)."""
    if s <= 0.01: return img
    z = 1 + 0.10 * s
    acc = np.zeros(img.shape, np.float32); n = 6
    for i in range(n):                                   # radial zoom blur
        zz = 1 + (z - 1) * i / (n - 1)
        M = cv2.getRotationMatrix2D((WD / 2, HT / 2), 0, zz)
        acc += cv2.warpAffine(img, M, (WD, HT), borderMode=cv2.BORDER_REFLECT)
    out = (acc / n).astype(np.uint8)
    sh = int(14 * s)                                     # RGB split
    b, g, r = cv2.split(out)
    r = np.roll(r, sh, axis=1); b = np.roll(b, -sh, axis=1)
    return cv2.merge([b, g, r])

def post(base, out):
    cap = cv2.VideoCapture(str(base))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WD}x{HT}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    joins = [e[0] for e in EDL[1:]]
    i = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        t = i / FPS; i += 1
        for j in joins:
            dt = t - j
            if -3 / FPS <= dt < 3 / FPS: f = join_fx(f, 1 - abs(dt) / (3 / FPS))
        enc.stdin.write(f.tobytes())
    enc.stdin.close(); enc.wait()

def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"

def build_ass(path):
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,62,&H00FFFFFF,&H000000FF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,1,3,4,2,60,60,430,1
Style: Num,DejaVu Sans,150,&H00FFFFFF,&H000000FF,&H00203040,&H80000000,1,0,0,0,100,100,0,0,1,8,4,8,60,60,230,1
Style: Chip,DejaVu Sans,60,&H00FFFFFF,&H000000FF,&H00403020,&HB0000000,1,0,0,0,100,100,2,0,3,16,0,8,60,60,420,1
Style: Ask,DejaVu Sans,96,&H00FFFFFF,&H000000FF,&H00203040,&H80000000,1,0,0,0,100,100,0,0,1,8,4,8,70,70,260,1
Style: Tag,DejaVu Sans,26,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,3,8,0,7,40,40,60,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = []
    def line(a, b, st, tx, layer=0): ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{st},,0,0,0,,{tx}")
    pop = "{\\fscx60\\fscy60\\t(0,120,\\fscx100\\fscy100)}"
    line(0.0, END, "Tag", "AI ANIMATION")
    line(wt(1, 4) - 0.05, ST[2], "Num", pop + "≈ 50%")                       # "about half"
    a, b = ST[4], ST[5]                                                         # growth counters on the c07 regrowth
    for k in range(9):
        t0 = a + (b - a) * k / 9; t1 = a + (b - a) * (k + 1) / 9
        line(t0, t1, "Num", f"{50 + round(50 * (k + 1) / 9)}%")
        line(t0, t1, "Chip", f"WEEK {k + 1}")
    a, b = wt(5, 5), ST[6]                                                      # recipient's half grows too
    for k in range(6):
        t0 = a + (b - a) * k / 6; t1 = a + (b - a) * (k + 1) / 6
        line(t0, t1, "Num", f"{50 + round(50 * (k + 1) / 6)}%")
    line(wt(6, 10) - 0.05, wt(6, 12), "Chip", pop + "SAME SHAPE  ✗")
    line(wt(6, 12) - 0.05, ST[7], "Chip", pop + "SAME SIZE  ✓")
    line(ST[7], END, "Ask", pop + "WHICH SUPERHERO\\NHEALS LIKE THIS?")
    ch = [(r["char"], float(r["start"]), float(r["end"])) for r in csv.DictReader(open(W / "lumean/alignment.csv"))]
    words, cur, s0, pb = [], "", None, 0
    for c, x, y in ch:
        if c == " ":
            if cur: words.append((cur, s0, pb)); cur, s0 = "", None
            continue
        if s0 is None: s0 = x
        cur += c; pb = y
    if cur: words.append((cur, s0, pb))
    g, pos = [], 0
    for li, ln in enumerate(script_lv.LINES):
        lw = words[pos:pos + len(ln.split())]; pos += len(ln.split())
        if li == len(script_lv.LINES) - 1: continue                            # last line is the on-screen question
        k = 0
        while k < len(lw):
            n = 3 if len(lw) - k > 4 else (2 if len(lw) - k == 4 else len(lw) - k)
            grp = lw[k:k + n]; k += n
            g.append((" ".join(w[0] for w in grp), grp[0][1], grp[-1][2]))
    for k, (txt, x, y) in enumerate(g):
        nb = g[k + 1][1] if k + 1 < len(g) else ST[-1]
        line(x, min(nb, y + 0.3), "Cap", txt, 1)
    Path(path).write_text(hdr + "\n".join(ev), encoding="utf-8")

def bed(total):
    sr = 44100; n = int(total * sr) + sr; rng = np.random.default_rng(5)
    mus = music(total, ST, T["T"], dark=(ST[6], ST[7]), stings=[(1, 4), (5, 4), (6, 3), (7, 2)])[:n]
    mus = np.pad(mus, (0, max(0, n - len(mus)))); sfx = np.zeros(n)
    for j in [e[0] for e in EDL[1:]]:                    # soft whoosh on every join
        i0 = int((j - 0.12) * sr); L = int(0.3 * sr)
        if i0 < 0 or i0 + L >= n: continue
        k = np.arange(L) / sr; nz = np.convolve(rng.standard_normal(L), np.ones(30) / 30, mode="same")
        sfx[i0:i0 + L] += nz * np.sin(np.pi * k / 0.3) * 1.2
    for at in (ST[4], wt(5, 5)):                          # rising shimmer under the growth shots
        i0 = int(at * sr); L = int(3.0 * sr); k = np.arange(L) / sr
        if i0 + L < n: sfx[i0:i0 + L] += np.sin(2 * np.pi * (300 + 140 * k) * k) * 0.05 * np.minimum(1, k) * np.exp(-((k - 2.5) ** 2))
    return mus + sfx

def write_wav(x, path):
    import wave
    x = np.clip(x / max(1e-9, np.abs(x).max()) * 0.9, -1, 1); w = wave.open(str(path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()

if __name__ == "__main__":
    for x, y, c, s0, s1, _ in EDL: assert y > x and s1 <= 8.0, (c, x, y)
    build_base(W / "lv_base.mp4"); post(W / "lv_base.mp4", W / "lv_video.mp4")
    build_ass(W / "lv.ass"); write_wav(bed(END), W / "bed.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "lv_video.mp4"), "-i", str(W / "lumean/result.mp3"), "-i", str(W / "bed.wav"),
        "-filter_complex", f"[0:v]ass={W / 'lv.ass'}[v];[1:a]aresample=44100,asplit[vo][sc];[2:a]volume=0.62[bed];"
        "[bed][sc]sidechaincompress=threshold=0.06:ratio=3:attack=20:release=300[duck];[vo][duck]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
        "-map", "[v]", "-map", "[a]", "-t", f"{END:.2f}", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(W / "lv_final.mp4")], check=True)
    print("done", round(END, 2), "s")
