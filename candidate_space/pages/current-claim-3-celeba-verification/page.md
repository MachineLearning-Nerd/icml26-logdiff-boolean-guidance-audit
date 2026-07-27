# Current verification — Claim 3 CelebA

**Verdict: BLOCKED.** The current verifier passes, but the empirical CelebA
claim does not. This page supersedes the historical release-audit page as the
current Claim 3 evidence.

## Exact claim and protocol

The paper states that on CelebA negation, LOGDIFF obtains FID **23.61** versus
**32.87** for the constant-mixing baseline, while AND and OR-CI conformity is
comparable. The domain is restricted to Blond/Non-blond and Male/Female.
Appendix E.2 requires **5,000 samples per task**, specifically 100 images for
each of 50 queries, and **clean-fid** independently per task. See the
[machine-readable claim contract](../../evidence/claim-3/claim_contract.json)
and [source audit](../../evidence/claim-3/source_audit.md).

| Task | Constant CS | Constant FID | LOGDIFF CS | LOGDIFF FID |
| --- | ---: | ---: | ---: | ---: |
| AND | 0.63 | 19.02 | 0.63 | 19.02 |
| NOT | 0.75 | 32.87 | 0.80 | 23.61 |
| OR-CI | 0.93 | 17.11 | 0.97 | 18.47 |

## Managed verification run

Fixed command:

```text
uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25
```

Run `07daf77f-8cf7-48ed-b4f7-55b112d7a223` executed commit
`ac7ad48b7dc4120acbbbbe0468f0cfa76c4591bc` on the local backend. The
pre-run estimate was one CPU worker and under 25 seconds. The host exposed
eight logical CPUs, the implementation used one algorithmic worker, the
verifier runtime was **8.2415 seconds**, and the managed run duration was
**15 seconds**. Python was 3.12.11, NumPy was 2.3.2, and deterministic seeds
0–24 reran the cumulative mathematical regression suite.

The author release was pinned at
`94ef35bafd4b4239e9832d8295128c09e8fc1472`; its 73-file `git archive`
has SHA-256
`d3e7f6a56f665055fd39d54ebdc8c6f0d755e4752877be33a2cdce07be5b4086`.
The raw audit found:

```json
{
  "claim_status": "BLOCKED",
  "empirical_generation_executed": false,
  "missing_checkpoint_paths": 3,
  "missing_composition_dataset_config": true,
  "fid_implementation_mismatch": true,
  "generated_samples_per_task": 5000,
  "reported_samples_argument": 500000,
  "paper_fid_implementation": "clean-fid",
  "release_fid_implementation": "torchmetrics.image.fid.FrechetInceptionDistance",
  "verification_routes_completed": 4,
  "falsification_succeeded": false
}
```

All three required CelebA checkpoints are absent. The composition config
requests `celeba_cs_latents_male_haircolors.yaml`, but only a copy-suffixed
near-match exists. The released evaluator generates 5,000 samples yet reports
500,000 at the default batch size and uses TorchMetrics FID rather than
clean-fid.

## Independent checker and control

The independent standard-library checker returned:

```json
{
  "checker": "independent Claim 3 release-integrity checker",
  "failures": [],
  "scientific_claim_status": "BLOCKED",
  "status": "PASS",
  "verification_routes_rederived": 4
}
```

The negative control adds the three required weights, the exact dataset config,
clean-fid, and correct sample accounting to a synthetic release manifest. The
same audit then returns `READY_TO_RUN`, correctly rejecting a false BLOCKED
verdict.

## Four research routes

| Route | Independent approach | Result |
| ---: | --- | --- |
| 1 | Exact author-release executability | Three checkpoints and one config missing; executable FID differs from the paper |
| 2 | Public author-checkpoint provenance | One official branch, no tags/releases/forks, and no author or exact-filename HF artifacts |
| 3 | Independent public-model reconstruction | A real 114,049,969-byte CelebA Diffusers UNet resolves, but it lacks the paper's diffusion, composition, and judge states |
| 4 | Assumption-satisfying falsification search | Table values match; no exact-method clean-fid image set exists, so no valid counterexample |

Download the complete
[route record](../../evidence/claim-3/verification_routes.json),
[public search summary](../../evidence/claim-3/public_checkpoint_search_summary.json),
[raw author-model search](../../evidence/claim-3/public-checkpoint-search/hf-models-TanjaBien.json),
[raw official-branch response](../../evidence/claim-3/public-checkpoint-search/github-branches.json),
[raw public-model response](../../evidence/claim-3/public-checkpoint-search/hf-public-celeba-model.json),
and
[strict falsification check](../../evidence/claim-3/falsification_check.json).
The public-model resolution is a positive discovery control, not proxy claim
evidence.

Download the [raw release audit](../../evidence/claim-3/release_audit.json),
[negative-control output](../../evidence/claim-3/negative_control.json),
[independent-checker output](../../evidence/claim-3/independent_checker_output.txt),
[complete author tree snapshot](../../evidence/claim-3/author_release_snapshot.json),
and [full cumulative summary](../../evidence/run-07daf77f-summary.json).
Executable sources are
[the cumulative verifier](../../code/run_logdiff.py) and
[the independent Claim 3 checker](../../code/check_claim3_release.py).

## Why this is not a pass or falsification

No author-equivalent images were generated and no clean-fid measurement was
performed. Missing checkpoints and a broken release path do not contradict the
paper's measured result. A direct verdict requires the three author-equivalent
weights or a faithful retraining and generation campaign with clean-fid,
replicates, uncertainty, an independent metric checker, and a corrupted-image
negative control.

## Evaluator visibility

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | This page | Yes | Yes | Yes | PASS | PASS | Yes | BLOCKED |

The earlier [release-audit page](#/claim-3-celeba-release-audit) is retained
unchanged as **Historical rejected baseline**.
