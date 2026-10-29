"""C08 manual alignment: the model says its line in 3 runs (1.16-3.5, 4.48-5.22, 6.73-8.03 s) and our voice has a long laugh before "to myself", so build_clip.py's automatic fit does not work.
Our words (voice/tts_ep1/C08.mp3): units [0:9] "All these people, and nobody may speak before me" | [9:12] "I love listening" | [12:15] "(laugh) to myself, mostly". Each unit at tempo 1.15 (the last one 1.22, the laugh-silence shortened) placed at the given start; the laugh falls on the model's snort."""
import subprocess, sys, numpy as np
from faster_whisper import WhisperModel
MODEL, OUT, PREV = "frames/seedance25_c08d_final.mp4", "frames/C08_final.mp4", "frames/C07_final.mp4"
CUTS = [0, 9, 12, 15]; STARTS = [1.10, 4.40, 6.30]; TEMPO = 1.15; SR = 48000; SKIP = 1 / 24
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe("../voice/tts_ep1/C08.mp3", word_timestamps=True, language="en")
ov = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]; assert len(ov) == 15
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "../voice/tts_ep1/C08.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, dtype=np.float32)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MODEL], capture_output=True, text=True).stdout) - SKIP
track = np.zeros(int(SR * (dur + 0.3)), dtype=np.float32)
for (a, b), t0 in zip(zip(CUTS, CUTS[1:]), STARTS):
    s0 = max(0, ov[a][1] - 0.06, ov[a - 1][2] if a else 0); s1 = min(ov[b - 1][2] + 0.10, ov[b][1] - 0.02 if b < len(ov) else 1e9)
    seg = x[int(s0 * SR):int(s1 * SR)]
    if a == 12:                                                      # shorten the silence between the laugh and "to myself" (it makes the words late against the lips)
        w = SR // 100; en = np.array([np.sqrt((seg[i:i + w] ** 2).mean()) for i in range(0, len(seg) - w, w)]); sil = en < 0.02 * en.max()
        keep = []; i = 0
        while i < len(sil):
            j = i
            while j < len(sil) and sil[j] == sil[i]: j += 1
            n = j - i
            keep.append(seg[i * w:(i + (min(n, 6) if sil[i] and i > 5 else n)) * w]); i = j
        seg = np.concatenate(keep)
    seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={TEMPO if a != 12 else 1.22}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, dtype=np.float32)
    i0 = int((t0 - SKIP) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]
    print("unit", a, b, "start", t0, "ends", round(t0 + len(seg) / SR, 2), "of", round(dur, 2))
open(SC + "c08_voice.f32", "wb").write(track.tobytes())
fc = ("[0:v]trim=start_frame=1,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p[vv];"
      "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,volume=2.2dB,alimiter=limit=0.80:attack=2:release=60:level=disabled[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", MODEL, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c08_voice.f32", "-filter_complex", fc, "-map", "[vv]", "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", OUT], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", PREV, "-i", OUT, "-filter_complex", "[0:v]setsar=1[a];[1:v]setsar=1[b];[a][0:a][b][1:a]concat=n=2:v=1:a=1[v][au]", "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k", OUT.replace(".mp4", "_with_prev.mp4")], check=True)
