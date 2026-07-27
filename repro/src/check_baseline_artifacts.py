#!/usr/bin/env python3
"""Independent, standard-library-only checker for baseline artifact files."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_baseline_artifacts.py ARTIFACT_DIR")
    root = Path(sys.argv[1])
    failures: list[str] = []

    c1 = read_csv(root / "claim-1" / "exhaustive_formulas.csv")
    c1_rules = read_csv(root / "claim-1" / "primitive_rules.csv")
    c1_controls = read_csv(root / "claim-1" / "negative_controls.csv")
    if len(c1) != 25 or sum(int(row["formulas"]) for row in c1) != 6350:
        failures.append("claim_1_counts")
    if max(float(row["max_probability_error"]) for row in c1) >= 1e-14:
        failures.append("claim_1_probability")
    if max(float(row["max_score_error"]) for row in c1) >= 1e-14:
        failures.append("claim_1_score")
    if len(c1_rules) != 100:
        failures.append("claim_1_rules")
    if len(c1_controls) != 3 or not all(row["rejected"] == "True" for row in c1_controls):
        failures.append("claim_1_controls")

    c2 = read_csv(root / "claim-2" / "table_2_cells.csv")
    c2_control = json.loads((root / "claim-2" / "negative_control.json").read_text())
    logdiff = [row for row in c2 if row["method"] == "LOGDIFF"]
    constant = [row for row in c2 if row["method"] == "constant"]
    if len(logdiff) != 8 or sum(row["inside_claimed_range"] == "True" for row in logdiff) != 2:
        failures.append("claim_2_logdiff_cells")
    if len(constant) != 8 or sum(row["inside_claimed_range"] == "True" for row in constant) != 5:
        failures.append("claim_2_constant_cells")
    if not c2_control["verifier_rejected_false_falsification"]:
        failures.append("claim_2_control")

    c5_independent = read_csv(root / "claim-5" / "independent_groups.csv")
    c5_taxonomy = read_csv(root / "claim-5" / "taxonomy.csv")
    c5_control = json.loads((root / "claim-5" / "negative_control.json").read_text())
    if len(c5_independent) != 25 or sum(int(row["events"]) for row in c5_independent) != 20650:
        failures.append("claim_5_independent_counts")
    if len(c5_taxonomy) != 25 or sum(int(row["events"]) for row in c5_taxonomy) != 6350:
        failures.append("claim_5_taxonomy_counts")
    if max(float(row["max_probability_error"]) for row in c5_independent + c5_taxonomy) >= 1e-14:
        failures.append("claim_5_probability")
    if max(float(row["max_score_error"]) for row in c5_independent + c5_taxonomy) >= 1e-14:
        failures.append("claim_5_score")
    if not c5_control["rejected"]:
        failures.append("claim_5_control")

    result = {
        "checker": "standard-library artifact checker",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "checked_claims": [1, 2, 5],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
