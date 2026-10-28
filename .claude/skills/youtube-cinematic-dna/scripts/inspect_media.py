#!/usr/bin/env python3
"""Prepare bounded local-media evidence samples using ffmpeg/ffprobe.

This extracts, but does NOT itself watch/hear/analyze, sampled frames or audio.
Example:
  python scripts/inspect_media.py input.mp4 --out inspection --start 0 --duration 10 --fps 6
A populated output directory cannot be reused without --overwrite. Overwrite
removes only this script's numbered frame outputs and named audio/manifest.
No YouTube downloader or network access is included.
"""
import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def probe(path):
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(proc.stdout)


def run(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("--out", type=Path, default=Path("inspection"))
    p.add_argument("--start", type=float, default=0)
    p.add_argument("--duration", type=float, default=10)
    p.add_argument("--fps", type=float, default=4)
    p.add_argument("--max-frames", type=int, default=120)
    p.add_argument("--overwrite", action="store_true", help="Replace previously generated numbered frames/audio/manifest in output directory")
    p.add_argument("--no-audio", action="store_true", help="Skip extracting the synchronized audio sample")
    args = p.parse_args(argv)
    if not args.input.is_file():
        p.error("input must be an existing local file; URL download is not supported")
    if args.start < 0 or args.duration <= 0 or args.fps <= 0:
        p.error("start must be nonnegative, duration and fps positive")
    if args.max_frames <= 0 or args.duration * args.fps > args.max_frames:
        p.error("requested sample is too large; shorten range or reduce fps")
    for tool in ("ffprobe", "ffmpeg"):
        if not shutil.which(tool):
            p.error(f"{tool} not found in PATH")

    try:
        media = probe(args.input)
    except (subprocess.CalledProcessError, ValueError) as exc:
        print(f"FAIL: cannot probe media: {exc}", file=sys.stderr)
        return 1
    if not any(s.get("codec_type") == "video" for s in media.get("streams", [])):
        p.error("no video stream detected")
    available_sec = float(media.get("format", {}).get("duration", "0") or 0)
    if available_sec > 0 and args.start >= available_sec:
        p.error(f"start {args.start}s is outside media duration {available_sec}s")

    frames_dir = args.out / "frames"
    old_outputs = list(frames_dir.glob("frame_*.jpg")) if frames_dir.exists() else []
    old_outputs += [x for x in (args.out / "sample_audio.wav", args.out / "manifest.json") if x.exists()]
    if old_outputs and not args.overwrite:
        p.error("output contains earlier samples; use a fresh --out or specify --overwrite")
    args.out.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(exist_ok=True)
    if args.overwrite:
        for item in old_outputs:
            item.unlink()

    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(args.start), "-t", str(args.duration), "-i", str(args.input), "-vf", f"fps={args.fps}", "-q:v", "3", str(frames_dir / "frame_%04d.jpg")]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        samples = sorted(str(item.relative_to(args.out)) for item in frames_dir.glob("frame_*.jpg"))
        if not samples:
            print("FAIL: ffmpeg produced no frames", file=sys.stderr)
            return 1
        audio = None
        has_audio = any(s.get("codec_type") == "audio" for s in media.get("streams", []))
        if has_audio and not args.no_audio:
            audio_cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(args.start), "-t", str(args.duration), "-i", str(args.input), "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(args.out / "sample_audio.wav")]
            subprocess.run(audio_cmd, capture_output=True, text=True, check=True)
            audio = "sample_audio.wav"
    except subprocess.CalledProcessError as exc:
        print(f"FAIL: ffmpeg sampling: {exc.stderr or exc}", file=sys.stderr)
        return 1
    manifest = {
        "source_file": str(args.input),
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "inspected_by_tool": "ffprobe + ffmpeg extraction ONLY; neither frames nor audio have been interpreted",
        "actual_media": media,
        "selected_range_sec": [args.start, min(args.start + args.duration, available_sec) if available_sec > 0 else args.start + args.duration],
        "nominal_sample_fps": args.fps,
        "frame_count": len(samples),
        "frames": samples,
        "audio_extracted": audio,
        "audio_present_in_source": has_audio,
        "sampling_limit": "sampled frames cannot reveal all fast cuts or motion; extracted audio is NOT automatically listened to",
    }
    (args.out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {len(samples)} sampled frames; audio={audio or 'none'}; manifest: {args.out / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
