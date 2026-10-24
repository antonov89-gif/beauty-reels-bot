import sys
sys.path.insert(0, "/home/claude/v14")
import ws
P = ("Vertical handheld smartphone video, one single continuous take with no cuts, filmed in a dark modern cinema auditorium. "
     "First second: selfie-style framing, a young man in his twenties in a dark jacket sits in a red cinema seat holding a clear plastic water bottle, glancing at the camera with an excited grin, the room dim and quiet. "
     "The camera then pans and tilts to the huge curved screen where a humpback whale swims through deep blue ocean straight toward the viewers, light rays from the screen flicker over the audience, everything feels tense and quiet. "
     "At about three seconds the whale's huge head and long pectoral fins burst out of the screen into the auditorium with a massive wave of water, foam and spray; the camera shakes violently and water droplets hit the lens; "
     "white foam floods the aisles and rows while the giant whale glides over the seats. "
     "At about six seconds the camera whips back down to the man, now soaked and waist-deep in thick white foam, laughing and pointing up at the whale above him. "
     "Photorealistic, natural handheld motion, practical lighting from the screen, real water and foam physics, other audience members as dark silhouettes. No text, no logos.")
NEG = "text, captions, subtitles, logos, watermark, brand names, cartoon, anime, plastic skin, distorted hands, extra fingers, cuts, jump cuts, split screen"
print("balance before", ws.balance(), flush=True)
r = ws.run("google/veo3.1-lite/text-to-video", {"prompt": P, "negative_prompt": NEG, "aspect_ratio": "9:16", "duration": 8, "resolution": "720p"}, out="cinema2.mp4", timeout=1200)
print(r.get("status"), r.get("error") or r.get("code"), flush=True)
print("balance after", ws.balance(), flush=True)
