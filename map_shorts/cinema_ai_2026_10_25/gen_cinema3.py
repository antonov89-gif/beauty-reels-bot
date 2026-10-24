"""Cinema v3: literal structure of the reference (see reference_vs_v2.md). Two Veo 3.1 Fast clips, 720p, 6 s each, audio on, about $1.80.
Part A: text to video (hold, pan, whale pushes out of the screen). Part B: image to video from the last frame of A (whale over the rows, crowd, finale).
Run: python3 gen_cinema3.py  (key: /home/claude/v14/.wavespeed_key, helper /home/claude/v14/ws.py). NOT RUN: waiting for the owner's top-up and go."""
import subprocess
import sys
sys.path.insert(0, "/home/claude/v14")
import ws


def upload(path):
    """WaveSpeed media upload (multipart) -> public URL of the frame. Endpoint: POST /media/upload/binary."""
    out = subprocess.run(["curl", "-sS", "-X", "POST", ws.BASE + "/media/upload/binary", "-H", "Authorization: Bearer " + ws.KEY, "-F", "file=@" + path],
                         capture_output=True, text=True, check=True).stdout
    import json
    return json.loads(out)["data"]["download_url"]


A = ("Vertical handheld smartphone selfie video, one continuous take, dark modern cinema auditorium, photorealistic. "
     "0-2.5 s: a young man in a dark denim jacket sits in a red seat in the foreground holding a clear water bottle, calm, almost no motion, "
     "behind him a huge curved screen shows a calm blue ocean, soft blue LED strips along the aisle, a low cinematic drone. "
     "2.5-4 s: he turns the phone toward the screen, the surface of the screen ripples like water and the sound rises. "
     "4-6 s: a humpback whale pushes its head and white pectoral fins out through the screen, a wave of real water and foam bursts into the front rows, "
     "droplets hit the lens, bokeh lights, the crowd silhouettes scream. No text, no logos.")
B = ("Continue the same handheld take. The whole humpback whale glides out over the audience three metres above the seats, belly and barnacles visible, "
     "foam and water flood the aisles, many people in the rows raise their phones, the camera swings back to the man, soaked, laughing, pointing up at the whale above him, "
     "water bottle still in his hand, blue aisle LEDs, bokeh, droplets on the lens. Real water physics, natural handheld motion, no text, no logos.")
NEG = "text, captions, subtitles, logos, watermark, brand names, cartoon, anime, plastic skin, distorted hands, extra fingers, cuts, split screen"
print("balance before", ws.balance(), flush=True)
r = ws.run("google/veo3.1-fast/text-to-video", {"prompt": A, "negative_prompt": NEG, "aspect_ratio": "9:16", "duration": 6, "resolution": "720p", "generate_audio": True}, out="cinema3_A.mp4", timeout=1200)
print("A", r.get("status"), r.get("error") or r.get("code"), flush=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.1", "-i", "cinema3_A.mp4", "-frames:v", "1", "cinema3_A_last.png"], check=True)
# part B needs the last frame as a public URL (upload through the helper used for v1) before this call
r = ws.run("google/veo3.1-fast/image-to-video", {"prompt": B, "image": upload("cinema3_A_last.png"), "negative_prompt": NEG, "aspect_ratio": "9:16", "duration": 6, "resolution": "720p", "generate_audio": True}, out="cinema3_B.mp4", timeout=1200)
print("B", r.get("status"), r.get("error") or r.get("code"), flush=True)
print("balance after", ws.balance(), flush=True)
