# OAM seed-0 migration to HF cpu-upgrade

## Status

This is a prepared, fail-closed migration for the active `logdiff_and`, seed-0
32-ligand molecular campaign. It has not been launched. No local process and no
Hugging Face Job was stopped, signalled, paused, cancelled, relabelled, or
otherwise modified while preparing it.

At `2026-07-20T08:04:29Z`, the durable local boundary was 16/32 samples. Samples
16--19 were active at steps 445--448 of 1000. A molecular sample has no
mid-trajectory checkpoint, so only a validated `sample.pt` plus its last-written
`SUCCESS.json` is transferable. The current recoverable set is samples 0--15;
an explicitly stopped in-flight sample is deterministically rerun from its
fixed sample seed.

The safe operational order is:

1. Let the guarded HF preflight pass while the local campaign remains intact.
2. Root explicitly authorizes cutover and stops the local controller using a
   separately reviewed action. These migration scripts never stop it.
3. Confirm the controller and every seed-0 `compose_sample_score.py` child are
   absent.
4. Run the cutover stager. It includes only hash-valid, success-marked samples.
5. Reserve the full six-hour USD 0.18 ceiling in the shared ledger.
6. Launch the guarded full continuation. It restores the cutover plus any prior
   HF checkpoints, revalidates tensors and protocol fields, and schedules only
   missing indices.

## Frozen inputs and runtime

- Scientific input archive: 63,049,318 bytes; SHA-256
  `a0bbb9678f72cb2239fb1dec62fc8decb8ee0706a97e19e0ec6a59983c7c3958`.
- Archive inventory: 91 exact source, configuration, target-data, aligned-pocket,
  and recovered-weight files.
- Recovered weights: 63,734,295 bytes total, with three hard-coded SHA-256
  identities checked again by the remote driver.
- Current 16-sample checkpoint payload: about 26.8 MB before gzip. The actual
  cutover size is recorded after local processes are absent.
- Persistence: existing canonical bucket `DineshAI/OAM1jJsMGp-artifacts`, prefix
  `hf-jobs/seed0-cpu-migration-v1/`. Each sample payload is hash-copied first and
  `SUCCESS.json` is written last; progress and final reports are separate.
- Hardware: authorized `cpu-upgrade`, 8 vCPU / 32 GB RAM / 50 GB storage at
  USD 0.03/hour.
- Runtime: Python 3.12, `torch==2.9.0+cpu`, `numpy==1.26.4`, PyG 2.6.1,
  CPU wheels for torch-scatter 2.1.2 and torch-cluster 1.6.3, plus pinned RDKit,
  Vina, Meeko, OpenBabel, W&B, EasyDict, pandas, PyYAML, psutil, SciPy,
  scikit-learn, and tqdm.

## Resumption and failure semantics

The full driver uses eight single-threaded workers. Before reusing a sample it
loads `sample.pt` on CPU and verifies the exact logic, seed, 1000 steps, FP32,
inverse temperature, resampling setting, posterior count, finite trajectory,
reconstruction, and SHA-256. Missing or invalid samples are rerun from their
fixed seed. Each sample is allowed up to ten attempts across invocations;
failure of one index does not prevent independent indices from running.

Work is submitted in cohorts of at most eight. A completed sample is persisted
immediately. The driver stops scheduling new cohorts after its internal 5.25-hour
wall budget and leaves a resumable partial state rather than intentionally
interrupting an active sample. The outer HF timeout is six hours.

## Time and cost estimate

The latest completed local cohort averaged about 5,044 seconds per sample, and
the active cohort was projecting a similar 84-minute duration. With 16 samples
left, the local four-worker controller projects roughly 4.9--5.5 additional
hours from the observation above. An eight-worker HF continuation requires two
cohorts: the conservative preflight estimator uses at least 5.1 seconds per
step and a 35% buffer, yielding about 3.83 hours and USD 0.115 for the full
continuation. The enforced ceiling is six hours / USD 0.18. The separate
one-hour preflight ceiling is USD 0.03; its measured report replaces this
projection before cutover.

## Launch gates

Dry-run only:

```bash
bash hf_jobs/launch_oam_seed0_cpu_upgrade.sh preflight --dry-run
bash hf_jobs/launch_oam_seed0_cpu_upgrade.sh full --dry-run
```

Actual preflight requires a prior shared-ledger reservation:

```bash
OAM_HF_BUDGET_RESERVED=1 \
  bash hf_jobs/launch_oam_seed0_cpu_upgrade.sh preflight
```

After preflight passes and root separately authorizes/stops the local campaign,
stage the immutable cutover:

```bash
python3 repro/hf/stage_oam_seed0_cutover.py --authorize-cutover
```

Actual full launch additionally requires explicit cutover authorization:

```bash
OAM_HF_BUDGET_RESERVED=1 OAM_HF_CUTOVER_AUTHORIZED=1 \
  bash hf_jobs/launch_oam_seed0_cpu_upgrade.sh full
```

Both launch paths inspect all account-wide `RUNNING` and `SCHEDULING` Jobs at
the beginning and immediately before submission. Any active `cpu-upgrade` Job,
including an unknown or external Job, causes a defer without modifying it.

## Remaining risks

- Linux x86 CPU kernels may not be bitwise identical to the completed macOS ARM
  samples. The seed protocol is unchanged, but the final seed-0 campaign must
  record this hardware-heterogeneous boundary.
- The pinned PyTorch/PyG CPU wheels and the recovered model have not yet been
  exercised on HF; the paid preflight exists specifically to close that gate.
- Bucket mounts can fail before container start. Such an infrastructure failure
  produces no scientific work; retry only after account and ledger checks.
- The HF API does not provide an atomic account-wide flavor reservation. A local
  advisory lock plus a final backend read narrows, but cannot eliminate, a race
  with another system submitting at the same instant.
