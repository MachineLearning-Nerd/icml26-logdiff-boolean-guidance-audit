#!/usr/bin/env python3
"""Independent standard-library checker for Claim 3 release integrity."""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED_NOT = {
    "constant_cs": 0.75,
    "constant_fid": 32.87,
    "logdiff_cs": 0.80,
    "logdiff_fid": 23.61,
}


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_claim3_release.py ARTIFACT_DIR")
    root = Path(sys.argv[1]) / "claim-3"
    raw = json.loads((root / "release_audit.json").read_text())
    control = json.loads((root / "negative_control.json").read_text())
    failures: list[str] = []

    if raw["source_commit"] != "94ef35bafd4b4239e9832d8295128c09e8fc1472":
        failures.append("source_commit")
    if raw["tree_file_count"] != 73:
        failures.append("tree_file_count")
    if len(raw["missing_checkpoint_paths"]) != 3:
        failures.append("checkpoint_count")
    if not raw["missing_composition_dataset_config"]:
        failures.append("dataset_config")
    if not raw["fid_implementation_mismatch"]:
        failures.append("fid_protocol")
    if raw["generated_samples_per_task"] != 5000 or raw["reported_samples_argument"] != 500000:
        failures.append("sample_accounting")
    if raw["table_3"]["NOT"] != EXPECTED_NOT:
        failures.append("table_transcription")
    if raw["claim_status"] != "BLOCKED" or raw["empirical_generation_executed"]:
        failures.append("fail_closed_status")
    if control["audit_status"] != "READY_TO_RUN" or not control["rejected_false_block"]:
        failures.append("negative_control")

    result = {
        "checker": "independent Claim 3 release-integrity checker",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "scientific_claim_status": raw.get("claim_status"),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
