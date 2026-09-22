#!/usr/bin/env python3
"""Assemble the 128-shot timeline into the final narrated video.

Cross-platform replacement for ASSEMBLE_FULL_VIDEO.ps1: the shot list is read
from ASSEMBLY_TIMELINE_128.csv instead of being hard-coded per shot.
"""

import argparse
import csv
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

WIDTH = 1920
HEIGHT = 1080
FPS = 25

TIMELINE = Path(__file__).resolve().parent / "timeline" / "ASSEMBLY_TIMELINE_128.csv"
SUBTITLE_STYLE = (
    "FontName=Arial,FontSize=22,Bold=1,PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=1,"
    "Alignment=2,MarginV=60"
)
FIT = (
    f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
    f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={FPS}"
)


class Shot:
    def __init__(self, row):
        self.order = int(row["order"])
        self.shot = row["shot"]
        self.animate = row["asset_type"] == "ANIMATE_CLIP"
        self.still_name = row["master_filename"]
        self.duration = float(row["dur_s"])
        self.source = None
        self.source_is_clip = False


def read_timeline(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return [Shot(row) for row in csv.DictReader(fh)]


def resolve_sources(shots, root):
    """Point every shot at a file on disk; return the shots with nothing to use."""
    clips = root / "veo_clips"
    stills = root / "master_pngs"
    missing = []
    for shot in shots:
        clip = None
        if shot.animate and clips.is_dir():
            clip = next(iter(sorted(clips.glob(f"{shot.shot}_*.mp4"))), None)
        still = stills / shot.still_name
        if clip is not None:
            shot.source, shot.source_is_clip = clip, True
        elif still.is_file():
            shot.source = still
        else:
            missing.append(shot)
    return missing


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd)}\n{result.stderr[-2000:]}")


def build_segment(shot, segments_dir):
    out = segments_dir / f"seg_{shot.shot}.mp4"
    if shot.source_is_clip:
        # Clips are 4s; clone the last frame so a longer slot still fills.
        source_args = ["-i", str(shot.source)]
        vf = f"{FIT},tpad=stop_mode=clone:stop_duration=10"
    else:
        source_args = ["-loop", "1", "-i", str(shot.source)]
        vf = FIT
    run(
        ["ffmpeg", "-y", *source_args, "-vf", vf, "-t", f"{shot.duration:.3f}",
         "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out)]
    )
    return out


def concat(files, out, work_dir, name):
    listing = work_dir / name
    listing.write_text(
        "".join(f"file '{Path(f).resolve().as_posix()}'\n" for f in files), encoding="ascii"
    )
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(out)])
    return out


def escape_for_filter(path):
    """ffmpeg's subtitles= filter needs its path escaped twice (\\ : ')."""
    text = Path(path).resolve().as_posix()
    for char in ("\\", ":", "'"):
        text = text.replace(char, "\\" + char)
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path.cwd(),
        help="folder holding master_pngs/, veo_clips/, vo_part*.mp3 and NARRATION.srt",
    )
    parser.add_argument("--out", type=Path, default=None, help="final mp4 path")
    parser.add_argument("--jobs", type=int, default=os.cpu_count() or 4)
    parser.add_argument("--check", action="store_true", help="report missing assets and stop")
    args = parser.parse_args()

    root = args.root.resolve()
    out = args.out or root / "FINAL_you-work-more-than-a-caveman.mp4"

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not found on PATH")

    shots = read_timeline(TIMELINE)
    missing = resolve_sources(shots, root)
    srt = root / "NARRATION.srt"
    vo_parts = [root / "vo_part1.mp3", root / "vo_part2.mp3"]
    missing_audio = [p for p in [*vo_parts, srt] if not p.is_file()]

    for shot in missing:
        print(f"MISSING  shot {shot.shot}: master_pngs/{shot.still_name}")
    for path in missing_audio:
        print(f"MISSING  {path.name}")
    stills_used = [s for s in shots if s.animate and not s.source_is_clip and s.source]
    for shot in stills_used:
        print(f"no clip for animated shot {shot.shot}, falling back to the still")

    total = sum(s.duration for s in shots)
    print(f"{len(shots)} shots, {total:.2f}s timeline, {len(missing) + len(missing_audio)} assets missing")
    if args.check:
        return
    if missing or missing_audio:
        sys.exit("cannot assemble with missing assets")

    work = root / "segments"
    work.mkdir(exist_ok=True)

    voice = concat(vo_parts, root / "voice_full.mp3", work, "vo_list.txt")

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        segments = list(pool.map(lambda s: build_segment(s, work), shots))
    print(f"built {len(segments)} segments")

    silent = concat(segments, root / "video_silent.mp4", work, "concat_list.txt")

    run(
        ["ffmpeg", "-y", "-i", str(silent), "-i", str(voice),
         "-vf", f"subtitles='{escape_for_filter(srt)}':force_style='{SUBTITLE_STYLE}'",
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)]
    )
    print(f"DONE -> {out}")


if __name__ == "__main__":
    main()
