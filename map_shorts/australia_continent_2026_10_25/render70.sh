#!/bin/bash
# render70.sh <short>: 4 parallel chunks + concat + mux with au/mix.wav
set -e
S=$1
export SHORT=$S SHOTS_DIR=/home/user/beauty-reels-bot/map_shorts/australia_continent_2026_10_25
NF=$(python3 engine70.py info | awk '{print $3}')
Q=$(( (NF + 3) / 4 ))
for i in 0 1 2 3; do
  a=$(( i * Q )); b=$(( (i + 1) * Q )); [ $b -gt $NF ] && b=$NF
  python3 engine70.py video $a $b $S/c$i.mp4 > $S/c$i.log 2>&1 &
done
wait
printf "file 'c0.mp4'\nfile 'c1.mp4'\nfile 'c2.mp4'\nfile 'c3.mp4'\n" > $S/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $S/list.txt -i $S/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest $S/${S}_final.mp4
echo done $(ffprobe -v error -show_entries format=duration -of csv=p=0 $S/${S}_final.mp4)
