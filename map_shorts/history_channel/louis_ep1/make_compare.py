"""Side-by-side visual comparison of one clip made by several models (owner 30.10: "Продублируй сцену первую чтоб я сравнил визуально").
Usage: python3 make_compare.py OUT.mp4 "Label A=clipA.mp4" "Label B=clipB.mp4" [...]   (2-3 clips)
Picture: the clips side by side, 540 px wide each, labels on top. The sound plays clip by clip: the same picture runs once per clip and the label of the clip whose sound plays is lit.
Every clip's sound is brought to -16 LUFS with one constant gain (loudness-matched for fair listening; raw levels differ by model).
Review file only (not an episode cut, not for publication). Free (local ffmpeg)."""
import subprocess, sys

out = sys.argv[1]
clips = [a.split("=", 1) for a in sys.argv[2:]]
n = len(clips); W, H = 540, 960; FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
dur = max(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout) for _, p in clips)
def lufs(p):
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in m.splitlines() if l.strip().startswith("I:")][-1].split()[1])


gains = [-16 - lufs(p) for _, p in clips]
inputs = []; fc = []
for i, (lab, p) in enumerate(clips):
    inputs += ["-i", p]
    fc.append(f"[{i}:v]scale={W}:{H}:flags=lanczos,fps=24,tpad=stop_mode=clone:stop_duration={dur:.2f},trim=duration={dur:.2f},setpts=PTS-STARTPTS,setsar=1[v{i}]")
fc.append("".join(f"[v{i}]" for i in range(n)) + f"hstack=inputs={n}[row]")
fc.append(f"[row]split={n}" + "".join(f"[r{k}]" for k in range(n)))
for k in range(n):
    dt = [f"drawtext=fontfile={FONT}:text='{lab.replace(chr(39), '')}{'  [sound]' if i == k else ''}':fontcolor={'yellow' if i == k else 'white@0.45'}:fontsize=22:x={i * W}+16:y=14:box=1:boxcolor=black@0.55:boxborderw=8"
          for i, (lab, _) in enumerate(clips)]
    fc.append(f"[r{k}]" + ",".join(dt) + f"[p{k}]")
    fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gains[k]:.2f}dB,alimiter=limit=0.9:attack=5:release=80:level=disabled,apad=whole_dur={dur:.2f},atrim=duration={dur:.2f},asetpts=PTS-STARTPTS[a{k}]")
fc.append("".join(f"[p{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out], check=True)
print(out, f"{n} clips x {dur:.1f} s = {n * dur:.1f} s; gains dB", [round(g, 1) for g in gains])
