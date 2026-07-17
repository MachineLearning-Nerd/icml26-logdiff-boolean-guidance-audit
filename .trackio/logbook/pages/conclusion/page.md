# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_7d2cd8090828", "created_at": "2026-07-17T03:43:16+00:00", "title": "Executive summary", "pinned": true, "pinned_at": "2026-07-17T03:43:17+00:00"}
-->
**Both official claims are verified.** LOGDIFF recursive guidance matches direct enumeration for all 6,350 compiled Boolean formulas, with posterior/score errors at floating-point roundoff and finite-difference agreement within 5.21e-10. Every primitive rule passes 100 checks, 12 tests pass, and all three structural-assumption violations are rejected.

## Scope & cost

| | This reproduction | Full empirical replication |
|---|---|---|
| Scope | Exact Propositions 3.1, 3.2 and C.3; exhaustive three-binary query space | CMNIST, Shapes3D, CelebA and protein generation |
| Hardware | CPU | GPU training and inference |
| Time | Under 2 seconds | Multiple training/evaluation runs |
| Cost | $0 | Hardware-dependent |
| Outcome | Both exact challenge claims verified | Tests downstream image/protein conformity, outside the two claim texts |
