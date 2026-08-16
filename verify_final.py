#!/usr/bin/env python3
"""Fail-closed checks for the published LOGDIFF repository snapshot."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_BRANCHES = {
    "main",
    "baseline/frozen-claims",
    "audit/celeba-release",
    "audit/celeba-evidence",
    "audit/molecular-recovery",
    "audit/molecular-evidence",
    "candidate/cumulative-claims",
    "release/evaluator-artifact",
    "audit/csv-release",
    "release/publication-surface",
    "release/final-provenance",
}
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = "MachineLearning-Nerd@users.noreply.github.com"
REQUIRED_FILES = {
    "README.md",
    "STATUS.md",
    "CLAIM_EVIDENCE.md",
    "BRANCH_AUDIT.md",
    "SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "REPORT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "claims.json",
    "EVIDENCE_MANIFEST.json",
}


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    missing = sorted(path for path in REQUIRED_FILES if not (ROOT / path).is_file())
    if missing:
        fail("missing required files: " + ", ".join(missing))

    origin = git("config", "--get", "remote.origin.url")
    if "MachineLearning-Nerd/icml26-logdiff-boolean-guidance-audit" not in origin:
        fail(f"unexpected origin: {origin}")
    if git("branch", "--show-current") != "main":
        fail("HEAD is not on main")

    remote_refs = git(
        "for-each-ref", "--format=%(refname)", "refs/remotes/origin"
    ).splitlines()
    remote_branches = {
        ref.removeprefix("refs/remotes/origin/")
        for ref in remote_refs
        if not ref.endswith("/HEAD")
    }
    if remote_branches != EXPECTED_BRANCHES:
        fail(
            "branch inventory mismatch: expected "
            + repr(sorted(EXPECTED_BRANCHES))
            + ", got "
            + repr(sorted(remote_branches))
        )
    if any(branch.startswith("orx/") for branch in remote_branches):
        fail("legacy orx branch remains")

    commits = git("rev-list", "--all").splitlines()
    if not commits:
        fail("no reachable commits")
    for commit in commits:
        record = git(
            "show",
            "-s",
            "--format=%an%n%ae%n%cn%n%ce%n%B",
            commit,
        ).splitlines()
        if len(record) < 4:
            fail(f"unreadable commit metadata: {commit}")
        if record[:4] != [
            CANONICAL_NAME,
            CANONICAL_EMAIL,
            CANONICAL_NAME,
            CANONICAL_EMAIL,
        ]:
            fail(f"non-canonical identity in {commit}: {record[:4]}")
        if any(line.lower().startswith("co-authored-by:") for line in record[4:]):
            fail(f"co-author trailer in {commit}")

    claims = json.loads((ROOT / "claims.json").read_text())
    expected_status = {
        "C1": "VERIFIED_SCOPED",
        "C2": "FALSIFIED_EXACT_STATEMENT",
        "C3": "BLOCKED",
        "C4": "BLOCKED",
        "C5": "VERIFIED_SCOPED",
    }
    actual_status = {claim["id"]: claim["status"] for claim in claims["claims"]}
    if actual_status != expected_status:
        fail(f"claim status mismatch: {actual_status}")

    manifest = json.loads((ROOT / "EVIDENCE_MANIFEST.json").read_text())
    for relative, expected in manifest["files"].items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"manifest file missing: {relative}")
        actual = sha256(path)
        if actual != expected:
            fail(f"manifest hash mismatch for {relative}: {actual}")

    summary = json.loads(
        (ROOT / ".openresearch/artifacts/run-07daf77f-summary.json").read_text()
    )
    if summary["verifier"]["status"] != "PASS":
        fail("published cumulative verifier is not PASS")
    if summary["claim_1"]["compiled_formulas_checked"] != 6350:
        fail("C1 formula count changed")
    if summary["claim_2"]["status"] != "FALSIFIED":
        fail("C2 status changed")
    if summary["claim_3"]["claim_status"] != "BLOCKED":
        fail("C3 status changed")
    if summary["claim_4"]["claim_status"] != "BLOCKED":
        fail("C4 status changed")
    if summary["claim_5"]["independent_group_events"] != 20650:
        fail("C5 independent-group count changed")

    readme = (ROOT / "README.md").read_text()
    if "icml26-logdiff-boolean-guidance-audit" not in readme:
        fail("README does not identify the final repository name")
    citation = (ROOT / "CITATION.cff").read_text()
    if "arxiv.org/abs/2602.05549" not in citation:
        fail("CITATION.cff does not cite the paper")

    print(
        "PASS: "
        f"{len(commits)} canonical commits, "
        f"{len(remote_branches)} descriptive branches, "
        "claim statuses and evidence hashes verified"
    )


if __name__ == "__main__":
    main()
