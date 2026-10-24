"""Cinema v3: the whale really leaves the screen (v2 kept it on the screen). Needs WaveSpeed balance >= $1.20 (Veo 3.1 Fast, 8 s, 720p, with audio).
Run: python3 gen_cinema3.py  (key: /home/claude/v14/.wavespeed_key, helper /home/claude/v14/ws.py). NOT RUN: waiting for the owner's top-up."""
import sys
sys.path.insert(0, "/home/claude/v14")
import ws
P = ("Vertical handheld smartphone video, one single continuous take with no cuts, filmed in a dark modern cinema auditorium, photorealistic. "
     "0-1 s: selfie-style framing, a young man in a dark denim jacket sits in a red cinema seat holding a clear plastic water bottle, grinning at the camera, the room dim and quiet, a low cinematic drone starts. "
     "1-3 s: the camera pans and tilts up to the huge curved screen where a humpback whale swims through deep blue ocean straight toward the viewers; the screen glows and the surface of the screen starts to ripple like water; the sound builds. "
     "At 3 s the screen surface ruptures: the humpback whale's enormous head and long white pectoral fins physically push out THROUGH the screen into the auditorium, a massive wave of real water and white foam bursts from the screen into the rows, "
     "the camera shakes violently, spray and droplets hit the lens, the crowd screams. "
     "3-6 s: the whole giant whale glides out over the audience, three metres above the seats, its belly and barnacles visible, foam and water flood every aisle and cover the red seats, people raising their arms. "
     "6-8 s: the camera whips back down to the man, soaked and waist-deep in thick white foam, laughing, pointing up at the whale floating above him, the water bottle still in his hand. "
     "Real water and foam physics, natural handheld motion, practical lighting from the screen, other audience members as dark silhouettes, no text, no logos.")
NEG = "text, captions, subtitles, logos, watermark, brand names, cartoon, anime, plastic skin, distorted hands, extra fingers, cuts, jump cuts, split screen, whale staying inside the screen"
print("balance before", ws.balance(), flush=True)
r = ws.run("google/veo3.1-fast/text-to-video", {"prompt": P, "negative_prompt": NEG, "aspect_ratio": "9:16", "duration": 8, "resolution": "720p", "generate_audio": True}, out="cinema3.mp4", timeout=1200)
print(r.get("status"), r.get("error") or r.get("code"), flush=True)
print("balance after", ws.balance(), flush=True)
