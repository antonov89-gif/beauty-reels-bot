"""Self-check of the episode cut (CLAUDE.md "проверяй всё сам" before showing): length and size, loudness, ASR of every clip's line against lines_ep1_emotion.json,
speaker similarity of each clip's voice to our v3 take and to its neighbours, music check, a contact sheet of the frames around every cut and of the plates, the last frame.
Usage: python3 check_ep1.py frames/EP1_full_A.mp4 -> prints the report, writes <scratchpad>/ep1_check/{cuts.jpg,plates.jpg,last.jpg}. Free (local)."""
import json, re, subprocess, sys, os, numpy as np
from faster_whisper import WhisperModel
from resemblyzer import VoiceEncoder, preprocess_wav
from PIL import Image, ImageDraw
P = sys.argv[1]; SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"; OUT = SC + "ep1_check/"; os.makedirs(OUT, exist_ok=True)
starts = [(l.split()[0], float(l.split()[1])) for l in open(SC + "ep1_starts.txt")]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", P], capture_output=True, text=True).stdout)
bounds = [(c, a, (starts[i + 1][1] if i + 1 < len(starts) else dur)) for i, (c, a) in enumerate(starts)]
print(f"file {P}: {dur:.2f} s ({int(dur // 60)}:{dur % 60:04.1f}), {os.path.getsize(P) / 1e6:.0f} MB")
print(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,sample_rate,channels", "-of", "compact", P], capture_output=True, text=True).stdout.strip())
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", P, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print("loudness:", " | ".join(l.strip() for l in r.split("Summary:")[-1].splitlines() if re.match(r"\s+(I|LRA|Peak):", l)))
wav = SC + "ep1_check.wav"; subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
lines = json.load(open("../voice/lines_ep1_emotion.json"))["lines"]
def clean(s): return re.sub(r"[^a-z' ]", " ", re.sub(r"\[[^\]]*\]|\{\{[^}]*\}\}", " ", s.lower())).split()
m = WhisperModel("medium", device="cpu", compute_type="int8"); enc = VoiceEncoder("cpu")
v3 = enc.embed_utterance(preprocess_wav(np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "../voice/tts_ep1/C10.mp3", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32), source_sr=16000))
emb = {}
print("clip | start-end | per-clip LUFS | ASR words found / expected | missing | voice sim to v3 take")
for c, a, b in bounds:
    seg = x[int(a * 16000):int(b * 16000)]
    rr = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", "16000", "-ac", "1", "-i", "-", "-af", "ebur128", "-f", "null", "-"], input=seg.tobytes(), capture_output=True).stderr.decode()
    li = float([l for l in rr.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    if c in ("C11", "END"):
        print(f"{c} | {a:.2f}-{b:.2f} | {li:.1f} | (no line)"); continue
    tmp = OUT + f"{c}.wav"; subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", "16000", "-ac", "1", "-i", "-", tmp], input=seg.tobytes(), check=True)
    s, _ = m.transcribe(tmp, language="en", beam_size=5); heard = clean(" ".join(z.text for z in s))
    want = clean(lines.get(c, "")); miss = [w for w in want if w not in heard]
    e = enc.embed_utterance(preprocess_wav(seg, source_sr=16000)); emb[c] = e
    print(f"{c} | {a:.2f}-{b:.2f} | {li:.1f} | {len(want) - len(miss)}/{len(want)} | {' '.join(miss) or '-'} | {float(e @ v3):.2f}")
ks = list(emb); print("neighbour voice similarity:", " ".join(f"{ks[i]}-{ks[i + 1]} {float(emb[ks[i]] @ emb[ks[i + 1]]):.2f}" for i in range(len(ks) - 1)))
# music check: a melody or a held note shows as the same strong spectral peak in many frames; speech harmonics move (same test that rejected recording 3432)
import scipy.signal as ss
f, t, Z = ss.stft(x, 16000, nperseg=4096, noverlap=3072); A = 20 * np.log10(np.abs(Z) + 1e-9); pk = (A - ss.medfilt(A, [31, 1])) > 12
per = pk[f > 200].mean(1); f2 = f[f > 200]; top = np.argsort(per)[-4:][::-1]
print("music check, most persistent strong peaks > 200 Hz (Hz: % of frames; approved beds <= 3.4 %, rejected 3432 had 8.1 %):", [(int(f2[i]), round(float(per[i]) * 100, 1)) for i in top])
def frame(t_, w=216):
    d = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t_):.3f}", "-i", P, "-frames:v", "1", "-vf", f"scale={w}:-2", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    from io import BytesIO; return Image.open(BytesIO(d)).convert("RGB")
cuts = [a for _, a, _ in bounds[1:]]; W = 216; H = 384
sheet = Image.new("RGB", (W * 2 * 8, (H + 18) * ((len(cuts) + 7) // 8)), "black"); dr = ImageDraw.Draw(sheet)
for i, a in enumerate(cuts):
    for j, tt in enumerate((a - 0.08, a + 0.04)):
        x0 = (i % 8) * 2 * W + j * W; y0 = (i // 8) * (H + 18); sheet.paste(frame(tt).resize((W, H)), (x0, y0 + 18)); dr.text((x0 + 4, y0 + 3), f"{bounds[i + 1][0]} {'out' if j == 0 else 'in'} {tt:.2f}", fill="yellow")
sheet.save(OUT + "cuts.jpg", quality=85)
pl = Image.new("RGB", (W * 6, (H + 18) * 2), "black"); dr = ImageDraw.Draw(pl)
from build_ep1 import PLATES
st = dict(starts)
for i, (c, a, b, _) in enumerate(PLATES[:11]):
    if i >= 12: break
    x0 = (i % 6) * W; y0 = (i // 6) * (H + 18); pl.paste(frame(st[c] + (a + b) / 2).resize((W, H)), (x0, y0 + 18)); dr.text((x0 + 4, y0 + 3), f"{c} {st[c] + (a + b) / 2:.1f}", fill="yellow")
pl.save(OUT + "plates.jpg", quality=85)
frame(dur - 0.05, 540).save(OUT + "last.jpg"); frame(st["END"] - 0.05, 540).save(OUT + "c15_last.jpg")
print("sheets:", OUT)
