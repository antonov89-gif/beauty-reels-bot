"""Baby story clips (veo3-1-fast, 720p, 8 s, $0.18 each) from the approved storyboard frames. Runs 2 at a time (APIpod rate limit).
Usage: python3 clips_b81.py c02 c07b ... -> /home/claude/v88/clips/<id>.mp4"""
import subprocess
import sys

TAIL = " No new people or objects appear, faces stay the same, no text, no subtitles, no logos, no gore."
MOTION = {
    "c02": "The camera follows the nurse from behind at shoulder height as she walks briskly down the crowded corridor carrying the baby; people on the benches turn their heads, a doctor steps aside; smooth continuous forward tracking.",
    "c07b": "The mother hums softly with her eyes closed and gently strokes the baby's cheek; the baby's crying face slowly relaxes and calms; very slow push-in toward the two of them, warm window light flickering gently.",
    "c01": "Slow low push-in toward the swaddled baby lying on the wet sand at dawn; small waves wash gently near the debris, the baby's chest rises and falls, the thin warm line of sun on the horizon grows slightly brighter; no people appear.",
    "c03": "The camera slowly glides along the row of iron cots toward the cot with the baby; the nurse smooths the cloth and her hand moves away, a blank tag swings slightly on the rail, soft window light.",
    "c05": "Slow push-in on the group of couples at the ward doorway; they shift anxiously, one woman points into the ward, heads turn toward the same direction; handheld feel.",
    "c04": "Slow push-in on the mother and father at the reception desk; the doctor shakes his head slowly, the mother opens her empty hands and looks down, the father tightens his hand on her shoulder.",
    "c06b": "The nurse asks a question and turns her clipboard; the red-sari mother gestures talking fast, the blue-sari mother nods, the green-sari mother stays quiet and looks down at her hands; slow push-in at eye level.",
    "c08b": "The baby in the yellow cloth slowly turns his calm face and looks up at the mother's face just out of frame, his eyes widen gently, a tiny smile starts; very slow push-in, warm light.",
    "c07": "The lab technician gently touches the cotton swab to the baby's cheek and withdraws it; the baby stays calm; the mother, father and nurse watch closely; slow push-in.",
    "c08": "Slow push-in on the monitor as the glowing blue DNA bars gently pulse and shift; a gloved hand moves the mouse; reflections flicker on the screen; no readable text.",
    "c10": "The mother's tense face slowly softens into relief, tears roll down her cheek, she breathes out and lowers her clasped hands; the father blurred beside her; very slow push-in.",
    "c11": "The mother presses her cheek to the baby and rocks him slowly while the father's arms close around both; the nurse steps back smiling; very slow push-in, then hold still.",
}
FRAME = {c: c.replace("c", "s") for c in MOTION}
if __name__ == "__main__":
    ids = sys.argv[1:]
    for k in range(0, len(ids), 2):
        procs = [subprocess.Popen(["python3", "/home/user/beauty-reels-bot/map_shorts/baby81_2026_10_27/gen_clip.py",
                                   f"/home/claude/v88/frames/{FRAME[c]}.jpg", f"/home/claude/v88/clips/{c}.mp4", MOTION[c] + TAIL],
                                  stdout=open(f"/home/claude/v88/clips/{c}.log", "w"), stderr=subprocess.STDOUT) for c in ids[k:k + 2]]
        for p in procs:
            p.wait()
        for c in ids[k:k + 2]:
            print(c, "ok" if subprocess.run(["test", "-s", f"/home/claude/v88/clips/{c}.mp4"]).returncode == 0 else "FAIL", flush=True)
