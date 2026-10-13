"""Vertical Short from cruise clips. python3 engine25s.py base | video out.mp4"""
import json, math, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script25s import LINES
W, H, FPS = 1080, 1920, 30
TM = json.load(open("timing.json")); D, TW = TM["D"], TM["T"]
LEAD = 0.2; ST = [LEAD + s for s in TM["starts"]]; TOTAL = ST[-1] + D[-1] + 0.8
CL = "/home/claude/v25/clips/"
SHOTS = [["departing_aerial", "money_count"], ["phone_sunset", "ocean_cruise", "texting_night"], ["phone_typing", "sea_from_ship"],
         ["cocktail_bar", "cocktails", "woman_cocktail"], ["coins", "family_arriving", "card_terminal"], ["balcony_sunset"]]
NUM = {1: 1, 3: 2, 4: 3}
YEL, WHT, BLK, INK = (255, 213, 0), (255, 255, 255), (0, 0, 0), (20, 20, 20)
_F = {}
def font(p, s):
    k = (p, int(s))
    if k not in _F: _F[k] = ImageFont.truetype(p, max(8, int(s)))
    return _F[k]
def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def back(x):
    x = min(1.0, max(0.0, x)); return 1 + 2.7 * (x - 1) ** 3 + 1.7 * (x - 1) ** 2
SPAN = [(0.0 if i == 0 else ST[i] - 0.1, ST[i + 1] - 0.1 if i + 1 < len(LINES) else TOTAL) for i in range(len(LINES))]
def base():
    segs = []; os.makedirs("seg", exist_ok=True); n = 0
    for i, keys in enumerate(SHOTS):
        a, b = SPAN[i]; d = b - a; k = max(len(keys), math.ceil(d / 2.2))
        for j in range(k):
            sa, sb = a + d * j / k, a + d * (j + 1) / k
            fr = round(sb * FPS) - round(sa * FPS); key = keys[j % len(keys)]
            out = f"seg/v{n:03d}.mp4"; segs.append(out); n += 1
            vf = f"scale=-2:2050,crop=1080:1920:x='(iw-1080)/2+40*sin(t)':y='65*t/{sb - sa:.2f}',eq=saturation=1.12:contrast=1.05,fps={FPS}"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{1.0 + j * 2.5:.1f}", "-i", CL + key + ".mp4", "-vf", vf, "-frames:v", str(fr), "-an",
                            "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], check=True)
    open("seg_list.txt", "w").write("".join(f"file {x}\n" for x in segs))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", "seg_list.txt", "-c", "copy", "base.mp4"], check=True)
def sticky(n, sc):
    s = int(190 * sc); im = Image.new("RGBA", (s + 40, s + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((26, 30, 26 + s, 30 + s), fill=(0, 0, 0, 100)); d.rectangle((18, 18, 18 + s, 18 + s), fill=YEL + (255,))
    d.text((18 + s / 2, 18 + s / 2 + 5 * sc), f"#{n}", font=font("Poppins-ExtraBold.ttf", 96 * sc), fill=INK, anchor="mm")
    return im.rotate(-5, resample=Image.BICUBIC, expand=True)
def overlay(t):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    i = max(j for j in range(len(LINES)) if SPAN[j][0] <= t); lt = t - SPAN[i][0]
    if i == 0:
        k = back(lt / 0.4)
        for q, (s, col) in enumerate((("3 CRUISE MISTAKES", WHT), ("THAT COST YOU MONEY", YEL))):
            f = font("Poppins-ExtraBold.ttf", 96 * max(0.3, k) if q == 0 else 78 * max(0.3, back((lt - 0.3) / 0.4)))
            d.text((W / 2, 430 + q * 120), s, font=f, fill=col, anchor="mm", stroke_width=10, stroke_fill=BLK)
    cur = max([NUM[j] for j in NUM if SPAN[j][0] <= t and j <= i] or [0])
    if cur and i < 5:
        j0 = [j for j in NUM if NUM[j] == cur][0]
        st = sticky(cur, back((t - SPAN[j0][0]) / 0.4)); lay.alpha_composite(st, (W // 2 - st.width // 2, 300))
    if i == 5:
        f = font("Poppins-ExtraBold.ttf", 84)
        d.text((W / 2, 520), "WHICH ONE", font=f, fill=WHT, anchor="mm", stroke_width=10, stroke_fill=BLK)
        d.text((W / 2, 630), "GOT YOU? 👇".replace(" 👇", ""), font=f, fill=YEL, anchor="mm", stroke_width=10, stroke_fill=BLK)
    for q in range(len(LINES)):
        if ST[q] - 0.05 <= t < ST[q] + D[q] + 0.15:
            ws = LINES[q].split(); cur_w = 0
            for j, o in enumerate(TW[q]):
                if t >= ST[q] + o - 0.05: cur_w = j
            c0 = cur_w // 3 * 3; chunk = ws[c0:c0 + 3]
            f = font("Poppins-ExtraBold.ttf", 82); gap = f.getlength(" ") * 1.5
            wl = [f.getlength(w.upper()) for w in chunk]; tot = sum(wl) + gap * (len(chunk) - 1)
            if tot > W - 80:
                f = font("Poppins-ExtraBold.ttf", 82 * (W - 80) / tot); gap = f.getlength(" ") * 1.5
                wl = [f.getlength(w.upper()) for w in chunk]; tot = sum(wl) + gap * (len(chunk) - 1)
            x = (W - tot) / 2
            for j, (w, ww) in enumerate(zip(chunk, wl)):
                d.text((x, 1380), w.upper(), font=f, fill=YEL if c0 + j == cur_w else WHT, anchor="lm", stroke_width=10, stroke_fill=BLK); x += ww + gap
            break
    return lay
def video(out):
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", "base.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    o = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "mix.wav",
                          "-c:v", "libx264", "-crf", "19", "-maxrate", "6000k", "-bufsize", "12000k", "-preset", "medium", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    sz = W * H * 3; fi = 0
    while True:
        b = p.stdout.read(sz)
        if len(b) < sz: break
        im = Image.frombytes("RGB", (W, H), b).convert("RGBA"); im.alpha_composite(overlay(fi / FPS)); o.stdin.write(im.convert("RGB").tobytes()); fi += 1
    o.stdin.close(); o.wait(); print("frames", fi)
if __name__ == "__main__":
    {"base": base, "video": lambda: video(sys.argv[2])}[sys.argv[1]]()
