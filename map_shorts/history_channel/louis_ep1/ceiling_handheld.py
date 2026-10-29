"""C01 opening, owner 29.10: "the camera must move over the ceiling like a phone in a hand".
Builds frames/C01_open_handheld.mp4 = (A) the 2K ceiling frame animated with a measured hand-held phone motion (slow drift + roll + tremor, eased to rest) + (B) Kling part 1 v2 from 0 s (its tilt down onto the king).
Both layers use the same 1.08 crop scale, so there is no zoom change at the handoff; at the handoff the drift is eased to zero, so the junction frame equals Kling's first frame (the same still).
Motion is a rotation of the phone: for a distant planar ceiling that is a 2-D drift, a roll and a tremor (no zoom). Usage: python3 ceiling_handheld.py"""
import subprocess
Z = 1.08; W, H = 1080, 1920; PW, PH = int(W * Z), int(H * Z); T_A = 1.7; FPS = 24; EASE = 0.5
# envelope: 1 until T_A-EASE, then smooth to 0 at T_A
env = f"(1-st(0,clip((t-{T_A-EASE})/{EASE},0,1))*(3-2*ld(0)))"   # smoothstep ease-out
env = f"(1-(3*pow(clip((t-{T_A-EASE})/{EASE},0,1),2)-2*pow(clip((t-{T_A-EASE})/{EASE},0,1),3)))"
dx = f"({env})*(30*sin(2*PI*0.55*t+0.4)+9*sin(2*PI*1.9*t+1.1)+3*sin(2*PI*7.3*t))"
dy = f"({env})*(52*sin(2*PI*0.42*t+2.0)+14*sin(2*PI*1.5*t+0.3)+4*sin(2*PI*6.1*t+1.7))"
ang = f"({env})*(0.012*sin(2*PI*0.5*t+0.9)+0.003*sin(2*PI*2.3*t))"        # radians (+-0.7 deg)
fc = (f"[0:v]scale={PW}:{PH},rotate=a='{ang}':ow={PW}:oh={PH}:fillcolor=black,"
      f"crop={W}:{H}:x='({PW}-{W})/2+{dx}':y='({PH}-{H})/2+{dy}',fps={FPS},setsar=1,format=yuv420p[a];"
      f"[1:v]trim=start=0.0,setpts=PTS-STARTPTS,scale={PW}:{PH},crop={W}:{H},fps={FPS},setsar=1,format=yuv420p[b];[a][b]concat=n=2:v=1:a=0[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", str(T_A), "-i", "frames/C01_ceiling2.jpg", "-i", "frames/kling_i2v_part1_v2.mp4",
                "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "frames/C01_open_handheld.mp4"], check=True)
print("written frames/C01_open_handheld.mp4")
