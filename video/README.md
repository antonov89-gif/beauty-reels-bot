# Video assembly — "You work more than a caveman"

Stitches the 128-shot timeline into the final 1920x1080 / 25 fps narrated cut:
one segment per shot, concatenated, then voiceover muxed in and `NARRATION.srt`
burned in.

## Assets (not in git — they live next to each other in one working folder)

```
<work>/master_pngs/        128 master PNGs, named as master_filename in the timeline
<work>/veo_clips/          the animated MP4s, named <shot>_*.mp4 (e.g. 005_*.mp4)
<work>/vo_part1.mp3
<work>/vo_part2.mp3
<work>/NARRATION.srt       copy of timeline/NARRATION.srt
```

## Run

```
python3 video/assemble_video.py --root <work> --check   # list missing assets, render nothing
python3 video/assemble_video.py --root <work>           # -> FINAL_you-work-more-than-a-caveman.mp4
```

Needs `ffmpeg` on PATH. `--jobs N` caps the parallel segment encodes.

An animated shot with no clip in `veo_clips/` falls back to its master PNG and
is reported on stdout, so a partial VEO batch still renders a full cut.

## timeline/

`ASSEMBLY_TIMELINE_128.csv` drives the assembly (shot order, asset type, source
filename, duration). `ASSEMBLY_TIMING_SHEET_128.csv`, `NARRATION.srt`,
`NARRATION_CLEAN_EN.txt` and `VEO_QA_REPORT_25_SHOTS.csv` are the editorial
reference. Expected runtime: 660.95 s.

The upload/handoff PowerShell scripts from the same batch are deliberately not
committed — they embed presigned S3 URLs carrying AWS session tokens.
