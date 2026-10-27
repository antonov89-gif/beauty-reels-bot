#!/bin/bash
# render_loop.sh <loop>: run in /home/claude/v84. Audio, 4 parallel video chunks, concat + mux -> <loop>/<loop>_final.mp4
set -e
L=$1
D=/home/user/beauty-reels-bot/map_shorts/loops_2026_10_27
export LOOP=$L
E=$D/engine_loop.py
python3 $D/audio_loop.py
NF=$(python3 $E info | awk '{print $3}')
Q=$(( (NF + 3) / 4 ))
for i in 0 1 2 3; do
  a=$(( i * Q )); b=$(( (i + 1) * Q )); [ $b -gt $NF ] && b=$NF
  python3 $E video $a $b $L/c$i.mp4 > $L/c$i.log 2>&1 &
done
wait
printf "file 'c0.mp4'\nfile 'c1.mp4'\nfile 'c2.mp4'\nfile 'c3.mp4'\n" > $L/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $L/list.txt -i $L/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest \
  -movflags +faststart $L/${L}_final.mp4
rm -f $L/c?.mp4
echo done $L $(ffprobe -v error -show_entries format=duration -of csv=p=0 $L/${L}_final.mp4)
