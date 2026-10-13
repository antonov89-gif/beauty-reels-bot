"""Cruise listicle long-form (16:9). python3 engine25.py plan | base | over A B out.mp4 | still N"""
import json, math, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script25 import S, LINES
W, H, FPS = 1920, 1080, 30
TM = json.load(open("timing.json")); D, TW = TM["D"], TM["T"]
LEAD = 0.4
ST = [LEAD + s for s in TM["starts"]]
TOTAL = ST[-1] + D[-1] + 3.0
NF = int(TOTAL * FPS)
YEL, WHT, BLK, INK = (255, 213, 0), (255, 255, 255), (0, 0, 0), (20, 20, 20)
BX = "Poppins-ExtraBold.ttf"; BB = "Poppins-Bold.ttf"
_F = {}
def font(p, s):
    k = (p, int(s))
    if k not in _F: _F[k] = ImageFont.truetype(p, max(8, int(s)))
    return _F[k]
def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def back(x):
    x = min(1.0, max(0.0, x)); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
# line spans (cut 0.15 s before each line)
SPAN = [(0.0 if i == 0 else ST[i] - 0.15, ST[i + 1] - 0.15 if i + 1 < len(S) else TOTAL) for i in range(len(S))]
def clip_len(k):
    if not hasattr(clip_len, "c"): clip_len.c = json.load(open("cliplen.json")) if os.path.exists("cliplen.json") else {}
    return clip_len.c.get(k, 10.0)
def plan():
    shots, used = [], {}
    for i, (text, clips, card) in enumerate(S):
        a, b = SPAN[i]; d = b - a
        if card and card[0] == "phase":
            shots.append(dict(k=clips[0], a=a, d=d, line=i)); continue
        n = max(len(clips), math.ceil(d / 4.2)); n = max(1, min(n, math.ceil(d / 1.8)))
        for j in range(n):
            k = clips[j % len(clips)]
            sa = a + d * j / n; sd = d / n
            shots.append(dict(k=k, a=sa, d=sd, line=i))
    for s in shots:
        u = used.get(s["k"], 0); used[s["k"]] = u + 1
        L = clip_len(s["k"]); room = max(0.0, L - s["d"] - 0.1)
        s["in"] = (u * 3.7) % room if room > 0.5 else 0.0
        s["slow"] = s["d"] > L - 0.05
    return shots
def base():
    shots = plan(); os.makedirs("seg", exist_ok=True); segs = []
    for n, s in enumerate(shots):
        out = f"seg/s{n:04d}.mp4"; segs.append(out)
        fr = max(1, round((s["a"] + s["d"]) * FPS) - round(s["a"] * FPS))
        L = clip_len(s["k"]); spd = max(1.0, (s["d"] + 0.1) / max(0.5, L - s["in"]))
        dirx = 1 if n % 2 else -1
        vf = (f"setpts={spd:.3f}*(PTS-STARTPTS),scale=2040:1148,crop=1920:1080:x='60+{dirx}*60*min(t/{s['d']:.2f}\\,1)':y=34,"
              f"eq=saturation=1.1:contrast=1.04,fps={FPS}")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{s['in']:.2f}", "-i", f"clips/{s['k']}.mp4", "-vf", vf,
                        "-frames:v", str(fr), "-an", "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], check=True)
    open("seg_list.txt", "w").write("".join(f"file {x}\n" for x in segs))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", "seg_list.txt", "-c", "copy", "base.mp4"], check=True)
    print("shots", len(shots))
