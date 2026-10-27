#!/bin/bash
# render83.sh: run in /home/claude/v83. Audio, 4 parallel chunks, concat + mux. Output wk/wk_final.mp4
set -e
S=wk
export SHORT=$S SHOTS_DIR=/home/user/beauty-reels-bot/map_shorts/walk_it_01_alaska_patagonia PYTHONPATH=$SHOTS_DIR
E=$SHOTS_DIR/engine83.py
python3 $SHOTS_DIR/audio83.py
NF=$(python3 $E info | awk '{print $3}')
Q=$(( (NF + 3) / 4 ))
for i in 0 1 2 3; do
  a=$(( i * Q )); b=$(( (i + 1) * Q )); [ $b -gt $NF ] && b=$NF
  python3 $E video $a $b $S/c$i.mp4 > $S/c$i.log 2>&1 &
done
wait
printf "file 'c0.mp4'\nfile 'c1.mp4'\nfile 'c2.mp4'\nfile 'c3.mp4'\n" > $S/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $S/list.txt -i $S/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest $S/${S}_final.mp4
echo done $(ffprobe -v error -show_entries format=duration -of csv=p=0 $S/${S}_final.mp4)
