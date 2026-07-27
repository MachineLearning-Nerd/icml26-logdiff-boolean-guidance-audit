# Claim 4 evaluator contract

Run the fixed project command:

```text
uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25
```

The command reruns accepted Claims 1, 2, and 5, audits all preserved Claim 4
manifests, invokes an independent standard-library checker, and exits nonzero
on any integrity or negative-control failure.

Expected scientific verdict at this node: `BLOCKED`. Passing means the
incompleteness finding is reproducible, not that the molecular claim passed.
