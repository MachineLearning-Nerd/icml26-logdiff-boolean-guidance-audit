# Molecular replicate continuation (seeds 1--7)

The paper reports eight 32-ligand experiments per logical condition.  The live
OAM chain owns seed 0; this continuation covers exactly seeds 1--7 for
`logdiff_and` and `logdiff_and_not` (14 independent campaigns).  It is prepared
but has not been launched.

## Artifacts

- `outputs/molecular-recovery/replicate-continuation/PLAN.json` is the
  deterministic queued-command manifest.
- `outputs/molecular-recovery/replicate-continuation/DRY_RUN.json` is the latest
  non-launching static and coordination audit.
- `repro/src/build_molecular_replicate_continuation_plan.py` rebuilds the plan
  from live source, protocol, vendor-commit, and recovered-weight identities.
- `repro/src/run_molecular_replicate_continuation_queue.py` validates the plan,
  defaults to dry-run mode, and requires `--execute` before it can launch work.

The plan binds arXiv `2602.05549v2`, the primary PDF hash, the exact LogDiff and
recovered-FKC commits, all scientific/orchestration source hashes, and all three
recovered model hashes.  Any drift rejects the plan instead of silently
continuing.

## Coordination gate

All of these exact identities must be released before launch:

| PID | Required command marker | Owner |
|---:|---|---|
| 476 | `run_parallel_molecular_protocol.py` | OAM seed-0 AND generation |
| 40427 | `run_molecular_postprocess_queue.py` | OAM seed-0 postprocess queue |
| 41276 | `run_full_matrix_queue.py` | CVM downstream queue |
| 41861 | `run_full_agent_probe_queue.py` | qIO downstream queue |

Waiting only on PID 41861 is unsafe: that tail can fail before an upstream job,
which would create process competition.  The queue therefore also scans every
current-user process for the queue markers plus the molecular sampler and
docking child-command markers; macOS system processes run under other UIDs and
are not workspace competitors.  A current-user
process-inspection error remains blocked.  A heavy phase is eligible only when all exact identities are
released, the global marker scan is empty, source identities still match, and
at least 4 GiB of memory is available.  The queue never signals, kills, times
out, or reprioritizes a process.

The current dry run is deliberately `blocked_no_launch`: the four exact jobs
are still present and the memory gate was below 4 GiB when inspected.

## Seed-0 preservation and failure behavior

The plan treats both seed-0 shard roots, both seed-0 merged roots, and the
existing seed-0 report area as protected read-only paths.  Static validation
extracts each command's write targets and rejects a target inside these paths.
Final aggregation may read seed 0 but cannot write there.

Each of the 14 campaigns owns different shard, merge, docking, report, and audit
paths.  Generation, merge, docking, reporting, and independent audit are
restartable.  A failed dependency blocks only its dependent phases; another
seed/condition continues.  The runner's ten operational retries per sample or
docking task are retries, not ten materially different approaches.

The plan contains an explicit ten-approach registry.  Only approach 1 (the
primary recovered-FKC CPU, compiled, sharded protocol) is automatic.  A failure
records approach 2 as the next escalation and leaves `unable_permitted=false`.
Approaches 2--5 are alternate execution topologies/backends that preserve the
primary protocol; approaches 6--10 are clearly labeled sensitivity,
triangulation, independent-rescoring, or source/equation falsification routes.
The campaign cannot report “unable” until evidence exists for all ten.

## Non-launching audit and later launch

Rebuild the deterministic plan and rerun the dry audit with:

```bash
.venv/bin/python repro/src/build_molecular_replicate_continuation_plan.py
.venv/bin/python repro/src/run_molecular_replicate_continuation_queue.py
```

These commands do not launch molecular generation.  After the main agent has
verified that the full OAM-to-CVM-to-qIO chain is gone and accepts the resource
gate, the explicit queued launch command is:

```bash
.venv/bin/python repro/src/run_molecular_replicate_continuation_queue.py --execute
```

No test suite is part of this research execution.  Integrity is established by
AST/static validation, cryptographic hashes, artifact-specific validators, and
the independent evidence auditor.  After all 14 continuations complete, the
final phases read all 16 condition/seed roots, keep AND and AND-NOT separate,
and require eight provenance-complete experiments with seeds 0--7 per
condition before readiness can become true.
