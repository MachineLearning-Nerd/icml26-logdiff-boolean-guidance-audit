# Source audit

## Paper source

- Title: Logical Guidance for the Exact Composition of Diffusion Models
- Authors: Francesco Alesiani, Jonathan Warrell, Tanja Bien, Henrik
  Christiansen, Matheus Ferraz, and Mathias Niepert
- arXiv: https://arxiv.org/abs/2602.05549
- OpenReview: https://openreview.net/forum?id=OAM1jJsMGp
- Version used by the evidence snapshot: arXiv v2, submitted 2026-02-05 and
  revised 2026-03-23
- Local HTML retrieval used by the audit: 2026-07-27, SHA-256
  67336441b284337c309cd66e2aee8d3a6bd01da716c145debe1319387b9c321a

The exact theorem and empirical anchors are preserved in each claim's
source_audit.md and claim_contract.json under
candidate_space/evidence/claim-1 through claim-5.

## Official implementation

The official image implementation is:

https://github.com/TanjaBien/LogDiff

The release-integrity audit pins commit
94ef35bafd4b4239e9832d8295128c09e8fc1472. That commit is present in the public
repository history. Its deterministic git archive has SHA-256
d3e7f6a56f665055fd39d54ebdc8c6f0d755e4752877be33a2cdce07be5b4086 and contains
73 paths.

The release README describes training, inference, and evaluation for
ColoredMNIST, Shapes3D, and CelebA. It also points to a separate molecular
implementation. The declared molecular repository was unavailable to the
public audit at the time of retrieval (HTTP 404); the related FKC source
preserved in the evidence is explicitly not treated as the missing LOGDIFF
implementation.

## Audit code

The repository's own producer and checkers are:

- repro/src/run_logdiff.py
- repro/src/check_baseline_artifacts.py
- repro/src/check_claim3_release.py
- repro/src/check_claim4_evidence.py
- candidate_space/code/audit_candidate_space.py

The copies under repro/src and candidate_space/code are byte-identical for the
four shared Python checkers. The finite certificate is therefore inspectable
from the repository root and from the evaluator-visible candidate surface.

## Evidence provenance

The public snapshot includes:

- paper-source and judged-Space provenance records under
  .openresearch/artifacts/provenance/
- claim contracts, methods, limitations, raw CSV/JSON evidence, and checker
  output under .openresearch/artifacts/claim-1 through claim-5
- human-readable evaluator pages under candidate_space/pages/

Generated images, model checkpoints, and full molecular input archives are not
silently represented as present. Their absence is part of the C3 and C4
decision boundary.
