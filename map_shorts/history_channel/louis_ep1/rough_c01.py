"""C01 rough cut for the lip-sync check: part 1 v2 (ceiling tilt, Kling) + part 2 (Seedance 720p test) with OUR locked voice aligned phrase by phrase to the
speech timing the video model used (its own audio is muted: no music, no foreign voice). Prints the residual offset per word.
Usage: python3 rough_c01.py  -> frames/C01_rough_seedance.mp4 (not committed)"""
import json, subprocess, numpy as np
from faster_whisper import WhisperModel

P1 = "frames/kling_i2v_part1_v2.mp4"; P2 = "frames/seedance_part2.mp4"
OURS = "../voice/tts_ep1/C01_drive_10s.mp3"; CUT1 = 1.92; XF = 0.13; HOLD = 0.7; SR = 48000  # cut inside the landing motion, 4-frame dissolve hides the re-rendered first frame
m = WhisperModel("small", device="cpu", compute_type="int8")


def words(path):
    segs, _ = m.transcribe(path, word_timestamps=True)
    return [(w.word.strip().strip(".,").lower(), w.start, w.end) for s in segs for w in s.words]


subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P2, "-vn", "-ac", "1", "-ar", "16000", "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/p2a.wav"], check=True)
mv = words("/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/p2a.wav"); ov = words(OURS)
assert [w[0] for w in mv] == [w[0] for w in ov], ([w[0] for w in mv], [w[0] for w in ov])
PHR = [(0, 4), (4, 5), (5, 6), (6, 9), (9, 10), (10, 13), (13, 17)]  # word index ranges: Marcel..ceiling | Me | Good | Welcome..Versailles | Yes | I'm that handsome | Try..faint
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", OURS, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
track = np.zeros(int(SR * 10.1), dtype=np.float32); report = []
for a, b in PHR:
    s0 = max(0.0, ov[a][1] - 0.06); e0 = ov[b - 1][2] + 0.10
    seg = x[int(s0 * SR):int(e0 * SR)]
    our_d = ov[b - 1][2] - ov[a][1]; mod_d = mv[b - 1][2] - mv[a][1]; tempo = 1.0
    if our_d > mod_d * 1.15 and b - a > 1:   # mild compression only, never above 1.3x
        tempo = min(1.3, our_d / mod_d)
        seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, dtype=np.float32)
    t0 = max(0.0, mv[a][1] - 0.06); i0 = int(t0 * SR)
    n_ = min(len(seg), len(track) - i0)
    track[i0:i0 + n_] += seg[:n_]
    for k in range(a, b):
        ours_rel = (ov[k][1] - ov[a][1]) / tempo; mod_rel = mv[k][1] - mv[a][1]
        report.append((ov[k][0], round(mv[k][1], 2), round(ours_rel - mod_rel, 2), round(tempo, 2)))
print("word | model onset s | residual s (our word later +) | tempo")
for r in report: print(*r)
print("max |residual|:", max(abs(r[2]) for r in report))
open("/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/c01_voice_aligned.f32", "wb").write(track.tobytes())
# timeline: 0.7 s longer ceiling hold (first frame cloned) + measured hand-held shake on part 1 (owner: ceiling >= 1.3 s, natural shake), cut inside the landing, part 2; voice starts with part 2
voice = f"[2:a]adelay={int((HOLD+CUT1-XF)*1000)},apad=whole_dur={HOLD+CUT1-XF+10.04:.2f},loudnorm=I=-14:TP=-1.5:LRA=11[v]"
fc = (f"[0:v]trim=0:{CUT1},setpts=PTS-STARTPTS,tpad=start_duration={HOLD}:start_mode=clone,scale=1112:1984,"
      f"crop=1080:1920:x='16+7*sin(t*11.3)+4*sin(t*27.1)+2*sin(t*53.7)':y='32+6*sin(t*9.1+1)+4*sin(t*23.3)+2*sin(t*47.9)',fps=24,format=yuv420p[a1];"
      f"[1:v]scale=1080:1920,setpts=PTS-STARTPTS,fps=24,format=yuv420p[a2];[a1][a2]xfade=transition=fade:duration={XF}:offset={HOLD+CUT1-XF:.3f}[vv];" + voice)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P1, "-i", P2, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i",
                "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/c01_voice_aligned.f32",
                "-filter_complex", fc, "-map", "[vv]", "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                "frames/C01_rough_seedance.mp4"], check=True)
print("written frames/C01_rough_seedance.mp4")
