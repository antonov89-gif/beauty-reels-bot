#!/usr/bin/env python3
"""Persistent small JSON production STATE helper.

Usage:
 python scripts/state_cli.py init path.json
 python scripts/state_cli.py show path.json
 python scripts/state_cli.py next path.json
 python scripts/state_cli.py update path.json patch.json

Update merges top-level fields in patch.json; it does NOT certify the stage,
inspect media, or approve spending. The agent must keep evidence-ledger and
paid-render constraints consistent using validate_project.py.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def write_atomic(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def main(argv):
    if len(argv) not in {3, 4} or argv[1] not in {"init", "show", "next", "update"} or (argv[1] == "update") != (len(argv) == 4):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    cmd, path = argv[1], Path(argv[2])
    if cmd == "init":
        if path.exists():
            print("STATE exists; will not overwrite", file=sys.stderr)
            return 1
        state = {
            "project_id": path.stem,
            "route": "ONE_LINK_STUDIO",
            "active_stage": "SOURCE_GATE",
            "reference": {"url": None, "access_level": "L0", "coverage": []},
            "evidence_ledger": None,
            "story_status": "not_started",
            "style_bible_id": None,
            "cost_authorization": {"approved": False},
            "artifacts": [],
            "blockers": [],
            "next_action": "inspect actual source access",
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        write_atomic(path, state)
        print(f"Created {path}")
        return 0
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(state, dict):
            raise ValueError("state root must be object")
    except (OSError, ValueError) as exc:
        print(f"Cannot read state: {exc}", file=sys.stderr)
        return 2
    if cmd == "show":
        print(json.dumps(state, ensure_ascii=False, indent=2))
    elif cmd == "next":
        print(f"stage={state.get('active_stage', 'UNKNOWN')} next={state.get('next_action', 'UNKNOWN')}")
    else:
        try:
            patch = json.loads(Path(argv[3]).read_text(encoding="utf-8"))
            if not isinstance(patch, dict) or not patch:
                raise ValueError("patch must be a nonempty object")
            if any(k in patch for k in ("project_id", "updated_at")):
                raise ValueError("project_id/updated_at are immutable")
        except (OSError, ValueError) as exc:
            print(f"Cannot read patch: {exc}", file=sys.stderr)
            return 2
        state.update(patch)
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_atomic(path, state)
        print(f"Updated {path}: stage={state.get('active_stage', 'UNKNOWN')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
