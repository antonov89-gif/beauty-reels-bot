#!/bin/bash
# Lofoten Short: globe part rendered by engine69 (frames 0-86), 7 real drone segments cut from Pexels clips (4K portrait, downscaled to 1080x1920, 30 fps),
# exact frame counts on the 124 BPM beat grid, music from audio69.py.  Source clips are NOT in the repo (Pexels download, free licence, credit required).
# segment source:start_s  (clips: lof_<pexels id>.mp4 from https://www.pexels.com/download/video/<id>/)
SRC=(34425904:6.5 35466636:6.0 34509933:22.0 35466391:15.0 34509933:36.0 34425904:10.5 34509933:96.0)
NFR=(72 73 72 73 72 73 74)            # frames; globe part = 86 frames, total 595 = 19.84 s
SHORT=lofoten python3 engine69.py video 0 86 seg/s0.mp4
for i in 0 1 2 3 4 5 6; do
  id=${SRC[$i]%%:*}; ss=${SRC[$i]##*:}
  ffmpeg -y -loglevel error -ss $ss -i lof_$id.mp4 -frames:v ${NFR[$i]} -an -vf "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" -c:v libx264 -crf 17 -preset fast seg/s$((i+1)).mp4
done
SHORT=lofoten python3 audio69.py
for i in 0 1 2 3 4 5 6 7; do echo "file 'seg/s$i.mp4'"; done > list.txt
ffmpeg -y -f concat -safe 0 -i list.txt -c copy raw.mp4
ffmpeg -y -i raw.mp4 -i mix.wav -c:v libx264 -preset medium -crf 19 -maxrate 8M -bufsize 16M -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart -shortest lofoten.mp4
