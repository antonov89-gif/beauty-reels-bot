"""Lifeboat Short (Zack D. DNA, no maps): cut list from the 18 owner-generated AI clips + Lumean voice + ASS overlays + synthesised bed/SFX.
Run: python3 build_lb.py  (needs /home/claude/v72/S*.mp4 clips, /home/claude/v73/lumean/result.mp3, timing.json). Output /home/claude/v73/lb_final.mp4."""
import json, subprocess, math, wave
import numpy as np
from pathlib import Path

V = Path("/home/claude/v72"); W = Path("/home/claude/v73")
FONT = "/home/claude/v38/fonts/bowlby-one.ttf"
T = json.load(open(W / "timing.json"))
ST, D = T["starts"], T["D"]
END = 46.4

# (clip, in, out): output follows the voice lines; every shot is a real owner-generated clip
CUTS = [
    ("S03", 0.0, 1.9), ("S03", 3.4, 5.7),                     # L1 sinking ship (the narrator insert 1.9-3.4 is cut out)
    ("S04", 0.3, 3.8), ("S06", 1.0, 3.1),                     # L2 five seats / three captains
    ("S01", 3.0, 6.0), ("S06", 3.1, 4.95),                    # L3 three AIs on the monitor
    ("S07", 0.2, 5.15),                                       # L4 six in the water
    ("S10", 0.6, 2.85),                                       # L5 yes yes yes (captains nod)
    ("S09", 0.5, 4.8),                                        # L6 the family
    ("S17", 0.0, 2.9), ("S16", 3.0, 4.6),                     # L7 own child
    ("S11", 0.3, 3.2), ("S13", 0.5, 3.4),                     # L8 answers split
    ("S15", 0.5, 5.2),                                        # L9 did you contradict yourself
    ("S06", 4.4, 6.0),                                        # L10 all three said no
    ("S18", 4.0, 6.0),                                        # L11 the boat alone (slowed, letterbox + label cropped)
]
CROP = {"S13": "crop=iw:ih*0.94:0:0,", "S18": "crop=1080:1430:0:250,"}   # S13 bottom artefact strip, S18 burned-in label + bars
SLOW = {"S18": 3.3 / 2.0}
FPS = 24

def seg(i, c):
    n, a, b = c; d = b - a
    f = f"[{i}:v]trim={a}:{b},setpts=PTS-STARTPTS," + CROP.get(n, "") + "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24"
    if n in SLOW: f += f",setpts={SLOW[n]}*PTS"
    # gentle push-in on every shot so no frame is static
    dur = d * SLOW.get(n, 1)
    f += f",scale=w='1080*(1+0.04*t/{dur:.3f})':h='1920*(1+0.04*t/{dur:.3f})':eval=frame,crop=1080:1920"
    return f + f"[v{i}]", dur

def build_video(out):
    inputs, chains, durs = [], [], []
    for i, c in enumerate(CUTS):
        inputs += ["-i", str(V / f"{c[0]}.mp4")]
        ch, d = seg(i, c); chains.append(ch); durs.append(d)
    total = sum(durs)
    cat = "".join(f"[v{i}]" for i in range(len(CUTS))) + f"concat=n={len(CUTS)}:v=1:a=0[vid]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + [cat]), "-map", "[vid]", "-r", "24", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(out)], check=True)
    return durs, total

