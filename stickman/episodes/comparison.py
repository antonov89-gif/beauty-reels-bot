"""Episode 2: The Comparison Trap."""
import math

import numpy as np

from make_video import (BG, GREEN, GREY, INK, RED, SHIRT, WHITE, YELLOW, back, blink_at, character, clamp,
                        clock, ease, handwrite, phone)

TITLE = "THE COMPARISON TRAP"
SLUG = "comparison_trap"

SCRIPT = [
    ("You open your phone, and everyone seems to be winning.", "Everyone's winning?"),
    ("New jobs. New cars. Perfect vacations.", "Perfect lives..."),
    ("And suddenly, your own life feels small.", "I feel small"),
    ("But you're comparing your behind the scenes to their highlight reel.", "Highlights vs. reality"),
    ("Nobody posts the failures, the doubts, or the boring days.", "Nobody posts this"),
    ("So here's the fix. Compare yourself only to who you were yesterday.", "You vs. Yesterday"),
    ("Read one page. Walk for ten minutes. Learn one small thing.", "One small thing"),
    ("Tiny steps don't look impressive today.", "Tiny steps"),
    ("But stacked together, they build a life you're proud of.", "Stack them up!"),
    ("So put the phone down, and take your next small step.", "Your next step."),
]

PALE = (236, 208, 150)
SKY = (150, 200, 240)


def star(p, x, y, r, col=YELLOW, w=4):
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    p.poly(pts, col, w)


def heart(p, x, y, r, col=RED):
    pts = []
    for k in range(40):
        t = k / 40 * 2 * math.pi
        hx = 16 * math.sin(t) ** 3
        hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((x + hx * r / 16, y + hy * r / 16))
    p.poly(pts, col, 4)


def frame_card(p, x, y, w, h, kind, k=1.0):
    """Instagram-like photo card with a tiny doodle inside."""
    if k <= 0.02:
        return
    w, h = w * k, h * k
    p.rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, WHITE, 5)
    ix0, iy0, ix1, iy1 = x - w / 2 + 14 * k, y - h / 2 + 14 * k, x + w / 2 - 14 * k, y + h / 2 - 50 * k
    p.rect(ix0, iy0, ix1, iy1, SKY, 3)
    cx, cy = (ix0 + ix1) / 2, (iy0 + iy1) / 2
    if kind == "car":
        p.poly([(cx - 70 * k, cy + 30 * k), (cx - 60 * k, cy - 5 * k), (cx - 25 * k, cy - 30 * k),
                (cx + 35 * k, cy - 30 * k), (cx + 70 * k, cy), (cx + 75 * k, cy + 30 * k)], RED, 4 * k)
        for dx in (-40, 45):
            p.circle(cx + dx * k, cy + 32 * k, 15 * k, INK, 0)
    elif kind == "palm":
        p.rect(ix0, iy1 - 30 * k, ix1, iy1, (240, 215, 150), 0)
        p.circle(cx + 50 * k, cy - 35 * k, 18 * k, YELLOW, 3 * k)
        p.line([(cx - 20 * k, iy1 - 25 * k), (cx - 5 * k, cy - 30 * k)], 8 * k, (140, 95, 60))
        for a in (-160, -120, -60, -20):
            ex = cx - 5 * k + 50 * k * math.cos(math.radians(a))
            ey = cy - 30 * k + 30 * k * math.sin(math.radians(a)) + 20 * k
            p.line([(cx - 5 * k, cy - 30 * k), (ex, ey)], 7 * k, GREEN)
    elif kind == "job":
        p.rect(cx - 45 * k, cy - 20 * k, cx + 45 * k, cy + 40 * k, (130, 90, 60), 4 * k)
        p.rect(cx - 15 * k, cy - 35 * k, cx + 15 * k, cy - 20 * k, None or (130, 90, 60), 4 * k)
        p.text(cx, cy + 10 * k, "$$$", 30 * k, YELLOW)
    # like counter
    heart(p, x - w / 2 + 34 * k, y + h / 2 - 25 * k, 14 * k)
    p.text(x - w / 2 + 95 * k, y + h / 2 - 25 * k, "12.4k", 24 * k)