# ---------------- overlays
def txt(d, xy, s, f, fill, stroke=0, sf=BLK, anchor="mm"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sf)
def sticky(n, scale=1.0):
    s = int(150 * scale)
    im = Image.new("RGBA", (s + 40, s + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((26, 30, 26 + s, 30 + s), fill=(0, 0, 0, 90))
    d.rectangle((18, 18, 18 + s, 18 + s), fill=YEL + (255,))
    d.polygon([(18 + s - 34 * scale, 18 + s), (18 + s, 18 + s - 34 * scale), (18 + s, 18 + s)], fill=(220, 180, 0, 255))
    txt(d, (18 + s / 2, 18 + s / 2 + 4 * scale), f"#{n}", font(BX, 70 * scale), INK)
    im = im.filter(ImageFilter.GaussianBlur(0.4))
    return im.rotate(-4, resample=Image.BICUBIC, expand=True)
def cur_card(t):
    tip = phase = None
    for i, (text, clips, card) in enumerate(S):
        if SPAN[i][0] > t: break
        if card and card[0] == "tip": tip = (i, card)
        if card and card[0] == "phase": phase = (i, card); tip = None
    return tip, phase
def overlay(t):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    i = max(j for j in range(len(S)) if SPAN[j][0] <= t)
    card = S[i][2]; lt = t - SPAN[i][0]; dur = SPAN[i][1] - SPAN[i][0]
    if card and card[0] == "phase":
        a = ease(lt / 0.4) * (1 - ease((lt - dur + 0.35) / 0.35))
        d.rectangle((0, 0, W, H), fill=(5, 12, 25, int(170 * a)))
        k = back((lt - 0.1) / 0.45)
        cy = 520
        txt(d, (W / 2, cy - 120), f"PHASE {card[1]}", font(BX, 54), YEL + (int(255 * a),))
        f = font(BX, 118 * max(0.3, k)); tw = f.getlength(card[2])
        txt(d, (W / 2, cy + 10), card[2], f, WHT + (int(255 * a),))
        lw = min(W - 200, tw + 120) * ease((lt - 0.2) / 0.5)
        for yy in (cy - 70, cy + 95):
            d.rectangle((W / 2 - lw / 2, yy, W / 2 + lw / 2, yy + 6), fill=WHT + (int(230 * a),))
    tip, phase = cur_card(t)
    if tip and not (card and card[0] in ("phase", "recap", "end")):
        ti, tc = tip; tl = t - SPAN[ti][0]
        big = 1 - ease((tl - 3.6) / 0.5)
        k = back(tl / 0.45)
        sc = (0.55 + 0.45 * big) * max(0.05, k)
        st = sticky(tc[1], sc)
        x0 = int(70 + (W / 2 - 520 - 70) * big * 0); y0 = int(60 + 300 * big)
        lay.alpha_composite(st, (x0, y0))
        fz = font(BX, (36 + 30 * big))
        label = tc[2]; lw = fz.getlength(label)
        bx0 = x0 + st.width + 10; by = y0 + st.height / 2
        a2 = ease((tl - 0.2) / 0.3)
        d.rectangle((bx0, by - 40 - 22 * big, bx0 + (lw + 50) * a2, by + 40 + 22 * big), fill=(10, 10, 10, int(200 * a2)))
        if a2 > 0.6: txt(d, (bx0 + 25, by), label, fz, WHT, anchor="lm")
    if card and card[0] == "title":
        a = ease(lt / 0.4) * (1 - ease((lt - 3.8) / 0.4))
        if a > 0:
            f = font(BX, 96); words = card[1]
            tw = f.getlength(words)
            if tw > W - 160: f = font(BX, 96 * (W - 160) / tw); tw = f.getlength(words)
            d.rectangle((W / 2 - tw / 2 - 40, 380, W / 2 + tw / 2 + 40, 540), fill=(10, 10, 10, int(190 * a)))
            d.rectangle((W / 2 - tw / 2 - 40, 534, (W / 2 - tw / 2 - 40) + (tw + 80) * ease(lt / 0.9), 548), fill=YEL + (int(255 * a),))
            txt(d, (W / 2, 462), words, f, WHT + (int(255 * a),))
    if card and card[0] == "recap":
        items = (["Arrive on time", "Smart carry-on", "Documents in hand", "Skip the buffet rush", "Safety drill early", "Book what matters",
                  "Cellular data off", "Walk the ship"] if card[1] == 1 else
                 ["Read the drink rules", "Budget for gratuities", "Check your account", "No rushed purchases", "Inspect, then unpack",
                  "Meet your steward", "Enjoy the sail away", "Get some sleep"])
        base_n = 0 if card[1] == 1 else 8
        a = ease(lt / 0.4) * (1 - ease((lt - dur + 0.3) / 0.3))
        d.rounded_rectangle((90, 120, 900, 120 + 70 * 8 + 60), 24, fill=(8, 12, 22, int(200 * a)))
        ws = [clean(w) for w in LINES[i].split()]
        for q, it in enumerate(items):
            tq = SPAN[i][0] + 0.4 + q * (dur - 1.2) / 8
            kk = ease((t - tq) / 0.3) * a
            if kk <= 0: continue
            y = 175 + q * 70
            d.rectangle((130, y - 22, 174, y + 22), fill=YEL + (int(255 * kk),))
            txt(d, (152, y + 1), "✓" if False else str(base_n + q + 1), font(BX, 26), INK + (int(255 * kk),))
            txt(d, (200, y), it, font(BB, 40), WHT + (int(255 * kk),), anchor="lm")
    if card and card[0] == "end":
        a = ease(lt / 0.5)
        d.rectangle((0, 0, W, H), fill=(5, 10, 20, int(120 * a)))
        bw = 520; k = back((lt - 0.3) / 0.5)
        if k > 0:
            d.rounded_rectangle((W / 2 - bw / 2 * k, 430 - 60 * k, W / 2 + bw / 2 * k, 430 + 60 * k), 18, fill=(220, 30, 30, 255))
            txt(d, (W / 2, 432), "SUBSCRIBE", font(BX, 64 * k), WHT)
        txt(d, (W / 2, 600), "next cruise guide coming soon", font(BB, 44), WHT + (int(255 * a),))
    subs(d, t)
    return lay
def clean(w): return "".join(c for c in w.lower() if c.isalnum())
def build_cues(maxw=7):
    cues = []
    for i, l in enumerate(LINES):
        ws = l.split(); tw = TW[i]; j = 0
        while j < len(ws):
            e = min(len(ws), j + maxw)
            for q in range(j + 3, e):
                if ws[q - 1].endswith((",", ".", "?", ":", "!")) and q - j >= 3: e = q; break
            a = ST[i] + tw[j]; b = ST[i] + (tw[e] if e < len(ws) else D[i] + 0.15)
            cues.append((a, b, " ".join(ws[j:e]))); j = e
    return cues
CUES = None
def subs(d, t):
    global CUES
    if CUES is None: CUES = build_cues()
    for a, b, s in CUES:
        if a - 0.05 <= t < b:
            f = font(BB, 44)
            txt(d, (W / 2, H - 92), s, f, WHT, 5, BLK); return
def over(a, b, out):
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{a / FPS:.4f}", "-i", "base.mp4", "-frames:v", str(b - a), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    o = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    sz = W * H * 3; fi = a; last = None
    while fi < b:
        buf = p.stdout.read(sz)
        if len(buf) < sz:
            if last is None: break
            buf = last
        last = buf
        im = Image.frombytes("RGB", (W, H), buf).convert("RGBA"); im.alpha_composite(overlay(fi / FPS))
        o.stdin.write(im.convert("RGB").tobytes()); fi += 1
        if fi % 300 == 0: print(fi, flush=True)
    o.stdin.close(); o.wait()
if __name__ == "__main__":
    c = sys.argv[1]
    if c == "plan":
        sh = plan(); print(len(sh), "shots, avg", round(TOTAL / len(sh), 2), "s, total", round(TOTAL, 1), "frames", NF)
    elif c == "base": base()
    elif c == "over": over(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    elif c == "still":
        for n in sys.argv[2:]:
            fi = int(n)
            im = Image.open(f"probe_{fi}.png").convert("RGBA") if os.path.exists(f"probe_{fi}.png") else Image.new("RGBA", (W, H), (60, 90, 120, 255))
            im.alpha_composite(overlay(fi / FPS)); im.convert("RGB").save(f"still_{fi}.png")
