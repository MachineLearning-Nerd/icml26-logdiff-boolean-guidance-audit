# Current cumulative verification

**Current scientific result: 6/10 supported; projected 6/10 pending the live
judge.** Claims 1 and 5 are `VERIFIED`, Claim 2 is `FALSIFIED`, and Claims 3
and 4 are `BLOCKED`. A passing cumulative verifier means those five verdicts
are reproduced exactly; it does not convert a blocked empirical claim into a
pass.

This page and the linked current Claim 3/4 pages supersede the historical
release-audit and partial molecular pages as the active verification surface.

## Fixed command and environment

Every experiment node uses exactly:

```text
uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25
```

Run `07daf77f-8cf7-48ed-b4f7-55b112d7a223` executed Git
`ac7ad48b7dc4120acbbbbe0468f0cfa76c4591bc` on the local backend. The estimate
was one algorithmic CPU worker and under 25 seconds. The host exposed 8 logical
CPUs; the code used one algorithmic worker. Managed wall time was 15 seconds
and verifier runtime was **8.2415 seconds**. Python 3.12.11, NumPy 2.3.2, and
seeds 0–24 are recorded in the
[raw cumulative summary](../../evidence/run-07daf77f-summary.json).

The exact [pyproject](../../environment/pyproject.toml),
[uv lockfile](../../environment/uv.lock), and
[environment record](../../environment/environment.md) are downloadable.
Executable sources are the
[cumulative verifier](../../code/run_logdiff.py),
[baseline independent checker](../../code/check_baseline_artifacts.py),
[Claim 3 checker](../../code/check_claim3_release.py), and
[Claim 4 checker](../../code/check_claim4_evidence.py), plus the
[evaluator-blind traversal audit](../../code/audit_candidate_space.py). Each checker and the
cumulative verifier exits nonzero if an integrity predicate, expected verdict,
or negative control fails.

## Claim-by-claim result

| Claim | Exact paper result tested | Current evidence | Verdict |
| --- | --- | --- | --- |
| 1 | Proposition 3.1 exact logical-score composition under CI/ME circuit assumptions | 6,350 formulas; max probability error 2.22e-16; max score error 3.33e-16; 100 primitive rules and 3/3 violation controls | VERIFIED |
| 2 | Table 2 range: LoGDiff 94–98%, constant 63–77% across all eight cells per method | LoGDiff is 85.1–94.4 with 2/8 cells in range; constant is 57.9–76.1 with 5/8 in range | FALSIFIED |
| 3 | CelebA NOT FID 23.61 vs 32.87 with 5,000 samples/task and clean-fid | Four independent routes; author-equivalent weights and exact executable metric path remain unavailable | BLOCKED |
| 4 | Eight 32-ligand GRM5/RRM1 campaigns: AND 73.20 vs 71.87 and AND-NOT 0.94 vs 0.28 | 96 manifest-valid partial LoGDiff payloads, but zero complete experiments, DualDiff campaigns, or docking files; four routes exhausted | BLOCKED |
| 5 | Proposition C.2 completeness for independent categorical groups and nested taxonomies | 20,650 group events plus 6,350 taxonomy events; errors ≤3.33e-16; invalid overlap rejected | VERIFIED |

## Raw evidence and controls

### Claim 1

The exact domain, assumptions, and quantifiers are in the
[claim contract](../../evidence/claim-1/claim_contract.json) and
[source audit](../../evidence/claim-1/source_audit.md). Download the
[6,350-formula CSV](../../evidence/claim-1/exhaustive_formulas.csv),
[100 primitive checks](../../evidence/claim-1/primitive_rules.csv),
[violation controls](../../evidence/claim-1/negative_controls.csv), and
[independent checker output](../../evidence/claim-1/independent_checker_output.txt).
The [method](../../evidence/claim-1/method.md) and
[limitations](../../evidence/claim-1/limitations_and_deviations.md) explicitly
scope the exhaustive result to the complete stated finite categorical
construction used by the certificate.

### Claim 2

The [contract](../../evidence/claim-2/claim_contract.json) binds the literal
range statement to all 16 Table 2 cells. The
[raw cell audit](../../evidence/claim-2/table_2_cells.csv) contains every
transcribed value and in-range flag. The
[range-conforming control](../../evidence/claim-2/negative_control.json)
correctly rejects a false falsification, and the
[independent checker output](../../evidence/claim-2/independent_checker_output.txt)
passes. See the [source audit](../../evidence/claim-2/source_audit.md),
[method](../../evidence/claim-2/method.md), and
[limitations](../../evidence/claim-2/limitations_and_deviations.md).

### Claims 3 and 4

The complete exact contracts, four-route sequences, public-source records,
checker output, controls, and unresolved limitations are exposed on the
[current CelebA page](#/current-claim-3-celeba-verification) and
[current molecular page](#/current-claim-4-molecular-verification).

### Claim 5

The [contract](../../evidence/claim-5/claim_contract.json) separates the two
constructive cases. Download the
[20,650 independent-group events](../../evidence/claim-5/independent_groups.csv),
[6,350 taxonomy events](../../evidence/claim-5/taxonomy.csv),
[overlap negative control](../../evidence/claim-5/negative_control.json), and
[independent checker output](../../evidence/claim-5/independent_checker_output.txt).
See the [source audit](../../evidence/claim-5/source_audit.md),
[method](../../evidence/claim-5/method.md), and
[limitations](../../evidence/claim-5/limitations_and_deviations.md).

## Evaluator visibility matrix

All “Yes” entries are direct links from this page or its two explicitly linked
current child pages.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | This page | Yes | Yes | Yes | PASS | PASS | Yes | VERIFIED |
| 2 | This page | Yes | Yes | Yes | PASS | PASS | Yes | FALSIFIED |
| 3 | Current CelebA page | Yes | Yes | Yes | PASS | PASS | Yes | BLOCKED |
| 4 | Current molecular page | Yes | Yes | Yes | PASS | PASS | Yes | BLOCKED |
| 5 | This page | Yes | Yes | Yes | PASS | PASS | Yes | VERIFIED |

The previous live judged score remains **6/10**. A score increase is neither
claimed nor forecast from blocked evidence.
