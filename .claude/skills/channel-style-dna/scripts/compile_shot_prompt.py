#!/usr/bin/env python3
"""Compile a concise owned-brand-first per-shot handoff. No calls to generators."""
import argparse
import json
from pathlib import Path
from validate_channel_project import validate


def flatten(x):
    if isinstance(x, dict): return "; ".join(f"{k}: {flatten(v)}" for k, v in x.items() if v not in (None, "", []))
    if isinstance(x, list): return ", ".join(map(flatten, x))
    return str(x)


def compile_shot(project, shot_id):
    errors = validate(project)
    if errors: raise ValueError("Invalid project: " + "; ".join(errors))
    shot = project.get("shots", {}).get(shot_id)
    if not shot: raise KeyError(f"Unknown shot {shot_id}")
    scene = project["scenes"][shot["scene_id"]]
    brand = project["brand"]
    transfer = next((t for t in project["competitor"].get("transfer_matrix", []) if t.get("id") == shot.get("transfer_id")), None)
    lines = [
        f"SHOT: {shot_id} | project={project['project_id']}",
        f"BRAND FIRST: {brand['status']} {brand.get('version','')} — do not borrow competitor branding.",
        "GLOBAL BRAND CORE: " + flatten(brand.get("core", {})),
        "APPROVED/PROPOSED CINEMATIC RANGE: " + flatten(brand.get("cinema", {})),
        "MUST KEEP: " + flatten(brand.get("must_keep", [])),
        "FORBIDDEN: " + flatten(brand.get("forbidden", [])),
        "SCENE LOCK: " + flatten(scene),
        "SHOT DELTA: " + flatten({k:v for k,v in shot.items() if k not in {"scene_id", "transfer_id"}}),
    ]
    if transfer:
        lines += ["REFERENCE MECHANIC (abstract, not copied): " + transfer.get("mechanic", ""),
                  "BRAND-NATIVE TRANSFER: " + transfer.get("brand_native", ""),
                  "ORIGINALITY CHANGE: " + transfer.get("originality_change", "")]
        if transfer.get("ref_evidence") == "UNVERIFIED": lines += ["EVIDENCE WARNING: competitor mechanics provisional; original A/V not inspected."]
    lines += ["QUALITY: physically plausible camera/lighting/motion and grounded Foley; check identity, blocking, look consistency and originality; do not claim generation/inspection without actual artifact."]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project_json", type=Path)
    ap.add_argument("--shot", required=True)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    project = json.loads(args.project_json.read_text(encoding="utf-8"))
    compiled = compile_shot(project, args.shot)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(compiled+"\n", encoding="utf-8")
        print(args.output)
    else:
        print(compiled)


if __name__ == "__main__": main()
