# Status — LOGDIFF (OAM1jJsMGp)

**Audit snapshot:** 2026-08-16
**Repository target:** MachineLearning-Nerd/icml26-logdiff-boolean-guidance-audit
**Paper:** [arXiv:2602.05549](https://arxiv.org/abs/2602.05549)
**Public evidence run:** ac7ad48b7dc4120acbbbbe0468f0cfa76c4591bc, recorded
2026-07-27

## Scientific status

| Claim | Status | Short reason |
| --- | --- | --- |
| C1 — Proposition 3.1 | VERIFIED_SCOPED | Exhaustive finite certificate and independent oracle agree within 1e-14; controls reject invalid rules |
| C2 — Table 2 range wording | FALSIFIED_EXACT_STATEMENT | The paper's own 16 cells do not satisfy the two literal aggregate ranges |
| C3 — CelebA | BLOCKED | Required author-equivalent checkpoints and exact clean-fid execution path are unavailable |
| C4 — GRM5/RRM1 | BLOCKED | Partial LOGDIFF payloads do not satisfy the complete paired LOGDIFF/DualDiff protocol |
| C5 — Proposition C.2 | VERIFIED_SCOPED | Both finite constructive domains pass; invalid overlap is rejected |

The historical external judge score is 6/10. It is retained as provenance,
not treated as a current score or as evidence that the blocked claims passed.

## Public evidence boundaries

- The mathematical certificates are exhaustive only over their declared finite
  domains; they are not machine-checked proofs for arbitrary continuous
  diffusion models.
- C2 audits the paper's table directly and does not assess every empirical
  advantage of LOGDIFF.
- C3 is a release-integrity audit, not a substitute image-generation run.
- C4 contains 96 manifest-bound partial payloads out of the planned 448
  LOGDIFF payloads, with no complete 32-ligand experiment, DualDiff campaign,
  or docking results.
- Historical live-job and external Space notes are preserved as dated
  provenance only. They are not silently promoted to current GitHub evidence.

## Reproduction entrypoints

- Fixed command: uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25
- Claim contracts and raw evidence: candidate_space/evidence/
- Independent checkers: repro/src/check_*.py
- Repository-state verifier: verify_final.py
- Branch mapping: BRANCH_AUDIT.md
- Source and runtime limits: SOURCE_AUDIT.md and ENVIRONMENT.md

The repository is intentionally fail-closed: missing assets, protocol
mismatches, incomplete campaigns, and invalid branch/identity states remain
visible rather than being converted into optimistic scores.
