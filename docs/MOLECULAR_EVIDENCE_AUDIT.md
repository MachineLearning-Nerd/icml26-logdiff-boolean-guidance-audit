# Molecular evidence audit

This audit is the independent reporting path for anchored Claim 4. It does not
generate ligands, perform docking, or alter a running campaign. It consumes the
finished artifacts and fails closed on a missing or mismatched protocol field,
target identity, source shard, SHA-256 digest, merged tensor, or docking table.

## Primary-source scope

The protocol is bound to arXiv `2602.05549v2`, Tables 5-6 and Appendix F:

- The primary PDF was text-extracted and Tables 5-6 were visually inspected;
  its SHA-256 is
  `a61cff0113dd03c30c8669114a4f49c9cd296c67f62812fdeb1cf411df507475`.

- GRM5 / P41594 / dataset index 29 is target A.
- RRM1 / P23921 / dataset index 371 is target B.
- Figure 5 visually prints `PP23921`, but Section 4.2 and Appendix F both give
  `P23921`, which is also the recovered dataset identifier. The audit uses the
  repeated body/appendix value and records this figure-label typo explicitly.
- Each experiment generates 32 ligands of 23 atoms with 1,000 denoising steps
  and inverse temperature beta 2.0, then evaluates them with AutoDock Vina.
- The paper reports eight experiments per condition. A finished 32-ligand run
  is one experiment; it is not an eight-experiment replication.
- Table 5 uses the mean paired docking product for `A AND B`.
- Table 6 uses mean `RRM1 - GRM5` docking score for `A AND NOT B`, because A is
  the on-target and B is the off-target.

## Independent checks

`repro/src/audit_molecular_campaign_evidence.py` uses a separate implementation
from the pandas summary path. It:

1. hashes the protocol, runner, merger, docking, summarizer, logical-guidance,
   and molecular-model source files and records both pinned repository commits;
2. verifies the merge manifest and every referenced one-ligand shard hash;
3. loads the merged tensor on CPU and checks its logic, steps, sample count,
   inverse temperature, precision, and reconstruction count;
4. checks every docking row is paired to the exact GRM5/RRM1 indices and
   UniProt IDs and, when present, verifies the restartable docking completion
   manifest and result hash;
5. canonicalizes SMILES before computing validity-and-uniqueness, preventing
   textual aliases from being counted as distinct molecules;
6. recomputes the paired product and directed separation, reports both quality
   denominators, and gives deterministic within-experiment bootstrap intervals;
7. permutes RRM1 scores across ligands as a pairing negative control and swaps
   target labels as a sign-orientation control; and
8. refuses to pool AND and AND-NOT as replicate runs and keeps the full-protocol
   readiness gate closed until seeds 0-7 are complete for both conditions.

## Current checkpoint command

Run from this paper directory:

```bash
.venv/bin/python repro/src/audit_molecular_campaign_evidence.py \
  --campaign logdiff_and=outputs/molecular-recovery/outputs/full-protocol-partial4-logdiff-and \
  --output outputs/molecular-recovery/independent-audit/partial4-logdiff-and.json
```

The executed checkpoint audit validates all four shard hashes and reproduces
the published product `64.53267625`. Its readiness result is correctly false:
the input is 4/32 ligands from seed 0, AND-NOT is absent, and neither condition
has the paper's eight completed experiments.

## Final protocol command

After all sixteen condition/seed roots exist, pass every root explicitly:

```bash
.venv/bin/python repro/src/audit_molecular_campaign_evidence.py \
  --campaign logdiff_and=outputs/molecular-recovery/full-protocol-merged/logdiff_and/run-seed-00 \
  --campaign logdiff_and_not=outputs/molecular-recovery/full-protocol-merged/logdiff_and_not/run-seed-00 \
  --campaign logdiff_and=outputs/molecular-recovery/full-protocol-merged/logdiff_and/run-seed-01 \
  --campaign logdiff_and_not=outputs/molecular-recovery/full-protocol-merged/logdiff_and_not/run-seed-01 \
  --campaign logdiff_and=outputs/molecular-recovery/full-protocol-merged/logdiff_and/run-seed-02 \
  --campaign logdiff_and_not=outputs/molecular-recovery/full-protocol-merged/logdiff_and_not/run-seed-02 \
  --campaign logdiff_and=outputs/molecular-recovery/full-protocol-merged/logdiff_and/run-seed-03 \
  --campaign logdiff_and_not=outputs/molecular-recovery/full-protocol-merged/logdiff_and_not/run-seed-03 \
  --campaign logdiff_and=outputs/molecular-recovery/full-protocol-merged/logdiff_and/run-seed-04 \
  --campaign logdiff_and_not=outputs/molecular-recovery/full-protocol-merged/logdiff_and_not/run-seed-04 \
  --campaign logdiff_and=outputs/molecular-recovery/full-protocol-merged/logdiff_and/run-seed-05 \
  --campaign logdiff_and_not=outputs/molecular-recovery/full-protocol-merged/logdiff_and_not/run-seed-05 \
  --campaign logdiff_and=outputs/molecular-recovery/full-protocol-merged/logdiff_and/run-seed-06 \
  --campaign logdiff_and_not=outputs/molecular-recovery/full-protocol-merged/logdiff_and_not/run-seed-06 \
  --campaign logdiff_and=outputs/molecular-recovery/full-protocol-merged/logdiff_and/run-seed-07 \
  --campaign logdiff_and_not=outputs/molecular-recovery/full-protocol-merged/logdiff_and_not/run-seed-07 \
  --output outputs/molecular-recovery/independent-audit/full-eight-experiment-report.json
```

This is a paper-scale research audit, not an automated test suite.
