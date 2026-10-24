import sys
sys.path.insert(0, "/home/claude/v14")
import ws
P = ("Vertical handheld smartphone video filmed from an aisle seat in a dark modern cinema auditorium, audience silhouettes seen from behind, "
     "a huge curved screen ahead showing a wooden sailing ship ploughing through a stormy sea toward the camera, deep orchestral swell. "
     "At about three seconds the ship's bow bursts out of the screen into the auditorium with an enormous wave of water and white foam that floods the aisles and rows, "
     "spray hits the camera lens, the camera shakes violently, the crowd screams and laughs, the giant wooden hull looms over the seats. "
     "Photorealistic, practical lighting from the screen, natural handheld motion, one continuous take, no cuts. No text, no logos, no readable signs, no close-up of faces.")
NEG = "text, captions, subtitles, logos, watermark, brand names, cartoon, anime, close-up faces, distorted hands, cuts"
print("balance before", ws.balance(), flush=True)
r = ws.run("google/veo3.1-fast/text-to-video", {"prompt": P, "negative_prompt": NEG, "aspect_ratio": "9:16", "duration": 8, "resolution": "720p", "generate_audio": True}, out="cinema.mp4", timeout=1200)
print(r.get("status"), r.get("error") or r.get("code"), flush=True)
print("balance after", ws.balance(), flush=True)
