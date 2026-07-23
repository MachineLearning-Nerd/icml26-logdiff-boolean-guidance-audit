# Challenge C4 terminal handoff

## Exact claim and score mapping

The live official verdict still scores this paper **6/10** at current and judged
Space revision `1fd04429cb112e90be5fa2bb7a19b827667922bf`:

- Claim 1 verified: 2 points.
- Claim 2 falsified: 2 points.
- Claim 3 inconclusive: 0 points.
- Claim 4 inconclusive: 0 points.
- Claim 5 verified: 2 points.

Challenge Claim 4 is:

> On dual-target GRM5-RRM1 molecular generation, LOGDIFF achieves an average
> docking score of 73.20±3.18 under an AND query versus 71.87±3.33 for the
> DualDiff baseline, and 0.94±0.24 target separation versus 0.28±0.08 for
> DualDiff under an AND-NOT query (Table 5, Table 6).

The current judge feedback is exact: only 4/32 AND ligands had been published,
their mean product was 64.53, and AND-NOT had not started. Completing seed 0
fixes those two immediate omissions but is still only one of the paper's eight
experiments per condition. It is not a paper-level mean/std replication.

## Historical protected live-chain snapshot

Read-only snapshot at `2026-07-20T16:47:21+0530`:

- PID 476 exactly matches the seed-0 `logdiff_and`, 32-ligand, four-worker,
  1,000-step controller. It has completed 24/32 success-marked shards, indices
  0-23. All four newest completed shards, 20-23, passed on attempt 1 with valid
  reconstructions and finite full trajectories.
- Four PID-476 children are actively generating shards 24-27. Each owns a
  separate output directory and was using approximately 75-96 percent CPU at
  inspection.
- PID 40427 exactly matches the persistent postprocess queue. It has no child,
  remains `waiting`, and its progress ledger most recently matched PID 476's
  exact command. All nine postprocess phases remain pending with zero attempts.
- Neither PID was signalled, stopped, reprioritized, or written through.

Based on the most recent completed four-shard wave (about 6,070-6,089 seconds
per shard), the remaining two AND waves are roughly 3-5 hours if throughput
holds and no retry is needed. The subsequent independent 32-ligand AND-NOT
generation is roughly another 14-20 hours at the same four-worker throughput.
Merging is short; full Vina docking, retries, and machine contention make a
defensible end-to-end seed-0-chain estimate approximately **18-30 hours**.
This is a projection, not a completion guarantee.

## Final-only terminal gate

The prepared terminal route intentionally rejects seed-0-only evidence. It
requires the existing independent auditor to report all of the following:

- both `logdiff_and` and `logdiff_and_not`;
- run seeds 0-7 for each condition;
- exactly eight provenance-complete experiments per condition;
- 32 ligands and 1,000 steps per experiment;
- full Vina docking with exhaustiveness 32;
- all raw-shard, merged-sample, results-table, target, source, and protocol
  hashes valid;
- condition pooling forbidden; and
- `full_protocol_readiness.ready == true` with no blockers.

The content-addressed importer reruns the independent auditor and requires
byte-for-byte equality with the operator-supplied audit digest. It exposes only
manifest-bound JSON/CSV evidence; `sample.pt` payloads are validated by the
auditor but are not copied into the public evidence tree.

## HF `cpu-upgrade` seeds 1-7 concurrency audit

The fourteen missing condition/seed campaigns are scientifically disjoint from
PID 476, PID 40427, and the CVM/qIO processes. Each sample seed is
`run_seed * 100000 + sample_index`; each campaign has an exclusive
`<logic>/run-seed-<NN>` shard, merge, docking, report, and audit namespace; and
the final auditor is the first consumer that combines the sixteen completed
campaigns. Consequently, guarded HF Jobs for seeds 1-7 do **not** need to wait
for the local seed-0 chain or unrelated local PIDs.

The separate fail-closed HF `cpu-upgrade` route has passed its contract-bound
paid preflight. Eight s00/s01 slices are terminal and hash-verified (64/448
seed-1--7 ligands), while four disjoint s02 slices for both conditions at seeds
1 and 2 are active. Do not point the seed-0 driver at another seed or submit the
local continuation queue remotely.

A safe HF route now implements the following static gates before any
submission:

- a parameterized CPU driver restricted to logic in
  `{logdiff_and, logdiff_and_not}` and run seed in `1..7`, rejecting seed 0;
- one exclusive bucket prefix per condition/seed, with scratch validation,
  hash-copy of payloads, `SUCCESS.json` written last, resumable attempt ledgers,
  and no shared progress file written by concurrent jobs;
