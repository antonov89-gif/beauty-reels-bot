#!/bin/bash
# Lofoten Short: globe part rendered by engine69 (frames 0-86), 7 real drone segments cut from Pexels clips (4K portrait, downscaled to 1080x1920, 30 fps),
# exact frame counts on the 124 BPM beat grid, music from audio69.py.  Source clips are NOT in the repo (Pexels download, free licence, credit required).
# segment source:start_s  (clips: lof_<pexels id>.mp4 from https://www.pexels.com/download/video/<id>/)
# shot lengths follow the second reference breakdown (4, 3, 4, 1, 1, 4 s): ascend over the ridge, lateral pan over the lagoon, high forward drift over the harbour,
# 1 s tele close-up, 1 s wide sweep, 4 s downward finish. Beats at 124 BPM: cuts at beats 6, 14, 20, 28, 30, 32; end at beat 41.
SRC=(34425904:0.0 35466636:12.5 34509933:8.0 34434951:13.0 34425904:11.5 34509933:94.0)
NFR=(116 87 116 29 30 130)            # cut frames round(beat*60/124*30): 87, 203, 290, 406, 435, 465; total 595 = 19.84 s
GR="eq=saturation=1.14:contrast=1.05:gamma=0.98"
MOVE=("scale=1080:1920:flags=lanczos"                                                           # ascend (native move)
      "zoompan=z='1.0+0.07*on/86':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"   # lateral pan + slight push
      "rotate=a='-0.035*t/3.87':ow=iw:oh=ih,zoompan=z='1.08+0.17*on/115':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"  # forward push + CCW yaw (4K source, no upscaling)
      "scale=1080:1920:flags=lanczos" "scale=1080:1920:flags=lanczos" "scale=1080:1920:flags=lanczos")
SHORT=lofoten python3 engine69.py video 0 87 seg/s0.mp4
for i in 0 1 2 3 4 5; do
  id=${SRC[$i]%%:*}; ss=${SRC[$i]##*:}
  ffmpeg -y -loglevel error -ss $ss -i lof_$id.mp4 -frames:v ${NFR[$i]} -an -vf "fps=30,${MOVE[$i]},$GR,format=yuv420p" -c:v libx264 -crf 17 -preset fast seg/s$((i+1)).mp4
done
SHORT=lofoten python3 audio69.py
for i in 0 1 2 3 4 5 6; do echo "file 'seg/s$i.mp4'"; done > list.txt
ffmpeg -y -f concat -safe 0 -i list.txt -c copy raw.mp4
ffmpeg -y -i raw.mp4 -i mix.wav -c:v libx264 -preset medium -crf 19 -maxrate 8M -bufsize 16M -pix_fmt yuv420p -af volume=1.6dB -c:a aac -b:a 160k -ac 2 -movflags +faststart -shortest lofoten.mp4
