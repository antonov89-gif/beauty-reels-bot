"""v22: 3D AI clips (WaveSpeed Kling/Seedream) + code overlays (captions, counters, cards). python3 engine22.py base | video"""
import subprocess, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import engine21 as E
W, H, FPS = E.W, E.H, E.FPS
WS = "ws/"
st = E.starts
def T(i, w=None): return E.WT(i, w)
# slots: (source, src_start, src_len, t0, t1, kind) kind: clip | kb(image or frame, push-in)
SL = [
 ("c1.mp4", 0.0, 2.75, 0.0, T(0, "one") + 0.0, "clip"),
 ("c1.mp4", 3.0, 1.3, T(0, "one"), st[1] - 0.06, "clip"),
 ("c_climb.mp4", 0.0, 3.0, st[1] - 0.06, st[2] - 0.06 - 1.52, "clip"),
 ("c_search.mp4", 0.0, 1.52, st[2] - 0.06 - 1.52, st[2] - 0.06, "clip"),
 ("c_throw.mp4", 0.0, 3.0, st[2] - 0.06, st[3] - 0.06, "clip"),
 ("c_shatter.mp4", 0.2, 1.84, st[3] - 0.06, st[4] - 0.06, "clip"),
 ("c_jars.mp4", 0.0, 3.0, st[4] - 0.06, st[4] + 2.95, "clip"),
 ("c_pull.mp4", 0.0, 3.0, st[4] + 2.95, st[5] - 0.06, "clip"),
 ("c_unroll.mp4", 0.0, 3.0, st[5] - 0.06, st[6] - 0.06, "clip"),
 ("c_unroll.mp4", 2.9, 0.1, st[6] - 0.06, st[7] - 0.06, "kb"),
 ("i_scale.jpg", 0, 0, st[7] - 0.06, st[8] - 0.06, "kb"),
 ("c_priceless.mp4", 0.0, 3.0, st[8] - 0.06, st[9] - 0.06, "clip"),
 ("i_caves.jpg", 0, 0, st[9] - 0.06, st[10] - 0.06, "kb"),
 ("c1.mp4", 3.0, 0.9, st[10] - 0.06, st[10] - 0.06 + 0.93, "clip"),
 ("c_throw.mp4", 1.0, 0.9, st[10] - 0.06 + 0.93, st[10] - 0.06 + 1.86, "clip"),
 ("c_jars.mp4", 1.5, 0.9, st[10] - 0.06 + 1.86, st[11] - 0.06, "clip"),
 ("c_end.mp4", 0.0, 3.0, st[11] - 0.06, E.TOTAL, "clip"),
]
def seg(i, s):
    src, a, ln, t0, t1, kind = s
    d = t1 - t0; out = f"seg_{i:02d}.mp4"; n = max(1, round(d * FPS))
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    if kind == "clip":
        spd = d / max(ln, 0.1)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a), "-t", str(ln), "-i", WS + src, "-vf", f"setpts={spd:.4f}*(PTS-STARTPTS),{vf},fps={FPS}", "-frames:v", str(n)]
    else:
        if src.endswith(".mp4"):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a), "-i", WS + src, "-frames:v", "1", "kb_tmp.png"], check=True); inp = "kb_tmp.png"
        else: inp = WS + src
        zp = f"scale=2160:3840,zoompan=z='1+0.18*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", inp, "-vf", zp, "-frames:v", str(n)]
    cmd += ["-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", out]
    subprocess.run(cmd, check=True); return out
def base():
    segs = [seg(i, s) for i, s in enumerate(SL)]
    open("seg_list.txt", "w").write("".join(f"file {s}\n" for s in segs))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", "seg_list.txt", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", "base.mp4"], check=True)