- the passed exact CPU environment/input preflight rebound to the parameterized
  driver, plus a per-campaign 20-step compatibility/timing probe if source or
  package hashes differ;
- an idempotent launcher that detects only duplicate OAM condition/seed jobs,
  preserves unrelated HF jobs, rechecks account state immediately before
  submission, and never cancels or relabels anything;
- a distinct shared-ledger reservation, timeout, and maximum cost for every
  submitted campaign or resumable slice; and
- a hash-manifested local importer that rejects seed 0, wrong identities,
  partial campaigns, mixed conditions, or evidence not bound to the exact
  source/input/environment ledger.

The measured CPU preflight used `122.218544` seconds for 20 steps. Applying its
existing 35 percent buffer and eight-worker topology projects approximately
`9.1664` job-hours / `USD 0.2750` for one fresh 32-ligand generation campaign,
or `128.3295` aggregate job-hours / `USD 3.8499` for all fourteen, before
docking, environment setup, retries, and transfer overhead. A six-hour job
ceiling therefore requires resumable slices rather than assuming one
invocation completes a campaign. These are budget projections, not runtime
guarantees.

At the read-only `2026-07-20T17:00+0530` account check, four unrelated
`cpu-upgrade` Jobs and one unrelated `t4-small` Job were RUNNING. None was
modified. The existing seed-0 launcher intentionally defers while any
`cpu-upgrade` Job is active; a future concurrent-replicate launcher must replace
that account-wide exclusion with exact duplicate condition/seed detection while
retaining a budget/concurrency-cap preflight.

## Deferred operator sequence

1. Preserve the completed seed-0 roots. Both conditions, merges, full Vina
   docking, separate summaries, and the combined summary are complete and
   independently accepted as provenance-complete single experiments.

2. Complete and independently verify/install seeds 1-7 from the already
   prepared CUDA handoff, or from a separately reviewed guarded HF CPU route
   satisfying the concurrency audit above. Do not mix condition roots and do
   not overwrite seed 0.

3. Run the final 16-root command already listed in
   `docs/MOLECULAR_EVIDENCE_AUDIT.md`, writing:

   ```text
   outputs/molecular-recovery/independent-audit/full-eight-experiment-report.json
   ```

4. Preserve its SHA-256 separately, then create the terminal import:

   ```bash
   .venv/bin/python repro/hf/import_oam_c4_terminal.py \
     --audit-report outputs/molecular-recovery/independent-audit/full-eight-experiment-report.json \
     --expected-audit-sha256 <printed-64-character-sha256>
   ```

5. Refetch the existing Space's current 40-character commit and prepare an
   additive exact-parent update:

   ```bash
   uv run --with huggingface_hub==1.24.0 repro/hf/repair_existing_space_c4.py \
     --prepare \
     --import-dir outputs/molecular-recovery/terminal-imports/c4/<audit-sha256> \
     --expected-parent <fresh-40-character-space-commit>
   ```

6. Inspect the staging manifest and all rendered payloads. Apply is a separate
   action requiring literal root approval
   `root-approved-existing-oam-c4-terminal-update`. The apply path uses only
   `CommitOperationAdd` against `DineshAI/OAM1jJsMGp` with the exact parent. It
   has no repository creation, deletion, move, hardware, job, or process path.

## Scientific claim boundary

Full completion supplies direct reconstructed-protocol evidence for Tables 5
and 6, but it does not force a verified verdict. The terminal page reports the
reproduced across-experiment means and sample standard deviations exactly,
whether supportive, negative, or mixed.

LOGDIFF did not release the molecular composition implementation, so this path
remains a paper-derived reconstruction. Seed 0 may run on local CPU while seeds
1-7 may run on Colab CUDA; that is protocol-complete but not hardware-homogeneous
or bitwise-parity evidence. These limitations are frozen into the terminal
contract and Space repair.

## Remaining blockers

- Seed 0 is complete for both conditions, but is only one of eight required
  experiments per condition. Its AND product is `59.57176296875`; its AND-NOT
  directed separation is `0.6097096774193547` over 31 valid-unique ligands,
  with sample 19 recorded as a disconnected-fragment rejection.
- Seeds 1-7 for both conditions have not been fully returned and installed.
  Eight of 56 slices (64/448 ligands) are terminal and four s02 slices are
  active. See `docs/OAM_HF_CPU_REPLICATES.md`.
- The final 16-root independent audit and its terminal digest do not exist.
- Claim 3 remains independently unresolved even if Claim 4 becomes defensible.
- No terminal publication is eligible while the full generation/import/docking
  gate remains incomplete.
