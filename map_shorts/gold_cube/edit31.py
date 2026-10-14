"""Gold cube Short: assembly of 9 Veo clips + VO + captions + number overlays. python3 edit31.py still T.. | info | video out.mp4"""
import json, math, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, "vo")
from script31 import LINES
W, H, FPS = 1080, 1920, 30
POPX = "Poppins-ExtraBold.ttf"
TM = json.load(open("vo/timing.json")); D, TW, VS = TM["D"], TM["T"], TM["starts"]
GAP, T0 = 0.22, 0.3
ST = []; t = T0
for d in D: ST.append(t); t += d + GAP
END = ST[-1] + D[-1] + 2.2
NF = int(END * FPS)
# (clip file, src start, src end, out start, out end)
SEG = [("v_s1.mp4", 0.0, 6.4, 0.0, ST[1] - 0.1), ("v_s2.mp4", 0.0, 7.0, ST[1] - 0.1, ST[2] - 0.1), ("v_s3.mp4", 3.0, 6.5, ST[2] - 0.1, ST[3] - 0.1),
       ("v_s4.mp4", 0.8, 3.6, ST[3] - 0.1, ST[4] - 0.1), ("v_s5.mp4", 0.5, 6.5, ST[4] - 0.1, ST[4] + 3.9), ("v_s6b.mp4", 0.2, 3.4, ST[4] + 3.9, ST[5] - 0.1),
       ("v_s7a.mp4", 0.5, 6.3, ST[5] - 0.1, ST[6] - 0.1), ("v_s7b.mp4", 2.5, 4.8, ST[6] - 0.1, ST[7] - 0.1), ("v_s8.mp4", 2.2, 5.3, ST[7] - 0.1, END)]
SEG[-1] = ("v_s8.mp4", 2.2, 5.3, ST[7] - 0.1, END)


def clean(w): return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word):
    ws = [clean(w) for w in LINES[i].split()]; q = clean(word)
    for j, w in enumerate(ws):
        if w == q or q in w: return ST[i] + TW[i][j]
    raise KeyError((i, word))


_F = {}
def font(s):
    s = int(s)
    if s not in _F: _F[s] = ImageFont.truetype(POPX, s)
    return _F[s]


def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def pop(x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    return 1.12 * ease(x / 0.6) if x < 0.6 else 1.12 - 0.12 * ease((x - 0.6) / 0.4)


_FR = {}
def clip_frames(seg):
    if seg not in _FR:
        f, a, b, o0, o1 = SEG[seg]; n = max(1, int(round((o1 - o0) * FPS)))
        vf = f"trim={a}:{b},setpts=(PTS-STARTPTS)*{(o1 - o0) / (b - a):.5f},fps={FPS},scale={W}:{H}:flags=lanczos"
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f, "-vf", vf, "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        _FR[seg] = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return _FR[seg]


def led(img, cx, cy, text, k, color=(80, 190, 255), size=108):
    if k <= 0.02: return
    f = font(size * min(k, 1.0)); d = ImageDraw.Draw(img); tw = f.getlength(text); ph = size * 1.5 * min(k, 1.0)
    x0, y0 = cx - tw / 2 - 40, cy - ph / 2
    d.rounded_rectangle((x0, y0, x0 + tw + 80, y0 + ph), 26, fill=(6, 18, 40, 225), outline=color + (255,), width=5)
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).text((cx, cy + 4), text, font=f, fill=color + (255,), anchor="mm")
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
    d.text((cx, cy + 4), text, font=f, fill=(235, 250, 255, 255), anchor="mm")


def label3(img, cx, cy, text, k, size=72):
    if k <= 0.02: return
    f = font(size * min(k, 1.0)); d = ImageDraw.Draw(img)
    d.text((cx + 4, cy + 5), text, font=f, fill=(0, 0, 0, 170), anchor="mm")
    d.text((cx, cy), text, font=f, fill=(255, 255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0, 255))


