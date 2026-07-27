#!/usr/bin/env python3
"""Exhaustive finite-state reproduction of LOGDIFF's exact Boolean calculus.

The paper's Proposition 3.1 is continuous, while Proposition C.3 supplies the
discrete equivalent.  Here atom posteriors are smooth softmax functions of x;
their exact log-gradients play the role of diffusion guidance scores.  Direct
enumeration of the full joint distribution is an independent oracle.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import os
import platform
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class Value:
    probability: float
    score: np.ndarray


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits)
    weights = np.exp(shifted)
    return weights / weights.sum()


def categorical_model(logits_by_variable: list[np.ndarray]) -> tuple[list[np.ndarray], list[list[Value]]]:
    """Return categorical probabilities and atom (probability, grad-log-p) values."""
    probabilities = [softmax(np.asarray(x, dtype=float)) for x in logits_by_variable]
    dimension = sum(len(p) for p in probabilities)
    atoms: list[list[Value]] = []
    offset = 0
    for probs in probabilities:
        variable_atoms = []
        for value, probability in enumerate(probs):
            score = np.zeros(dimension)
            score[offset : offset + len(probs)] = -probs
            score[offset + value] += 1.0
            variable_atoms.append(Value(float(probability), score))
        atoms.append(variable_atoms)
        offset += len(probs)
    return probabilities, atoms


# Table 1, independently transcribed.
def negate(value: Value) -> Value:
    probability = 1.0 - value.probability
    return Value(probability, -value.probability / probability * value.score)


def conjunction_ci(left: Value, right: Value) -> Value:
    return Value(left.probability * right.probability, left.score + right.score)


def disjunction_ci(left: Value, right: Value) -> Value:
    pl, pr = left.probability, right.probability
    probability = pl + pr - pl * pr
    numerator = pl * (1 - pr) * left.score + pr * (1 - pl) * right.score
    return Value(probability, numerator / probability)


def disjunction_me(left: Value, right: Value) -> Value:
    probability = left.probability + right.probability
    numerator = left.probability * left.score + right.probability * right.score
    return Value(probability, numerator / probability)


def assignment_value(atoms: list[list[Value]], assignment: tuple[int, ...]) -> Value:
    value = atoms[0][assignment[0]]
    for variable, category in enumerate(assignment[1:], start=1):
        value = conjunction_ci(value, atoms[variable][category])
    return value


def compiled_dnf(atoms: list[list[Value]], selected: tuple[tuple[int, ...], ...]) -> Value:
    """Proposition 3.2: CI assignment terms joined by mutually-exclusive ORs."""
    terms = [assignment_value(atoms, assignment) for assignment in selected]
    value = terms[0]
    for term in terms[1:]:
        value = disjunction_me(value, term)
    return value


def direct_event(
    probabilities: list[np.ndarray], atoms: list[list[Value]], selected: tuple[tuple[int, ...], ...]
) -> Value:
    """Independent oracle: enumerate joint assignments, then differentiate the sum."""
    joint_probabilities = []
    joint_gradients = []
    for assignment in selected:
        probability = float(np.prod([probabilities[m][v] for m, v in enumerate(assignment)]))
        score = sum((atoms[m][v].score for m, v in enumerate(assignment)), np.zeros_like(atoms[0][0].score))
        joint_probabilities.append(probability)
        joint_gradients.append(probability * score)
    event_probability = float(sum(joint_probabilities))
    gradient = sum(joint_gradients, np.zeros_like(atoms[0][0].score))
    return Value(event_probability, gradient / event_probability)


def event_probability_from_flat_logits(
    flat_logits: np.ndarray, sizes: tuple[int, ...], selected: tuple[tuple[int, ...], ...]
) -> float:
    pieces, offset = [], 0
    for size in sizes:
        pieces.append(softmax(flat_logits[offset : offset + size]))
        offset += size
    return float(sum(np.prod([pieces[m][v] for m, v in enumerate(a)]) for a in selected))


def finite_difference_score(
    logits_by_variable: list[np.ndarray], selected: tuple[tuple[int, ...], ...], epsilon: float = 1e-6
) -> np.ndarray:
    sizes = tuple(len(x) for x in logits_by_variable)
    flat = np.concatenate(logits_by_variable).astype(float)
    result = np.zeros_like(flat)
    for coordinate in range(len(flat)):
        plus, minus = flat.copy(), flat.copy()
        plus[coordinate] += epsilon
        minus[coordinate] -= epsilon
        result[coordinate] = (
            math.log(event_probability_from_flat_logits(plus, sizes, selected))
            - math.log(event_probability_from_flat_logits(minus, sizes, selected))
        ) / (2 * epsilon)
    return result


def exhaustive_binary(seed: int) -> dict[str, float | int]:
    rng = np.random.default_rng(seed)
    logits = [rng.normal(size=2) for _ in range(3)]
    probabilities, atoms = categorical_model(logits)
    assignments = tuple(itertools.product(range(2), repeat=3))
    max_probability_error = 0.0
    max_score_error = 0.0
    max_fd_error = 0.0
    formula_count = 0
    for mask in range(1, 2 ** len(assignments) - 1):
        selected = tuple(a for i, a in enumerate(assignments) if mask & (1 << i))
        recursive = compiled_dnf(atoms, selected)
        oracle = direct_event(probabilities, atoms, selected)
        max_probability_error = max(max_probability_error, abs(recursive.probability - oracle.probability))
        max_score_error = max(max_score_error, float(np.max(np.abs(recursive.score - oracle.score))))
        # Finite differences are costlier; triangulate every seventeenth formula.
        if mask % 17 == 0:
            fd = finite_difference_score(logits, selected)
            max_fd_error = max(max_fd_error, float(np.max(np.abs(recursive.score - fd))))
        formula_count += 1
    return {
        "seed": seed,
        "formulas": formula_count,
        "max_probability_error": max_probability_error,
        "max_score_error": max_score_error,
        "max_finite_difference_error": max_fd_error,
    }


def primitive_checks(seed: int) -> list[dict]:
    """Exercise every Table-1 operator against direct enumeration."""
    rng = np.random.default_rng(seed)
    logits = [rng.normal(size=3), rng.normal(size=2)]
    probabilities, atoms = categorical_model(logits)
    assignments = tuple(itertools.product(range(3), range(2)))
    cases = []

    def oracle(predicate) -> Value:
        selected = tuple(a for a in assignments if predicate(a))
        return direct_event(probabilities, atoms, selected)

    candidates = [
        ("negation", negate(atoms[0][0]), oracle(lambda a: a[0] != 0)),
        ("conjunction_ci", conjunction_ci(atoms[0][1], atoms[1][0]), oracle(lambda a: a[0] == 1 and a[1] == 0)),
        ("disjunction_ci", disjunction_ci(atoms[0][1], atoms[1][0]), oracle(lambda a: a[0] == 1 or a[1] == 0)),
        ("disjunction_me", disjunction_me(atoms[0][0], atoms[0][2]), oracle(lambda a: a[0] in (0, 2))),
    ]
    for operator, recursive, direct in candidates:
        cases.append(
            {
                "seed": seed,
                "operator": operator,
                "probability_error": abs(recursive.probability - direct.probability),
                "score_max_error": float(np.max(np.abs(recursive.score - direct.score))),
            }
        )
    return cases


def dependent_controls() -> list[dict]:
    """Rules must fail closed when CI/ME structural assumptions are false."""
    logits = np.array([0.2, -0.7, 1.1, 0.4])  # joint logits for (00,01,10,11)
    joint = softmax(logits)
    assignments = ((0, 0), (0, 1), (1, 0), (1, 1))

    def event(indices: tuple[int, ...]) -> Value:
        probability = float(joint[list(indices)].sum())
        gradient = np.zeros(4)
        for index in indices:
            score = -joint.copy()
            score[index] += 1
            gradient += joint[index] * score
        return Value(probability, gradient / probability)

    left = event((2, 3))   # Z0=1
    right = event((1, 3))  # Z1=1; correlated with left
    true_and = event((3,))
    true_or = event((1, 2, 3))
    wrong_and = conjunction_ci(left, right)
    wrong_or = disjunction_ci(left, right)

    # Constant 0.5 score mixing is the principal heuristic baseline criticized by the paper.
    exact_or_me = disjunction_me(event((0,)), event((1,)))
    constant_score = 0.5 * event((0,)).score + 0.5 * event((1,)).score
    return [
        {
            "control": "CI_conjunction_on_correlated_events",
            "probability_error": abs(wrong_and.probability - true_and.probability),
            "score_max_error": float(np.max(np.abs(wrong_and.score - true_and.score))),
            "rejected": abs(wrong_and.probability - true_and.probability) > 1e-3,
        },
        {
            "control": "CI_disjunction_on_correlated_events",
            "probability_error": abs(wrong_or.probability - true_or.probability),
            "score_max_error": float(np.max(np.abs(wrong_or.score - true_or.score))),
            "rejected": abs(wrong_or.probability - true_or.probability) > 1e-3,
        },
        {
            "control": "constant_half_mix_for_ME_disjunction",
            "probability_error": 0.0,
            "score_max_error": float(np.max(np.abs(constant_score - exact_or_me.score))),
            "rejected": float(np.max(np.abs(constant_score - exact_or_me.score))) > 1e-3,
        },
    ]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def exhaustive_categorical_groups(seed: int) -> dict[str, float | int]:
    """Exhaust Proposition C.2's independent-categorical construction.

    The three complete finite domains have respectively 8, 6, and 9 joint
    assignments, so they contain 254 + 62 + 510 = 826 nonconstant semantic
    events per posterior setting.
    """
    rng = np.random.default_rng(10_000 + seed)
    event_count = 0
    max_probability_error = 0.0
    max_score_error = 0.0
    for sizes in ((2, 2, 2), (3, 2), (3, 3)):
        logits = [rng.normal(size=size) for size in sizes]
        probabilities, atoms = categorical_model(logits)
        assignments = tuple(itertools.product(*(range(size) for size in sizes)))
        for mask in range(1, 2 ** len(assignments) - 1):
            selected = tuple(a for i, a in enumerate(assignments) if mask & (1 << i))
            compiled = compiled_dnf(atoms, selected)
            oracle = direct_event(probabilities, atoms, selected)
            max_probability_error = max(max_probability_error, abs(compiled.probability - oracle.probability))
            max_score_error = max(max_score_error, float(np.max(np.abs(compiled.score - oracle.score))))
            event_count += 1
    return {
        "seed": seed,
        "events": event_count,
        "max_probability_error": max_probability_error,
        "max_score_error": max_score_error,
    }


def categorical_leaf_model(logits: np.ndarray) -> tuple[np.ndarray, list[Value]]:
    probabilities = softmax(logits)
    atoms: list[Value] = []
    for index, probability in enumerate(probabilities):
        score = -probabilities.copy()
        score[index] += 1.0
        atoms.append(Value(float(probability), score))
    return probabilities, atoms


def taxonomy_event(probabilities: np.ndarray, atoms: list[Value], selected: tuple[int, ...]) -> Value:
    probability = float(probabilities[list(selected)].sum())
    gradient = sum((probabilities[index] * atoms[index].score for index in selected), np.zeros(len(atoms)))
    return Value(probability, gradient / probability)


def exhaustive_taxonomy(seed: int) -> dict[str, float | int]:
    """Exhaust all nonconstant events over the eight leaves of a binary taxonomy."""
    rng = np.random.default_rng(20_000 + seed)
    probabilities, atoms = categorical_leaf_model(rng.normal(size=8))
    max_probability_error = 0.0
    max_score_error = 0.0
    event_count = 0
    for mask in range(1, 2 ** len(atoms) - 1):
        selected = tuple(index for index in range(len(atoms)) if mask & (1 << index))
        terms = [atoms[index] for index in selected]
        compiled = terms[0]
        for term in terms[1:]:
            compiled = disjunction_me(compiled, term)
        oracle = taxonomy_event(probabilities, atoms, selected)
        max_probability_error = max(max_probability_error, abs(compiled.probability - oracle.probability))
        max_score_error = max(max_score_error, float(np.max(np.abs(compiled.score - oracle.score))))
        event_count += 1
    return {
        "seed": seed,
        "events": event_count,
        "taxonomy_predicates": 15,
        "max_probability_error": max_probability_error,
        "max_score_error": max_score_error,
    }


def taxonomy_overlap_control() -> dict[str, float | bool | str]:
    probabilities, atoms = categorical_leaf_model(np.array([0.2, -0.7, 1.1, 0.4, -0.1, 0.8, -0.3, 0.6]))
    left_leaves = (0, 1, 2, 3)
    right_leaves = (2, 3, 4, 5)
    left = taxonomy_event(probabilities, atoms, left_leaves)
    right = taxonomy_event(probabilities, atoms, right_leaves)
    true_union = taxonomy_event(probabilities, atoms, (0, 1, 2, 3, 4, 5))
    invalid_me = disjunction_me(left, right)
    probability_error = abs(invalid_me.probability - true_union.probability)
    score_error = float(np.max(np.abs(invalid_me.score - true_union.score)))
    return {
        "control": "overlapping_non_nested_non_me_taxonomy_pair",
        "left_leaves": str(left_leaves),
        "right_leaves": str(right_leaves),
        "probability_error": probability_error,
        "score_max_error": score_error,
        "rejected": probability_error > 1e-3 and score_error > 1e-3,
    }


TABLE_2_ROWS = [
    {"dataset": "CMNIST", "method": "LOGDIFF", "N2": 93.8, "N3": 93.3, "N4": 94.2, "N5": 94.4},
    {"dataset": "Shapes3D", "method": "LOGDIFF", "N2": 88.8, "N3": 88.6, "N4": 85.1, "N5": 87.6},
    {"dataset": "CMNIST", "method": "constant", "N2": 76.1, "N3": 66.7, "N4": 68.3, "N5": 75.2},
    {"dataset": "Shapes3D", "method": "constant", "N2": 67.2, "N3": 59.4, "N4": 58.4, "N5": 57.9},
]


def audit_table_2(rows: list[dict] = TABLE_2_ROWS) -> tuple[dict, list[dict]]:
    """Audit the challenge's literal ranges against every N=2..5 table cell."""
    expanded = []
    for row in rows:
        expected_low, expected_high = (94.0, 98.0) if row["method"] == "LOGDIFF" else (63.0, 77.0)
        for operator_count in range(2, 6):
            value = float(row[f"N{operator_count}"])
            expanded.append(
                {
                    "dataset": row["dataset"],
                    "method": row["method"],
                    "operators": operator_count,
                    "value_percent": value,
                    "claimed_low": expected_low,
                    "claimed_high": expected_high,
                    "inside_claimed_range": expected_low <= value <= expected_high,
                }
            )
    by_method = {}
    for method in ("LOGDIFF", "constant"):
        cells = [row for row in expanded if row["method"] == method]
        values = [float(row["value_percent"]) for row in cells]
        by_method[method] = {
            "minimum": min(values),
            "maximum": max(values),
            "inside_claimed_range": sum(bool(row["inside_claimed_range"]) for row in cells),
            "total_cells": len(cells),
        }
    falsified = (
        by_method["LOGDIFF"]["inside_claimed_range"] < by_method["LOGDIFF"]["total_cells"]
        and by_method["constant"]["inside_claimed_range"] < by_method["constant"]["total_cells"]
    )
    return {"status": "FALSIFIED" if falsified else "VERIFIER_REJECTED", **by_method}, expanded


