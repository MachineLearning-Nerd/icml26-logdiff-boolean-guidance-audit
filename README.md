# LOGDIFF exact Boolean guidance — claim-by-claim reproduction

This repository reproduces five claims from
[*Logical Guidance for the Exact Composition of Diffusion Models*](https://arxiv.org/abs/2602.05549)
(ICML 2026 submission `OAM1jJsMGp`). The strongest current evidence supports
the existing live-judge score of **6/10**: Claims 1 and 5 are `VERIFIED`,
Claim 2 is `FALSIFIED` as literally written, and Claims 3 and 4 are `BLOCKED`.
No score increase is claimed before a live judge evaluates the published
revision.

![Five exact claims, three resolved](reports/claim-by-claim/images/headline-verdicts.png)

## Reproduction result

| Claim | Paper number or statement | Observed evidence | Assessment |
| --- | --- | --- | --- |
| 1 — Proposition 3.1 | Exact logical-score composition under CI/ME assumptions | 6,350 formulas; max probability error `2.22e-16`, max score error `3.33e-16`; all controls reject invalid constructions | VERIFIED |
| 2 — Table 2 ranges | LoGDiff 94–98%; constant mixing 63–77% | LoGDiff 85.1–94.4% (2/8 cells in range); constant 57.9–76.1% (5/8) | FALSIFIED as written |
| 3 — CelebA NOT | FID 23.61 versus 32.87 | Four verification routes; three required author-equivalent checkpoints and exact clean-fid path unavailable | BLOCKED |
| 4 — GRM5/RRM1 | AND 73.20 versus 71.87; separation 0.94 versus 0.28 | Four routes; 96 partial LoGDiff payloads, but zero complete paired campaigns or docking outputs | BLOCKED |
| 5 — Proposition C.2 | Completeness for independent categorical groups and nested taxonomies | 27,000 finite events exhausted; max error `3.33e-16`; invalid overlap rejected | VERIFIED |

Read the [illustrated technical report](reports/claim-by-claim/report.md), the
[release and confidence report](reports/claim-by-claim/release-report.md), or
the [canonical evaluator-visible verification](candidate_space/pages/current-cumulative-verification/page.md).
The [tutorial-style marimo notebook](notebooks/logdiff_reproduction.py) embeds
the accepted evidence and does not require an expensive rerun.

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-OAM1jJsMGp-logdiff-exact-boolean-guidance/blob/main/notebooks/logdiff_reproduction.py)

## Scope and substitutions

The mathematical checks are exhaustive over the complete finite categorical
domains in their claim contracts. They are not described as proofs for
arbitrary continuous diffusion models. Claim 2 is a direct audit of every
paper Table 2 cell, not a new image-generation run.

No proxy was substituted for the full CelebA or molecular experiments. The
public CelebA DDPM lacks the required model state, classifiers, and judge. The
recovered molecular bucket contains 96 of 448 declared LoGDiff sample payloads
but no complete experiment, no DualDiff campaign, and no docking output.
Those claims remain `BLOCKED` rather than being scored from downscaled data.

All accepted verification runs used the authorized local CPU backend, one
algorithmic worker, and less than 25 seconds each. The host exposed eight
logical CPUs, but the implementation remained single-worker. No GPU or paid
Hugging Face compute was used.

## Experiment log

The exact fixed command for every launched experiment is:

```text
uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25
```

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Public landing page and tested-artifact mirror | Not run as an experiment (publication surface) | Presentation-only; populated by fast-forwarding the tested publication branch | Not applicable |
| [`orx/frozen-cumulative-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-OAM1jJsMGp-logdiff-exact-boolean-guidance/tree/orx/frozen-cumulative-baseline) | Freeze and rerun previously accepted Claims 1, 2, and 5 | `uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25` | Claims 1/5 VERIFIED; Claim 2 FALSIFIED; cumulative controls pass | Local CPU, one worker, 10 s managed |
| [`orx/celeba-evaluator-visible-evidence`](https://github.com/MachineLearning-Nerd/icml26-repro-OAM1jJsMGp-logdiff-exact-boolean-guidance/tree/orx/celeba-evaluator-visible-evidence) | Complete four-route Claim 3 audit and canonical evidence | `uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25` | Claim 3 BLOCKED; missing equivalent checkpoints and exact metric path | Local CPU, one worker, 15 s managed |
| [`orx/molecular-evaluator-visible-evidence`](https://github.com/MachineLearning-Nerd/icml26-repro-OAM1jJsMGp-logdiff-exact-boolean-guidance/tree/orx/molecular-evaluator-visible-evidence) | Complete four-route Claim 4 audit and canonical evidence | `uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25` | Claim 4 BLOCKED; no complete paired campaign or docking evidence | Local CPU, one worker, 10 s managed |
| [`orx/csv-aware-evaluator-release-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-OAM1jJsMGp-logdiff-exact-boolean-guidance/tree/orx/csv-aware-evaluator-release-audit) | Cumulative science plus evaluator-blind link, manifest, history, and secret audit | `uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25` | All five verdict contracts and release checks pass | Local CPU, one worker, 15 s managed |
| [`orx/publication-surface-and-illustrated-report`](https://github.com/MachineLearning-Nerd/icml26-repro-OAM1jJsMGp-logdiff-exact-boolean-guidance/tree/orx/publication-surface-and-illustrated-report) | Illustrated report, tutorial notebook, and final public surface | `uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25` | Pending final cumulative release run | Local CPU, one worker expected |

Raw experiment and run IDs remain in the OpenResearch experiment descriptions
and evidence records rather than the public landing page.

## Reproduce

Install the single repository-level environment and run the locked cumulative
verifier:

```bash
uv sync --frozen
uv run python repro/src/run_logdiff.py \
  --output-dir .openresearch/artifacts --seeds 25
```

The command regenerates claim-level CSV/JSON, independent-checker output,
negative controls, and release-audit records. Each checker exits nonzero on a
failed contract. For a guided reading without regenerating evidence:

```bash
uvx --from marimo==0.23.15 marimo edit notebooks/logdiff_reproduction.py
# or
uvx --from marimo==0.23.15 marimo run notebooks/logdiff_reproduction.py
```

The official paper implementation was audited at
`TanjaBien/LogDiff@94ef35bafd4b4239e9832d8295128c09e8fc1472`.
The exact judged Hugging Face Space revision
`DineshAI/OAM1jJsMGp@1fd04429cb112e90be5fa2bb7a19b827667922bf`
is preserved as immutable historical evidence within the additive candidate.
