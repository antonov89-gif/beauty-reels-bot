"""Sullivan Short (reference c3aRLh3SoAs DNA, frame-verified): act 1 joined as one moving camera with whip-blur transitions,
hard cut at the reveal, own keyword graphics (truck ring, roll arrow, cliff-edge glow), strike counter, 1-3 word captions at ~77% height,
own synth bed + thunder SFX. Clips /home/claude/v77/c*.mp4, voice /home/claude/v78/lumean. Output /home/claude/v78/su_final.mp4"""
import csv, json, math, subprocess, sys
from pathlib import Path
import cv2
import numpy as np
sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/ai_lifeboat_2026_10_25"); sys.path.insert(0, str(Path(__file__).parent))
import script_su
from music_lb import music
V, W = Path("/home/claude/v77"), Path("/home/claude/v78")
T = json.load(open(W / "timing.json")); ST, D = T["starts"], T["D"]
VO_END = ST[-1] + D[-1]; END = VO_END + 1.4
FPS, WD, HT = 24, 1080, 1920

def wt(line, word):            # absolute time of a word
    return ST[line] + T["T"][line][word]

# (out_start, out_end, clip, src_in, src_out, push_in) ; src span is stretched to fit (slow-mo when longer)
REVEAL = ST[3]
EDL = [
    (0.0,        1.75,     "c01", 6.0, 7.75, True),    # 1969: truck on the mountain road in rain
    (1.75,       3.30,     "c01", 0.10, 1.45, False),  # lightning hits the truck (ring on "truck"); cut before the fake fireball (~1.6 s)
    (3.30,       ST[1],    "c02", 0.30, 2.10, True),   # inside the cab, white flash
    (ST[1],      wt(1, 5), "c03", 4.0, 6.4, True),     # close: smoke from singed hair
    (wt(1, 5),   ST[2],    "c03", 0.0, 2.2, True),     # knocked out
    (ST[2],      wt(2, 6), "c04", 0.0, 1.2, False),    # truck rolls (arrow) - before the tip-over
    (wt(2, 6),   REVEAL,   "c05", 0.6, 1.55, False),   # tire stops at the edge (edge glow on "cliff")
    (REVEAL,     ST[3] + 1.4, "c05", 4.0, 5.4, True),  # HARD CUT: truck holds at the edge, flashes
    (ST[3] + 1.4, ST[4],   "c06", 0.0, 2.3, True),     # he stands alive, looks up
    (ST[4],      ST[5],    "c13", 4.0, 6.6, True),     # back view facing the storm: x7
    (ST[5],      ST[6],    "c07", 0.0, 1.3, True),     # 1942 tower
    (ST[6],      ST[7],    "c09", 0.0, 1.3, False),    # 1970 yard
    (ST[7],      ST[8],    "c10", 0.0, 1.6, True),     # 1972 ranger station
    (ST[8],      ST[9],    "c11", 0.3, 1.5, False),    # 1977 fishing
    (ST[9],      ST[10],   "c12", 0.0, 3.3, True),     # survived every one
    (ST[10],     wt(10, 5), "c06", 2.3, 3.9, True),    # his face to the storm (hat still in hand)
    (wt(10, 5),  END,      "c13", 0.0, 2.2, True),     # ending: puts his hat on and faces the storm (cut before the hat glitch)
]
WHIP = {1, 2, 3, 4, 5, 6}          # act 1: these EDL starts get a whip-blur join (no hard cut look)

def build_base(out):
    inputs, chains = [], []
    for i, (a, b, c, s0, s1, push) in enumerate(EDL):
        inputs += ["-i", str(V / f"{c}.mp4")]
        d = b - a; k = d / (s1 - s0)
        f = (f"[{i}:v]trim={s0}:{s1},setpts=PTS-STARTPTS,scale={WD}:{HT}:force_original_aspect_ratio=increase,crop={WD}:{HT},setsar=1,"
             f"setpts={k:.4f}*PTS,fps={FPS},trim=duration={d:.4f}")
        if push:
            f += f",scale=w='{WD}*(1+0.05*t/{d:.3f})':h='{HT}*(1+0.05*t/{d:.3f})':eval=frame,crop={WD}:{HT}"
        f += ",eq=brightness=0.03:contrast=1.06:saturation=1.08"   # lift the storm a little (reference is bright daylight)
        chains.append(f + f"[v{i}]")
    cat = "".join(f"[v{i}]" for i in range(len(EDL))) + f"concat=n={len(EDL)}:v=1:a=0[vid]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + [cat]), "-map", "[vid]", "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(out)], check=True)

def glow_line(img, pts, t01, col=(255, 255, 255)):
    lay = np.zeros_like(img); pts = np.array(pts, np.int32)
    cv2.polylines(lay, [pts], False, col, 10, cv2.LINE_AA)
    g = cv2.GaussianBlur(lay, (0, 0), 14)
    return cv2.addWeighted(img, 1.0, cv2.add(g, lay), 0.9 * t01, 0)

