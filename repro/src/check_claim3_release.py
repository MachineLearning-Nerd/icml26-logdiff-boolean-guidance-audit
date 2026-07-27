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
    routes = json.loads((root / "verification_routes.json").read_text())
    search = json.loads((root / "public_checkpoint_search_summary.json").read_text())
    falsification = json.loads((root / "falsification_check.json").read_text())
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
    route_rows = routes.get("routes", [])
    if [row.get("route") for row in route_rows] != [1, 2, 3, 4]:
        failures.append("four_route_sequence")
    if len({row.get("name") for row in route_rows}) != 4:
        failures.append("distinct_route_names")
    if routes.get("final_status") != "BLOCKED" or routes.get("confidence") != "LOW":
        failures.append("route_fail_closed_status")
    if route_rows and route_rows[-1].get("falsification_succeeded") is not False:
        failures.append("falsification_route_status")
    if search.get("author_equivalent_checkpoint_found") is not False:
        failures.append("checkpoint_search_status")
    proxy = search.get("public_proxy_model", {})
    if (
        proxy.get("revision") != "91d0ff096e031c21b8313bd5877316a52900d4ec"
        or proxy.get("unet_bytes") != 114049969
        or proxy.get("exact_protocol_equivalent") is not False
    ):
        failures.append("public_model_control")
    if (
        falsification.get("claimed_not_fid_ordering_holds_in_paper_table") is not True
        or falsification.get("available_evidence_admissible_as_counterexample") is not False
        or falsification.get("falsification_succeeded") is not False
        or falsification.get("status") != "BLOCKED"
    ):
        failures.append("falsification_check")
    if not falsification.get("synthetic_negative_control", {}).get("reversal_detected"):
        failures.append("falsification_negative_control")

    result = {
        "checker": "independent Claim 3 release-integrity checker",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "verification_routes_rederived": len(route_rows),
        "scientific_claim_status": raw.get("claim_status"),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