def txt(d, xy, s, f, fill, stroke=0, sf=(0, 0, 0, 255), anchor="mm"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sf)
def overlay(t):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    ease, back = E.ease, E.back
    if t < T(0, "one") + 0.5:
        k = back(t / 0.35); f = E.font("hand", 190 * max(0.3, k))
        txt(d, (W / 2, 330), "1947", f, (255, 244, 205, 255), 10, (40, 25, 10, 255))
    if st[5] - 0.06 <= t < st[6] - 0.06:
        k = ease((t - st[5] + 0.06) / 1.2); f = E.font("sans", 110, True)
        txt(d, (W / 2, 300), "{:,} years".format(int(2000 * k)), f, (255, 255, 255, 255), 8)
    if st[6] - 0.06 <= t < st[7] - 0.06:
        k = back((t - st[6] + 0.06) / 0.35)
        d.rounded_rectangle((90, 260, W - 90, 400), 32, fill=(255, 255, 255, 235))
        txt(d, (W / 2, 330), "oldest known copies", E.font("sans", 66 * max(0.5, k), True), (30, 25, 22, 255))
        txt(d, (W / 2, 1280), "of the Hebrew Bible", E.font("hand", 96), (255, 235, 190, 255), 6)
    if st[7] - 0.06 <= t < st[8] - 0.06:
        f = E.font("hand", 110)
        if t < T(7, "few") - 0.1: txt(d, (W / 2, 300), "the first sale...", f, (255, 255, 255, 255), 8, (60, 40, 20, 255))
        else:
            k = back((t - T(7, "few") + 0.1) / 0.35)
            d.rounded_rectangle((200, 230, W - 200, 400), 36, fill=(255, 255, 255, 240))
            txt(d, (W / 2, 315), "a few pounds", E.font("sans", 82 * max(0.5, k), True), (200, 60, 50, 255))
    if st[8] - 0.06 <= t < st[9] - 0.06:
        k = back((t - st[8] + 0.2) / 0.3)
        txt(d, (W / 2, 330), "priceless", E.font("hand", 190 * max(0.4, k)), (255, 214, 110, 255), 10, (70, 40, 10, 255))
    if st[9] - 0.06 <= t < st[10] - 0.06:
        k = ease((t - st[9] + 0.06) / 1.4)
        txt(d, (W / 2, 300), "{} caves".format(int(round(11 * k))), E.font("hand", 170), (255, 255, 255, 255), 10, (60, 40, 20, 255))
        if k > 0.9 and t > T(9, "eleven"): txt(d, (W / 2, 450), "≈ {:,} manuscripts".format(int(900 * min(1, (t - T(9, "eleven")) / 0.9))), E.font("sans", 62, True), (255, 230, 150, 255), 6)
    if st[10] - 0.06 <= t < st[11] - 0.06:
        txt(d, (W / 2, 260), "all because of", E.font("hand", 100), (255, 255, 255, 255), 8, (60, 40, 20, 255))
        if t > st[10] + 1.5: txt(d, (W / 2, 420), "one lost goat", E.font("hand", 150), (255, 90, 80, 255), 9, (60, 20, 10, 255))
    # captions: 1-3 words, bold white, black outline, bottom centre
    for i in range(len(E.LINES)):
        if st[i] - 0.05 <= t < st[i] + E.D[i] + 0.15:
            words = E.LINES[i].split(); cur = 0
            for j, o in enumerate(E.TW[i]):
                if t >= st[i] + o - 0.05: cur = j
            c0 = cur // 3 * 3; s = " ".join(words[c0:c0 + 3])
            f = E.font("sans", 100, True)
            while f.getlength(s) > W - 90: f = E.font("sans", f.size - 2, True)
            txt(d, (W / 2, H * 0.80), s, f, (255, 255, 255, 255), 9)
            break
    return lay
def video():
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", "base.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    o = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "mix.wav",
                          "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-maxrate", "5200k", "-bufsize", "10400k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", "dead_sea_goat_3d.mp4"], stdin=subprocess.PIPE)
    fi = 0; sz = W * H * 3
    while True:
        b = p.stdout.read(sz)
        if len(b) < sz: break
        im = Image.frombytes("RGB", (W, H), b).convert("RGBA")
        im.alpha_composite(overlay(fi / FPS)); o.stdin.write(im.convert("RGB").tobytes()); fi += 1
    o.stdin.close(); o.wait(); print("frames", fi)
if __name__ == "__main__":
    {"base": base, "video": video}[sys.argv[1]]()