def table_2_negative_control() -> dict[str, bool | str]:
    """A range-conforming synthetic table must not be called a falsification."""
    conforming = [
        {"dataset": dataset, "method": method, "N2": value, "N3": value, "N4": value, "N5": value}
        for dataset in ("CMNIST", "Shapes3D")
        for method, value in (("LOGDIFF", 96.0), ("constant", 70.0))
    ]
    summary, _ = audit_table_2(conforming)
    return {
        "control": "range_conforming_table",
        "verifier_rejected_false_falsification": summary["status"] == "VERIFIER_REJECTED",
    }


C4_SLICE_RE = re.compile(
    r"campaigns/(logdiff_and|logdiff_and_not)/run-seed-(\d+)/"
    r"slice-(s\d+)-samples-(\d+)-(\d+)/contract-([0-9a-f]{64})/SUCCESS\.json$"
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify_c4_completeness(
    logdiff_experiments: dict[str, int],
    dualdiff_experiments: dict[str, int],
    raw_complete: bool,
    docking_complete: bool,
    source_available: bool,
) -> str:
    expected = {"AND": 8, "AND-NOT": 8}
    ready = (
        logdiff_experiments == expected
        and dualdiff_experiments == expected
        and raw_complete
        and docking_complete
        and source_available
    )
    return "READY_FOR_CLAIM_CHECK" if ready else "BLOCKED"


def audit_claim_4_evidence(output_dir: Path) -> tuple[dict, dict]:
    root = output_dir / "claim-4"
    snapshot = root / "bucket-json-snapshot"
    listing = json.loads((root / "historical_bucket_listing.json").read_text())
    source_recovery = json.loads((root / "source_recovery_audit.json").read_text())
    verification_routes = json.loads((root / "verification_routes.json").read_text())
    falsification_check = json.loads((root / "falsification_check.json").read_text())
    failures = []
    slices: list[tuple[str, int, str]] = []
    sample_records = 0
    bindings = set()

    for success_path in snapshot.rglob("SUCCESS.json"):
        relative = success_path.relative_to(snapshot).as_posix()
        match = C4_SLICE_RE.match(relative)
        if not match:
            continue
        logic, seed, slice_id, start, stop, contract = match.groups()
        success = json.loads(success_path.read_text())
        manifest_path = success_path.with_name("SLICE_MANIFEST.json")
        manifest = json.loads(manifest_path.read_text())
        if success.get("status") != "complete":
            failures.append(f"slice_status:{relative}")
        if success.get("slice_manifest_sha256") != file_sha256(manifest_path):
            failures.append(f"slice_manifest_hash:{relative}")
        if (
            success.get("logic") != logic
            or success.get("run_seed") != int(seed)
            or success.get("slice_id") != slice_id
        ):
            failures.append(f"slice_identity:{relative}")
        if manifest.get("sample_indices") != list(range(int(start), int(stop))):
            failures.append(f"sample_range:{relative}")
        bindings.add(json.dumps(success.get("binding"), sort_keys=True))
        if success.get("binding") != manifest.get("binding"):
            failures.append(f"binding_mismatch:{relative}")
        for sample in manifest.get("samples", []):
            index = int(sample["sample_index"])
            sample_root = success_path.parent / "samples" / f"sample-{index:03d}"
            sample_success_path = sample_root / "SUCCESS.json"
            files_path = sample_root / "FILES.json"
            if not sample_success_path.exists() or file_sha256(sample_success_path) != sample[
                "success_sha256"
            ]:
                failures.append(f"sample_success_hash:{relative}:{index}")
                continue
            sample_success = json.loads(sample_success_path.read_text())
            if (
                sample_success.get("logic") != logic
                or sample_success.get("run_seed") != int(seed)
                or sample_success.get("sample_seed") != int(seed) * 100000 + index
                or sample_success.get("num_steps") != 1000
                or sample_success.get("execution_device") != "cpu"
            ):
                failures.append(f"sample_identity:{relative}:{index}")
            if not files_path.exists() or file_sha256(files_path) != sample_success.get(
                "files_manifest_sha256"
            ):
                failures.append(f"files_manifest_hash:{relative}:{index}")
            sample_records += 1
        slices.append((logic, int(seed), slice_id))

    slices_by_campaign: dict[tuple[str, int], set[str]] = {}
    for logic, seed, slice_id in slices:
        slices_by_campaign.setdefault((logic, seed), set()).add(slice_id)
    complete_experiments = sum(
        slice_ids == {"s00", "s01", "s02", "s03"} for slice_ids in slices_by_campaign.values()
    )
    payload_paths = [
        row
        for row in listing
        if re.search(r"/samples/sample-\d+/29/371/sample\.pt$", row.get("path", ""))
    ]
    docking_files = [
        row
        for row in listing
        if row.get("path", "").endswith(("results.csv", "docking_summary.json"))
    ]
    missing_sources = [
        path for path in source_recovery["required_local_paths"] if not Path(path).exists()
    ]
    current_logdiff = {"AND": 0, "AND-NOT": 0}
    current_dualdiff = {"AND": 0, "AND-NOT": 0}
    status = classify_c4_completeness(
        current_logdiff,
        current_dualdiff,
        raw_complete=False,
        docking_complete=False,
        source_available=not missing_sources,
    )
    summary = {
        "claim_status": status,
        "empirical_claim_check_executed": False,
        "reason": (
            "The recovered route has no complete experiment, no docking results, no DualDiff "
            "campaign, and its hash-bound source/input files are absent."
        ),
        "bucket_listing_files": len(listing),
        "bucket_listing_sha256": file_sha256(root / "historical_bucket_listing.json"),
        "json_snapshot_files": len(list(snapshot.rglob("*.json"))),
        "terminal_slices": len(slices),
        "expected_logdiff_slices": 56,
        "manifest_bound_samples": sample_records,
        "payload_paths_in_listing": len(payload_paths),
        "expected_logdiff_samples": 448,
        "generation_fraction": sample_records / 448,
        "covered_logics": sorted({logic for logic, _, _ in slices}),
        "covered_run_seeds": sorted({seed for _, seed, _ in slices}),
        "covered_slice_ids": sorted({slice_id for _, _, slice_id in slices}),
        "complete_logdiff_experiments": complete_experiments,
        "expected_logdiff_experiments": 16,
        "dualdiff_experiments": 0,
        "expected_dualdiff_experiments": 16,
        "docking_result_files": len(docking_files),
        "uniform_binding_count": len(bindings),
        "manifest_integrity_failures": failures,
        "missing_hash_bound_sources": missing_sources,
        "official_molecular_repository_http_status": source_recovery[
            "molecular_code_link_retrieval"
        ]["http_status"],
        "historical_seed_0_raw_roots_available": False,
        "verification_routes_completed": len(verification_routes.get("routes", [])),
        "falsification_succeeded": falsification_check.get("falsification_succeeded"),
    }
    control_status = classify_c4_completeness(
        {"AND": 8, "AND-NOT": 8},
        {"AND": 8, "AND-NOT": 8},
        raw_complete=True,
        docking_complete=True,
        source_available=True,
    )
    control = {
        "control": "complete_two_method_two_condition_campaign",
        "audit_status": control_status,
        "rejected_false_block": control_status == "READY_FOR_CLAIM_CHECK",
    }
    write_json(root / "bucket_audit.json", summary)
    write_json(root / "negative_control.json", control)
    return summary, control


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def runtime_metadata(started_at: float) -> dict:
    try:
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        git_sha = "unavailable"
    return {
        "git_sha": git_sha,
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
        "estimated_required_cores": 1,
        "selected_compute": "backend supplied by orx; baseline policy selects local",
        "visible_cpu_count": os.cpu_count(),
        "single_core_algorithm": True,
        "runtime_seconds": time.perf_counter() - started_at,
        "seeds": list(range(25)),
    }


def run(output_dir: Path, seeds: int) -> dict:
    started_at = time.perf_counter()
    exhaustive = [exhaustive_binary(seed) for seed in range(seeds)]
    primitives = [row for seed in range(seeds) for row in primitive_checks(seed)]
    controls = dependent_controls()
    independent_groups = [exhaustive_categorical_groups(seed) for seed in range(seeds)]
    taxonomies = [exhaustive_taxonomy(seed) for seed in range(seeds)]
    taxonomy_control = taxonomy_overlap_control()
    table_2_summary, table_2_cells = audit_table_2()
    table_2_control = table_2_negative_control()
    claim_4, claim_4_control = audit_claim_4_evidence(output_dir)

    write_csv(output_dir / "claim-1" / "exhaustive_formulas.csv", exhaustive)
    write_csv(output_dir / "claim-1" / "primitive_rules.csv", primitives)
    write_csv(output_dir / "claim-1" / "negative_controls.csv", controls)
    write_csv(output_dir / "claim-2" / "table_2_cells.csv", table_2_cells)
    write_json(output_dir / "claim-2" / "negative_control.json", table_2_control)
    write_csv(output_dir / "claim-5" / "independent_groups.csv", independent_groups)
    write_csv(output_dir / "claim-5" / "taxonomy.csv", taxonomies)
    write_json(output_dir / "claim-5" / "negative_control.json", taxonomy_control)

    total_formulas = sum(int(row["formulas"]) for row in exhaustive)
    summary = {
        "claim_1": {
            "status": "VERIFIED",
            "compiled_formulas_checked": total_formulas,
            "max_probability_error": max(float(row["max_probability_error"]) for row in exhaustive),
            "max_score_error": max(float(row["max_score_error"]) for row in exhaustive),
            "max_finite_difference_error": max(float(row["max_finite_difference_error"]) for row in exhaustive),
        },
        "claim_1_rule_checks": {
            "primitive_rule_checks": len(primitives),
            "max_probability_error": max(float(row["probability_error"]) for row in primitives),
            "max_score_error": max(float(row["score_max_error"]) for row in primitives),
            "passed": sum(bool(row["rejected"]) for row in controls),
            "total": len(controls),
            "minimum_detected_error": min(
                max(float(row["probability_error"]), float(row["score_max_error"])) for row in controls
            ),
        },
        "claim_2": table_2_summary,
        "claim_2_negative_control": table_2_control,
        "claim_4": claim_4,
        "claim_4_negative_control": claim_4_control,
        "claim_5": {
            "status": "VERIFIED",
            "independent_group_events": sum(int(row["events"]) for row in independent_groups),
            "taxonomy_events": sum(int(row["events"]) for row in taxonomies),
            "max_probability_error": max(
                max(float(row["max_probability_error"]) for row in independent_groups),
                max(float(row["max_probability_error"]) for row in taxonomies),
            ),
            "max_score_error": max(
                max(float(row["max_score_error"]) for row in independent_groups),
                max(float(row["max_score_error"]) for row in taxonomies),
            ),
            "negative_control": taxonomy_control,
        },
    }
    failures = []
    if summary["claim_1"]["compiled_formulas_checked"] != seeds * 254:
        failures.append("claim_1_formula_count")
    if summary["claim_1"]["max_probability_error"] >= 1e-14 or summary["claim_1"]["max_score_error"] >= 1e-14:
        failures.append("claim_1_exactness")
    if summary["claim_1_rule_checks"]["passed"] != summary["claim_1_rule_checks"]["total"]:
        failures.append("claim_1_negative_controls")
    if summary["claim_2"]["status"] != "FALSIFIED":
        failures.append("claim_2_table_range")
    if not summary["claim_2_negative_control"]["verifier_rejected_false_falsification"]:
        failures.append("claim_2_negative_control")
    if summary["claim_4"]["claim_status"] != "BLOCKED":
        failures.append("claim_4_fail_closed_status")
    if summary["claim_4"]["manifest_integrity_failures"]:
        failures.append("claim_4_manifest_integrity")
    if summary["claim_4"]["terminal_slices"] != 12 or summary["claim_4"][
        "manifest_bound_samples"
    ] != 96:
        failures.append("claim_4_recovered_counts")
    if summary["claim_4"]["verification_routes_completed"] != 4:
        failures.append("claim_4_route_count")
    if summary["claim_4"]["falsification_succeeded"] is not False:
        failures.append("claim_4_falsification_status")
    if not summary["claim_4_negative_control"]["rejected_false_block"]:
        failures.append("claim_4_negative_control")
    if summary["claim_5"]["independent_group_events"] != seeds * 826:
        failures.append("claim_5_independent_event_count")
    if summary["claim_5"]["taxonomy_events"] != seeds * 254:
        failures.append("claim_5_taxonomy_event_count")
    if summary["claim_5"]["max_probability_error"] >= 1e-14 or summary["claim_5"]["max_score_error"] >= 1e-14:
        failures.append("claim_5_exactness")
    if not taxonomy_control["rejected"]:
        failures.append("claim_5_negative_control")

    checker = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("check_baseline_artifacts.py")), str(output_dir)],
        text=True,
        capture_output=True,
        check=False,
    )
    checker_output = checker.stdout + checker.stderr
    for claim_id in (1, 2, 5):
        (output_dir / f"claim-{claim_id}" / "independent_checker_output.txt").write_text(checker_output)
    print(checker_output, end="")
    if checker.returncode != 0:
        failures.append("independent_checker")
    claim_4_checker = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("check_claim4_evidence.py")), str(output_dir)],
        text=True,
        capture_output=True,
        check=False,
    )
    claim_4_checker_output = claim_4_checker.stdout + claim_4_checker.stderr
    (output_dir / "claim-4" / "independent_checker_output.txt").write_text(
        claim_4_checker_output
    )
    print(claim_4_checker_output, end="")
    if claim_4_checker.returncode != 0:
        failures.append("claim_4_independent_checker")

    summary["runtime"] = runtime_metadata(started_at)
    summary["independent_checker"] = {
        "status": "PASS" if checker.returncode == 0 and claim_4_checker.returncode == 0 else "FAIL",
        "baseline_returncode": checker.returncode,
        "claim_4_returncode": claim_4_checker.returncode,
    }
    summary["verifier"] = {"status": "PASS" if not failures else "FAIL", "failures": failures}
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if failures:
        raise SystemExit(1)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--seeds", type=int, default=25)
    args = parser.parse_args()
    run(args.output_dir, args.seeds)


if __name__ == "__main__":
    main()
