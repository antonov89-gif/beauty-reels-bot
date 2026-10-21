#!/bin/bash
# Render one engine65 Short: audio + SRT, 6 parallel video parts, concat, mux, encode.  ./render65.sh turkey
cd /home/claude/v62
k=$1
export SHORT=$k
python3 audio65.py > $k/audio.log 2>&1 || { echo "AUDIO FAIL $k"; exit 1; }
python3 srt65.py >> $k/audio.log 2>&1
NF=$(python3 engine65.py info | head -1 | awk '{print $3}')
for i in 0 1 2 3 4 5; do
  a=$((NF*i/6)); b=$((NF*(i+1)/6))
  python3 engine65.py video $a $b $k/p$i.mp4 > $k/p$i.log 2>&1 &
done
wait
printf "file 'p0.mp4'\nfile 'p1.mp4'\nfile 'p2.mp4'\nfile 'p3.mp4'\nfile 'p4.mp4'\nfile 'p5.mp4'\n" > $k/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $k/list.txt -c copy $k/raw.mp4
ffmpeg -y -loglevel error -i $k/raw.mp4 -i $k/mix.wav -c:v libx264 -preset medium -crf 21 -maxrate 6M -bufsize 12M -pix_fmt yuv420p \
  -c:a aac -b:a 160k -movflags +faststart -shortest $k/$k.mp4
rm -f $k/p?.mp4 $k/raw.mp4
echo "DONE $k $(du -h $k/$k.mp4 | cut -f1) $(ffprobe -v error -show_entries format=duration -of csv=p=0 $k/$k.mp4)"
