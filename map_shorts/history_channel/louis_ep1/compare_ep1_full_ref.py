"""Episode 1 full cut vs the reference Vlog 1 (LjfGP7wpjVs), owner 31.10: "Ещё раз сравни и напиши чем отличается и где лучше".
The reference mp4 is not on disk: its numbers come from compare_reference_ep1_v2.md (measured 30.10 with the same formulas). This script measures OUR cut the same way:
picture at 240 px sheet-tile size, 1 fps (brightness = mean luma, texture = Laplacian variance: calibrated on C02_final 116/895 vs the recorded 116/887; grain = Immerkaer noise sigma, approximate);
motion = frame_forensics.py (fps 10, 160 px, mean frame difference per second); cuts = scene > 0.3; speech = faster-whisper word timestamps per clip; loudness = ebur128; pause floor = RMS of 50-ms windows in the gaps between words.
Usage: python3 compare_ep1_full_ref.py frames/EP1_full_C.mp4. Free (local)."""
import re, subprocess, sys, numpy as np, cv2
from faster_whisper import WhisperModel
P = sys.argv[1]; SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
starts = [(l.split()[0], float(l.split()[1])) for l in open(SC + "ep1_starts.txt")]
end_card = dict(starts)["END"]
raw = subprocess.run(["ffmpeg", "-v", "error", "-t", f"{end_card:.2f}", "-i", P, "-vf", "fps=1,scale=240:426", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 426, 240, 3); g = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in fr]
K = np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]], float)
bright = [x.mean() for x in g]; tex = [cv2.Laplacian(x, cv2.CV_64F).var() for x in g]; grain = [np.sqrt(np.pi / 2) * np.abs(cv2.filter2D(x.astype(float), -1, K)).mean() / 6 for x in g]
print(f"picture (1 fps, without the end card): brightness {np.mean(bright):.0f} | texture {np.mean(tex):.0f} | grain ~{np.mean(grain):.2f}")
for c, a in starts:
    if c == "END": continue
    b = [s for k, s in starts if k != c and s > a]; b = min(b) if b else end_card; idx = range(int(a), min(int(b), len(g)))
    if len(idx): print(f"  {c}: brightness {np.mean([bright[i] for i in idx]):.0f}, texture {np.mean([tex[i] for i in idx]):.0f}")
r = subprocess.run(["ffmpeg", "-hide_banner", "-t", f"{end_card:.2f}", "-i", P, "-vf", "fps=10,scale=160:-1,format=gray,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
v = [float(x) for x in re.findall(r"YAVG=([0-9.]+)", r)]; sec = [np.mean(v[s * 10:(s + 1) * 10]) for s in range(len(v) // 10)]
print(f"camera motion: {100 * np.mean(np.array(sec) < 2):.0f} % of seconds below 2 (still); median {np.median(sec):.1f}; calm seconds: {[i for i, x in enumerate(sec) if x < 2]}")
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", P, "-vf", "select='gt(scene,0.3)',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
cuts = [round(float(t), 2) for t in re.findall(r"pts_time:([0-9.]+)", r)]
print(f"hard cuts (scene > 0.3): {len(cuts)} in {end_card:.0f} s: {cuts}")
wav = SC + "cmp_full16.wav"; subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
m = WhisperModel("medium", device="cpu", compute_type="int8"); s, _ = m.transcribe(wav, word_timestamps=True, language="en", beam_size=5)
words = [(w.start, w.end, w.word) for seg in s for w in seg.words]
tot_w = 0; tot_speak = 0; gaps_all = []
print("clip | words | wpm (clip length) | words per speaking second | pauses > 0.5 s")
for i, (c, a) in enumerate(starts):
    if c in ("END", "C11"): continue
    b = starts[i + 1][1]; ws = [w for w in words if a <= w[0] < b]
    if not ws: continue
    speak = sum(e - st for st, e, _ in ws); gaps = [ws[k + 1][0] - ws[k][1] for k in range(len(ws) - 1)]; gaps_all += [(ws[k][1], ws[k + 1][0]) for k in range(len(ws) - 1) if ws[k + 1][0] - ws[k][1] > 0.25]
    tot_w += len(ws); tot_speak += speak
    print(f"{c} | {len(ws)} | {60 * len(ws) / (b - a):.0f} | {len(ws) / speak:.1f} | {sum(1 for q in gaps if q > 0.5)}")
spoken = end_card - dict(starts)["C11"] + dict(starts)["C11"] - 8.0
print(f"whole episode: {tot_w} words, {60 * tot_w / spoken:.0f} wpm over the {spoken:.0f} s with speech clips, {tot_w / tot_speak:.1f} words per speaking second")
fl = [20 * np.log10(np.sqrt((x[int((a + .05) * 16000):int((b - .05) * 16000)] ** 2).mean()) + 1e-9) for a, b in gaps_all if b - a > 0.2]
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", P, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
print(f"sound: {r.split('I:')[-1].split('LUFS')[0].strip()} LUFS; pause floor (between words) median {np.median(fl):.1f} dB RMS")
