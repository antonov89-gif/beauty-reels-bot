#!/bin/bash
# Render, mux and encode all 7 Shorts: parts run 4-way parallel per short.
cd /home/claude/v60
for k in "$@"; do
  export SHORT=$k
  python3 audio60.py > $k/audio.log 2>&1 || { echo "AUDIO FAIL $k"; continue; }
  python3 srt60.py >> $k/audio.log 2>&1
  NF=$(python3 engine60.py info | head -1 | awk '{print $3}')
  for i in 0 1 2 3; do
    a=$((NF*i/4)); b=$((NF*(i+1)/4))
    python3 engine60.py video $a $b $k/p$i.mp4 > $k/p$i.log 2>&1 &
  done
  wait
  printf "file 'p0.mp4'\nfile 'p1.mp4'\nfile 'p2.mp4'\nfile 'p3.mp4'\n" > $k/list.txt
  ffmpeg -y -loglevel error -f concat -safe 0 -i $k/list.txt -c copy $k/raw.mp4
  T=$(python3 - <<PY
import json;from math import floor
print(json.load(open("$k/timing.json"))["starts"][-1])
PY
)
  ffmpeg -y -loglevel error -i $k/raw.mp4 -i $k/mix.wav -c:v libx264 -preset medium -crf 21 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart -shortest $k/$k.mp4
  rm -f $k/p?.mp4 $k/raw.mp4
  echo "DONE $k $(du -h $k/$k.mp4 | cut -f1) $(ffprobe -v error -show_entries format=duration -of csv=p=0 $k/$k.mp4)"
done
