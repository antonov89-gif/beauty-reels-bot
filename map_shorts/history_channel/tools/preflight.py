"""PRE-GENERATION GATE for the history channel (owner 05.11: "создай агента, который по всем правилам проверял перед каждым запуском генерации").
Mechanical checks of ONE generation script before it may run. Writes .preflight/<script>.json with the script's sha256 when everything passes;
the PreToolUse hook (.claude/hooks/require_preflight.py) blocks any real run of a gen_*.py whose current sha256 has no PASS record.
Judgment checks (emotion per beat, laugh, angle new vs earlier setups, living room, phone mistake, end pose) are done by the agent
.claude/agents/pregen-reviewer.md and recorded with --reviewer-pass. The owner's "да" after seeing the refs + Russian prompt is recorded with --owner-yes.
Usage:
  python3 tools/preflight.py <gen_script.py>                         # mechanical checks only (prints the report)
  python3 tools/preflight.py <gen_script.py> --reviewer-pass "<note>"  # after the reviewer agent said PASS
  python3 tools/preflight.py <gen_script.py> --owner-yes "<owner's words>"  # after the owner's yes; writes the PASS record
"""
import os, hashlib, json, os, re, subprocess, sys, time, urllib.request
REPO = "/home/user/beauty-reels-bot"
RAW_PREFIX = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/"
BEST_ORIGINAL_SMALL_OK = {"R1_king_card_A3_white_wig.jpg", "A3_white_wig.jpg", "K4_master_neutral_O8.png", "K4_expr_shock_O9.png", "K4_angle_profileL_O10.png", "K4_angle_34right_O11.png", "K4_angle_low_O12.png", "K4_angle_high_O13.png", "K4_angle_overshoulder_O14.png", "t4bA_start_4k.jpg", "t4bA_end_4k.jpg"}   # best existing original, named as such
OWNER_QUALITY_EXCEPTION = {"t5a_start_4k.jpg": "owner 07.11 'Взять, дальше': start still 5a, sharp 280 / detail 1.94 (limit 2.0), BRAK items (4 fingers, face 21 %) on the rework list (reference_check.md)", "t1na_start_4k.jpg": "owner 07.11 'нормально, дальше': third attempt, sharp 97.8 / detail 1.54 (limits 150 / 2.0), content clean (no phone), reference_check.md","T4a_end_v2_4k.jpg": "owner 05.11 'Да': last pin of the 720p T4a clip, sharp 163 / detail 1.89 (limit 2.0), -21 % at video size (reference_check.md)", "T3c_end_4k.jpg": "owner 05.11 'Да': last pin of the 720p T3b-C clip, sharp 151 / detail 1.78, -21 % at video size (reference_check.md)", "T2c_end_v2_4k.jpg": "owner 05.11 'Делай': last pin of the 720p T2c clip, sharp 132 / detail 1.81, -27 % at video size (reference_check.md)"}   # explicit owner exceptions, one file each, never chain from them
PRICE = {"kling-4.0-i2v": {"720p": 0.145, "1080p": 0.2175}, "seedance-2.5-lite-i2v": {"720p": 0.15}, "seedance-2.5-i2v": {"720p": 0.2205, "480p": 0.098}, "gpt-image-2.5-sunburst-lite": 0.12, "gpt-image-2.5-sunburst": 0.50}

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    script = os.path.abspath(sys.argv[1]); src = open(script).read(); name = os.path.basename(script)
    fails, warns, notes = [], [], []
    # --- refs: RAW + "path" pieces ---
    raw_base = re.search(r'RAW\s*=\s*"([^"]+)"', src)
    raw_base = raw_base.group(1) if raw_base else ""
    refs = re.findall(r'RAW\s*\+\s*"([^"]+)"', src)
    if not refs and "# TEXT_ONLY_NO_REFERENCE" in src: notes.append("text-only call, no reference image (declared in the script)")
    elif not refs: fails.append("no reference images found (RAW + \"...\")")
    for r in refs:
        url = raw_base + r
        rel = url.replace(RAW_PREFIX, "")
        local = os.path.join(REPO, rel)
        if not os.path.exists(local): fails.append(f"ref missing locally: {rel}"); continue
        tracked = subprocess.run(["git", "-C", REPO, "ls-files", "--error-unmatch", rel], capture_output=True).returncode == 0
        if not tracked: fails.append(f"ref not committed: {rel}")
        try:
            code = urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30).status
        except Exception as e:
            code = getattr(e, "code", str(e))
        if code != 200: fails.append(f"ref URL not reachable ({code}): {url}")
        wh = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", local], capture_output=True, text=True).stdout.strip().split(",")
        try: w, h = int(wh[0]), int(wh[1])
        except Exception: fails.append(f"cannot read size: {rel}"); continue
        short = min(w, h); base = os.path.basename(rel)
        if short < 1024 and base not in BEST_ORIGINAL_SMALL_OK:
            fails.append(f"ref too small ({w}x{h}, short side {short} < 1024): {rel}  (rule H7: use a better source or words)")
        elif short < 1024:
            notes.append(f"{base} {w}x{h}: below 1024 but the best existing original (allowed, named)")
        else:
            notes.append(f"{base} {w}x{h} OK")
        if re.search(r"(_last\.jpg|frame_?\d+|/tmp/)", rel): warns.append(f"ref looks like a video frame: {rel} (rule H3)")
        # real quality, not only the pixel size (owner 05.11)
        qpy = next((x for x in ("/tmp/fv/bin/python",) if os.path.exists(x)), None)
        if not qpy:
            fails.append("quality tool missing: create /tmp/fv (see tools/quality_metrics.py header)")
        else:
            out = subprocess.run([qpy, os.path.join(REPO, "map_shorts/history_channel/tools/quality_metrics.py"), local], capture_output=True, text=True).stdout.strip().splitlines()
            qm = json.loads(out[-1]) if out else {}
            room = "hall" in base.lower()
            lim = {"sharp": 80, "detail": 1.3, "blocks": 1.30} if room else {"sharp": 150, "detail": 2.0, "blocks": 1.20}
            bad = [k for k in ("sharp", "detail") if qm.get(k, 0) < lim[k]] + (["blocks"] if qm.get("blocks", 9) > lim["blocks"] else [])
            msg = f"quality {base}: sharp {qm.get('sharp')} detail {qm.get('detail')} blocks {qm.get('blocks')} ({'room-only limits' if room else 'subject limits'})"
            if bad and base in OWNER_QUALITY_EXCEPTION:
                notes.append(msg + f" -> TOO LOW {bad} but OWNER EXCEPTION: {OWNER_QUALITY_EXCEPTION[base]}"); bad = []
            else:
                (fails if bad else notes).append(msg + (f" -> TOO LOW: {bad}" if bad else " OK"))
    # --- prompt text checks ---
    m = re.search(r'prompt\s*=\s*\((.*?)\)\n', src, re.S)
    prompt = " ".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))) if m else ""
    model = (re.search(r'"model":\s*"([^"]+)"', src) or [None, ""])[1]
    is_video = "videos" in src or "i2v" in model
    if not prompt: fails.append("prompt not found")
    # --- reference brief (PIPELINE_ROLES.md step 1, owner 07.11): the prompt must follow a brief written by the reference-comparator BEFORE it ---
    bm = re.search(r'BRIEF:\s*(\S+)', src)
    if not bm: fails.append("no 'BRIEF: briefs/<file>.md' line in the script: the prompt must be written from a reference brief (reference-comparator brief mode, PIPELINE_ROLES.md)")
    else:
        bp = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), bm.group(1).rstrip('.,;'))
        if not os.path.exists(bp): fails.append(f"reference brief file missing: {bm.group(1)} (write it with the reference-comparator in brief mode first)")
        else: notes.append(f"reference brief: {bm.group(1)} ({os.path.getsize(bp)} bytes)")
    low = prompt.lower()
    for k, why in [("no text", "no burned-in text"), ("modern", "no modern objects")]:
        if k not in low: fails.append(f"prompt lacks '{k}' ({why})")
    if is_video:
        if "kling" in model and "@first_frame" not in prompt: fails.append("Kling prompt lacks the @first_frame tag (rule H1)")
        if "@last_frame" in prompt and len(set(re.findall(r'"image_urls":\s*\[([^\]]*)\]', src))) == 0: warns.append("@last_frame named but image_urls not parsed")
        if not re.search(r"hand-held|hand held|in (a|his|one) hand", low): fails.append("video prompt lacks hand-held camera (rule C1, no static frames)")
        if not re.search(r"no music", low): fails.append("video prompt lacks 'no music'")
        if not re.search(r"fan|whisper|shift|servant|courtier", low): warns.append("no living-room cue (fans, whispering, servants) found (rule E2)")
        if re.search(r"propped|tripod|locked[- ]off|static camera", low): fails.append("static/propped camera in a video prompt (owner 05.11: none)")
        if re.search(r"framing (stays|remains|is kept) the same|same framing all the time|frame stays the same", low): fails.append("prompt says the framing stays the same: write 'the frame drifts, rolls and re-centres by a few percent' (PROMPT_CAMERA_LESSONS rule 4)")
        moves = len(re.findall(r"push-in|push-back|drift|tilt|re-aim|jerk|roll|swing|sway|focus hunt|slides? in", low))
        timed = len(re.findall(r"\d+(?:\.\d+)?\s*-\s*\d+(?:\.\d+)?\s*s:", low))
        if timed < 3: warns.append(f"only {timed} timed beats in the video prompt (PROMPT_CAMERA_LESSONS: a camera/pose/room score with times)")
        if moves < 4: fails.append(f"camera motion is described only {moves} times: write a camera score per beat (PROMPT_CAMERA_LESSONS rule 1)")
        if not re.search(r"no fast pans|no whip|never a smooth gimbal", low): warns.append("no guard against whip pans/gimbal (ghosting risk)")
    # --- price ---
    dur = re.search(r'"duration":\s*(\d+)', src); res = re.search(r'"resolution":\s*"([^"]+)"', src)
    if is_video and dur and res and model in PRICE:
        price = PRICE[model].get(res.group(1), 0) * int(dur.group(1))
    else:
        price = PRICE.get(model, 0) if isinstance(PRICE.get(model, 0), float) else 0
    # --- record ---
    os.makedirs(os.path.join(REPO, ".preflight"), exist_ok=True)
    rec_path = os.path.join(REPO, ".preflight", name + ".json")
    rec = json.load(open(rec_path)) if os.path.exists(rec_path) else {}
    h = sha(script)
    if rec.get("sha256") != h: rec = {"sha256": h}
    rec.update({"script": script, "model": model, "price_usd": round(price, 3), "refs": refs, "mechanical": "PASS" if not fails else "FAIL", "fails": fails, "warns": warns, "time": time.time()})
    if "--reviewer-pass" in sys.argv: rec["reviewer"] = sys.argv[sys.argv.index("--reviewer-pass") + 1]
    if "--owner-yes" in sys.argv: rec["owner_yes"] = sys.argv[sys.argv.index("--owner-yes") + 1]
    rec["PASS"] = bool(not fails and rec.get("reviewer") and rec.get("owner_yes"))
    json.dump(rec, open(rec_path, "w"), indent=1, ensure_ascii=False)
    print(f"PREFLIGHT {name}: model {model}, price about ${price:.3f}")
    if is_video and res:
        print(f"  ordered resolution {res.group(1)} (9:16 = 720x1280): right after the download run tools/check_resolution.py <mp4> {res.group(1).rstrip('p')}  (owner 07.11: we must get the resolution we ordered; any deviation is reported to the owner)")
    for n in notes: print("  ok   ", n)
    for w in warns: print("  WARN ", w)
    for f in fails: print("  FAIL ", f)
    print("  mechanical:", rec["mechanical"], "| reviewer:", rec.get("reviewer", "MISSING"), "| owner yes:", rec.get("owner_yes", "MISSING"), "| RUN ALLOWED:", rec["PASS"])
    sys.exit(0 if not fails else 1)

if __name__ == "__main__":
    main()