def ts(t):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def build_ass(path):
    # ASS colours are &HBBGGRR&
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,Bowlby One,64,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,6,2,2,60,60,300,1
Style: Q,Bowlby One,58,&H0000D6FF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,6,2,8,60,60,230,1
Style: Chip,Bowlby One,54,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,3,14,0,5,60,60,0,1
Style: Stamp,Bowlby One,30,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,3,8,0,2,40,40,150,1
Style: Tag,Bowlby One,30,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,3,8,0,7,40,40,60,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = []
    def line(a, b, style, text, layer=0, pos=None):
        t = (f"{{\\pos({pos[0]},{pos[1]})}}" if pos else "") + text
        ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{t}")
    # persistent labels (AI disclosure + real-answers stamp)
    # on-screen AI tag removed at the owner's request (26.10); disclosure stays in the description and platform flags
    line(0.3, END, "Stamp", "AI answers are real: public API, 25-26 Oct 2026")
    # captions (voice words) in groups, from the Lumean alignment
    import csv, re
    ch = [(r["char"], float(r["start"]), float(r["end"])) for r in csv.DictReader(open(W / "lumean/alignment.csv"))]
    words, cur, s0 = [], "", None
    for c, a, b in ch:
        if c == " ":
            if cur: words.append((cur, s0, pb)); cur, s0 = "", None
            continue
        if s0 is None: s0 = a
        cur += c; pb = b
    if cur: words.append((cur, s0, pb))
    g = []
    for i in range(0, len(words), 3):
        grp = words[i:i + 3]; g.append((" ".join(w[0] for w in grp), grp[0][1], grp[-1][2]))
    for k, (txt, a, b) in enumerate(g):
        nb = g[k + 1][1] if k + 1 < len(g) else END
        line(a, min(nb, b + 0.35), "Cap", txt.upper())
    # questions (top card)
    qs = [(ST[1], ST[1] + 4.4, "6 PEOPLE · 5 SEATS"), (ST[3] + 0.4, ST[4] - 0.2, "LEAVE ONE BEHIND?"), (ST[6] + 0.9, ST[7] - 0.1, "YOUR OWN CHILD?"), (ST[8], ST[9] + D[9], "DID YOU CONTRADICT YOURSELF?")]
    for a, b, t in qs: line(a, b, "Q", t)
    # answer chips (real answers), placed at the spoken words: three chips stacked at the vertical middle
    def word_t(line_i, w_i): return ST[line_i] + T["T"][line_i][w_i]
    GREEN, RED, ORANGE = "&H0050B450&", "&H003C3CE0&", "&H000090FF&"
    def chips(line_i, answers, hold):
        # answers: [(label, colour)] spoken as 'ChatGPT: no. Gemini: no. Grok: no.' -> word idx 0, 2, 4
        for j, (lab, col) in enumerate(answers):
            a = word_t(line_i, j * 2)
            line(a, a + hold, "Chip", f"{{\\1c&H000000&\\3c{col}}}{lab}", layer=3, pos=(540, 1210 + j * 105))
    chips(2, [("GPT-5.5 · NO", RED), ("GEMINI 3.6 · NO", RED), ("GROK 4.6 · NO", RED)], 4.2)
    # L5 'Yes. Yes. Yes.' -> chips at each yes
    for j, (lab) in enumerate(["GPT-5.5 · YES", "GEMINI 3.6 · YES", "GROK 4.6 · YES"]):
        a = word_t(4, j); line(a, ST[4] + D[4] + 0.3, "Chip", f"{{\\1c&H000000&\\3c{GREEN}}}{lab}", layer=3, pos=(540, 1210 + j * 105))
    chips(7, [("GPT-5.5 · YES", GREEN), ("GEMINI 3.6 · NO", RED), ("GROK 4.6 · NO", RED)], 5.0)
    chips(9, [], 0)
    for j, lab in enumerate(["GPT-5.5 · NO", "GEMINI 3.6 · NO", "GROK 4.6 · NO"]):
        a = ST[9] + 0.15 * (j + 1); line(a, ST[9] + D[9] + 0.6, "Chip", f"{{\\1c&H000000&\\3c{RED}}}{lab}", layer=3, pos=(540, 1210 + j * 105))
    Path(path).write_text(hdr + "\n".join(ev), encoding="utf-8")
    return [t for t in ST]

def sr(): return 44100

