"""Stonehenge Short: AI reconstruction clips (/home/claude/v85/clips), voice (/home/claude/v85/lumean), 1-3 word captions at ~77 % height,
number chips on the facts, small "AI RECONSTRUCTION" tag, own synth bed (music_lb) ducked under the voice. Output /home/claude/v85/st_final.mp4"""
import csv
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/ai_lifeboat_2026_10_25"); sys.path.insert(0, str(Path(__file__).parent))
import script_st
from music_lb import music

V, W = Path("/home/claude/v85/clips"), Path("/home/claude/v85")
T = json.load(open(W / "timing.json")); ST, D = T["starts"], T["D"]
END = ST[-1] + D[-1] + 1.2
FPS, WD, HT = 24, 1080, 1920

# (out_start, out_end, clip, src_in, src_out, push_in, saturation)
EDL = [
    (0.0,          ST[1],        "c01", 0.0, 4.3, True, 1.08),    # hook: the finished circle, people with hammers and ropes
    (ST[1],        ST[2],        "c03", 0.0, 3.6, False, 1.08),   # stone on its sledge (25 km chip)
    (ST[2],        ST[3],        "c05", 0.0, 2.8, True, 1.08),    # giant stone close (25 t chip)
    (ST[3],        ST[4],        "c03", 3.6, 7.6, True, 1.08),    # sledge over timber rails
    (ST[4],        ST[4] + 1.9,  "c04", 0.0, 3.0, False, 1.08),   # slides into the pit (cut before the shape changes ~4.5 s)
    (ST[4] + 1.9,  ST[5],        "c05", 3.8, 6.0, False, 1.08),   # hauled upright
    (ST[5],        ST[6],        "c06", 0.0, 4.1, True, 1.08),    # lintel on the timber crib
    (ST[6],        ST[7],        "c07", 1.0, 5.0, False, 0.72),   # Wales: desaturate the too-blue stone
    (ST[7],        ST[8],        "c08", 0.0, 2.7, False, 1.08),   # Altar Stone (Scotland chip)
    (ST[8],        END,          "c08", 4.3, 8.0, False, 1.08),   # question over the sunrise
]


def build_base(out):
    inputs, chains = [], []
    for i, (a, b, c, s0, s1, push, sat) in enumerate(EDL):
        inputs += ["-i", str(V / f"{c}.mp4")]
        d = b - a; k = d / (s1 - s0)
        f = (f"[{i}:v]trim={s0}:{s1},setpts=PTS-STARTPTS,scale={WD}:{HT}:force_original_aspect_ratio=increase,crop={WD}:{HT},setsar=1,"
             f"setpts={k:.4f}*PTS,fps={FPS},trim=duration={d:.4f}")
        if push:
            f += f",scale=w='{WD}*(1+0.05*t/{d:.3f})':h='{HT}*(1+0.05*t/{d:.3f})':eval=frame,crop={WD}:{HT}"
        f += f",eq=contrast=1.06:saturation={sat}"
        chains.append(f + f"[v{i}]")
    cat = "".join(f"[v{i}]" for i in range(len(EDL))) + f"concat=n={len(EDL)}:v=1:a=0[vid]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + [cat]), "-map", "[vid]", "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", str(out)], check=True)


def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def words():
    ch = [(r["char"], float(r["start"]), float(r["end"])) for r in csv.DictReader(open(W / "lumean/alignment.csv"))]
    out, cur, s0, pb = [], "", None, 0
    for c, a, b in ch:
        if c == " ":
            if cur:
                out.append((cur, s0, pb)); cur, s0 = "", None
            continue
        if s0 is None:
            s0 = a
        cur += c; pb = b
    if cur:
        out.append((cur, s0, pb))
    return out


def build_ass(path):
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,64,&H00FFFFFF,&H000000FF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,1,4,4,2,60,60,430,1
Style: Chip,DejaVu Sans,70,&H00FFFFFF,&H000000FF,&H001C1C1C,&HB0000000,1,0,0,0,100,100,2,0,3,18,0,8,60,60,260,1
Style: Tag,DejaVu Sans,26,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,3,8,0,7,40,40,60,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = []
    def line(a, b, st, tx, layer=0):
        ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{st},,0,0,0,,{tx}")
    pop = "{\\fscx60\\fscy60\\t(0,120,\\fscx100\\fscy100)}"
    line(0.0, END, "Tag", "AI RECONSTRUCTION")
    w = words()
    lw, pos = [], 0
    for ln in script_st.LINES:
        n = len(ln.split()); lw.append(w[pos:pos + n]); pos += n
    line(0.05, ST[1], "Chip", pop + "≈ 2500 BC")
    line(lw[1][6][1], ST[2], "Chip", pop + "25 KM")                       # "twenty-five" (kilometres)
    line(lw[2][4][1], ST[3], "Chip", pop + "≈ 25 TONNES")
    line(lw[6][6][1], ST[7], "Chip", pop + "WALES · 220+ KM")             # "over"
    line(lw[7][8][1], ST[8], "Chip", pop + "SCOTLAND · 700+ KM")          # "Scotland."
    g = []
    for ws_ in lw:
        k = 0
        while k < len(ws_):
            n = 3 if len(ws_) - k > 4 else (2 if len(ws_) - k == 4 else len(ws_) - k)
            grp = ws_[k:k + n]; k += n
            g.append((" ".join(x[0] for x in grp), grp[0][1], grp[-1][2]))
    rep = {"Forty-five": "45", "twenty-five": "25"}
    for k, (txt, a, b) in enumerate(g):
        nb = g[k + 1][1] if k + 1 < len(g) else END
        txt = " ".join(rep.get(x, x) for x in txt.split())
        line(a, min(nb, b + 0.3), "Cap", txt, 1)
    Path(path).write_text(hdr + "\n".join(ev), encoding="utf-8")


def write_wav(x, path):
    import wave
    x = np.clip(x / max(1e-9, np.abs(x).max()) * 0.9, -1, 1); w = wave.open(str(path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()


if __name__ == "__main__":
    for a, b, c, s0, s1, *_ in EDL:
        assert b > a and s1 <= 8.0, (c, a, b)
    build_base(W / "st_base.mp4")
    build_ass(W / "st.ass")
    write_wav(music(END, ST, T["T"], dark=(ST[7], ST[8] + 0.5), stings=[(1, 3), (7, 6), (8, 5)]), W / "bed.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "st_base.mp4"), "-i", str(W / "lumean/result.mp3"), "-i", str(W / "bed.wav"),
        "-filter_complex", f"[0:v]ass={W / 'st.ass'}[v];[1:a]aresample=44100,asplit[vo][sc];[2:a]volume=0.62[bed];"
        "[bed][sc]sidechaincompress=threshold=0.06:ratio=3:attack=20:release=300[duck];[vo][duck]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
        "-map", "[v]", "-map", "[a]", "-t", f"{END:.2f}", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(W / "st_final.mp4")], check=True)
    print("done", round(END, 2), "s")