def stairs(p, x0, base_y, n, step_w=150, step_h=70, col=(205, 150, 90)):
    for i in range(n):
        p.rect(x0 + i * step_w, base_y - (i + 1) * step_h, x0 + (i + 1) * step_w, base_y, col, 5)


def sc1(p, t, T):
    character(p, 760, 480, 1.0, la=(115, 100), ra=(40, -60), face="neutral", blink=blink_at(t), look=(16, 4),
              right_hand_item=lambda pp, hx, hy: phone(pp, hx + 10, hy - 40, t * 90))
    rng = np.random.default_rng(7)
    for i in range(9):
        st = 0.3 + i * 0.25
        k = back((t - st) / 0.4)
        if k <= 0:
            continue
        a = rng.uniform(-70, 70)
        r = rng.uniform(260, 420)
        x = 1300 + math.cos(math.radians(a - 90)) * r
        y = 600 + math.sin(math.radians(a - 90)) * r * 0.9 + 60
        y -= (t - st) * 25
        [lambda: heart(p, x, y, 26 * k), lambda: star(p, x, y, 30 * k), lambda: p.text(x, y, "+1k", 40 * k, GREEN)][i % 3]()
    handwrite(p, 760, 120, SCRIPT[0][1], 88, t - 0.4)


def sc2(p, t, T):
    for i, (kind, x) in enumerate((("job", 420), ("car", 960), ("palm", 1500))):
        k = back((t - 0.2 - i * (T / 4)) / 0.45)
        frame_card(p, x, 520 + math.sin(t * 2 + i) * 8, 380, 380, kind, clamp(k, 0, 1.2))
    character(p, 960, 880, 0.45, la=(120, 100), ra=(60, 80), face="worried", blink=blink_at(t), look=(0, -14))
    handwrite(p, 960, 140, SCRIPT[1][1], 92, t - 0.3)


def sc3(p, t, T):
    s = 1.0 - 0.5 * ease((t - 0.4) / 1.6)
    base = 940
    y = base - (165 + 176) * s
    character(p, 960, y, s, la=(105, 95), ra=(75, 85), face="worried", blink=blink_at(t), look=(0, 10),
              head_dy=6 * s)
    cy = y - 300 * s
    k = ease((t - 0.8) / 0.6)
    if k > 0:
        for dx, r in ((-60, 55), (0, 75), (65, 55)):
            p.circle(960 + dx * k, cy - 10, r * k, (170, 170, 180), 5)
        for i in range(6):
            dy = (t * 220 + i * 37) % 160
            rx = 960 - 80 + i * 32
            p.line([(rx, cy + 50 + dy), (rx - 6, cy + 70 + dy)], 4, SKY)
    p.line([(0, base + 2), (1920, base + 2)], 6)
    handwrite(p, 960, 140, SCRIPT[2][1], 92, t - 0.5)


