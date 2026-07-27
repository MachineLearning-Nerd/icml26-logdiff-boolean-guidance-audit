# Claim 3 source audit

The exact paper source is arXiv 2602.05549, retrieved from
`https://ar5iv.labs.arxiv.org/html/2602.05549` on 2026-07-27 with SHA-256
`67336441b284337c309cd66e2aee8d3a6bd01da716c145debe1319387b9c321a`.

Section anchor `S4.SS1.p7.1` restricts CelebA evaluation to the binary
Blond/Non-blond and Male/Female attributes and states that LOGDIFF has
substantially lower FID than the constant baseline for negation. Table anchor
`S4.T3` reports 23.61 versus 32.87. Appendix anchor
`A5.SS2.SSS0.Px3.p1.1` specifies 5,000 generated samples per task, comprising
100 images for each of 50 queries, evaluated with clean-fid.

The author repository was retrieved from `https://github.com/TanjaBien/LogDiff`
at commit `94ef35bafd4b4239e9832d8295128c09e8fc1472`. A deterministic `git archive`
of that revision has SHA-256
`d3e7f6a56f665055fd39d54ebdc8c6f0d755e4752877be33a2cdce07be5b4086`.
The complete 73-path tree is recorded in `author_release_snapshot.json`.

The three CelebA checkpoint paths declared by `configs/celeba_inference.yaml`
are absent. The classifier-training config requests
`configs/dataset/celeba_cs_latents_male_haircolors.yaml`, which is absent; only
a copy-suffixed near-match exists. The released evaluation generates 5,000
images per task, but calls the result writer with `5000 * batch_size` (500,000
at the default batch size), and imports TorchMetrics FID rather than the
paper-specified clean-fid.

These facts block execution of the exact author-equivalent protocol. They do
not contradict the empirical claim and therefore cannot support FALSIFIED.

## Four verification routes

The complete low-confidence sequence is recorded in
`verification_routes.json`: exact release executability, public author
checkpoint provenance, independent public-model reconstruction, and a strict
falsification route. The public reconstruction resolves a real 114,049,969-byte
CelebA Diffusers UNet, but it lacks every LoGDiff-specific classifier and the
paper's diffusion state. The fourth route finds no admissible counterexample,
so Claim 3 remains `BLOCKED`.
