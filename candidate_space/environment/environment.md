# Pinned environment and command

- Python requirement: exactly 3.12.x
- Resolver and runner: `uv`
- Lockfile: `uv.lock`
- Scientific dependency: `numpy==2.3.2`
- Fixed command: `uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25`
- Baseline compute estimate: one CPU core, under five minutes
- Baseline backend policy: local, supervised through `orx exp run`

The run log records the branch Git SHA, actual visible CPU allocation, Python
and NumPy versions, deterministic seed list, and wall-clock runtime.