def sc4(p, t, T):
    k1 = back((t - 0.2) / 0.4)
    k2 = back((t - 1.0) / 0.4)
    if k1 > 0:
        p.rect(520 - 330 * k1, 560 - 260 * k1, 520 + 330 * k1, 560 + 260 * k1, (225, 215, 200), 6)
        p.text(520, 240, "YOU (behind the scenes)", 44 * k1 + 1)
        rng = np.random.default_rng(int(t * 6))
        for i in range(7):
            x0, y0 = 520 + rng.uniform(-250, 250) * k1, 560 + rng.uniform(-200, 200) * k1
            pts = [(x0 + 30 * math.cos(a) * k1 + rng.uniform(-8, 8), y0 + 30 * math.sin(a) * k1)
                   for a in np.linspace(0, 6, 8)]
            p.line(pts, 4, GREY)
        character(p, 520, 560, 0.55 * clamp(k1), face="worried", blink=blink_at(t), sweat=(t * 0.7) % 1)
    if k2 > 0:
        p.rect(1400 - 330 * k2, 560 - 260 * k2, 1400 + 330 * k2, 560 + 260 * k2, WHITE, 8)
        p.rect(1400 - 300 * k2, 560 - 230 * k2, 1400 + 300 * k2, 560 + 230 * k2, SKY, 4)
        p.text(1400, 240, "THEM (highlights)", 44 * k2 + 1)
        for i in range(5):
            a = t * 1.5 + i * 1.256
            star(p, 1400 + math.cos(a) * 230 * k2, 560 + math.sin(a) * 170 * k2, 22 * k2)
        character(p, 1400, 560, 0.55 * clamp(k2), face="happy", la=(-150, -115), ra=(-30, -65), blink=blink_at(t))
    p.text(960, 560, "vs", 80 * clamp(k2), RED)
    handwrite(p, 960, 110, SCRIPT[3][1], 84, t - 0.3)


def sc5(p, t, T):
    # a phone screen with a perfect post, failures piling up hidden behind it
    for i in range(int(clamp(t / (T * 0.8)) * 14)):
        rng = np.random.default_rng(i)
        x = 960 + rng.uniform(-420, 420)
        y = 900 - (i % 4) * 30 - rng.uniform(0, 20)
        p.circle(x, y, 32, (235, 235, 230), 4)
        p.line([(x - 15, y - 8), (x + 10, y + 5), (x - 5, y + 14)], 3, GREY)
    labels = ["FAILS", "DOUBTS", "BORING DAYS"]
    for i, lab in enumerate(labels):
        k = back((t - 0.6 - i * 0.6) / 0.35)
        if k > 0:
            p.text(560 + i * 400, 990, lab, 40 * k + 1, (120, 100, 80))
    p.rect(760, 180, 1160, 860, INK, 6)
    p.rect(780, 220, 1140, 820, WHITE, 0)
    frame_card(p, 960, 470, 300, 300, "palm")
    p.text(960, 700, "Living my best life", 30)
    p.text(960, 750, "#blessed", 30, SHIRT)
    handwrite(p, 960, 100, SCRIPT[4][1], 84, t - 0.3)


def sc6(p, t, T):
    k = ease((t - 0.3) / 0.5)
    character(p, 560, 470, 0.85, la=(110, 100), ra=(70, 80), face="neutral", blink=blink_at(t + 1))
    p.text(560, 880, "Yesterday", 54)
    if k > 0:
        x0, x1 = 760, 760 + 380 * k
        p.line([(x0, 520), (x1, 520)], 10, GREEN)
        p.poly([(x1 + 30, 520), (x1 - 10, 490), (x1 - 10, 550)], GREEN, 4)
    k2 = back((t - 0.9) / 0.45)
    if k2 > 0:
        character(p, 1360, 470, 0.85 * clamp(k2, 0, 1.1), la=(-150, -115), ra=(-30, -65), face="happy",
                  blink=blink_at(t))
        p.text(1360, 880, "Today", 54 * clamp(k2))
        p.text(1440, 230, "+1%", 70 * clamp(k2), GREEN)
    handwrite(p, 960, 110, SCRIPT[5][1], 92, t - 1.0)


