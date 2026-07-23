# Recovered molecular campaign runbook

This runbook records infrastructure gates separately from the scientific
32-ligand x 8-run protocol. Failed infrastructure commands do not count as
claim evidence and do not end the campaign.

## Source and protocol

- LOGDIFF primary source: arXiv `2602.05549v2`, especially Section D.3 and
  Appendix F.
- Recovered FKC source: `martaskrt/fkc-diffusion@aa6f5ed4a0ebb91329d4cd5823cc7e77c5e196e6`.
- Targets: GRM5/P41594/index 29 and RRM1/P23921/index 371.
- Full protocol: 32 ligands, 23 atoms, 1000 denoising steps, beta 2.0, eight
  runs, AutoDock Vina docking against both targets.
- Anchored comparisons: AND docking product `73.20 +/- 3.18` for LOGDIFF versus
  `71.87 +/- 3.33` for DualDiff; AND-NOT separation `0.94 +/- 0.24` versus
  `0.28 +/- 0.08`.

## Portability failures and repairs

1. Generated-ligand evaluation initially failed before docking because RDKit
   2026.03.4 removed `rdkit.six`. The legacy SA scorer now falls back to
   standard-library `pickle` and `dict.items`; an ethanol scoring import gate
   passed afterward.
2. Cross-target `score_only` failed because pre-alignment coordinates can lie
   outside the second target's Vina grid. Full Vina docking is now executed
   first; score-only/minimize fall back to the full-dock affinity only for that
   explicit out-of-grid condition. The authoritative metric remains `dock`.
3. Vina returns PDBQT pose text, so RDKit's PDB parser produced `None` and the
   released alignment script had no candidate. Docked poses are now converted
   with Meeko `PDBQTMolecule.export_rdkit_mol`, preserving coordinates and atom
   mapping.

Each repair is narrow, source-parses, and is validated by standalone molecular
research gates with raw artifacts. No generated molecule, affinity, or failed
sample was hidden. Automated test suites are not part of this campaign.

## Exact probability-estimator repair and runtime gates

Appendix D.3 constructs the estimator probe from the current sample with the
single-transition `alpha_t`. The recovered checkpoint stores cumulative
products, so the implementation now recovers the exact transition as
`alpha_bar_t / alpha_bar_(t-1)`. The earlier portability smokes used cumulative
alpha and are therefore retained only as infrastructure evidence.

The full runner is `repro/src/run_parallel_molecular_protocol.py`. Each shard
is one independent deterministic trajectory and must pass protocol metadata,
finite-position, 1000-posterior-step, and SHA-256 gates before it is accepted.
A failed shard is retried up to ten times without discarding its command log or
failure record.

- Four-worker beta-2 gate: 4/4 trajectories and 80/80 steps completed; sampling
  time was 175.5-177.0 seconds per trajectory.
- Eight-worker gate: complete but slower in aggregate and caused heavy swap;
  it is rejected for the full campaign.
- Operator profile: dense linear layers dominate (1.744 seconds across 456
  calls in a one-step profile), followed by layer normalization and scatter.
  No removable data-loading or KNN hotspot remains.

## Smoke alignment gate

The only reconstructable molecule from the one-step 32-sample portability
batch was
`CCCSN[PH](CNP)(ONNNSCCPSF)S[SH](C)P`. It is chemically poor and is retained
only to exercise the complete docking/alignment path.

- GRM5 full-dock affinity: `-4.964` kcal/mol.
- RRM1 full-dock affinity: `-4.479` kcal/mol.
- Pocket-alignment atom map: 23 atoms.
- Alignment RMSD: `0.5589596772` A.
- Inputs/results:
  `outputs/molecular-recovery/alignment-prior-bs32-numatoms23-v2`.
- Aligned pockets:
  `outputs/molecular-recovery/aligned-protein-pockets-smoke-bs32-numatoms23-v2`.

This gate is not used to support the paper's reported docking values because it
uses one denoising step rather than 1000 and has 1/32 validity. It only proves
that full docking and alignment can execute locally before the expensive run.

## Next commands

1. Complete seed 0 with 32 restartable 1000-step trajectories using
   `--logic logdiff_and`, four workers, and beta 2.0.
2. Run the same 32-trajectory seed with `--logic logdiff_and_not`.
3. Dock every valid generated ligand to both targets at the paper's default
   Vina exhaustiveness 32.
4. Repeat seeds 0 through 7, preserving all failures and raw `sample.pt`, SDF,
   pickle, CSV, posterior-trajectory, and runtime artifacts.

## Independent evidence audit

The active postprocessing queue covers seed 0 for both conditions. That is one
32-ligand experiment per condition, whereas Appendix F and the reported
mean-plus/minus-standard-deviation values cover eight experiments. Seeds 1-7
remain required before claiming paper-level replication.

After each merged-and-docked seed, run
`repro/src/audit_molecular_campaign_evidence.py` as documented in
`docs/MOLECULAR_EVIDENCE_AUDIT.md`. The auditor validates every source shard
hash, merged tensor, target identity, and docking-table hash; canonicalizes
SMILES; independently recomputes Table 5/6 metrics; applies pairing and target
orientation negative controls; and refuses to pool AND with AND-NOT.
