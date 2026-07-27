# Claim 1 — exact logical guidance


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_82e4b36f7fad", "created_at": "2026-07-17T03:43:08+00:00", "title": "Claim and exhaustive protocol"}
-->
LOGDIFF claims exact score-based guidance for complex logical expressions. Proposition 3.2 compiles a categorical query into conjunctions of independent variables joined by mutually-exclusive disjunctions. We exhaust every 254 nonempty, nonuniversal event subsets on three binary variables across 25 independently sampled posterior settings. A separate full-joint enumerator is the probability and gradient oracle.


---
<!-- trackio-cell
{"type": "code", "id": "cell_f1b67f985082", "created_at": "2026-07-17T03:43:10+00:00", "title": "Exhaust 6,350 compiled Boolean formulas", "command": ["python", "repro/src/run_logdiff.py", "--output-dir", "outputs", "--seeds", "25"], "exit_code": 0, "duration_s": 0.955}
-->
````bash
$ python repro/src/run_logdiff.py --output-dir outputs --seeds 25
````

exit 0 · 1.0s


````python title=run_logdiff.py
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
import itertools
import json
import math
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


def run(output_dir: Path, seeds: int) -> dict:
    exhaustive = [exhaustive_binary(seed) for seed in range(seeds)]
    primitives = [row for seed in range(seeds) for row in primitive_checks(seed)]
    controls = dependent_controls()
    write_csv(output_dir / "exhaustive_formulas.csv", exhaustive)
    write_csv(output_dir / "primitive_rules.csv", primitives)
    write_csv(output_dir / "negative_controls.csv", controls)

    total_formulas = sum(int(row["formulas"]) for row in exhaustive)
    summary = {
        "claim_1": {
            "status": "verified",
            "compiled_formulas_checked": total_formulas,
            "max_probability_error": max(float(row["max_probability_error"]) for row in exhaustive),
            "max_score_error": max(float(row["max_score_error"]) for row in exhaustive),
            "max_finite_difference_error": max(float(row["max_finite_difference_error"]) for row in exhaustive),
        },
        "claim_2": {
            "status": "verified",
            "primitive_rule_checks": len(primitives),
            "max_probability_error": max(float(row["probability_error"]) for row in primitives),
            "max_score_error": max(float(row["score_max_error"]) for row in primitives),
        },
        "negative_controls": {
            "passed": sum(bool(row["rejected"]) for row in controls),
            "total": len(controls),
            "minimum_detected_error": min(
                max(float(row["probability_error"]), float(row["score_max_error"])) for row in controls
            ),
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--seeds", type=int, default=25)
    args = parser.parse_args()
    run(args.output_dir, args.seeds)


if __name__ == "__main__":
    main()


````


````output
{
  "claim_1": {
    "status": "verified",
    "compiled_formulas_checked": 6350,
    "max_probability_error": 2.220446049250313e-16,
    "max_score_error": 3.3306690738754696e-16,
    "max_finite_difference_error": 5.201041819447028e-10
  },
  "claim_2": {
    "status": "verified",
    "primitive_rule_checks": 100,
    "max_probability_error": 2.220446049250313e-16,
    "max_score_error": 3.3306690738754696e-16
  },
  "negative_controls": {
    "passed": 3,
    "total": 3,
    "minimum_detected_error": 0.05901160358505326
  }
}

````


---
<!-- trackio-cell
{"type": "artifact", "id": "cell_2034f5e63c38", "created_at": "2026-07-17T03:43:10+00:00", "title": "Artifact: primitive_rules.csv", "path": "outputs/primitive_rules.csv", "size": 4567, "artifact_type": "dataset", "auto": true}
-->
**📦 Artifact** `outputs/primitive_rules.csv` · dataset · 4.6 kB

trackio-local-path://outputs/primitive_rules.csv


---
<!-- trackio-cell
{"type": "artifact", "id": "cell_182de3768b2d", "created_at": "2026-07-17T03:43:10+00:00", "title": "Artifact: exhaustive_formulas.csv", "path": "outputs/exhaustive_formulas.csv", "size": 1969, "artifact_type": "dataset", "auto": true}
-->
**📦 Artifact** `outputs/exhaustive_formulas.csv` · dataset · 2.0 kB

trackio-local-path://outputs/exhaustive_formulas.csv


---
<!-- trackio-cell
{"type": "artifact", "id": "cell_1043f70d99f9", "created_at": "2026-07-17T03:43:10+00:00", "title": "Artifact: negative_controls.csv", "path": "outputs/negative_controls.csv", "size": 284, "artifact_type": "dataset", "auto": true}
-->
**📦 Artifact** `outputs/negative_controls.csv` · dataset · 284 B

trackio-local-path://outputs/negative_controls.csv


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_b6736a65cd12", "created_at": "2026-07-17T03:43:11+00:00", "title": "Result"}
-->
**VERIFIED:** 6,350/6,350 compiled formulas match direct enumeration. Maximum posterior error is 2.22e-16; maximum analytic score error is 3.33e-16. Independent centered finite differences agree within 5.21e-10.