def ring(img, c, ax, t01, col=(40, 215, 255)):          # BGR yellow
    lay = np.zeros_like(img)
    cv2.ellipse(lay, c, ax, 0, 0, 360, col, 9, cv2.LINE_AA)
    g = cv2.GaussianBlur(lay, (0, 0), 12)
    return cv2.addWeighted(img, 1.0, cv2.add(g, lay), t01, 0)

def arrow(img, p0, p1, grow):                           # animated dashed arrow p0 -> p1
    p0, p1 = np.array(p0, float), np.array(p1, float); end = p0 + (p1 - p0) * grow
    lay = np.zeros_like(img); L = np.linalg.norm(end - p0); u = (p1 - p0) / np.linalg.norm(p1 - p0)
    s = 0.0
    while s < L - 30:
        a = p0 + u * s; b = p0 + u * min(s + 34, L - 30)
        cv2.line(lay, tuple(a.astype(int)), tuple(b.astype(int)), (255, 255, 255), 12, cv2.LINE_AA); s += 58
    n = np.array([-u[1], u[0]])
    tri = np.array([end, end - u * 60 + n * 38, end - u * 60 - n * 38], np.int32)
    cv2.fillPoly(lay, [tri], (255, 255, 255), cv2.LINE_AA)
    g = cv2.GaussianBlur(lay, (0, 0), 10)
    return cv2.add(img, cv2.add((g * 0.8).astype(np.uint8), lay))

def whip(img, s):                                       # horizontal motion blur + small shift, s in 0..1
    if s <= 0.01: return img
    k = int(9 + 80 * s) | 1; ker = np.zeros((1, k), np.float32); ker[0, :] = 1.0 / k
    out = cv2.filter2D(img, -1, ker)
    M = np.float32([[1 + 0.06 * s, 0, -WD * 0.03 * s - 40 * s], [0, 1 + 0.06 * s, -HT * 0.03 * s]])
    return cv2.warpAffine(out, M, (WD, HT), borderMode=cv2.BORDER_REFLECT)

def post(base, out):
    cap = cv2.VideoCapture(str(base))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WD}x{HT}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    joins = [EDL[i][0] for i in WHIP]
    seg = lambda t: max(i for i, e in enumerate(EDL) if e[0] <= t + 1e-6)
    i = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        t = i / FPS; k = seg(t); a, b = EDL[k][0], EDL[k][1]; i += 1
        if k == 1:                                     # ring on the truck from "hit" to the end of the shot
            t0 = wt(0, 4); p = min(1, max(0, (t - t0) / 0.25)) * (0.75 + 0.25 * math.sin(t * 18))
            if t >= t0: f = ring(f, (int(0.51 * WD), int(0.745 * HT)), (120, 88), p)
        if k == 5:                                     # roll arrow toward the drop
            f = arrow(f, (int(0.60 * WD), int(0.63 * HT)), (int(0.22 * WD), int(0.74 * HT)), min(1, (t - a) / 0.7))
        if k == 6:                                     # cliff edge glow on "cliff"
            t0 = wt(2, 6) - 0.05; p = min(1, max(0, (t - t0) / 0.2))
            f = glow_line(f, [(int(0.42 * WD), int(0.615 * HT)), (int(0.62 * WD), int(0.600 * HT)), (WD, int(0.585 * HT))], p)
        for j in joins:                                # whip-blur joins: 4 frames each side
            dt = t - j
            if -4 / FPS <= dt < 4 / FPS: f = whip(f, 1 - abs(dt) / (4 / FPS))
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
Style: Year,DejaVu Sans,120,&H0028D7FF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,4,8,60,60,250,1
Style: Strike,DejaVu Sans,64,&H00FFFFFF,&H000000FF,&H001C1C1C,&HB0000000,1,0,0,0,100,100,2,0,3,16,0,8,60,60,250,1
Style: Big,DejaVu Sans,260,&H0028D7FF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,10,6,5,60,60,0,1
Style: Tag,DejaVu Sans,26,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,3,8,0,7,40,40,60,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = []
    def line(a, b, st, tx, layer=0): ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{st},,0,0,0,,{tx}")
    pop = "{\\fscx60\\fscy60\\t(0,120,\\fscx100\\fscy100)}"
    line(0.0, END, "Tag", "AI RECONSTRUCTION")   # real person + real events -> small on-screen label (authenticity-check item 3)
    line(0.05, 1.75, "Year", pop + "1969")
    line(wt(3, 9) - 0.05, ST[4], "Strike", pop + "STRIKE #2")                     # "second"
    line(wt(4, 6) - 0.05, ST[5], "Big", pop + "×7")                               # "seven"
    for li, tx in ((5, "#1 · 1942"), (6, "#3 · 1970"), (7, "#4 · 1972"), (8, "#7 · 1977")):
        line(ST[li], ST[li + 1], "Strike", pop + tx)
    line(wt(9, 1), ST[10], "Strike", pop + "7 / 7 SURVIVED")
    # captions: 1-3 words per group from the alignment
    ch = [(r["char"], float(r["start"]), float(r["end"])) for r in csv.DictReader(open(W / "lumean/alignment.csv"))]
    words, cur, s0, pb = [], "", None, 0
    for c, a, b in ch:
        if c == " ":
            if cur: words.append((cur, s0, pb)); cur, s0 = "", None
            continue
        if s0 is None: s0 = a
        cur += c; pb = b
    if cur: words.append((cur, s0, pb))
    g, pos = [], 0
    for ln in script_su.LINES:
        lw = words[pos:pos + len(ln.split())]; pos += len(ln.split())
        k = 0
        while k < len(lw):
            n = 3 if len(lw) - k > 4 else (2 if len(lw) - k == 4 else len(lw) - k)
            grp = lw[k:k + n]; k += n
            g.append((" ".join(w[0] for w in grp), grp[0][1], grp[-1][2]))
    for k, (txt, a, b) in enumerate(g):
        nb = g[k + 1][1] if k + 1 < len(g) else END
        lift = "{\\pos(540,1180)}" if 1.75 <= a < 3.3 else ""      # keep the caption off the ringed truck
        line(a, min(nb, b + 0.3), "Cap", lift + txt.replace("nineteen sixty-nine,", "1969,"), 1)
    Path(path).write_text(hdr + "\n".join(ev), encoding="utf-8")

