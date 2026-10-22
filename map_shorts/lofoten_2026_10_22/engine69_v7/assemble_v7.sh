#!/bin/bash
# Lofoten v7 = v6 + two AI clips (Veo 3.1 Lite via WaveSpeed, image-to-video, 4 s, 720p, 9:16, audio discarded; cost $0.20 each).
# s2: low telephoto drift from the water: keyframe = Nano Banana 2.1 Edit (WaveSpeed, $0.04) from a real Reine drone frame (reference image), prompt in the log.
# s6: nadir descent with slow clockwise turn: start frame = Esri satellite crop of Reine roofs (sat65/RE3.jpg); the model added drone-propeller artefacts in the corners,
#     removed by a centre crop 520x924 of the 720x1280 clip, stretched 1.1425x to 137 frames.
GR="eq=saturation=1.1:contrast=1.04:gamma=0.98"
ffmpeg -y -ss 0.4 -i v2_sea.mp4 -frames:v 83 -an -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.5,fps=30,$GR,format=yuv420p" -c:v libx264 -crf 17 seg/s2.mp4
ffmpeg -y -i v1_nadir.mp4 -frames:v 137 -an -vf "crop=520:924:100:100,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,setpts=1.1425*PTS,fps=30,$GR,format=yuv420p" -c:v libx264 -crf 17 seg/s6.mp4
# s0,s1,s3,s4,s5 and mix.wav as in v6 (assemble_v6.sh); concat s0..s6, mux with mix.wav
