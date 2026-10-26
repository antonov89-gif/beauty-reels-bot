"""Tristan Short v2 (hook with the stake, shorter, ends with a viewer question). Output /home/claude/v76/tr2_final.mp4"""
import json, subprocess, sys, math, csv
from pathlib import Path
import numpy as np
sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/ai_lifeboat_2026_10_25"); sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/tristan_fiction_2026_10_26")
import build_lb as bl, script_tr2
from music_lb import music
W = Path("/home/claude/v76"); bl.W = W; bl.V = Path("/home/claude/v74")
T = json.load(open(W / "timing.json")); ST, D = T["starts"], T["D"]; bl.T, bl.ST, bl.D = T, ST, D
bl.CROP, bl.SLOW = {}, {}
END = ST[-1] + D[-1] + 1.3
PLAN = [[("c01", 0.0), ("c12", 0.8)], [("c01", 3.5), ("c02", 0.3)], [("c02", 4.8), ("c03", 0.5)], [("c03", 3.0)], [("c04", 3.5)], [("c05", 0.5), ("c06", 1.0)],
        [("c07", 0.5), ("c06", 4.0)], [("c08", 0.5)], [("c09", 1.0)], [("c10", 0.5), ("c11", 0.5)], [("c11", 3.0)]]
CUTS = []
for i, shots in enumerate(PLAN):
    a = ST[i] if i else 0.0; b = ST[i + 1] if i + 1 < len(ST) else END
    span = (b - a) / len(shots)
    for clip, s in shots:
        assert s + span <= 8.0, (clip, s, span)
        CUTS.append((clip, round(s, 2), round(s + span, 2)))
bl.CUTS = CUTS
def build_ass(path):
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,Bowlby One,64,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,6,2,2,60,60,300,1
Style: Year,Bowlby One,112,&H0000D6FF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,8,2,8,60,60,260,1
Style: Ask,Bowlby One,120,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,9,2,5,60,60,0,1
Style: Tag,Bowlby One,28,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,3,8,0,7,40,40,60,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = []
    def line(a, b, st, tx): ev.append(f"Dialogue: 0,{bl.ts(a)},{bl.ts(b)},{st},,0,0,0,,{tx}")
    line(0.0, END, "Tag", "FICTION · BASED ON REAL EVENTS · TRISTAN DA CUNHA, 1961")
    line(0.15, ST[1] - 0.2, "Year", "264 PEOPLE\\N1 NIGHT")
    line(ST[8] - 0.1, ST[8] + 2.0, "Year", "1963")
    line(ST[10] - 0.1, END, "Ask", "WOULD YOU\\NGO BACK?")
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
    for i, ln in enumerate(script_tr2.LINES):
        n = len(ln.split()); lw = words[pos:pos + n]; pos += n
        if i == 10: continue                      # last line is the on-screen question
        per = math.ceil(n / math.ceil(n / 3))
        for k in range(0, n, per):
            grp = lw[k:k + per]; g.append((" ".join(w[0] for w in grp), grp[0][1], grp[-1][2]))
    for k, (txt, a, b) in enumerate(g):
        nb = g[k + 1][1] if k + 1 < len(g) else END
        line(a, min(nb, b + 0.35), "Cap", txt.upper())
    Path(path).write_text(hdr + "\n".join(ev), encoding="utf-8")
def bed(total):
    n = int(total * bl.sr()) + bl.sr(); t = np.arange(n) / bl.sr(); rng = np.random.default_rng(11)
    br = np.cumsum(rng.standard_normal(n)); br -= np.convolve(br, np.ones(4000) / 4000, mode="same"); br /= np.abs(br).max()
    ocean = br * (0.5 + 0.5 * np.sin(2 * np.pi * t / 8.0)) * 0.06
    mus = music(total, ST, T["T"], dark=(ST[6] - 1.2, ST[8] - 0.2), stings=[(2, 0), (5, 0), (8, 0), (10, 0)])[:n]
    mus = np.pad(mus, (0, max(0, n - len(mus)))); sfx = np.zeros(n); k = np.arange(60000) / bl.sr()
    sfx[:60000] += (np.sin(2 * np.pi * 38 * k) * 0.8 + rng.standard_normal(60000) * 0.05) * np.exp(-k * 2.2) * 0.5
    for at in (0.15, ST[8] - 0.1, ST[10] - 0.1):
        i0 = int(at * bl.sr()); kk = np.arange(30000) / bl.sr()
        if i0 + 30000 < n: sfx[i0:i0 + 30000] += np.sin(2 * np.pi * 52 * kk) * np.exp(-kk * 7) * 0.5
    return ocean + mus + sfx
if __name__ == "__main__":
    durs, total = bl.build_video(W / "tr2_video.mp4"); print("video", round(total, 2), "s,", len(CUTS), "shots; voice ends", round(ST[-1] + D[-1], 2))
    build_ass(W / "tr2.ass"); bl.write_wav(bed(max(total, END)), W / "bed.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "tr2_video.mp4"), "-i", str(W / "lumean/result.mp3"), "-i", str(W / "bed.wav"),
        "-filter_complex", f"[0:v]ass={W / 'tr2.ass'}:fontsdir=/home/claude/v38/fonts[v];[1:a]aresample=44100,asplit[vo][sc];[2:a]volume=0.30[bed];"
        "[bed][sc]sidechaincompress=threshold=0.06:ratio=3:attack=20:release=300[duck];[vo][duck]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
        "-map", "[v]", "-map", "[a]", "-t", f"{min(total, END):.2f}", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(W / "tr2_final.mp4")], check=True)
    print("done")
