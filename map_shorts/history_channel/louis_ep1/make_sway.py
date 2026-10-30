"""Digital hand-held sway for the frozen propped-phone clips C04-C05 (compare_reference_ep1_v2.md item 3: 16 % of our seconds were nearly still, reference 3 %).
The phone rests loosely against something on the table: slow drift and roll (smoothed random walk) plus short nudges when he touches the table, then it settles.
8 % zoom hides the borders. Usage: python3 make_sway.py <in.mp4> <out.mp4> <seed> <nudge times s, comma separated> [settle_end]
settle_end: the last 0.7 s returns to the untouched frame (zoom 1.0, no offset), so an invisible join into the next clip (C05 -> C06, same frame) stays invisible."""
import sys, subprocess, numpy as np, cv2
src, out, seed, nudges = sys.argv[1], sys.argv[2], int(sys.argv[3]), [float(t) for t in sys.argv[4].split(",") if t]
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); W = int(cap.get(3)); H = int(cap.get(4)); N = int(cap.get(7))
r = np.random.default_rng(seed); t = np.arange(N) / fps


def walk(sd, smooth_s):
    k = max(3, int(smooth_s * fps)); w = np.cumsum(r.normal(0, 1, N + 2 * k)); w = np.convolve(w, np.hanning(k) / np.hanning(k).sum(), "same")[k:k + N]
    w -= np.linspace(w[0], w[-1], N) * 0.6; return w / (np.abs(w).max() + 1e-9) * sd


dx = walk(0.012 * W, 1.2) + walk(0.003 * W, 0.25); dy = walk(0.010 * H, 1.4) + walk(0.0025 * H, 0.25); rot = walk(0.9, 1.6)
for n0 in nudges:                                                     # a nudge: fast offset in 0.12 s, settles with a small overshoot over 0.6 s
    a = r.uniform(-1, 1, 3) * np.array([0.03 * W, 0.022 * H, 2.0]); x = t - n0
    e = np.where(x < 0, 0, np.where(x < .12, x / .12, np.exp(-(x - .12) / .35) * np.cos((x - .12) * 9)))
    dx += a[0] * e; dy += a[1] * e; rot += a[2] * e
zoom = np.full(N, 1.08)
if len(sys.argv) > 5 and sys.argv[5] == "settle_end":
    k = np.clip((t - (t[-1] - 0.7)) / 0.7, 0, 1); k = k * k * (3 - 2 * k); dx *= 1 - k; dy *= 1 - k; rot *= 1 - k; zoom = 1.08 - 0.08 * k
p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a",
                      "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", out], stdin=subprocess.PIPE)
for i in range(N):
    ok, f = cap.read()
    if not ok: break
    M = cv2.getRotationMatrix2D((W / 2, H / 2), rot[i], zoom[i]); M[0, 2] += dx[i]; M[1, 2] += dy[i]
    p.stdin.write(cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT).tobytes())
p.stdin.close(); p.wait()
