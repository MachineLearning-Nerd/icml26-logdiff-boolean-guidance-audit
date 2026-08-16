# Reproduction audit report

## Decision

The public evidence supports a scoped result of:

- C1: finite-domain verification
- C2: falsification of the literal Table 2 range statement
- C3: blocked exact CelebA reproduction
- C4: blocked exact molecular comparison
- C5: finite-domain verification

The audit deliberately distinguishes a mathematical certificate, a primary
table contradiction, a release-integrity blocker, and a missing empirical
campaign. These categories must not be collapsed into one blanket score.

## Evidence flow

~~~text
paper and official source pins
          ↓
claim contracts and explicit assumptions
          ↓
producers + independent checkers + negative controls
          ↓
raw CSV/JSON evidence and evaluator-visible pages
          ↓
scoped claim status
~~~

The full claim paths are in CLAIM_EVIDENCE.md. Branch lineage is in
BRANCH_AUDIT.md. Source and environment assumptions are in SOURCE_AUDIT.md and
ENVIRONMENT.md.

## Reproduction status by modality

| Modality | Result |
| --- | --- |
| Boolean calculus | Exhaustive finite certificates with independent full-joint oracles |
| Table 2 statement | Exact cell-by-cell primary-source audit |
| CelebA | Release and protocol audit only; no proxy generation |
| Molecular design | Hash-bound partial-manifest audit only; no complete campaign |
| External judge | Historical 6/10 record retained as provenance |

## Publication hygiene

The final repository surface uses a descriptive ICML 2026 name, descriptive
branch names, canonical MachineLearning-Nerd commit identities, a citation
file, and an author thank-you note. The original experiment checkpoints remain
reachable through the mapped branches; the normalization changes naming and
attribution metadata, not the scientific files.
