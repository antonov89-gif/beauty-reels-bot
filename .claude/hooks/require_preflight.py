"""PreToolUse hook (owner 05.11): a real run of a history-channel gen_*.py is blocked unless tools/preflight.py recorded PASS
(mechanical checks + reviewer agent + owner's yes) for the script's CURRENT content (sha256). Preview runs of scripts that only
submit with 'go' are allowed. Exit code 2 = block, the message goes back to Claude."""
import hashlib, json, os, re, sys
d = json.load(sys.stdin)
if d.get("tool_name") != "Bash": sys.exit(0)
cmd = (d.get("tool_input") or {}).get("command", "")
for m in re.finditer(r"python3?\s+(?:-\S+\s+)*([\w./-]*gen_[\w-]+\.py)([^;&|]*)", cmd):
    path, args = m.group(1), m.group(2)
    cand = [path] + [os.path.join(p, path) for p in (os.getcwd(), "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2", "/home/user/beauty-reels-bot/map_shorts/history_channel")]
    cd = re.findall(r"cd\s+([^\s;&]+)", cmd)
    cand = [os.path.join(c, path) for c in cd] + cand
    script = next((c for c in cand if os.path.isfile(c)), None)
    if not script: continue
    if "history_channel" not in os.path.abspath(script): continue
    src = open(script).read()
    preview = ('sys.argv[1] == "go"' in src or "mode == \"go\"" in src) and " go" not in args
    if preview: continue
    rec_p = os.path.join("/home/user/beauty-reels-bot/.preflight", os.path.basename(script) + ".json")
    ok = False
    if os.path.exists(rec_p):
        rec = json.load(open(rec_p))
        ok = rec.get("PASS") and rec.get("sha256") == hashlib.sha256(open(script, "rb").read()).hexdigest()
    if not ok:
        print(f"BLOCKED: {os.path.basename(script)} has no valid preflight PASS for its current content. Run: python3 map_shorts/history_channel/tools/preflight.py {script} ; then the pregen-reviewer agent; show the owner the refs + the Russian prompt; after her yes record --reviewer-pass and --owner-yes.", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