def thunder(n, sr, at, rng, big=1.0):
    x = np.zeros(n); i0 = int(at * sr); L = min(int(2.8 * sr), n - i0)
    if L <= 0: return x
    k = np.arange(L) / sr; noise = rng.standard_normal(L)
    crack = noise * np.exp(-k * 18) * 0.9
    rumble = np.convolve(noise, np.ones(220) / 220, mode="same") * 9 * np.exp(-k * 1.4) * (1 - np.exp(-k * 25))
    x[i0:i0 + L] = (crack + rumble) * 0.5 * big
    return x

def bed(total):
    sr = 44100; n = int(total * sr) + sr; rng = np.random.default_rng(7); t = np.arange(n) / sr
    rain = np.convolve(rng.standard_normal(n), np.ones(6) / 6, mode="same") * 0.035 * np.clip(1 - (t - ST[9]) / 2, 0.25, 1)
    mus = music(total, ST, T["T"], dark=(REVEAL, ST[9]), stings=[(3, 9), (4, 6), (9, 1)])[:n]
    mus = np.pad(mus, (0, max(0, n - len(mus))))
    mus[: int(REVEAL * sr)] *= 1.0                        # act 1 at full bed level (the reveal is marked by the sub hit + sting)
    sfx = np.zeros(n)
    for at, big in ((1.75 + (1.0 - 0.10) * 1.148, 1.0), (3.30 + 1.2, 0.6), (ST[5] + 0.1, 0.8), (ST[6] + 0.1, 0.7),
                    (ST[7] + 0.1, 0.7), (ST[8] + 0.15, 0.8), (wt(10, 5) + 0.4, 0.4)):
        sfx += thunder(n, sr, at, rng, big)
    i0 = int(REVEAL * sr); kk = np.arange(int(0.8 * sr)) / sr              # sub hit on the reveal cut
    sfx[i0:i0 + len(kk)] += np.sin(2 * np.pi * 42 * kk) * np.exp(-kk * 4) * 0.7
    return rain + mus + sfx

def write_wav(x, path):
    import wave
    x = np.clip(x / max(1e-9, np.abs(x).max()) * 0.9, -1, 1); w = wave.open(str(path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()

if __name__ == "__main__":
    assert abs(EDL[-1][1] - END) < 1e-6
    for a, b, c, s0, s1, _ in EDL: assert b > a and s1 <= 8.0, (c, a, b)
    build_base(W / "su_base.mp4"); post(W / "su_base.mp4", W / "su_video.mp4")
    build_ass(W / "su.ass"); write_wav(bed(END), W / "bed.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "su_video.mp4"), "-i", str(W / "lumean/result.mp3"), "-i", str(W / "bed.wav"),
        "-filter_complex", f"[0:v]ass={W / 'su.ass'}[v];[1:a]aresample=44100,asplit[vo][sc];[2:a]volume=0.62[bed];"
        "[bed][sc]sidechaincompress=threshold=0.06:ratio=3:attack=20:release=300[duck];[vo][duck]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
        "-map", "[v]", "-map", "[a]", "-t", f"{END:.2f}", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(W / "su_final.mp4")], check=True)
    print("done", round(END, 2), "s")
