- Previous live judged score: `6/10`
- Conservative projected score range after the proposed change: **6/10**
- Best-supported possible new score: **6/10 (forecast, not a judge result)**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 2 | 2 | HIGH | VERIFIED | Exhaustive finite-domain certificate, independent full-joint oracle, and assumption-violation controls pass. |
| 2 | 2 | 2 | HIGH | FALSIFIED | All 16 Table 2 cells contradict the literal aggregate ranges; independent recomputation and a range-conforming control pass. |
| 3 | 0 | 2 | LOW | BLOCKED | Four distinct routes completed; three author-equivalent checkpoints and the exact clean-fid path remain unavailable. |
| 4 | 0 | 2 | LOW | BLOCKED | Four distinct routes completed; no complete paired LoGDiff/DualDiff campaign or docking output exists in the recovered evidence. |
| 5 | 2 | 2 | HIGH | VERIFIED | Both constructive cases are exhausted over 27,000 finite events; the invalid-overlap control is rejected. |

## Score and changes

The current live total is **6/10**. The conservative projected total is
**6/10**, and the best-supported possible total is **6/10**. These are
forecasts only; only the live evaluator can alter the score.

Claims 1, 2, and 5 retain their prior full-credit verdicts. Claims 3 and 4 have
changed from an evaluator-visible inconclusive state to rigorously documented
`BLOCKED` contracts after four verification-oriented routes apiece. Their
point forecast does not change.

Claim 3 is blocked by unavailable author-equivalent CelebA model/classifier
checkpoints and an unreconstructable paper metric path. Claim 4 is blocked by
the absence of complete paired campaigns and docking outputs. Neither a public
proxy checkpoint nor partial molecular payloads are treated as faithful
evidence.

## Evaluator visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Current cumulative verification | Yes | Yes | Yes | PASS | PASS | Yes | VERIFIED |
| 2 | Current cumulative verification | Yes | Yes | Yes | PASS | PASS | Yes | FALSIFIED |
| 3 | Current CelebA verification | Yes | Yes | Yes | PASS | PASS | Yes | BLOCKED |
| 4 | Current molecular verification | Yes | Yes | Yes | PASS | PASS | Yes | BLOCKED |
| 5 | Current cumulative verification | Yes | Yes | Yes | PASS | PASS | Yes | VERIFIED |

All rows are reachable by traversing links from the candidate Space README and
`pages/index.md`. The evaluator-blind audit does not use repository knowledge
to fill a cell.

## Experiment tree

The stacked lineage is:

```text
Frozen cumulative baseline
├── CelebA exact audit → CelebA evaluator-visible evidence
└── Molecular evidence audit → Molecular evaluator-visible evidence
    └── Cumulative release candidate
        └── Evaluator-visible artifact
            └── CSV-aware release audit
                └── Publication surface and illustrated report
```

Every node inherits this fixed command:

```text
uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25
```

The winning scientific branch before presentation work is
`orx/csv-aware-evaluator-release-audit` at Git
`1d37e8b…`. Its managed local run completed in 15 seconds, used one
algorithmic CPU worker, and incurred no paid compute cost. The final
publication surface is
`orx/publication-surface-and-illustrated-report@13569ed474f2872b5827e57f4c7fbf791be4119c`.
Its cumulative run completed in 10 seconds managed wall time (4.1231 seconds
inside the verifier), exposed 8 logical host CPUs, and used one algorithmic
worker. No GPU, Hugging Face job, or paid compute was used.

## Release gates and publication action

The candidate must pass all cumulative scientific checkers, JSON and link
validation, historical-file subset and hash checks, visibility-matrix checks,
text-only allowlist generation, secret scanning, and evaluator-blind traversal
from the canonical README. The judged Space revision
`1fd04429cb112e90be5fa2bb7a19b827667922bf` remains immutable evidence.

The latest audited candidate contains 353 files; all 23 judged paths are
present, and the historical pages are byte-identical. The evaluator-blind
review opened 78 reachable files, left no conclusion unverified, checked 288
JSON files, found no broken links or secret hits, and produced an exact
333-path text-only upload allowlist plus a SHA-256 manifest.

After the metadata-only final gate run passes, the exact publication action is: upload only
the SHA-256-manifested text allowlist to the existing Hugging Face Space
`DineshAI/OAM1jJsMGp` through the Hugging Face commit API, verify the returned
revision, download that exact revision and repeat the traversal/hash audit,
then fast-forward GitHub `main` to the tested publication commit and confirm
the remote SHA. No second Space will be created.

The exact pre-publication commands are preserved in the
[campaign command ledger](command-ledger.md). The published Hugging Face
revision and post-publication hash verification are recorded only after the
API returns the immutable revision.
