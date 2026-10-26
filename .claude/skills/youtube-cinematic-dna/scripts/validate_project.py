#!/usr/bin/env python3
"""Validate ledger *bookkeeping*, not image/video quality or source authenticity.

Usage:
    python scripts/validate_project.py path/to/project.json

This catches unsupported OBSERVED claims, status jumps and approving shots
without a logged inspection or while open hard failures remain.
"""
import json
import sys
from pathlib import Path

STATUSES = {"SPECIFIED", "READY", "GENERATED", "INSPECTED", "FIX_REQUIRED", "APPROVED", "BLOCKED"}
CLAIM_STATUSES = {"OBSERVED", "ESTIMATED", "UNKNOWN"}
MEDIA_TYPES = {"video", "audio", "video+audio", "frames"}


def validate(data):
    errors = []

    def fail(where, issue):
        errors.append(f"{where}: {issue}")

    if not isinstance(data, dict):
        return ["project: root must be an object"]

    access = data.get("reference", {}).get("access_level")
    if access not in {"L0", "L1", "L2", "L3", "L4"}:
        fail("reference", "access_level must be L0–L4")

    evidence = {}
    for i, e in enumerate(data.get("evidence", [])):
        at = f"evidence[{i}]"
        eid = e.get("id")
        if not eid or eid in evidence:
            fail(at, "evidence id missing/duplicate")
            continue
        evidence[eid] = e
        for field in ("source", "modality", "method", "observation"):
            if not e.get(field):
                fail(at, f"{field} required")
        if e.get("confirmed") is not True:
            fail(at, "evidence must be confirmed from actual inspection; use no entry for placeholders")
        if e.get("modality") in MEDIA_TYPES and not e.get("inspected_range"):
            fail(at, "media evidence requires inspected_range/time range")
        if e.get("source_type") not in {"reference", "output", "public_metrics", "creator_analytics"}:
            fail(at, "source_type must identify provenance")

    claims = {}
    for i, c in enumerate(data.get("claims", [])):
        at = f"claims[{i}]"
        cid = c.get("id")
        if not cid or cid in claims:
            fail(at, "claim id missing/duplicate")
            continue
        claims[cid] = c
        status = c.get("status")
        if status not in CLAIM_STATUSES:
            fail(at, "invalid claim status")
        ids = c.get("evidence_ids", [])
        if status != "UNKNOWN" and not ids:
            fail(at, "OBSERVED/ESTIMATED needs evidence_ids")
        for eid in ids:
            if eid not in evidence:
                fail(at, f"missing evidence {eid}")
            elif evidence[eid].get("source_type") not in {"reference", "public_metrics", "creator_analytics"}:
                fail(at, f"reference claim points to non-reference evidence {eid}")
        if status == "OBSERVED" and ids and all(evidence.get(eid, {}).get("modality") in {"metadata", "transcript", "analytics"} for eid in ids):
            kind = c.get("claim_type")
            if kind in {"camera", "animation", "vfx", "sound", "editing", "lighting"}:
                fail(at, f"observed {kind} claim cannot rely only on metadata/transcript/analytics")

    principles = {}
    for i, p in enumerate(data.get("principles", [])):
        at = f"principles[{i}]"
        pid = p.get("id")
        if not pid or pid in principles:
            fail(at, "principle id missing/duplicate")
            continue
        principles[pid] = p
        ids = p.get("claim_ids", [])
        if not ids and p.get("origin") != "CREATIVE_CHOICE":
            fail(at, "reference principle needs evidence-linked claims, or explicit CREATIVE_CHOICE origin")
        for cid in ids:
            if cid not in claims:
                fail(at, f"unknown claim {cid}")

    for i, s in enumerate(data.get("shots", [])):
        at = f"shots[{i}]"
        sid = s.get("id")
        if not sid:
            fail(at, "shot id required")
        status = s.get("status")
        if status not in STATUSES:
            fail(at, f"invalid shot status {status!r}")
        for pid in s.get("principle_ids", []):
            if pid not in principles:
                fail(at, f"unknown principle {pid}")
        attempts = s.get("attempts", [])
        if status in {"GENERATED", "INSPECTED", "FIX_REQUIRED", "APPROVED"} and not attempts:
            fail(at, f"{status} requires at least one real artifact attempt")
        for j, a in enumerate(attempts):
            aj = f"{at}.attempts[{j}]"
            if not a.get("artifact_ref"):
                fail(aj, "artifact_ref required (not just a prompt)")
            if a.get("number") != j + 1:
                fail(aj, "attempt numbers must start from 1 and be sequential")
            qc = a.get("qc", {})
            for eid in qc.get("evidence_ids", []):
                if eid not in evidence:
                    fail(aj, f"unknown QC evidence {eid}")
                elif evidence[eid].get("source_type") != "output":
                    fail(aj, f"QC evidence {eid} must refer to inspected output")
        if status in {"INSPECTED", "FIX_REQUIRED", "APPROVED"} and attempts:
            qc = attempts[-1].get("qc", {})
            if qc.get("inspected") is not True or not qc.get("evidence_ids"):
                fail(at, f"{status} requires confirmed QC inspection evidence for latest attempt")
        if status == "APPROVED" and attempts:
            qc = attempts[-1].get("qc", {})
            if qc.get("verdict") != "PASS":
                fail(at, "APPROVED requires last QC verdict PASS")
            unresolved = [issue for issue in qc.get("issues", []) if issue.get("severity") in {"HARD", "CRITICAL"} and issue.get("status") != "RESOLVED"]
            if unresolved:
                fail(at, f"APPROVED has {len(unresolved)} unresolved hard/critical issues")
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_project.py project.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read JSON: {exc}")
        return 2
    errors = validate(data)
    if errors:
        print(f"FAIL: {len(errors)} traceability/status error(s):")
        for err in errors:
            print(f"- {err}")
        return 1
    print("PASS: project ledger is structurally consistent. This does NOT verify media quality or truthfulness of supplied evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
