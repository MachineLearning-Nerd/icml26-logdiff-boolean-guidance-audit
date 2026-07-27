# Claim 3 - CelebA release audit


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_218e573f73f5", "created_at": "2026-07-19T18:56:31+00:00", "title": "Fail-closed source audit"}
-->
The pinned author repository declares nine CMNIST, Shapes3D, and CelebA checkpoint paths; none is present. For CelebA specifically, the composition config requests a dataset YAML that does not exist, while a copy-suffixed near-match exists. The paper specifies clean-fid over 5,000 samples per task, but the released code imports TorchMetrics FID and records 500,000 samples under its default accounting.

The published numerical transcription is correct: negation FID 23.61 for LOGDIFF versus 32.87 for the constant baseline, with comparable AND and OR-CI conformity. Those numbers are not relabeled as reproduced because the released package cannot execute the stated protocol without absent checkpoints and repairs.
