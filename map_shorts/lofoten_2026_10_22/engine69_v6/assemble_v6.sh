#!/bin/bash
# v6: cut frames snapped to the measured drum hits: 87, 202, 285, 400, 429, 458 (segment frames 87/115/83/115/29/29/137); dive on the oblique camera with terrain relief (dem69.py, AWS Terrain Tiles).
# Lofoten v5: one hero subject (Reine). Globe + satellite dive to the rooftops (engine69, frames 0-85), 5 drone shots of Reine, satellite
# finale straight down on Reine's rooftops (engine69, frames 461-594). Cuts on the 125 BPM grid of the music track (beats 6/14/20/28/30/32).
# Sources (not in the repo): Pexels clips rei_<id>.mp4 / lof_34425904.mp4, Mixkit track 679 "Epical Drums 04" (Grigoriy Nuzhny).
GR="eq=saturation=1.12:contrast=1.05:gamma=0.98"
SHORT=lofoten python3 engine69.py video 0 87 seg/s0.mp4
SHORT=lofoten python3 engine69.py video 458 595 seg/s6.mp4
ffmpeg -y -ss 12.0 -i rei_39810267.mp4 -frames:v 115 -an -vf "fps=30,crop=1215:2160:1900:0,scale=1080:1920:flags=lanczos,$GR,format=yuv420p" -c:v libx264 -crf 17 seg/s1.mp4   # ascend over the ridge, Reine revealed at dusk
ffmpeg -y -ss 6.0 -i lof_34425904.mp4 -frames:v 83 -an -vf "fps=30,scale=1080:1920:flags=lanczos,$GR,format=yuv420p" -c:v libx264 -crf 17 seg/s2.mp4                     # pan over Reine fjord, daylight
ffmpeg -y -ss 5.0 -i rei_39835660.mp4 -frames:v 115 -an -vf "fps=30,crop=1215:2160:1500:0,scale=1080:1920:flags=lanczos,$GR,format=yuv420p" -c:v libx264 -crf 17 seg/s3.mp4   # forward drift toward Reine
ffmpeg -y -ss 2.5 -i rei_39835662.mp4 -frames:v 29 -an -vf "fps=30,crop=608:1080:1496:800,scale=1080:1920:flags=lanczos,$GR,format=yuv420p" -c:v libx264 -crf 17 seg/s4.mp4  # 1 s tele close-up of the red cabins
ffmpeg -y -ss 12.5 -i lof_34425904.mp4 -frames:v 29 -an -vf "fps=30,scale=1080:1920:flags=lanczos,$GR,format=yuv420p" -c:v libx264 -crf 17 seg/s5.mp4                    # 1 s wide sweep over Reine islets
ffmpeg -y -ss 2.38 -t 19.84 -i m_679.mp3 -af "afade=t=in:d=0.04,afade=t=out:st=19.2:d=0.64,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=44100" -ac 2 mix.wav
for i in 0 1 2 3 4 5 6; do echo "file 'seg/s$i.mp4'"; done > list.txt
ffmpeg -y -f concat -safe 0 -i list.txt -c copy raw.mp4
ffmpeg -y -i raw.mp4 -i mix.wav -c:v libx264 -preset medium -crf 19 -maxrate 8M -bufsize 16M -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart -shortest lofoten.mp4