def synth_audio(total, out):
    n = int(total * sr()); t = np.arange(n) / sr(); rng = np.random.default_rng(7)
    # ocean: filtered brown noise with slow swell
    br = np.cumsum(rng.standard_normal(n)); br -= np.convolve(br, np.ones(4000) / 4000, mode="same"); br /= np.abs(br).max()
    ocean = br * (0.55 + 0.45 * np.sin(2 * math.pi * t / 7.5)) * 0.10
    # tense pad: A minor drone (A1, E2, A2, C3) with slow tremolo, rises into the 'own child' line
    pad = sum(np.sin(2 * math.pi * f * t) * a for f, a in [(55, 0.5), (82.4, 0.35), (110, 0.3), (130.8, 0.18)]) * (0.55 + 0.45 * np.sin(2 * math.pi * t / 11.0))
    rise = np.clip((t - ST[6]) / 4.0, 0, 1) * np.clip((ST[8] - t) / 3.0 + 1, 0, 1)
    pad = pad * (0.10 + 0.10 * rise)
    # heartbeat under the whole piece, faster in the 'own child' section
    hb = np.zeros(n)
    tt = 0.0
    while tt < total:
        for off, amp in [(0, 1.0), (0.22, 0.7)]:
            i0 = int((tt + off) * sr())
            if i0 < n - 4000:
                k = np.arange(4000) / sr(); hb[i0:i0 + 4000] += np.sin(2 * math.pi * 52 * k) * np.exp(-k * 28) * amp * 0.16
        tt += 1.15 if tt < ST[6] else 0.8
    # SFX: a soft tick on every answer chip, a low hit at 'own child'
    sfx = np.zeros(n)
    def tick(at, f=880, a=0.16):
        i0 = int(at * sr()); k = np.arange(5000) / sr()
        if i0 < n - 5000: sfx[i0:i0 + 5000] += np.sin(2 * math.pi * f * k) * np.exp(-k * 38) * a
    def hit(at):
        i0 = int(at * sr()); k = np.arange(30000) / sr()
        if i0 < n - 30000: sfx[i0:i0 + 30000] += (np.sin(2 * math.pi * 45 * k) * 0.55 + rng.standard_normal(30000) * 0.06) * np.exp(-k * 6)
    for li, idxs in [(2, [0, 2, 4]), (4, [0, 1, 2]), (7, [0, 2, 4])]:
        for w in idxs: tick(ST[li] + T["T"][li][w], 880 if li != 7 else (660 if w else 880))
    for j in range(3): tick(ST[9] + 0.15 * (j + 1), 520, 0.14)
    hit(ST[6] + T["T"][6][3])          # 'changed'
    hit(ST[10] - 0.05)
    import sys; sys.path.insert(0, str(Path(__file__).parent)); from music_lb import music
    mus = music(total, ST, T['T'])[:n]
    mus = np.pad(mus, (0, max(0, n - len(mus))))
    bed = ocean * 0.6 + mus + hb * 0.5 + sfx
    return bed

def write_wav(x, path):
    x = np.clip(x, -1, 1); w = wave.open(str(path), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr()); w.writeframes((x * 32767).astype("<i2").tobytes()); w.close()

if __name__ == "__main__":
    W.mkdir(exist_ok=True)
    durs, total = build_video(W / "lb_video.mp4")
    print("video", round(total, 2), "s,", len(CUTS), "shots")
    build_ass(W / "lb.ass")
    bed = synth_audio(max(total, END), None)
    write_wav(bed, W / "bed.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "lb_video.mp4"), "-i", str(W / "lumean/result.mp3"), "-i", str(W / "bed.wav"),
        "-filter_complex",
        f"[0:v]ass={W / 'lb.ass'}:fontsdir=/home/claude/v38/fonts[v];"
        "[1:a]aresample=44100,volume=1.0,asplit[vo][sc];[2:a]volume=0.53[bed];"
        "[bed][sc]sidechaincompress=threshold=0.06:ratio=3:attack=20:release=300[duck];"
        "[vo][duck]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
        "-map", "[v]", "-map", "[a]", "-t", f"{min(total, END):.2f}", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(W / "lb_final.mp4")], check=True)
    print("done")
