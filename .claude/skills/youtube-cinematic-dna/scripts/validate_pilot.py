#!/usr/bin/env python3
"""Static pilot storyboard timing/continuity validator (NOT audiovisual QC).

python scripts/validate_pilot.py examples/sample-pilot.json
"""
import json
import sys
from pathlib import Path


def check(plan):
    problems = []
    shots = plan.get("shots", [])
    target = plan.get("target_duration_sec", None)
    if not isinstance(target, (int, float)) or not 20 <= target <= 40:
        problems.append("target_duration_sec should be 20–40 seconds")
    if not 4 <= len(shots) <= 8:
        problems.append("pilot should typically have 4–8 connected shots (adjust if justified)")
    end = 0.0
    used = set()
    for i, shot in enumerate(shots):
        place = f"shots[{i}]"
        sid = shot.get("id")
        if not sid or sid in used:
            problems.append(f"{place}: unique id required")
        used.add(sid)
        start, finish = shot.get("start_sec"), shot.get("end_sec")
        if not isinstance(start, (int,float)) or not isinstance(finish, (int,float)) or finish <= start:
            problems.append(f"{place}: invalid start/end")
            continue
        if abs(start - end) > 0.02:
            problems.append(f"{place}: timeline gap/overlap at {start}s (expected {end}s)")
        end = finish
        for key in ("story_purpose", "camera", "action", "continuity", "sound"):
            if not shot.get(key):
                problems.append(f"{place}: missing {key}")
    if isinstance(target, (int,float)) and abs(end-target) > 0.02:
        problems.append(f"pilot ends at {end}s but target duration is {target}s")
    return problems


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        plan=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"Cannot read pilot: {exc}", file=sys.stderr)
        return 2
    failures=check(plan)
    if failures:
        print("FAIL (static pilot timeline):")
        for f in failures: print("- " + f)
        return 1
    print("PASS: static 20–40s pilot timeline and mandatory shot specs are consistent. This does NOT validate footage, sound or cinematic quality.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
