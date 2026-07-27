#!/usr/bin/env python3
"""Independent standard-library checker for the Claim 4 evidence audit."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


SLICE_RE = re.compile(
    r"campaigns/(logdiff_and|logdiff_and_not)/run-seed-(\d+)/"
    r"slice-(s\d+)-samples-(\d+)-(\d+)/contract-([0-9a-f]{64})/SUCCESS\.json$"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_claim4_evidence.py ARTIFACT_DIR")
    root = Path(sys.argv[1]) / "claim-4"
    snapshot = root / "bucket-json-snapshot"
    summary = json.loads((root / "bucket_audit.json").read_text())
    control = json.loads((root / "negative_control.json").read_text())
    failures: list[str] = []
    slices = []
    bindings = set()

    for success_path in snapshot.rglob("SUCCESS.json"):
        relative = success_path.relative_to(snapshot).as_posix()
        match = SLICE_RE.match(relative)
        if not match:
            continue
        logic, seed, slice_id, start, stop, contract = match.groups()
        success = json.loads(success_path.read_text())
        manifest_path = success_path.with_name("SLICE_MANIFEST.json")
        manifest = json.loads(manifest_path.read_text())
        if success.get("status") != "complete":
            failures.append(f"slice_status:{relative}")
        if success.get("slice_manifest_sha256") != sha256(manifest_path):
            failures.append(f"slice_manifest_hash:{relative}")
        if (
            success.get("logic") != logic
            or int(success.get("run_seed", -1)) != int(seed)
            or success.get("slice_id") != slice_id
        ):
            failures.append(f"slice_identity:{relative}")
        if manifest.get("sample_indices") != list(range(int(start), int(stop))):
            failures.append(f"sample_range:{relative}")
        binding_text = json.dumps(success.get("binding"), sort_keys=True)
        bindings.add(binding_text)
        if success.get("binding") != manifest.get("binding"):
            failures.append(f"binding_mismatch:{relative}")
        for sample in manifest.get("samples", []):
            index = int(sample["sample_index"])
            sample_root = success_path.parent / "samples" / f"sample-{index:03d}"
            sample_success = sample_root / "SUCCESS.json"
            files_manifest = sample_root / "FILES.json"
            if not sample_success.exists() or sha256(sample_success) != sample["success_sha256"]:
                failures.append(f"sample_success_hash:{relative}:{index}")
                continue
            sample_record = json.loads(sample_success.read_text())
            if (
                sample_record.get("logic") != logic
                or sample_record.get("run_seed") != int(seed)
                or sample_record.get("sample_index") != index
                or sample_record.get("sample_seed") != int(seed) * 100000 + index
                or sample_record.get("num_steps") != 1000
                or sample_record.get("execution_device") != "cpu"
            ):
                failures.append(f"sample_identity:{relative}:{index}")
            if not files_manifest.exists() or sha256(files_manifest) != sample_record.get(
                "files_manifest_sha256"
            ):
                failures.append(f"files_manifest_hash:{relative}:{index}")
        slices.append((logic, int(seed), slice_id))

    if len(slices) != 12 or len(set(slices)) != 12:
        failures.append("terminal_slice_count")
    if len(bindings) != 1:
        failures.append("uniform_binding")
    if summary.get("terminal_slices") != 12 or summary.get("manifest_bound_samples") != 96:
        failures.append("summary_counts")
    if summary.get("complete_logdiff_experiments") != 0:
        failures.append("complete_experiment_count")
    if summary.get("payload_paths_in_listing") != 96:
        failures.append("payload_listing_count")
    if summary.get("dualdiff_experiments") != 0 or summary.get("docking_result_files") != 0:
        failures.append("missing_routes_misreported")
    if summary.get("claim_status") != "BLOCKED":
        failures.append("fail_closed_status")
    if control.get("audit_status") != "READY_FOR_CLAIM_CHECK" or not control.get(
        "rejected_false_block"
    ):
        failures.append("negative_control")

    result = {
        "checker": "independent Claim 4 manifest and completeness checker",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "terminal_slices_rederived": len(slices),
        "scientific_claim_status": summary.get("claim_status"),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
