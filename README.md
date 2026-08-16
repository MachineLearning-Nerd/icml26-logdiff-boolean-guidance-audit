# ICML 2026 — LOGDIFF reproduction audit

This repository is an independent, claim-by-claim audit of
[*Logical Guidance for the Exact Composition of Diffusion Models*](https://arxiv.org/abs/2602.05549)
(OpenReview OAM1jJsMGp). It preserves the executable finite certificates,
release-integrity checks, historical molecular manifests, and evaluator-visible
reports used to reach each result.

The intended final repository name is
icml26-logdiff-boolean-guidance-audit; the old name was
icml26-repro-OAM1jJsMGp-logdiff-exact-boolean-guidance.

## Paper

- **Title:** Logical Guidance for the Exact Composition of Diffusion Models
- **Authors:** Francesco Alesiani, Jonathan Warrell, Tanja Bien, Henrik
  Christiansen, Matheus Ferraz, and Mathias Niepert
- **Paper:** [arXiv:2602.05549](https://arxiv.org/abs/2602.05549)
- **Submission:** [OpenReview OAM1jJsMGp](https://openreview.net/forum?id=OAM1jJsMGp)
- **Official implementation:** [TanjaBien/LogDiff](https://github.com/TanjaBien/LogDiff),
  audited at commit 94ef35bafd4b4239e9832d8295128c09e8fc1472

The paper proposes LOGDIFF, an exact Boolean calculus for composing diffusion
guidance signals under conditional-independence and mutual-exclusion
conditions, together with a hybrid guidance method for image and protein
generation.

## Current claim ledger

| Claim | What is tested | Evidence outcome |
| --- | --- | --- |
| C1 — Proposition 3.1 | Exact recursive probability and score composition under the paper's CI/ME assumptions | VERIFIED_SCOPED: 6,350 finite formulas, maximum probability error 2.22e-16, maximum score error 3.33e-16; 3/3 violation controls rejected |
| C2 — Table 2 ranges | The literal ranges “LOGDIFF 94–98%” and “constant 63–77%” over all 16 cells | FALSIFIED_EXACT_STATEMENT: LOGDIFF has 2/8 cells in range and constant mixing has 5/8; this does not falsify the broader qualitative comparison |
| C3 — CelebA negation | Reported NOT FID 23.61 versus 32.87 with the paper's 5,000-sample clean-fid protocol | BLOCKED: the pinned author release lacks the required checkpoints/config and uses a different FID path; no proxy was substituted |
| C4 — GRM5/RRM1 molecules | Eight 32-ligand experiments per method and condition, including LOGDIFF versus DualDiff | BLOCKED: 96 partial LOGDIFF payloads are preserved, but no complete experiment, DualDiff campaign, or docking result exists |
| C5 — Proposition C.2 | Completeness for independent categorical groups and nested taxonomies | VERIFIED_SCOPED: 20,650 independent-group events and 6,350 taxonomy events; invalid-overlap control rejected |

These are evidence labels, not claims that every continuous theorem or every
full-scale empirical result has been reproduced. The recorded external judge
result is a historical 6/10 at the immutable judged Space revision
1fd04429cb112e90be5fa2bb7a19b827667922bf; no score increase is claimed here.

The detailed production paths are in
[CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md), and the machine-readable version is
[claims.json](claims.json).

## How each claim is produced

- **C1:** repro/src/exhaustive_binary, primitive_checks, and
  dependent_controls enumerate finite categorical events, compare recursive
  rules with an independent full-joint oracle, and run negative controls.
- **C2:** repro/src/audit_table_2 expands the paper's Table 2 into all 16
  cells and checks interval membership without rounding or aggregation.
- **C3:** repro/src/audit_claim_3_release and
  repro/src/check_claim3_release.py inspect the pinned official release,
  checkpoint paths, dataset configuration, sample accounting, and FID
  implementation. A synthetic complete-release control prevents a false
  BLOCKED verdict.
- **C4:** repro/src/audit_claim_4_evidence and
  repro/src/check_claim4_evidence.py validate the preserved bucket listing,
  terminal slice manifests, sample hashes, method/condition counts, and
  completeness contract. A synthetic complete two-method control prevents a
  false BLOCKED verdict.
- **C5:** repro/src/exhaustive_categorical_groups,
  exhaustive_taxonomy, and taxonomy_overlap_control enumerate both finite
  constructive cases and deliberately reject an invalid non-nested overlap.

The public evaluator-visible surface remains under
[candidate_space](candidate_space/README.md). The illustrated technical and
release reports are under [reports/claim-by-claim](reports/claim-by-claim/).

## Branches

main is the landing page and final publication surface. The former orx/*
branches are historical experiment checkpoints; they are being mapped to
descriptive baseline/, audit/, candidate/, and release/ names. See the
complete old-to-new mapping and purpose of every branch in
[BRANCH_AUDIT.md](BRANCH_AUDIT.md).

## Reproduce the published snapshot

The locked verifier command is:

~~~bash
uv sync --frozen
uv run python repro/src/run_logdiff.py \
  --output-dir .openresearch/artifacts --seeds 25
~~~

The tracked .openresearch/artifacts/ directory supplies the hash-bound release
evidence required by the C3 and C4 fail-closed checks. To preserve the
published snapshot, copy that directory to a temporary output directory before
running a new audit. The command does not claim to regenerate the missing
CelebA or molecular evidence; it verifies their documented blockers.

For a lightweight repository-state check after cloning:

~~~bash
python3 verify_final.py
~~~

The recorded environment, runtime, source pins, and limitations are in
[ENVIRONMENT.md](ENVIRONMENT.md) and [SOURCE_AUDIT.md](SOURCE_AUDIT.md).

## Citation and thanks

Please cite the paper with [CITATION.cff](CITATION.cff). A direct thank-you
note to the authors is preserved in
[AUTHOR_THANK_YOU.md](AUTHOR_THANK_YOU.md). This audit is not an official
paper implementation and does not imply author endorsement.