def overlays(img, t):
    k = lambda t0, dur=0.3: pop((t - t0) / dur)
    def sf(fn):
        try: fn()
        except KeyError: pass
    if ST[1] <= t < ST[2]: sf(lambda: led(img, W / 2, 330, "≈ 220,000 t", k(WT(1, "twenty"))))
    if ST[2] <= t < ST[4]: label3(img, W / 2, 330, "22.5 m", k(ST[2] + 1.3))
    if ST[4] <= t < ST[5]:
        sf(lambda: led(img, W / 2, 330, "+66,000 t", k(WT(4, "now") + 0.2)))
        sf(lambda: led(img, W / 2, 500, "+30 % gold", k(WT(4, "thirty")), (255, 200, 60)))
        sf(lambda: led(img, W / 2, 670, "+2 m only", k(WT(4, "two")), (255, 120, 90)))
    if ST[5] <= t < ST[6]:
        sf(lambda: led(img, W / 2, 330, "8.3 billion", k(WT(5, "eight")), (255, 255, 255)))
        sf(lambda: led(img, W / 2, 500, "≈ 35 g each", k(WT(5, "thirtyfive")), (255, 200, 60)))
    if ST[6] <= t < ST[7]: led(img, W / 2, 330, "≈ 1.2 cm", k(ST[6] + 0.15), (255, 200, 60))


def caption(img, t):
    for i in range(len(LINES)):
        if ST[i] - 0.05 <= t < ST[i] + D[i] + 0.2:
            words = LINES[i].split(); cur = 0
            for j, o in enumerate(TW[i]):
                if t >= ST[i] + o - 0.05: cur = j
            c0 = cur // 3 * 3; chunk = words[c0:c0 + 3]
            f = font(66); gap = f.getlength(" ") * 1.0
            txts = [w.lower() for w in chunk]; ws = [f.getlength(x) for x in txts]; tot = sum(ws) + gap * (len(txts) - 1)
            if tot > W - 100:
                f = font(66 * (W - 100) / tot); gap = f.getlength(" "); ws = [f.getlength(x) for x in txts]; tot = sum(ws) + gap * (len(txts) - 1)
            x = (W - tot) / 2; d = ImageDraw.Draw(img)
            for j, (x_, ww) in enumerate(zip(txts, ws)):
                col = (255, 214, 10, 255) if c0 + j == cur else (255, 255, 255, 255)
                d.text((x + 3, 1372 + 4), x_, font=f, fill=(0, 0, 0, 160), anchor="lm")
                d.text((x, 1372), x_, font=f, fill=col, anchor="lm", stroke_width=6, stroke_fill=(0, 0, 0, 255))
                x += ww + gap
            return


def frame(fi):
    t = fi / FPS
    seg = max(i for i, s in enumerate(SEG) if s[3] <= t + 1e-6) if t >= 0 else 0
    fr = clip_frames(seg); j = min(len(fr) - 1, int((t - SEG[seg][3]) * FPS))
    img = Image.fromarray(fr[j]).convert("RGBA")
    overlays(img, t); caption(img, t)
    a = 1.0 if t > 0.25 else t / 0.25
    if t > END - 0.6: a = max(0, (END - t) / 0.6)
    out = img.convert("RGB")
    if a < 1: out = Image.eval(out, lambda v: int(v * a))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print("end", round(END, 2), "frames", NF, "starts", [round(s, 2) for s in ST]); print([(s[0], round(s[3], 2), round(s[4], 2)) for s in SEG])
    elif cmd == "still":
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"e_{float(a):05.1f}.png")
    elif cmd == "video":
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", sys.argv[2]], stdin=subprocess.PIPE)
        for fi in range(NF):
            p.stdin.write(frame(fi).tobytes())
            if fi % 60 == 0: print(fi, flush=True)
        p.stdin.close(); p.wait()
