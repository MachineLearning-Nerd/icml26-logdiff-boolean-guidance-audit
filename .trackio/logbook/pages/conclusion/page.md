# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_conclusion_anchored_20260720", "created_at": "2026-07-20T00:25:00+00:00", "title": "Anchored conclusion", "pinned": true, "pinned_at": "2026-07-20T00:25:00+00:00"}
-->
**The evidence is mixed, and the verdicts remain claim-specific.** C1 and C5
are verified by exhaustive independent oracles. C2 is falsified as written by
the paper's own Table 2 values. C3's published table transcription matches, but
the empirical protocol cannot be reproduced from the pinned author package
because its checkpoints are absent and its released config/FID path diverges
from the paper. C4 has progressed beyond a release audit: the exact targets,
weights, real 3D sampler, and AutoDock Vina workflow are recovered and execute;
the full generated-ligand campaign remains active until its metrics complete.

## Verification scale

| Evidence gate | Result |
| --- | ---: |
| Exhaustive logical events | C1: 6,350; C5: 27,000 |
| Fixed-timestep classifier evaluations | 70,000 predictions per attribute |
| Exact upstream CMNIST training | 50 epochs, 60,000-example source split |
| Molecular checkpoint hashes | 3 of 3 match |
| Exact GRM5/RRM1 target files | 8 of 8 present |
| Real reference-complex Vina docking gates | 2 of 2 pass |
| Anchored claims overclaimed as reproduced | 0 |

The exhaustive-event rows overlap between certificates, so the table avoids
presenting their sum as a count of unique formulas. All published evidence is
deterministic or source-pinned, and all incomplete empirical claims are labeled
incomplete rather than inferred from the paper's numbers.


---
<!-- trackio-cell
{"type": "artifact", "id": "cell_bf4c3f971732", "created_at": "2026-07-19T19:06:02+00:00", "title": "Reproduction bundle v0", "artifact": "reproduction-logdiff/repro-bundle:v0", "artifact_type": "reproduction-evidence"}
-->
**📦 Artifact** `reproduction-logdiff/repro-bundle:v0` · reproduction-evidence

[Public reproduction bundle](https://huggingface.co/buckets/DineshAI/OAM1jJsMGp-artifacts/reproduction-bundle)

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_e73e01a85411", "created_at": "2026-07-19T19:06:04+00:00", "title": "Public evidence bucket"}
-->
Public artifact mirror: https://huggingface.co/buckets/DineshAI/OAM1jJsMGp-artifacts/reproduction-bundle
