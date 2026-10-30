"""C03 manual alignment (owner 30.10: "24-25 секунда как будто нужна пауза"): the model says "...see them. Everyone came..." with only a 0.24 s gap, so the automatic fit left no beat
before the punchline. Here sentence 1 runs a little faster (tempo 1.2, it then ends with the model's "them" at about 4.6 s) and "Everyone came to see me." starts later,
which gives a real pause before the punchline. Cost: "Everyone came to see me" sits about 0.2 s after the model's lips. "Naturally." stays on the model's second phrase.
Our words (voice/tts_ep1/C03.mp3, 18 words): units [0:12] [12:17] [17:18]."""
import subprocess, numpy as np
from faster_whisper import WhisperModel
MODEL, OUT, PREV = "frames/seedance25_c03_final.mp4", "frames/C03_final.mp4", "frames/C02_final.mp4"
CUTS = [0, 12, 17, 18]; STARTS = [1.56, 4.88, 7.00]; TEMPOS = [1.20, 1.12, 1.0]; SR = 48000; SKIP = 1 / 24
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe("../voice/tts_ep1/C03.mp3", word_timestamps=True, language="en")
ov = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]; assert len(ov) == 18, [w for w, _, _ in ov]
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "../voice/tts_ep1/C03.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, dtype=np.float32)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MODEL], capture_output=True, text=True).stdout) - SKIP
track = np.zeros(int(SR * (dur + 0.3)), dtype=np.float32)


def cut_at(j):                                                      # quietest point of the pause before our word j
    lo, hi = max(0.0, ov[j - 1][2] - 0.05), min(len(x) / SR, ov[j][1] + 0.15)
    return min((np.sqrt((x[int(t * SR):int((t + .02) * SR)] ** 2).mean()), t) for t in np.arange(lo, max(lo + .01, hi - .02), .005))[1] + 0.01


for (a, b), t0, tp in zip(zip(CUTS, CUTS[1:]), STARTS, TEMPOS):
    s0 = cut_at(a) if a else max(0, ov[0][1] - 0.06); s1 = cut_at(b) if b < len(ov) else ov[-1][2] + 0.25
    seg = x[int(s0 * SR):int(s1 * SR)].copy(); f = int(SR * .006); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    if tp != 1.0: seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tp}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, dtype=np.float32)
    lead = (ov[a][1] - s0) / tp; i0 = int(max(0, t0 - lead - SKIP) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]   # t0 = where the first word starts
    print("unit", " ".join(w for w, _, _ in ov[a:b]), "| word starts", t0, "ends", round(t0 - lead + len(seg) / SR, 2), "of", round(dur, 2))
open(SC + "c03_voice.f32", "wb").write(track.tobytes())
fc = ("[0:v]trim=start_frame=1,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p[vv];"
      "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,volume=2.2dB,alimiter=limit=0.80:attack=2:release=60:level=disabled[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", MODEL, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c03_voice.f32", "-filter_complex", fc, "-map", "[vv]", "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", OUT], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", PREV, "-i", OUT, "-filter_complex", "[0:v]setsar=1[a];[1:v]setsar=1[b];[a][0:a][b][1:a]concat=n=2:v=1:a=1[v][au]", "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k", OUT.replace(".mp4", "_with_prev.mp4")], check=True)
