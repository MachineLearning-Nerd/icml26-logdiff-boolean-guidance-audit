# OAM HF CPU replicate route

## Scope and current state

This route is executing under its frozen contract. Its paid preflight and eight
s00/s01 slices are terminal and independently hash-verified (64/448 ligands).
Four disjoint s02 slices for AND/AND-NOT seeds 1 and 2 are active. It moves only
the fourteen missing molecular generation campaigns to HF `cpu-upgrade`:

- `logdiff_and` and `logdiff_and_not` remain separate;
- run seeds are exactly 1-7;
- seed 0 is rejected by the contract, bootstrap, runner, launcher, and local
  importer;
- every campaign contains 32 ligands at 1,000 denoising steps; and
- each sample seed is `run_seed * 100000 + sample_index`.

The route does not depend on or write through PID 476, PID 40427, CVM, qIO, or
any other local process. Unrelated HF Jobs are read-only observations and are
not launch blockers. The launcher refuses only an active OAM replicate Job with
the same condition and run seed, so it never submits two slices of one campaign
at the same time.

This route terminates at independently verified raw generation. Merge, full
Vina docking, per-experiment summaries, and the final sixteen-root audit remain
separate terminal gates after import. No molecular claim is complete merely
because all HF generation slices succeed.

## Immutable execution units

Each of the fourteen campaigns has four fixed slices:

| Slice | Sample indices | Workers | Internal wall gate | Job timeout | Maximum cost |
|---|---:|---:|---:|---:|---:|
| `s00` | 0-7 | 8 | 5.25 h | 6 h | USD 0.18 |
| `s01` | 8-15 | 8 | 5.25 h | 6 h | USD 0.18 |
| `s02` | 16-23 | 8 | 5.25 h | 6 h | USD 0.18 |
| `s03` | 24-31 | 8 | 5.25 h | 6 h | USD 0.18 |

The exact bucket namespace is:

```text
hf-jobs/oam-replicates-cpu-v1/
  campaigns/<logic>/run-seed-<NN>/
    slice-<slice-id>-samples-<start>-<stop>/contract-<contract-sha256>/
```

Within a slice, a sample's payload is hash-copied first, `FILES.json` is written
atomically, and the sample `SUCCESS.json` is written last. After all eight
samples independently revalidate, `SLICE_MANIFEST.json` is written atomically
and the slice `SUCCESS.json` is written last. A later invocation that sees a
successful namespace verifies it without writing. Partial slices retain atomic
attempt and progress ledgers and can resume under another six-hour invocation.

No concurrently running Job writes a shared progress file. The only shared
artifact is the read-only contract-bound preflight.

## Exact bindings

The route contract is
`repro/configs/oam_hf_cpu_replicates_v1.json`. It binds:

- the 63,049,318-byte scientific input archive and SHA-256
  `a0bbb9678f72cb2239fb1dec62fc8decb8ee0706a97e19e0ec6a59983c7c3958`;
- the input manifest, plan, vendor commits, and three recovered-weight hashes;
- Python 3.12.12, PyTorch 2.9.0 CPU, NumPy 1.26.4, every required package version,
  x86-64, the `cpu-upgrade` flavor, and minimum hardware;
- the exact runner, bootstrap, requirements, and source-manifest hashes; and
- the USD 40 aggregate authorization, USD 0.03/hour verified rate, and slice
  ceilings.

The earlier successful seed-0 timing probe is only a baseline because the new
runner has a different source hash. The new route must first complete its own
contract-bound 20-step preflight. Every slice requires the same stable
environment fingerprint and refuses if the preflight's measured buffered slice
projection exceeds 5.25 hours or USD 0.18.

The existing baseline is 122.218544 seconds for 20 steps. With the same 35
percent buffer it projects:

- 2.2916 job-hours / USD 0.06875 per eight-sample slice;
- 9.1664 job-hours / USD 0.2750 per 32-sample campaign; and
- 128.3295 aggregate job-hours / USD 3.8499 for all fourteen campaigns.

These are estimates. The hard generation reservation is 56 slices x USD 0.18
= USD 10.08, plus USD 0.03 for preflight, or USD 10.11. Docking, setup, transfer,
and retries outside a successful slice are not included in the measured
estimate. All reservations must keep the shared ledger at or below USD 40.

## Guarded commands

These dry-run commands are local and do not submit Jobs:

```bash
bash hf_jobs/launch_oam_replicate_cpu_slice.sh preflight --dry-run
bash hf_jobs/launch_oam_replicate_cpu_slice.sh \
  slice logdiff_and 1 s00 --dry-run
```

An actual submission is forbidden until the shared budget ledger contains the
launcher's exact pending row with state `reserved; not submitted`, flavor
`cpu-upgrade`, and exact cost ceiling. It also requires both literal gates:

