"""Cruise Insider-style vertical Short: real-looking footage cut on words, yellow sticky numbers, white headers, running cost counter.
python3 engine26.py base | video out.mp4 | still t.."""
import json, math, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
from script26 import LINES
W, H, FPS = 1080, 1920, 30
TM = json.load(open("timing.json")); D, TW = TM["D"], TM["T"]
LEAD = 0.25; ST = [LEAD + s for s in TM["starts"]]; TOTAL = ST[-1] + D[-1] + 0.9
STOCK = "/home/claude/v25/clips/"
YEL, WHT, BLK, INK, GRN, RED = (255, 213, 0), (255, 255, 255), (0, 0, 0), (20, 20, 20), (70, 220, 120), (255, 80, 70)
def clean(w): return "".join(c for c in w.lower() if c.isalnum())
def WT(i, w, n=1):
    ws = [clean(x) for x in LINES[i].split()]; c = 0
    for j, x in enumerate(ws):
        if x == clean(w) or clean(w) in x:
            c += 1
            if c == n: return ST[i] + TW[i][j]
    raise KeyError(w)
CUTS = [  # (time, clip)
 (0.0, "departing_aerial"), (WT(0, "Here's") - 0.1, "ai_checkout"),
 (ST[1] - 0.1, "docked_port_aerial"), (WT(1, "Around") - 0.1, "credit_laptop"), (WT(1, "added") - 0.1, "ai_bill"),
 (ST[2] - 0.1, "ai_steward"), (WT(2, "About") - 0.1, "maids_bed"), (WT(2, "That's") - 0.1, "money_count"),
 (ST[3] - 0.1, "ai_cocktails"), (WT(3, "Just") - 0.1, "cocktail_bar"), (WT(3, "add") - 0.1, "woman_cocktail"),
 (ST[4] - 0.1, "ai_wifi"), (WT(4, "Roughly") - 0.1, "phone_typing"), (WT(4, "if") - 0.1, "ocean_cruise"),
 (ST[5] - 0.1, "ai_tender"), (WT(5, "and") - 0.1, "ai_hotel"), (WT(5, "so") - 0.1, "boarding2"),
 (ST[6] - 0.1, "ai_shock"),
 (ST[7] - 0.1, "aerial_lux"), (WT(7, "budget") - 0.1, "card_terminal"), (WT(7, "Which") - 0.1, "balcony_sunset"),
]
ITEMS = {1: (1, "TAXES & PORT FEES"), 2: (2, "GRATUITIES"), 3: (3, "DRINKS"), 4: (4, "WI-FI"), 5: (5, "EXCURSIONS + HOTEL")}
ADDS = [(WT(1, "hundred"), 150), (WT(2, "hundred"), 126), (WT(3, "hundred"), 200), (WT(4, "twenty"), 140), (WT(5, "excursions"), 200), (WT(5, "hotel"), 150)]
PHR = [("four hundred ninety-nine dollar", "$499"), ("a hundred and fifty dollars", "$150"), ("eighteen dollars", "$18"),
       ("hundred and twenty-six", "$126"), ("two hundred dollars", "$200"), ("twenty dollars", "$20"), ("fifteen hundred", "$1,500")]
def disp(i):
    ws = LINES[i].split(); out = list(ws); j = 0
    while j < len(ws):
        for ph, rep in PHR:
            n = len(ph.split())
            if [clean(x) for x in ws[j:j + n]] == [clean(x) for x in ph.split()]:
                tail = "".join(c for c in ws[j + n - 1] if c in ",.?!:")
                out[j] = rep + tail
                for q in range(1, n): out[j + q] = ""
                j += n - 1; break
        j += 1
    return out
DISP = None
def src(k): return f"{k}.mp4" if k.startswith("ai_") else STOCK + k + ".mp4"
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def base():
    os.makedirs("seg", exist_ok=True); segs = []; used = {}
    ts = [c[0] for c in CUTS] + [TOTAL]
    for n, (t0, k) in enumerate(CUTS):
        t1 = ts[n + 1]; fr = round(t1 * FPS) - round(t0 * FPS); d = t1 - t0; f = src(k); L = dur(f)
        u = used.get(k, 0); used[k] = u + 1
        ss = 0.0 if k.startswith("ai_") else min(max(0.0, L - d - 0.1), 1.0 + u * 3.0)
        spd = max(1.0, (d + 0.05) / max(0.5, L - ss))
        if k.startswith("ai_"): vf = f"setpts={spd:.3f}*(PTS-STARTPTS),scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        else: vf = f"setpts={spd:.3f}*(PTS-STARTPTS),scale=-2:2000,crop=1080:1920:x='(iw-1080)/2+50*t/{d:.2f}':y=40"
        vf += f",eq=saturation=1.08:contrast=1.04,fps={FPS}"
        out = f"seg/c{n:03d}.mp4"; segs.append(out)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{ss:.2f}", "-i", f, "-vf", vf, "-frames:v", str(fr), "-an",
                        "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], check=True)
    open("seg_list.txt", "w").write("".join(f"file {x}\n" for x in segs))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", "seg_list.txt", "-c", "copy", "base.mp4"], check=True)
_F = {}
def font(p, s):
    k = (p, int(s))
    if k not in _F: _F[k] = ImageFont.truetype(p, max(8, int(s)))
    return _F[k]
