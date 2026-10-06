"""Vertical 9:16 Shorts cut from the long AI video: python3 shorts14.py NAME [still SEC]  (no paid services used).
Layout: stock shots are full-bleed 9:16 with punch-in cuts; graphic shots sit on the channel's light-grey canvas as a
framed card under a headline. Word-highlight captions on both."""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import engine14 as E

SHORTS = {
    "s1_curve": dict(lines=(3, 7), title=["WHY AI IS", "MOVING SO FAST"]),
    "s2_voice": dict(lines=(22, 25), title=["AI VOICE SCAMS:", "ONE FREE DEFENSE"]),
    "s3_jobs": dict(lines=(38, 42), title=["IS AI TAKING", "ENTRY-LEVEL JOBS?"]),
    "s4_agi": dict(lines=(43, 46), title=["WHEN WILL", "AGI ARRIVE?"]),
}
VW, VH = 1080, 1920
CARD_X0, CARD_X1 = 150, 1770
ZK = dict(title=1.0, stat=1.0, quote=1.0, counter=1.0, list=1.0, timeline=1.1)
GREEN, RED, INK, BG = E.GREEN, E.RED, E.INK, E.BG


def window(name):
    a, b = SHORTS[name]["lines"]
    return max(0.0, E.starts[a] - 0.3), E.starts[b] + E.D[b] + 0.5