```bash
OAM_HF_REPLICATES_AUTHORIZED=1 OAM_HF_BUDGET_RESERVED=1 \
  bash hf_jobs/launch_oam_replicate_cpu_slice.sh preflight
```

The preflight reservation ID is:

```text
pending-oam-replicates-cpu-preflight-v1
```

A slice reservation ID is deterministic. For example:

```text
pending-oam-replicates-logdiff_and-seed01-s00-v1
```

After the preflight completes naturally, independently retrieve and inspect its
`PREFLIGHT.json` and `SUCCESS.json`. Slice launchers also read them before
submission and verify all source hashes, timing, and cost gates. Example:

```bash
OAM_HF_REPLICATES_AUTHORIZED=1 OAM_HF_BUDGET_RESERVED=1 \
  bash hf_jobs/launch_oam_replicate_cpu_slice.sh \
  slice logdiff_and 1 s00
```

The launcher performs two account-wide read-only active-job scans. It ignores
unrelated jobs, but refuses if labels exactly match:

```text
paper=OAM1jJsMGp
campaign=oam-replicates-cpu-v1
logic=<same logic>
run_seed=<same run seed>
```

It also refuses if the exact slice already has a valid terminal `SUCCESS.json`.
It has no cancel, pause, kill, relabel, delete, or local-process path.

## Safe staged order under USD 40

1. Re-read the shared ledger and live HF Job list without modifying either.
   Reserve at most USD 0.03 and run the route preflight. Wait for it to end
   naturally, then verify the persisted report and release unused reservation.
2. Use four-slice waves: `s00`, then `s01`, `s02`, and `s03`. Within a wave,
   condition/seed pairs are disjoint. To preserve capacity for the user's other
   work, submit no more than four OAM slices concurrently even though the exact
   duplicate guard permits one active slice for each of fourteen campaigns.
3. Before every slice, reserve its USD 0.18 ceiling separately and confirm that
   all billed plus committed campaign spending remains at or below USD 40.
   Never reserve the same condition/seed/slice twice.
4. Let every Job terminate naturally. A partial slice has no slice SUCCESS and
   is resumed only after its prior Job is terminal and a new exact reservation
   exists. A successful slice is immutable and must not be rerun.
5. After all 56 successes exist, copy the complete route prefix to a new local
   staging directory. Do not overlay the paper's live seed-0 or canonical
   output roots.
6. Run the content-addressed importer. Only its successful output is eligible
   for merge/docking/audit.

At the full timeout ceiling this route reserves USD 10.11, leaving USD 29.89 of
the USD 40 authorization for already committed and other work. Because the
ledger already contains other commitments, the live ledger value—not USD
29.89 in isolation—is the submission authority.

## Content-addressed import

Download the route so that the staging directory contains
`hf-jobs/oam-replicates-cpu-v1/...`. Preserve the bucket hierarchy. Record the
contract digest locally, then import:

```bash
contract_sha256="$(shasum -a 256 \
  repro/configs/oam_hf_cpu_replicates_v1.json | awk '{print $1}')"

.venv/bin/python repro/hf/import_oam_cpu_replicates_terminal.py \
  --staging-root /path/to/oam-hf-bucket-snapshot \
  --expected-contract-sha256 "${contract_sha256}"
```

The importer requires exactly 56 slice identities and 448 unique raw samples.
It independently loads every `sample.pt` and checks logic, run seed, sample
seed, 1,000-step finite posterior trajectory, precision, compilation mode,
payload hash manifest, SUCCESS-last binding, and stable environment. It rejects
seed 0, incomplete slices, extra or missing condition/seed/slice directories,
multiple contract namespaces, and mixed input/source/environment hashes.

The resulting root is:

```text
outputs/molecular-recovery/hf-cpu-replicates/terminal-imports/<content-address>/
```

It contains fourteen complete local campaign roots under
`campaigns/full-protocol-shards/`. The final content address covers all remote
slice/sample hashes plus every materialized campaign manifest. The importer
does not write the live canonical seed-0 tree and does not publish anything.

## Remaining terminal work

For every imported campaign, run the existing fail-closed merge, restartable
full-Vina docking at exhaustiveness 32, summary, and independent audit against
the content-addressed roots. Conditions must remain separate. Only after all
fourteen imports and the two seed-0 campaigns are provenance-complete should
the existing sixteen-root auditor and challenge-C4 terminal importer run.

Current blockers are therefore:

- 48 of 56 slices and 384 of 448 raw ligands are not yet terminal; four s02
  slices are currently active;
- the all-56-slice terminal staging snapshot does not exist;
- the content-addressed raw-campaign import does not exist; and
- merge, full docking, summaries, and final independent audit remain pending.
