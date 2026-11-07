"""Take 7 piece 7b-WALK CLIP on Seedance 2.5 LITE i2v (07.11): image_urls[0] = first frame ONLY (owner rule 07.11: no end still; the last word is followed by a hard cut to the end card in the edit), 720p, 14 s, 9:16, $0.15/s = $2.10, audio off. Owner 07.11: the king has stopped in the middle of the hall, looks into the camera and says (script_v7_final.md Take 7, brief 'BRIEF 7a-walk and 7b-walk'): "That's all. Bye. I'm busy. [beat, points at the lens] ...And you: subscribe to my stunning channel. And like. [pause, a lazy wave of the hand, he looks away, bored] Or... whatever." (RU of the owner: «Всё, пока, я занят... а вы подписывайтесь на мой потрясающий канал и ставьте лайки... ну илиии...»). The pin: low arm-held view, wig top 5 % from the top edge, long curls at 21 % left and 87 % right: camera moves are written in what the viewer sees (the king only slides toward the LEFT edge of the picture by a few percent, never up, never toward the right edge). Realism rule 07.11: plain natural acting. One call, no retries without a new yes. Run: python3 gen_take_t7bw_seedance.py go
BRIEF: briefs/brief_t5_t7.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = (
    "The first frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. "
    "Realistic live action in the look of a hand-held low vlog that he films of himself, real skin texture, sharp focus on the face except 3.4 to 3.9 s. "
    "The same king in every frame: the same face, age about 45, heavy-lidded light grey-hazel eyes, thin dark waxed moustache with curled tips, a small dark beauty mark below the mouth on the viewer's right exactly as in the first frame and always visible, light rouge, the tall powdered wig in silver-grey and white, the scarlet velvet coat with gold suns, lace cravat; "
    "he stands in the middle of the long candlelit gilded hall lit by wall sconces, the camera held low at arm's length in front of him, the standing courtiers in plain wigs bow deeply in two rows at both sides, the cuff and the back of the hand at the lower right edge stay as in the first frame. "
    "0-0.6 s: he has just stopped, his eyes on the lens, the courtiers hold their bows. "
    "0.6-3.6 s: he says \"That's all. Bye. I'm busy.\" "
    "brisk and businesslike, one brow slightly raised, a faint smug smirk; the courtiers straighten up from their bows at 3.0 s; the lady with the fan at the back right raises her head at 3.5 s. "
    "3.6-4.4 s: a silent beat, "
    "his eyes stay on the lens, the smirk deepens a little, his free hand rises from the lower left with the index finger extended toward the lens and the other fingers curled. "
    "4.4-8.6 s: he says \"...And you: subscribe to my stunning channel. And like.\" "
    "the finger stays pointed at the lens, a slight nod on \"you\", the brows rise a little on \"stunning\", the finger lowers at 7.0 s; two courtiers whisper at 5.0 s and the lady with the fan fans herself at 6.0 s; a servant crosses far behind at 8.0 s. "
    "8.6-9.6 s: a silent pause, "
    "his face smug and still, the eyes on the lens, the lips closed; at 8.8 s a pink fingertip enters at the bottom left edge, 12 percent of the width, and leaves at 9.4 s, far from the face. "
    "9.6-12.0 s: a lazy wave of the hand, "
    "his free hand makes one loose small flick at chest height, he turns his head a little to the side and his eyes drift away from the lens, bored, the lids heavy; a courtier on the right shifts his weight at 10.0 s. "
    "12.0-14.0 s: he says \"Or... whatever.\" "
    "his eyes stay away from the lens, bored, the last word at about 13.4 s and the mouth stays open for a moment on the last syllable. "
    "CAMERA SCORE in absolute amounts, written in what the viewer sees (hand-held low at arm's length, chest height, tilted up about 12 degrees; the whole wig and the long curls stay inside the picture at every moment; the wig top never rises above its starting height and has only 5 percent of free wall, the long curls on the right only 13 percent, so the king only slides toward the left edge of the picture and never moves up or toward the right edge): "
    "0.3-4.4 s: the king slides 2 percent toward the left edge, a hand shake of 1 percent, the roll about 5 degrees counter-clockwise; "
    "3.4 to 3.9 s the picture softens for 0.5 s and snaps sharp; "
    "4.4-9.6 s: the king slides 2 percent more toward the left edge, a slow sway of 1 percent, the roll eases to 4 degrees; "
    "9.6-12.0 s: the picture follows his head turn with a small re-aim of 3 percent toward the left, the king stays inside; "
    "12.0-14.0 s: the frame settles with a sway of 1 percent. "
    "His lips form every spoken word clearly (the voice is added later); in the silent beats the mouth is closed. "
    "POSE SCORE as verbs: stop, bow, straighten, speak briskly, point, nod, lower the finger, wait, flick the hand, turn the head, look away; the acting is natural and plain, as a real person films himself; "
    "no expression lasts longer than 2 seconds except the bored look at the end. "
    "Acting limits: ordinary blinks aside the eyes are open at every moment, the face stays natural, five natural fingers on each hand, the pointing hand has one extended index finger and the other fingers curled. "
    "The camera moves only as small hand shakes and small re-aims by hand; the frame follows the hand. "
    "Sound: only the low murmur of a large hall, fabric, candle flicker, breath, room tone, no music. "
    "A clean picture with no text, only things of the 1680s, no modern objects, one king in the frame. "
)

body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt, "image_urls": [RAW + "t7bw_start_4k.jpg"],
        "duration": 14, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": False}
open(H0 + "take_t7bw_seedance_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t7bw_seedance.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=500, every=10)
    open(H0 + "pilot_frames/TAKE_t7bw_seedance.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t7bw_seedance.mp4"); print("saved")
