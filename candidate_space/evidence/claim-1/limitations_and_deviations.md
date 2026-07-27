# Claim 1 limitations and deviations

- The paper theorem is continuous and universally quantified; this certificate
  is exhaustive only over the complete declared finite semantic domain.
- Smooth softmax posteriors replace a trained diffusion network. This is a
  theorem-calibration certificate, not an image-generation proxy.
- The independent full-joint oracle and finite-difference triangulation test the
  calculus directly; no formula-derived tolerance or sample budget is used.
