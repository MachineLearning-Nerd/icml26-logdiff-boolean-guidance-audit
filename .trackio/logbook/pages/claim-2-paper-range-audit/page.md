# Claim 2 - paper-range audit


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_220f26d582d6", "created_at": "2026-07-19T18:56:30+00:00", "title": "Literal Table 2 audit"}
-->
The anchored wording says recursive 2-5 operation tasks obtain 94-98 percent for LOGDIFF versus 63-77 percent for the constant baseline across CMNIST and Shapes3D. A cell-by-cell audit of Table 2 does not support that literal range statement.

| Dataset | Method | N=2 | N=3 | N=4 | N=5 |
| --- | --- | ---: | ---: | ---: | ---: |
| CMNIST | LOGDIFF | 93.8 | 93.3 | 94.2 | 94.4 |
| Shapes3D | LOGDIFF | 88.8 | 88.6 | 85.1 | 87.6 |
| CMNIST | constant | 76.1 | 66.7 | 68.3 | 75.2 |
| Shapes3D | constant | 67.2 | 59.4 | 58.4 | 57.9 |

LOGDIFF actual range: 85.1-94.4. Constant actual range: 57.9-76.1. Verdict: falsified as written, independently of whether the broader qualitative ordering is favorable.
