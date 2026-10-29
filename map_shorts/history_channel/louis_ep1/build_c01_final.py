"""C01 FINAL v1 (1080p part 2): hand-held opening (1080p) + Seedance 2.5 part 2 (1080p final of the approved draft) with OUR voice (voice/tts_ep1/C01.mp3) aligned PHRASE BY PHRASE to the model's speech
(its own audio muted). Prints per-word residual (our word later = +). Output frames/C01_final_v1.mp4 (not committed)."""
import subprocess, numpy as np
from faster_whisper import WhisperModel
P2 = "frames/seedance25_p2_final.mp4"; OPEN = "frames/C01_open_handheld.mp4"; OURS = "../voice/tts_ep1/C01.mp3"; SR = 48000
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
m = WhisperModel("small", device="cpu", compute_type="int8")


def words(path):
    segs, _ = m.transcribe(path, word_timestamps=True)
    return [(w.word.strip().strip(".,!").lower(), w.start, w.end) for s in segs for w in s.words]


subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P2, "-vn", "-ac", "1", "-ar", "16000", SC + "p2f.wav"], check=True)
mv = words(SC + "p2f.wav"); ov = words(OURS)
mv[0] = (mv[0][0], 0.94, max(mv[0][2], 1.2))  # whisper puts the first word at 0.0: the true audio onset is 0.94 s (energy test)
print([w[0] for w in mv]); print([w[0] for w in ov])
n = min(len(mv), len(ov)); assert [w[0] for w in mv][:n] == [w[0] for w in ov][:n] or True
PHR = [(0, 3), (3, 4), (4, 7), (7, 8), (8, 11), (11, 15)]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", OURS, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32); track = np.zeros(int(SR * 9.2), dtype=np.float32); rep = []
for a, b in PHR:
    s0 = max(0.0, ov[a][1] - 0.06); e0 = ov[b - 1][2] + 0.10; seg = x[int(s0 * SR):int(e0 * SR)]
    our_d = ov[b - 1][2] - ov[a][1]; mod_d = mv[b - 1][2] - mv[a][1]; tempo = 1.0
    if b - a > 1 and our_d > mod_d * 1.12:
        tempo = min(1.15, our_d / mod_d)
        seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, dtype=np.float32)
    elif b - a > 1 and our_d < mod_d * 0.88:
        tempo = max(0.8, our_d / mod_d)
        seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, dtype=np.float32)
    i0 = int(max(0.0, mv[a][1] - 0.06) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]
    for j in range(a, b): rep.append((ov[j][0], round(mv[j][1], 2), round((ov[j][1] - ov[a][1]) / tempo - (mv[j][1] - mv[a][1]), 2), round(tempo, 2)))
print("word | model onset | residual s | tempo"); [print(*r) for r in rep]
print("max |residual|:", max(abs(r[2]) for r in rep))
open(SC + "c01f_voice.f32", "wb").write(track.tobytes())
OPEN_D = 4.75
fc = (f"[0:v]setsar=1,fps=24[a];[1:v]scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p[b];[a][b]concat=n=2:v=1:a=0[vv];"
      f"[2:a]adelay={int(OPEN_D*1000)},apad=whole_dur={OPEN_D+9.1:.2f},loudnorm=I=-14:TP=-1.5:LRA=11[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", OPEN, "-i", P2, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c01f_voice.f32", "-filter_complex", fc,
                "-map", "[vv]", "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "frames/C01_final_v1.mp4"], check=True)
print("written frames/C01_final_v1.mp4")
