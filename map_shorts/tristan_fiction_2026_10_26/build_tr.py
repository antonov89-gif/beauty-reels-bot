"""Tristan Short: 11 voice lines over trimmed Veo clips (c01..c12), ASS captions + year pops, own music (music_lb.py), mix, loudnorm.
Run: python3 build_tr.py -> /home/claude/v75/tr_final.mp4"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/ai_lifeboat_2026_10_25")
import build_lb as bl
from music_lb import music
W = Path("/home/claude/v75"); bl.W = W; bl.V = Path("/home/claude/v74")
T = json.load(open(W / "timing.json")); ST, D = T["starts"], T["D"]; bl.T, bl.ST, bl.D = T, ST, D
bl.CROP, bl.SLOW = {}, {}
END = ST[-1] + D[-1] + 1.0
CUTS = [("c01", 0.0, 1.2), ("c12", 0.8, 3.1), ("c02", 0.3, 2.8), ("c02", 4.8, 7.3), ("c03", 0.5, 4.1), ("c04", 3.5, 6.2), ("c05", 0.5, 3.4),
        ("c06", 1.0, 3.9), ("c07", 0.5, 4.7), ("c08", 0.5, 3.5), ("c09", 1.0, 4.0), ("c10", 0.5, 4.1), ("c11", 0.5, 3.1)]
bl.CUTS = CUTS
FONTS = "/home/claude/v38/fonts"

def build_ass(path):
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,Bowlby One,64,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,6,2,2,60,60,300,1
Style: Year,Bowlby One,120,&H0000D6FF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,8,2,8,60,60,260,1
Style: Tag,Bowlby One,28,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,3,8,0,7,40,40,60,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = []
    def line(a, b, style, text): ev.append(f"Dialogue: 0,{bl.ts(a)},{bl.ts(b)},{style},,0,0,0,,{text}")
    line(0.0, END, "Tag", "FICTION · BASED ON REAL EVENTS · TRISTAN DA CUNHA, 1961")
    line(0.3, 3.0, "Year", "10 OCT 1961")
    line(ST[8] - 0.1, ST[8] + 2.2, "Year", "1963")
    import csv
    ch = [(r["char"], float(r["start"]), float(r["end"])) for r in csv.DictReader(open(W / "lumean/alignment.csv"))]
    words, cur, s0, pb = [], "", None, 0
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
    Path(path).write_text(hdr + "\n".join(ev), encoding="utf-8")

def bed(total):
    n = int(total * bl.sr()) + bl.sr(); t = np.arange(n) / bl.sr(); rng = np.random.default_rng(11)
    br = np.cumsum(rng.standard_normal(n)); br -= np.convolve(br, np.ones(4000) / 4000, mode="same"); br /= np.abs(br).max()
    ocean = br * (0.5 + 0.5 * np.sin(2 * np.pi * t / 8.0)) * 0.06
    mus = music(total, ST, T["T"], dark=(ST[5] - 1.2, ST[8] - 0.2), stings=[(1, 0), (4, 0), (7, 0), (10, 0)])[:n]
    mus = np.pad(mus, (0, max(0, n - len(mus))))
    sfx = np.zeros(n)
    k = np.arange(60000) / bl.sr()
    sfx[:60000] += (np.sin(2 * np.pi * 38 * k) * 0.8 + rng.standard_normal(60000) * 0.05) * np.exp(-k * 2.2) * 0.5   # volcano rumble at the start
    for at in (0.3, ST[8] - 0.1):                                                                                          # year pops
        i0 = int(at * bl.sr()); kk = np.arange(30000) / bl.sr()
        if i0 + 30000 < n: sfx[i0:i0 + 30000] += np.sin(2 * np.pi * 52 * kk) * np.exp(-kk * 7) * 0.5
    return ocean + mus + sfx

if __name__ == "__main__":
    durs, total = bl.build_video(W / "tr_video.mp4"); print("video", round(total, 2), "s,", len(CUTS), "shots; voice ends", round(ST[-1] + D[-1], 2))
    build_ass(W / "tr.ass")
    b = bed(max(total, END)); bl.write_wav(b, W / "bed.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "tr_video.mp4"), "-i", str(W / "lumean/result.mp3"), "-i", str(W / "bed.wav"),
        "-filter_complex", f"[0:v]ass={W / 'tr.ass'}:fontsdir={FONTS}[v];[1:a]aresample=44100,asplit[vo][sc];[2:a]volume=0.30[bed];"
        "[bed][sc]sidechaincompress=threshold=0.06:ratio=3:attack=20:release=300[duck];[vo][duck]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
        "-map", "[v]", "-map", "[a]", "-t", f"{min(total, END):.2f}", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(W / "tr_final.mp4")], check=True)
    print("done")
