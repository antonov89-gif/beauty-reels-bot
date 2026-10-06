"""Vertical 9:16 Shorts cut from the long AI video: python3 shorts14.py NAME  (no paid services used)"""
import subprocess, sys, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import engine14 as E

SHORTS = {
    "s1_curve": dict(lines=(3, 7), title=["WHY AI IS MOVING", "SO FAST"]),
    "s2_voice": dict(lines=(22, 25), title=["AI VOICE SCAMS:", "ONE FREE DEFENSE"]),
    "s3_jobs": dict(lines=(38, 42), title=["IS AI TAKING", "ENTRY-LEVEL JOBS?"]),
    "s4_agi": dict(lines=(43, 46), title=["WHEN WILL", "AGI ARRIVE?"]),
}
VW, VH = 1080, 1920
CUES = E.build_cues(5)
_bg_cache = {}


def window(name):
    a, b = SHORTS[name]["lines"]
    t0 = max(0.0, E.starts[a] - 0.3)
    t1 = E.starts[b] + E.D[b] + 0.5
    return t0, t1


def vframe(fi, name):
    t = fi / E.FPS
    src = E.frame(fi, subs=False).convert("RGB")
    bg = src.resize((int(E.W * VH / E.H), VH), Image.BILINEAR)
    x0 = (bg.width - VW) // 2
    bg = bg.crop((x0, 0, x0 + VW, VH)).filter(ImageFilter.GaussianBlur(36))
    bg = Image.blend(Image.new("RGB", (VW, VH), (14, 24, 44)), bg, 0.30).convert("RGBA")
    fg = src.resize((VW, int(VW * 9 / 16)), Image.BILINEAR).convert("RGBA")
    fy = 640
    d = ImageDraw.Draw(bg)
    d.rectangle((0, fy - 4, VW, fy + fg.height + 4), fill=(0, 0, 0, 255))
    bg.alpha_composite(fg, (0, fy))
    d = ImageDraw.Draw(bg)
    for q, line in enumerate(SHORTS[name]["title"]):
        d.text((VW // 2, 240 + q * 120), line, font=E.font(112, "Bold"), fill=(255, 205, 60) if q else (255, 255, 255),
               anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    for t0, t1, txt in CUES:
        if t0 <= t < t1:
            f = E.font(74, "Bold")
            lines = E.wrap(txt, f, 960)
            for q, l in enumerate(lines):
                d.text((VW // 2, 1500 + q * 92), l, font=f, fill=(255, 255, 255), anchor="mm", stroke_width=7,
                       stroke_fill=(0, 0, 0))
            break
    return bg.convert("RGB")


if __name__ == "__main__":
    name = sys.argv[1]
    t0, t1 = window(name)
    a, b = int(t0 * E.FPS), int(t1 * E.FPS)
    out = f"{name}_silent.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}",
                          "-r", str(E.FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt",
                          "yuv420p", out], stdin=subprocess.PIPE)
    for fi in range(a, b):
        p.stdin.write(vframe(fi, name).tobytes())
        if (fi - a) % 120 == 0:
            print(name, fi - a, "/", b - a, flush=True)
    p.stdin.close()
    p.wait()
    dur = (b - a) / E.FPS
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-ss", f"{a / E.FPS:.3f}", "-t", f"{dur:.3f}", "-i",
                    "mix.wav", "-map", "0:v", "-map", "1:a", "-af", f"afade=t=in:d=0.15,afade=t=out:st={dur - 0.5:.2f}:d=0.5",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{name}.mp4"], check=True)
    print("done", name, round(dur, 1), "s")
