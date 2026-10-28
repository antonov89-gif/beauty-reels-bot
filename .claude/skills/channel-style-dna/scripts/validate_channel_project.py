#!/usr/bin/env python3
"""Validate Channel Style DNA project bookkeeping; does not analyze media."""
import argparse
import json
from pathlib import Path

PHASES = {"SOURCE_GATE", "BRAND_SCAN", "BRAND_LOCK", "COMPETITOR_SCAN", "TRANSFER", "STORY", "PILOT_SPEC", "PILOT_GENERATED", "PILOT_INSPECTED", "PILOT_QC", "BATCH", "DELIVER"}
PILOT_STATES = {"NOT_STARTED", "SPECIFIED", "GENERATED", "INSPECTED", "QC_PASSED", "QC_FAILED"}
SOURCE_KINDS = {"channel", "banner", "avatar", "thumbnail", "video", "audio", "brief", "analytics"}
DECISIONS = {"KEEP_AS_PRINCIPLE", "TRANSLATE_TO_BRAND", "REJECT", "UNKNOWN"}
QC_CATEGORIES = {"BRAND_FIT", "FILMCRAFT", "ORIGINALITY", "MECHANIC_EFFECT", "CONTINUITY"}


def validate(p, require_local_media=False, base_dir=None):
    errors = []
    def err(msg): errors.append(msg)
    if not isinstance(p, dict):
        return ["Project must be a JSON object"]
    if p.get("skill_version") != "1.0.0": err("skill_version must be 1.0.0")
    if not p.get("project_id"): err("project_id must be provided")
    if p.get("phase") not in PHASES: err("Invalid phase")
    sources = p.get("sources", [])
    if not isinstance(sources, list):
        err("sources must be a list"); sources = []
    source_ids = set()
    for i, src in enumerate(sources):
        if not isinstance(src, dict):
            err(f"sources[{i}] must be an object"); continue
        sid = src.get("id")
        if not sid or sid in source_ids: err(f"sources[{i}] needs unique id")
        source_ids.add(sid)
        if src.get("owner") not in {"OWN", "COMPETITOR"}: err(f"{sid}: owner must be OWN or COMPETITOR")
        if src.get("kind") not in SOURCE_KINDS: err(f"{sid}: invalid kind")
        if src.get("access") not in {"UNVERIFIED", "METADATA_ONLY", "INSPECTED"}: err(f"{sid}: invalid access")
        if src.get("access") == "INSPECTED" and not src.get("evidence"): err(f"{sid}: inspection requires evidence")
    brand = p.get("brand", {})
    if not isinstance(brand, dict):
        err("brand must be object"); brand = {}
    if brand.get("status") not in {"DRAFT", "PROPOSED", "APPROVED"}: err("brand.status invalid")
    if brand.get("status") == "APPROVED":
        if not brand.get("approval_evidence"): err("APPROVED brand requires explicit approval_evidence")
        if not brand.get("version"): err("APPROVED brand requires version")
    for sid in brand.get("source_ids", []):
        if sid not in source_ids: err(f"brand source {sid} missing")
        elif next((s for s in sources if s.get("id") == sid), {}).get("owner") != "OWN": err(f"brand source {sid} must be OWN")
    competitor = p.get("competitor", {})
    if not isinstance(competitor, dict):
        err("competitor must be object"); competitor = {}
    for sid in competitor.get("reference_ids", []):
        if sid not in source_ids: err(f"competitor source {sid} missing")
        elif next((s for s in sources if s.get("id") == sid), {}).get("owner") != "COMPETITOR": err(f"competitor source {sid} must be COMPETITOR")
    transfer = competitor.get("transfer_matrix", [])
    if not isinstance(transfer, list):
        err("transfer_matrix must be list"); transfer = []
    tids = set()
    for i, t in enumerate(transfer):
        if not isinstance(t, dict): err(f"transfer_matrix[{i}] not object"); continue
        tid = t.get("id")
        if not tid or tid in tids: err(f"transfer_matrix[{i}] needs unique id")
        tids.add(tid)
        if t.get("decision") not in DECISIONS: err(f"{tid}: invalid decision")
        if not t.get("ref_evidence"): err(f"{tid}: ref_evidence required; use UNVERIFIED when unknown")
        if t.get("decision") == "TRANSLATE_TO_BRAND" and not t.get("brand_native"): err(f"{tid}: brand_native required")
    scenes = p.get("scenes", {})
    shots = p.get("shots", {})
    if not isinstance(scenes, dict): err("scenes must be object"); scenes = {}
    if not isinstance(shots, dict): err("shots must be object"); shots = {}
    for sid, shot in shots.items():
        if not isinstance(shot, dict): err(f"shot {sid} not object"); continue
        if shot.get("scene_id") not in scenes: err(f"shot {sid} references missing scene")
        try:
            if float(shot.get("duration_s", 0)) <= 0: err(f"shot {sid} duration must be positive")
        except (ValueError, TypeError): err(f"shot {sid} duration invalid")
        if shot.get("transfer_id") and shot["transfer_id"] not in tids: err(f"shot {sid} missing transfer_id")
    pilot = p.get("pilot", {})
    if not isinstance(pilot, dict): err("pilot must be object"); pilot = {}
    status = pilot.get("status")
    if status not in PILOT_STATES: err("invalid pilot status")
    shot_ids = pilot.get("shot_ids", [])
    if not isinstance(shot_ids, list): err("pilot.shot_ids must be list"); shot_ids = []
    for sid in shot_ids:
        if sid not in shots: err(f"pilot missing shot {sid}")
    if status != "NOT_STARTED":
        if len(shot_ids) < 4 or len(shot_ids) > 8: err("pilot must contain 4–8 shot IDs (or revise spec explicitly)")
        try:
            total = sum(float(shots[s]["duration_s"]) for s in shot_ids if s in shots)
            if total < 20 or total > 40: err("pilot sequence duration must be 20–40 seconds")
            if abs(total - float(pilot.get("duration_s", -1))) > 0.1: err("pilot.duration_s differs from shots total")
        except (ValueError, TypeError, KeyError): err("pilot duration cannot be computed")
    if status in {"GENERATED", "INSPECTED", "QC_PASSED", "QC_FAILED"}:
        media = pilot.get("actual_media_path")
        if not media: err("generated/inspected pilot requires actual_media_path")
        elif require_local_media:
            dest = Path(media)
            if not dest.is_absolute(): dest = (Path(base_dir or ".") / dest).resolve()
            if not dest.is_file(): err(f"pilot media file missing: {dest}")
    if status in {"INSPECTED", "QC_PASSED", "QC_FAILED"} and not pilot.get("inspected_evidence"):
        err("inspected pilot requires time-coded inspected_evidence")
    if status == "QC_PASSED":
        for c in QC_CATEGORIES:
            if pilot.get("qc", {}).get(c) != "PASS": err(f"QC_PASSED requires {c}=PASS")
    cost = p.get("cost_approval", {})
    if cost.get("approved"):
        if not cost.get("scope") or cost.get("budget_cap") is None or not cost.get("approval_evidence"):
            err("cost approval requires scope, budget_cap and explicit approval_evidence")
        try:
            if float(cost.get("budget_cap")) < 0: err("budget_cap cannot be negative")
        except (ValueError, TypeError): err("budget_cap invalid")
    if not isinstance(p.get("state", {}), dict): err("state must be object")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project_json", type=Path)
    ap.add_argument("--require-local-media", action="store_true")
    args = ap.parse_args()
    p = json.loads(args.project_json.read_text(encoding="utf-8"))
    errors = validate(p, args.require_local_media, args.project_json.parent)
    if errors:
        print("INVALID PROJECT:")
        for x in errors: print("-", x)
        raise SystemExit(1)
    print("VALID project bookkeeping (not visual/audio quality):", args.project_json)


if __name__ == "__main__": main()
