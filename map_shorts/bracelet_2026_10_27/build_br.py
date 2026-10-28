"""Bracelet rescue Short (another channel, AI-generated, realistic): 13 Seedance 2.0 clips cut to the reference's rhythm (about 2.6 s per shot, 34 s),
no voice, no music, no captions: the clips' native foley (cutter, torch, rollers, hammer) with short fades at the cuts, loudness -14 LUFS.
Clips /home/claude/v90/clips (b01 from /home/claude/v90/pilot/seedance_b01.mp4). Output /home/claude/v90/br_final.mp4 (1080x1920, upscaled from 720p)."""
import subprocess
from pathlib import Path

W = Path("/home/claude/v90")
FPS, WD, HT = 24, 1080, 1920
# (clip file, src_in, duration)
EDL = [
    (W / "pilot/seedance_b01.mp4", 0.0, 2.4),   # 1 the cutter on the bangle (hook)
    (W / "clips/b02.mp4", 0.5, 1.8),            # 2 cutter, gold dust
    (W / "clips/b03_v2.mp4", 1.4, 2.0),         # 3 cut through (v2: thin groove between the cut ends instead of a tan band; the gap opens after ~1.8 s)
    (W / "clips/b04.mp4", 1.4, 2.2),            # 4 pliers, bangle off (it slides off after ~3 s in the clip)
    (W / "clips/b05.mp4", 0.0, 2.0),            # 5 crucible + flux
    (W / "clips/b06.mp4", 0.0, 3.6),            # 6 torch melt
    (W / "clips/b07.mp4", 0.0, 3.0),            # 7 pour
    (W / "clips/b08.mp4", 0.0, 3.0),            # 8 quench
    (W / "clips/b09.mp4", 0.0, 3.0),            # 9 rolling mill
    (W / "clips/b10.mp4", 0.0, 3.0),            # 10 strip
    (W / "clips/b11.mp4", 0.0, 3.0),            # 11 hammer on the mandrel
    (W / "clips/b12.mp4", 0.0, 2.0),            # 12 polish
    (W / "clips/b13.mp4", 0.0, 3.4),            # 13 she wears the cuff
]
FADE = 0.04


def seg_gain(f, s0, d, target=-24.0, cap=15.0):
    """Gain in dB that brings the segment's mean volume to the target (the clips' native audio differs by up to 20 dB), capped so that room noise is not boosted too far."""
    import re
    e = subprocess.run(["ffmpeg", "-hide_banner", "-ss", str(s0), "-t", str(d), "-i", str(f), "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.search(r"mean_volume: (-?[0-9.]+) dB", e)
    return 0.0 if not m else max(-6.0, min(cap, target - float(m.group(1))))


def two_pass(out):
    """EBU R128 in two passes on the finished mix (-14 LUFS, true peak -1.5), then remux with the untouched video."""
    import json
    import re
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-vn", "-af", "loudnorm=I=-14:TP=-2.3:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", raw, re.S).group(0))
    af = (f"loudnorm=I=-14:TP=-2.3:LRA=9:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    tmp = Path(str(out) + ".tmp.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(out)


def main(out=W / "br_final.mp4"):
    inputs, vf, af = [], [], []
    for i, (f, s0, d) in enumerate(EDL):
        inputs += ["-i", str(f)]
        vf.append(f"[{i}:v]trim=start={s0}:duration={d + 0.05:.3f},setpts=PTS-STARTPTS,scale={WD}:{HT}:flags=lanczos,setsar=1,fps={FPS},trim=duration={d:.3f},setpts=PTS-STARTPTS,"
                  f"eq=contrast=1.04:saturation=1.04,unsharp=5:5:0.5[v{i}]")
        g = seg_gain(f, s0, d)
        af.append(f"[{i}:a]atrim=start={s0}:duration={d:.3f},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,volume={g:.1f}dB,"
                  f"afade=t=in:st=0:d={FADE},afade=t=out:st={d - FADE:.3f}:d={FADE}[a{i}]")
    n = len(EDL)
    cat = "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v];" + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,acompressor=threshold=-22dB:ratio=3:attack=10:release=150:makeup=2,alimiter=limit=0.84[a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(vf + af + [cat]), "-map", "[v]", "-map", "[a]", "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    two_pass(out)
    print("done", sum(d for _, _, d in EDL), "s")


if __name__ == "__main__":
    main()
