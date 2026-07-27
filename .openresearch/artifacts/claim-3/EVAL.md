# Claim 3 evaluator contract

Run the project-wide fixed command:

```text
uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25
```

The command exits nonzero if the release audit, independent checker, negative
control, or any accepted Claim 1/2/5 regression fails.

Expected scientific verdict at this node: `BLOCKED`. A passing verifier means
the BLOCKED distinction is supported; it does not mean the CelebA claim passed.