def sc7(p, t, T):
    icons = ["book", "shoe", "bulb"]
    for i, ic in enumerate(icons):
        st = 0.3 + i * (T - 1.0) / 3
        k = back((t - st) / 0.4)
        x = 480 + i * 480
        if k <= 0:
            continue
        p.circle(x, 470, 170 * clamp(k, 0, 1.1), WHITE, 6)
        if ic == "book":
            p.poly([(x - 90 * k, 420), (x, 445), (x, 545), (x - 90 * k, 520)], SHIRT, 5)
            p.poly([(x + 90 * k, 420), (x, 445), (x, 545), (x + 90 * k, 520)], (110, 175, 220), 5)
            label = "1 page"
        elif ic == "shoe":
            p.poly([(x - 80 * k, 520), (x - 80 * k, 440), (x - 20 * k, 440), (x + 20 * k, 490),
                    (x + 90 * k, 500), (x + 90 * k, 520)], RED, 5)
            p.rect(x - 85 * k, 520, x + 95 * k, 540, WHITE, 4)
            label = "10 min walk"
        else:
            p.circle(x, 450, 60 * k, YELLOW, 5)
            p.rect(x - 25 * k, 505, x + 25 * k, 540, GREY, 4)
            label = "1 new thing"
        p.text(x, 700, label, 54 * clamp(k))
        if t > st + 0.6:
            p.line([(x - 30, 780), (x - 8, 805), (x + 35, 755)], 9, GREEN)
    handwrite(p, 960, 130, SCRIPT[6][1], 92, t - 0.4)


def sc8(p, t, T):
    base = 960
    stairs(p, 700, base, 1)
    character(p, 775, base - 70 - 220, 0.65, la=(115, 100), ra=(65, 80), face="smile", blink=blink_at(t),
              look=(14, -6))
    p.line([(0, base + 2), (1920, base + 2)], 6)
    k = ease((t - 0.8) / 0.6)
    if k > 0:
        p.text(1250, 640, "(just one step)", 52 * k + 1, (120, 100, 80))
    handwrite(p, 960, 150, SCRIPT[7][1], 110, t - 0.3)


def sc9(p, t, T):
    base = 1000
    n = 1 + int(clamp(t / (T * 0.55)) * 6)
    stairs(p, 420, base, n, step_w=150, step_h=70)
    climb = min(clamp(t / (T * 0.75)) * 6, n - 1)
    step = int(climb)
    frac = climb - step
    x = 420 + 75 + (step + ease(frac)) * 150
    hop = math.sin(frac * math.pi) * 40
    y = base - (step + 1 + ease(frac)) * 70 - 228 - hop
    done = t > T * 0.75
    character(p, x, y, 0.65, la=(-150, -115) if done else (120, 90), ra=(-30, -65) if done else (60, 90),
              face="happy" if done else "smile", blink=blink_at(t))
    if done:
        rng = np.random.default_rng(5)
        for i in range(30):
            cx = rng.uniform(200, 1720)
            cy = -40 + ((t * rng.uniform(150, 260) + rng.uniform(0, 1100)) % 1150)
            star(p, cx, cy, 12, [YELLOW, RED, GREEN, SHIRT][i % 4], 0)
    p.line([(0, base + 2), (1920, base + 2)], 6)
    handwrite(p, 760, 170, SCRIPT[8][1], 96, t - 0.4)


def sc10(p, t, T):
    toss = ease((t - 0.5) / 0.7)
    wave = math.sin(t * 7) * 22
    character(p, 700, 470, 1.0, la=(115, 100), ra=(-40, -75 + wave) if toss >= 1 else (40 - 80 * toss, -60),
              face="smile", blink=blink_at(t), look=(10, 0))
    if 0 < toss < 1:
        px, py = 820 + 700 * toss, 380 - 260 * math.sin(toss * math.pi) + 400 * toss ** 2
        phone(p, px, py, 0)
    k = back((t - 1.2) / 0.6)
    if k > 0:
        p.text(1300, 420, SCRIPT[9][1], 120 * k)
    k2 = ease((t - 2.0) / 0.5)
    if k2 > 0:
        stairs(p, 1150, 720, 3, step_w=100, step_h=50)
        p.text(1300, 800, "one small step", 46 * k2 + 1, (120, 100, 80))


SCENES = [sc1, sc2, sc3, sc4, sc5, sc6, sc7, sc8, sc9, sc10]
