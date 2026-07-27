# Claim 4 source audit

The paper HTML was retrieved on 2026-07-27 with SHA-256
`67336441b284337c309cd66e2aee8d3a6bd01da716c145debe1319387b9c321a`.
Section anchor `S4.SS2.p1.1` specifies 32 ligands of size 23 over eight
experiments for GRM5 (P41594) and RRM1 (P23921). Tables `S4.T5` and `S4.T6`
contain the claimed values. Section anchor `S4.SS2.p4.1` describes delta only
as the average difference between the minimum and maximum docking scores.
Appendix anchor `A6.p1.1` specifies 1,000 denoising steps, beta 2.0, and
AutoDock Vina.

The image-code author repository at commit
`94ef35bafd4b4239e9832d8295128c09e8fc1472` says the molecular code is at
`https://github.com/nec-research/Logical-Guidance-for-the-Exact-Composition-of-Diffusion-Models`.
An explicit-User-Agent retrieval of that URL returned HTTP 404 on 2026-07-27.

The prior reconstructed route bound its work to runner SHA-256
`ce6b6a67...`, contract SHA-256 `cadf9130...`, and a 63,049,318-byte input
archive with SHA-256 `a0bbb967...`. None of those execution inputs remains in
the repository, OpenResearch cache, or prior local-run roots. The bootstrap and
historical documentation remain, but they cannot recreate a hash-identical
runner or scientific input.

The bucket contains 12 successful generation slices and 96 payload paths:
indices 0–23 for LOGDIFF AND and LOGDIFF AND-NOT, seeds 1 and 2. It contains
no complete 32-ligand experiment, no seed 3–7 data, no DualDiff campaign, and
no docking results. The complete listing and all 242 available JSON manifests
are preserved as raw evidence.

The paper does not state the Vina exhaustiveness, the exact across-experiment
spread convention, or an algebraic signed definition of delta. Historical
reconstruction choices must therefore remain labeled as deviations.
