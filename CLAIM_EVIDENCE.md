# Claim-to-evidence ledger

This ledger separates the paper statement, the executable producer, the
stored evidence, and the decision boundary. A passing checker means that the
recorded evidence satisfies its contract; it does not erase a missing
full-scale experiment.

## Summary

| Claim | Paper anchor | Producer | Evidence | Verdict |
| --- | --- | --- | --- | --- |
| C1 | Proposition 3.1 | repro/src/run_logdiff.py: exhaustive_binary, primitive_checks, dependent_controls | .openresearch/artifacts/claim-1/* and the C1 contract | VERIFIED_SCOPED |
| C2 | Table 2, N=2 through N=5 | repro/src/run_logdiff.py: audit_table_2, table_2_negative_control | .openresearch/artifacts/claim-2/table_2_cells.csv and negative_control.json | FALSIFIED_EXACT_STATEMENT |
| C3 | Section 4.1, Table 3, Appendix A.5 | repro/src/run_logdiff.py: audit_claim_3_release; check_claim3_release.py | .openresearch/artifacts/claim-3/* and the pinned author-release manifest | BLOCKED |
| C4 | Section 4.2, Tables 5–6, Appendix A.6 | repro/src/run_logdiff.py: audit_claim_4_evidence; check_claim4_evidence.py | .openresearch/artifacts/claim-4/* and the hash-bound bucket snapshot | BLOCKED |
| C5 | Proposition C.2 | repro/src/run_logdiff.py: exhaustive_categorical_groups, exhaustive_taxonomy, taxonomy_overlap_control | .openresearch/artifacts/claim-5/* | VERIFIED_SCOPED |

## C1 — exact Boolean calculus

The producer creates smooth softmax posteriors for three independent binary
categorical variables. For each of 25 seeds it compiles every one of the 254
nonempty, non-universal events, for 6,350 formulas in total. It compares the
recursive CI/ME calculation with an independently enumerated full-joint
probability and score. Every seventeenth event also receives a central
finite-difference check.

Published measurements:

- maximum probability error: 2.220446049250313e-16
- maximum score error: 3.3306690738754696e-16
- maximum finite-difference error: 5.201041819447028e-10
- primitive rules checked: 100
- invalid-rule controls rejected: 3 of 3

The result is rigorous for the declared finite certificate domain. It is not
presented as a proof for all continuous diffusion models.

## C2 — Table 2 range statement

The producer transcribes all eight CMNIST and Shapes3D cells for each method,
keeps the paper's stated intervals beside each value, and evaluates membership
without rounding. The recorded values span 85.1–94.4 for LOGDIFF and 57.9–76.1
for constant mixing. Only 2/8 LOGDIFF cells and 5/8 constant cells meet their
literal intervals.

The verdict is limited to the exact aggregate range wording. It does not say
that LOGDIFF loses the broader qualitative comparison. The range-conforming
negative control is rejected by the verifier, which prevents a false
falsification caused by the decision rule.

## C3 — CelebA negation

The producer reads the complete 73-path tree of the official
TanjaBien/LogDiff release at commit
94ef35bafd4b4239e9832d8295128c09e8fc1472. It checks the three declared
CelebA checkpoint paths, the composition dataset configuration, the requested
sample count, and the metric implementation.

The paper contract is 5,000 images per task, 50 queries of 100 images, and
clean-fid. The pinned release lacks the author-equivalent diffusion,
composition-classifier, and judge checkpoints; the composition config target is
missing; and the evaluation path uses TorchMetrics FID with a mismatched sample
accounting path. The four-route audit therefore remains BLOCKED. No public
Diffusers model is used as a substitute.

The synthetic complete-release control returns READY_TO_RUN, proving that the
checker does not block a release merely because it is not the current one.

## C4 — GRM5/RRM1 molecular comparison

The producer validates the preserved bucket listing and all available JSON
manifests before assessing completeness. It checks SUCCESS-last ordering,
source/input/environment binding, sample identity, sample hashes, and the
required method, condition, seed, and slice dimensions.

The paper contract requires both LOGDIFF and DualDiff, AND and AND-NOT, eight
experiments per condition, 32 ligands per experiment, 23 atoms, 1,000
denoising steps, and docking results for both GRM5 and RRM1. The snapshot has
12 terminal slices and 96 manifest-bound LOGDIFF payloads, or 21.4% of the
planned 448 LOGDIFF payloads. It has no complete experiment, no DualDiff
campaign, and no docking-result file. The result is BLOCKED, not falsified.

The complete two-method/two-condition synthetic control returns
READY_FOR_CLAIM_CHECK. Partial molecular files are never promoted to a
headline score.

## C5 — completeness certificate

The producer exhausts 20,650 events across independent categorical domains
(2,2,2), (3,2), and (3,3), and 6,350 events across a complete eight-leaf
taxonomy. The recursive compiler is compared with a full-joint oracle at 25
posterior settings.

Published measurements:

- independent-group events: 20,650
- taxonomy events: 6,350
- maximum probability error: 2.220446049250313e-16
- maximum score error: 3.3306690738754696e-16
- overlapping non-nested control: rejected

This is scoped to the finite domains in the contract. The invalid-overlap
control demonstrates fail-closed behavior outside the assumptions; it is not a
counterexample to Proposition C.2.

## Evidence integrity

The exact snapshot hashes are listed in EVIDENCE_MANIFEST.json. The independent
repository-state checker is verify_final.py. The full source, paper, and
runtime boundaries are in SOURCE_AUDIT.md and ENVIRONMENT.md.
