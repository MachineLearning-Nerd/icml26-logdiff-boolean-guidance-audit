import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest


MODULE_PATH = Path(__file__).parents[1] / "src" / "run_logdiff.py"
SPEC = importlib.util.spec_from_file_location("run_logdiff", MODULE_PATH)
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


@pytest.mark.parametrize("seed", range(5))
def test_all_254_nontrivial_three_binary_queries(seed):
    result = M.exhaustive_binary(seed)
    assert result["formulas"] == 254
    assert result["max_probability_error"] < 1e-14
    assert result["max_score_error"] < 1e-14
    assert result["max_finite_difference_error"] < 1e-8


@pytest.mark.parametrize("seed", range(5))
def test_every_primitive_rule(seed):
    for result in M.primitive_checks(seed):
        assert result["probability_error"] < 1e-14
        assert result["score_max_error"] < 1e-14


def test_assumption_violations_are_detected():
    controls = M.dependent_controls()
    assert len(controls) == 3
    assert all(result["rejected"] for result in controls)


def test_compiled_dnf_matches_independent_oracle_for_ternary_system():
    rng = np.random.default_rng(2026)
    probabilities, atoms = M.categorical_model([rng.normal(size=3), rng.normal(size=3), rng.normal(size=2)])
    assignments = tuple(__import__("itertools").product(range(3), range(3), range(2)))
    for _ in range(100):
        selected = tuple(a for a in assignments if rng.random() < 0.5)
        if not selected:
            selected = (assignments[0],)
        recursive = M.compiled_dnf(atoms, selected)
        oracle = M.direct_event(probabilities, atoms, selected)
        assert recursive.probability == pytest.approx(oracle.probability, abs=1e-14)
        assert np.max(np.abs(recursive.score - oracle.score)) < 1e-14
