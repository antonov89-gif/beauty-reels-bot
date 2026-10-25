"""Frame forensics for a reference video file: real frames, cuts and motion, so the visual analysis does not rest on a text description.
Usage: python3 frame_forensics.py <video.mp4> <out_dir> [--dense 10]
Writes: sheets_dense_*.jpg (4 fps for the first N s, 12 frames per sheet, timecode burned in), sheets_rest_*.jpg (1 fps), cuts.txt (scene cuts with timecodes),
motion.csv (per-second mean frame difference = visual activity, plus mean brightness), audio_peaks.txt (loud events with timecodes), summary.md.
The analyst then LOOKS at the sheets (Read tool) and writes the second-by-second table from what is on screen; vidIQ/Gemini text stays a hypothesis until confirmed here."""
import csv, json, re, subprocess, sys
from pathlib import Path

FONT = "/home/claude/v38/fonts/bowlby-one.ttf"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(v):
    j = json.loads(run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", v]).stdout)
    vs = next(s for s in j["streams"] if s["codec_type"] == "video")
    num, den = vs["r_frame_rate"].split("/")
    return float(j["format"]["duration"]), int(vs["width"]), int(vs["height"]), float(num) / float(den), any(s["codec_type"] == "audio" for s in j["streams"])


def sheets(v, out, start, end, fps, tag, cols=6, rows=2):
    n = int((end - start) * fps)
    draw = f"drawtext=fontfile={FONT}:text='%{{pts\\:hms\\:{start}}}':x=6:y=6:fontsize=26:fontcolor=yellow:box=1:boxcolor=black@0.6"
    vf = f"fps={fps},scale=240:-1,{draw},tile={cols}x{rows}"
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(end - start), "-i", v, "-vf", vf, str(out / f"sheets_{tag}_%02d.jpg")])


def cuts(v, thr=0.3):
    r = run(["ffmpeg", "-hide_banner", "-i", v, "-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"])
    return [round(float(t), 2) for t in re.findall(r"pts_time:([0-9.]+)", r.stderr)]


def motion(v, out):
    r = run(["ffmpeg", "-hide_banner", "-i", v, "-vf", "fps=10,scale=160:-1,format=gray,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"])
    vals = [float(x) for x in re.findall(r"YAVG=([0-9.]+)", r.stderr)]
    rows = []
    for s in range(0, len(vals) // 10 + 1):
        chunk = vals[s * 10:(s + 1) * 10]
        if chunk:
            rows.append((s, round(sum(chunk) / len(chunk), 2)))
    with open(out / "motion.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["second", "mean_frame_difference"]); w.writerows(rows)
    return rows


def audio_peaks(v, out):
    r = run(["ffmpeg", "-hide_banner", "-i", v, "-af", "astats=metadata=1:reset=5,ametadata=print:key=lavfi.astats.Overall.Peak_level", "-vn", "-f", "null", "-"])
    pk = [(round(i * 0.1 * 5, 1) if False else None) for i in range(0)]
    lines = re.findall(r"pts_time:([0-9.]+).*?Peak_level=(-?[0-9.]+|-inf)", r.stderr.replace("\n", " "))
    ev = [(float(t), float(p)) for t, p in lines if p != "-inf" and float(p) > -6]
    (out / "audio_peaks.txt").write_text("\n".join(f"{t:.1f}s peak {p} dBFS" for t, p in ev) or "no peaks above -6 dBFS")
    return ev


if __name__ == "__main__":
    v, out = sys.argv[1], Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    dense = float(sys.argv[sys.argv.index("--dense") + 1]) if "--dense" in sys.argv else 10.0
    dur, w, h, fps, has_a = probe(v)
    sheets(v, out, 0, min(dense, dur), 4, "dense")
    if dur > dense:
        sheets(v, out, dense, dur, 1, "rest")
    c = cuts(v); m = motion(v, out); a = audio_peaks(v, out) if has_a else []
    (out / "cuts.txt").write_text("\n".join(f"{t}s" for t in c))
    per10 = [sum(1 for t in c if k * 10 <= t < (k + 1) * 10) for k in range(int(dur // 10) + 1)]
    md = [f"# Frame forensics: {Path(v).name}", f"- {w}x{h}, {fps:.2f} fps, {dur:.2f} s, audio: {has_a}", f"- hard cuts (scene>0.3): {len(c)}; per 10 s: {per10}",
          f"- mean cut length: {dur / (len(c) + 1):.2f} s", f"- busiest seconds: {sorted(m, key=lambda x: -x[1])[:5]}", f"- calmest seconds: {sorted(m, key=lambda x: x[1])[:3]}",
          f"- loud audio events (> -6 dBFS): {len(a)}", "", "Next: open the sheets and write the second-by-second table from what is visible. Text descriptions from tools are HYPOTHESES until confirmed on these frames."]
    (out / "summary.md").write_text("\n".join(md)); print("\n".join(md))