def word_groups(maxw=3):
    g = []
    for i, line in enumerate(E.LINES):
        words = line.split()
        n = -(-len(words) // maxw)
        size = len(words) / n
        b = [round(size * k) for k in range(n + 1)]
        for j, k in zip(b[:-1], b[1:]):
            t0 = E.starts[i] + E.TW[i][j] - 0.06
            t1 = (E.starts[i] + E.TW[i][k] - 0.06) if k < len(words) else E.starts[i] + E.D[i] + 0.3
            g.append((t0, t1, words, j, k, i))
    return g


GROUPS = word_groups()


def captions(img, t, light):
    for t0, t1, words, j, k, i in GROUPS:
        if t0 <= t < t1:
            ws = words[j:k]
            act = 0
            for q in range(j, k):
                if E.starts[i] + E.TW[i][q] - 0.06 <= t:
                    act = q - j
            f = E.font(112, "Bold")
            txt = " ".join(ws).upper()
            sp = f.getlength(" ")
            widths = [f.getlength(w.upper()) for w in ws]
            tot = sum(widths) + sp * (len(ws) - 1)
            scale = min(1.0, 980 / tot)
            if scale < 1.0:
                f = E.font(int(112 * scale), "Bold")
                sp = f.getlength(" ")
                widths = [f.getlength(w.upper()) for w in ws]
                tot = sum(widths) + sp * (len(ws) - 1)
            d = ImageDraw.Draw(img)
            x = VW / 2 - tot / 2
            y = 1400 if light else 1430
            pop = 1.0
            for q, w in enumerate(ws):
                on = q == act
                if light:
                    col = GREEN if on else INK
                    d.text((x, y), w.upper(), font=f, fill=col, anchor="lm")
                else:
                    col = (255, 214, 64) if on else (255, 255, 255)
                    d.text((x, y), w.upper(), font=f, fill=col, anchor="lm", stroke_width=9, stroke_fill=(0, 0, 0))
                x += widths[q] + sp
            return


def raw_clip(s, t):
    """full-bleed 9:16 crop of a stock shot with slow push + pan and a punch-in on the cut"""
    img = E.frame_img(E.clip_dir(s), s["t0"], t)
    p = (t - s["t0"]) / max(0.01, s["t1"] - s["t0"])
    lt = t - s["t0"]
    z = 1.0 + 0.10 * p if s["k"] % 2 == 0 else 1.10 - 0.10 * p
    z *= 1.0 + 0.10 * max(0.0, 1 - lt / 0.25) ** 2  # punch-in settling after the cut
    ch = int(E.H / z)
    cw = int(ch * VW / VH)
    pan = (0.5 + (0.12 * (p - 0.5)) * (1 if s["k"] % 2 == 0 else -1))
    x0 = int((E.W - cw) * pan)
    y0 = (E.H - ch) // 2
    return img.crop((x0, y0, x0 + cw, y0 + ch)).resize((VW, VH), Image.BILINEAR)


def grey():
    a = np.zeros((VH, VW, 3), np.float32)
    a[:] = BG
    yy = np.linspace(0, 1, VH)[:, None, None]
    a *= 1 - 0.05 * yy
    return Image.fromarray(a.astype(np.uint8))


_GREY = None

NATIVE = ("title", "stat", "quote", "timeline", "list")


def pop(lt, delay=0.0, dur=0.35):
    x = min(1.0, max(0.0, (lt - delay) / dur))
    return E.out_back(x) if x < 1 else 1.0


def native_scene(img, kind, sc, p, lt):
    d = ImageDraw.Draw(img)
    cx = VW // 2
    if kind == "title":
        lines = sc["lines"]
        y = 760
        for q, l in enumerate(lines):
            big = len(l) <= 2
            fs = 300 if big else 190
            a = pop(lt, 0.08 * q)
            f = E.font(int(fs * max(0.2, a)), "Bold")
            col = RED if big else INK
            d.text((cx, y + (1 - a) * 40), l, font=f, fill=col, anchor="mm")
            y += int(fs * 0.95)
        w = int(520 * pop(lt, 0.3, 0.4))
        d.rectangle((cx - w // 2, y + 20, cx + w // 2, y + 32), fill=GREEN)
        if sc.get("sub"):
            d.text((cx, y + 110), sc["sub"], font=E.font(62, "SemiBold"), fill=(95, 104, 112), anchor="mm")
    elif kind == "stat":
        a = pop(lt)
        big = sc["big"]
        fs = 330
        f = E.font(fs, "Bold")
        while f.getlength(big) > 960:
            fs -= 12
            f = E.font(fs, "Bold")
        f = E.font(int(fs * max(0.2, a)), "Bold")
        d.text((cx, 760), big, font=f, fill=GREEN, anchor="mm")
        w = int(f.getlength(big) * pop(lt, 0.25, 0.4))
        d.rectangle((cx - w // 2, 760 + int(fs * 0.62), cx + w // 2, 760 + int(fs * 0.62) + 12), fill=RED)
        for q, l in enumerate(E.wrap(sc["small"], E.font(76, "SemiBold"), 900)):
            d.text((cx, 1010 + q * 92), l, font=E.font(76, "SemiBold"), fill=INK, anchor="mm")
    elif kind == "quote":
        f = E.font(168, "Bold")
        for q, l in enumerate(E.wrap(sc["text"], f, 900)):
            a = pop(lt, 0.12 * q)
            d.text((cx, 780 + q * 190 + (1 - a) * 50), l, font=f, fill=INK if q % 2 == 0 else GREEN, anchor="mm")
        d.text((cx - 440, 520), "\u201c", font=E.font(300, "Bold"), fill=RED, anchor="lm")
    elif kind == "timeline":
        items = sc["items"]
        n = len(items)
        y0, gap = 540, 290
        x = 190
        prog = min(1.0, lt / 1.2)
        d.rectangle((x - 3, y0, x + 3, y0 + int((n - 1) * gap * prog)), fill=GREEN)
        for q, (a_, b_) in enumerate(items):
            a = pop(lt, 0.45 * q)
            y = y0 + q * gap
            r = int(26 * a)
            d.ellipse((x - r, y - r, x + r, y + r), fill=GREEN)
            d.text((x + 90 + (1 - a) * 60, y - 40), a_, font=E.font(150, "Bold"), fill=INK, anchor="lm")
            for k, l in enumerate(E.wrap(b_, E.font(62, "SemiBold"), 720)):
                d.text((x + 90 + (1 - a) * 60, y + 62 + k * 70), l, font=E.font(62, "SemiBold"), fill=(95, 104, 112), anchor="lm")
    elif kind == "list":
        items = sc["items"]
        for q, it in enumerate(items):
            a = pop(lt, 0.7 * q)
            y = 640 + q * 215
            d.rounded_rectangle((90 + (1 - a) * 400, y - 80, 990 + (1 - a) * 400, y + 80), radius=24, fill=(255, 255, 255), outline=INK, width=4)
            d.ellipse((130 + (1 - a) * 400, y - 40, 210 + (1 - a) * 400, y + 40), fill=GREEN)
            d.text((170 + (1 - a) * 400, y), "\u2713", font=E.font(60, "Bold"), fill=(255, 255, 255), anchor="mm")
            d.text((250 + (1 - a) * 400, y), it, font=E.font(78, "Bold"), fill=INK, anchor="lm")


def vframe(fi, name):
    global _GREY
    t = fi / E.FPS
    t0, t1 = window(name)
    s = E.shot_at(t)
    sc = s["sc"]
    kind = sc["t"]
    p = (t - s["t0"]) / max(0.01, s["t1"] - s["t0"])
    lt = t - s["t0"]
    if kind == "clip":
        img = raw_clip(s, t).convert("RGBA")
        sh = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
        g = np.zeros((VH, VW, 4), np.uint8)
        ramp = np.clip((np.arange(VH) - 1100) / 820, 0, 1) ** 1.4 * 170
        g[..., 3] = ramp[:, None].astype(np.uint8)
        img.alpha_composite(Image.fromarray(g, "RGBA"))
        d = ImageDraw.Draw(img)
        if sc["src"].startswith("gen:"):
            f = E.font(40, "Bold")
            w_ = f.getlength("GENERATED BY AI") + 56
            d.rounded_rectangle((VW / 2 - w_ / 2, 1150, VW / 2 + w_ / 2, 1218), radius=10, fill=E.TAG_RED)
            d.text((VW / 2, 1184), "GENERATED BY AI", font=f, fill=(255, 255, 255), anchor="mm")
        if sc.get("tag") == "script":
            f = E.font(40, "Bold")
            w_ = f.getlength("SCRIPT WRITTEN WITH AI") + 56
            d.rounded_rectangle((VW / 2 - w_ / 2, 1150, VW / 2 + w_ / 2, 1218), radius=10, fill=E.TAG_BLUE)
            d.text((VW / 2, 1184), "SCRIPT WRITTEN WITH AI", font=f, fill=(255, 255, 255), anchor="mm")
        light = False
    else:
        if _GREY is None:
            _GREY = grey()
        img = _GREY.copy().convert("RGBA")
        if kind in NATIVE:
            native_scene(img, kind, sc, p, lt)
            nat = True
        else:
            nat = False
        if not nat:
            sc_img = E.SCENES[kind](sc, p, lt, s) if kind == "curve" else E.SCENES[kind](sc, p, lt)
            card = sc_img.convert("RGB")
            z = ZK.get(kind, 1.0) * (1.0 + 0.04 * p)
            cw = int(1700 / z)
            ch = int(E.H * 0.93 / z)
            cx0 = (E.W - cw) // 2
            cy0 = (E.H - ch) // 2
            card = card.crop((cx0, cy0, cx0 + cw, cy0 + ch)).resize((VW - 80, int((VW - 80) * ch / cw)), Image.BILINEAR)
            cy = 520
            sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(sh).rounded_rectangle((46, cy + 16, VW - 34, cy + card.height + 16), radius=18, fill=(0, 0, 0, 70))
            img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
            mask = Image.new("L", card.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, card.width, card.height), radius=16, fill=255)
            img.paste(card, (40, cy), mask)
            ImageDraw.Draw(img).rounded_rectangle((40, cy, VW - 40, cy + card.height), radius=16, outline=INK, width=4)
        light = True
    d = ImageDraw.Draw(img)
    # headline: always on graphic shots, only the first 2.6 s on stock
    show_title = (light and not (kind in NATIVE)) or (not light and (t - t0) < 2.6)
    if show_title:
        for q, line in enumerate(SHORTS[name]["title"]):
            y = 250 + q * 135
            if light:
                d.text((VW / 2, y), line, font=E.font(122, "Bold"), fill=GREEN if q else INK, anchor="mm")
            else:
                d.text((VW / 2, y + 120), line, font=E.font(122, "Bold"), fill=(255, 214, 64) if q else (255, 255, 255),
                       anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
        if light:
            d.rectangle((VW / 2 - 90, 452, VW / 2 + 90, 460), fill=RED)
    captions(img, t, light)
    if light:
        d.text((VW / 2, 1740), 'AI WILL CHANGE EVERYTHING  ·  2026', font=E.font(40, 'SemiBold'), fill=(120, 128, 136), anchor='mm')
    # progress bar
    prog = (t - t0) / (t1 - t0)
    d.rectangle((0, VH - 14, VW, VH), fill=(0, 0, 0, 60) if not light else (200, 205, 210))
    d.rectangle((0, VH - 14, int(VW * prog), VH), fill=RED)
    return img.convert("RGB")


if __name__ == "__main__":
    name = sys.argv[1]
    t0, t1 = window(name)
    a, b = int(t0 * E.FPS), int(t1 * E.FPS)
    if len(sys.argv) > 2 and sys.argv[2] == "still":
        for sec in sys.argv[3:]:
            vframe(a + int(float(sec) * E.FPS), name).save(f"vstill_{name}_{sec}.jpg", quality=88)
        sys.exit()
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
