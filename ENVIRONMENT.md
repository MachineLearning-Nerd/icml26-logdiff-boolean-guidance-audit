# Environment and reproduction boundary

## Locked project environment

- Python: exactly 3.12.x
- Resolver: uv
- Scientific dependency: numpy 2.3.2
- Development test dependency: pytest 8.4.1
- Lockfiles: pyproject.toml and uv.lock
- Fixed command:
  uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25

The tracked candidate-space environment record and lockfile are also under
candidate_space/environment/. The command must be run from the repository
root because the evaluator-blind candidate audit resolves candidate_space/
relative to the working directory.

## Published evidence run

The strongest complete cumulative run stored in the public evidence is bound
to Git commit ac7ad48b7dc4120acbbbbe0468f0cfa76c4591bc and records:

- Python 3.12.11
- NumPy 2.3.2
- macOS ARM 64-bit
- eight visible logical CPUs
- one algorithmic worker
- seeds 0 through 24
- runtime 8.241534708009567 seconds
- no GPU or paid Hugging Face compute
- independent checker status PASS

The run summary is
.openresearch/artifacts/run-07daf77f-summary.json. Its exact hash and the
hashes of the claim-level artifacts are in EVIDENCE_MANIFEST.json.

## What a passing run means

A pass certifies the finite calculations, table-range decision, release
integrity predicates, historical manifest completeness decision, negative
controls, and evaluator-visible file audit. It does not create missing model
weights, reconstruct a missing molecular repository, or turn partial payloads
into complete experiments.

For a new run, copy .openresearch/artifacts to a separate temporary directory
and pass that directory with --output-dir. This keeps the published
hash-bound snapshot unchanged while allowing the verifier to read its C3/C4
input contracts.

## Reproducibility limits

- C1 and C5 use finite smooth categorical certificates rather than trained
  diffusion networks.
- C2 is a direct primary-table audit and requires no image generation.
- C3 cannot execute the paper-equivalent CelebA campaign without the missing
  checkpoints, dataset config, and clean-fid path.
- C4 cannot execute the paper-equivalent molecular comparison without complete
  LOGDIFF and DualDiff campaigns, docking outputs, and the missing hash-bound
  inputs.
- The recorded external judge and OpenResearch/Hugging Face runtime notes are
  historical provenance; they are not assumed to be live or reproducible from
  this GitHub checkout alone.