def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def back(x):
    x = min(1.0, max(0.0, x)); return 1 + 2.7 * (x - 1) ** 3 + 1.7 * (x - 1) ** 2
BX, BB = "Poppins-ExtraBold.ttf", "Poppins-Bold.ttf"
def sticky(n, sc):
    s = int(150 * sc); im = Image.new("RGBA", (s + 40, s + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((26, 30, 26 + s, 30 + s), fill=(0, 0, 0, 100)); d.rectangle((18, 18, 18 + s, 18 + s), fill=YEL + (255,))
    d.polygon([(18 + s - 30 * sc, 18 + s), (18 + s, 18 + s - 30 * sc), (18 + s, 18 + s)], fill=(215, 175, 0, 255))
    d.text((18 + s / 2, 18 + s / 2 + 4 * sc), f"#{n}", font=font(BX, 74 * sc), fill=INK, anchor="mm")
    return im.rotate(-4, resample=Image.BICUBIC, expand=True)
def total(t):
    v = 499.0
    for ta, a in ADDS: v += a * ease((t - ta) / 0.6)
    return v
def overlay(t):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    i = max(j for j in range(len(LINES)) if ST[j] - 0.1 <= t) if t >= ST[0] - 0.1 else 0
    # header with rules (Cruise Insider phase style)
    head = "THE REAL COST" if i in (0, 6, 7) else ITEMS[i][1]
    hs = ST[i] - 0.1 if i else 0.0; k = ease((t - hs) / 0.35)
    f = font(BX, 58); tw = f.getlength(head); y = 250
    if i in ITEMS:
        st = sticky(ITEMS[i][0], back((t - hs) / 0.4)); lay.alpha_composite(st, (int(W / 2 - tw / 2 - st.width - 10), int(y - st.height / 2)))
    lw = (tw + 60) * k
    d.rectangle((W / 2 - lw / 2, y - 52, W / 2 + lw / 2, y - 47), fill=WHT); d.rectangle((W / 2 - lw / 2, y + 47, W / 2 + lw / 2, y + 52), fill=WHT)
    d.text((W / 2, y), head, font=f, fill=WHT + (int(255 * k),), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0, int(160 * k)))
    # running total
    v = total(t); rising = any(0 <= t - ta < 0.7 for ta, a in ADDS)
    if i < 6:
        txt = f"${int(round(v)):,}"
        d.rounded_rectangle((W / 2 - 230, 360, W / 2 + 230, 500), 26, fill=(10, 10, 10, 190))
        d.text((W / 2, 432), txt, font=font(BX, 104), fill=YEL if rising else WHT, anchor="mm")
        for ta, a in ADDS:
            if 0 <= t - ta < 1.3:
                q = (t - ta) / 1.3
                d.text((W / 2 + 300, 432 - 60 * q), f"+${a}", font=font(BX, 64), fill=RED + (int(255 * (1 - q * q)),), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0, int(200 * (1 - q * q))))
    else:
        kk = back((t - ST[6] + 0.1) / 0.45) if i == 6 else 1.0
        d.rounded_rectangle((W / 2 - 300, 350, W / 2 + 300, 520), 30, fill=(10, 10, 10, 200))
        d.text((W / 2, 435), "≈ $1,500", font=font(BX, 120 * max(0.3, kk)), fill=RED, anchor="mm")
        d.text((W / 2, 565), "was $499", font=font(BB, 52), fill=WHT, anchor="mm", stroke_width=5, stroke_fill=BLK)
        d.line([(W / 2 - 120, 568), (W / 2 + 120, 562)], fill=RED, width=7)
    # captions: 2-4 words, white, black outline, lower third
    for q in range(len(LINES)):
        if ST[q] - 0.05 <= t < ST[q] + D[q] + 0.15:
            global DISP
            if DISP is None: DISP = [disp(z) for z in range(len(LINES))]
            ws = DISP[q]; cur = 0
            for j, o in enumerate(TW[q]):
                if t >= ST[q] + o - 0.05 and ws[j]: cur = j
            idx = [j for j, w in enumerate(ws) if w]; pos = idx.index(cur)
            grp = idx[pos // 3 * 3: pos // 3 * 3 + 3]; s = " ".join(ws[j] for j in grp)
            fz = font(BX, 76)
            while fz.getlength(s) > W - 90: fz = font(BX, fz.size - 3)
            d.text((W / 2, 1400), s, font=fz, fill=WHT, anchor="mm", stroke_width=9, stroke_fill=BLK)
            break
    return lay
def video(out):
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", "base.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    o = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "mix.wav",
                          "-c:v", "libx264", "-crf", "19", "-maxrate", "5000k", "-bufsize", "10000k", "-preset", "medium", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    sz = W * H * 3; fi = 0
    while True:
        b = p.stdout.read(sz)
        if len(b) < sz: break
        im = Image.frombytes("RGB", (W, H), b).convert("RGBA"); im.alpha_composite(overlay(fi / FPS)); o.stdin.write(im.convert("RGB").tobytes()); fi += 1
    o.stdin.close(); o.wait(); print("frames", fi)
if __name__ == "__main__":
    c = sys.argv[1]
    if c == "base": base()
    elif c == "video": video(sys.argv[2])
    elif c == "still":
        for tt in sys.argv[2:]:
            im = Image.new("RGBA", (W, H), (70, 110, 150, 255)); im.alpha_composite(overlay(float(tt))); im.convert("RGB").save(f"still_{tt}.png")
