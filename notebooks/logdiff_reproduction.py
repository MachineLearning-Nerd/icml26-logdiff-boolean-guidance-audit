import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Logical Guidance for Exact Diffusion Composition

    <img
      src="https://raw.githubusercontent.com/MachineLearning-Nerd/icml26-logdiff-boolean-guidance-audit/main/reports/claim-by-claim/images/headline-verdicts.png"
      alt="Five exact claims: Claims 1 and 5 verified, Claim 2 falsified, Claims 3 and 4 blocked; supported score 6/10"
      style="width: 100%; border-radius: 12px;"
    />

    This notebook is a self-contained tour of the evidence for
    [*Logical Guidance for the Exact Composition of Diffusion Models*](https://arxiv.org/abs/2602.05549).
    It starts from the already-produced results; no expensive generation or
    docking run is required. The previous live judge score is **6/10**, and
    this reproduction supports that same score rather than claiming an
    increase.
    """)
    return


@app.cell
def _():
    claims = [
        {
            "claim": 1,
            "topic": "Proposition 3.1",
            "paper_result": "Exact CI/ME Boolean score composition",
            "observed": "6,350 formulas; max error 3.33e-16",
            "verdict": "VERIFIED",
        },
        {
            "claim": 2,
            "topic": "Table 2",
            "paper_result": "LoGDiff 94–98%; constant 63–77%",
            "observed": "85.1–94.4%; 57.9–76.1%",
            "verdict": "FALSIFIED",
        },
        {
            "claim": 3,
            "topic": "CelebA NOT",
            "paper_result": "FID 23.61 vs 32.87",
            "observed": "Required checkpoints and metric path unavailable",
            "verdict": "BLOCKED",
        },
        {
            "claim": 4,
            "topic": "GRM5/RRM1",
            "paper_result": "AND 73.20 vs 71.87; separation 0.94 vs 0.28",
            "observed": "No complete paired campaign or docking outputs",
            "verdict": "BLOCKED",
        },
        {
            "claim": 5,
            "topic": "Proposition C.2",
            "paper_result": "Completeness for groups and taxonomies",
            "observed": "27,000 events; max error 3.33e-16",
            "verdict": "VERIFIED",
        },
    ]
    return (claims,)


@app.cell
def _(claims, mo):
    mo.vstack(
        [
            mo.md("## The five evidence contracts"),
            mo.ui.table(
                claims,
                label="Paper claims and observed evidence",
                pagination=False,
                selection=None,
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## How exact logical composition is checked

    For an event \(A\), the conditional score is

    \[
    \nabla_x \log p_t(x\mid A)
    = \nabla_x \log p_t(x) + \nabla_x \log p_t(A\mid x).
    \]

    The paper gives rules for compiling the final guidance term from
    atomic predicates when conjunctions satisfy conditional independence
    and disjunctions are conditionally independent or mutually exclusive.
    The verifier does not compare the implementation with itself: it
    enumerates the full joint distribution independently, computes each
    Boolean event directly, and compares probability and score.

    The certificate is exhaustive over the finite categorical constructions
    in the contract. It is deliberately not described as a numerical proof
    for every continuous diffusion model.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    <img
      src="https://raw.githubusercontent.com/MachineLearning-Nerd/icml26-logdiff-boolean-guidance-audit/main/reports/claim-by-claim/images/theorem-certificates.png"
      alt="Finite-domain certificates for Claims 1 and 5"
      style="width: 100%; border-radius: 12px;"
    />
    """)
    return


@app.cell
def _():
    table2 = [
        {
            "method": "LoGDiff",
            "claimed_low": 94.0,
            "claimed_high": 98.0,
            "actual_low": 85.1,
            "actual_high": 94.4,
            "cells_inside": "2 / 8",
        },
        {
            "method": "Constant",
            "claimed_low": 63.0,
            "claimed_high": 77.0,
            "actual_low": 57.9,
            "actual_high": 76.1,
            "cells_inside": "5 / 8",
        },
    ]
    return (table2,)


@app.cell
def _(mo, table2):
    mo.vstack(
        [
            mo.md(
                """
                ## Claim 2 is falsified as written

                The statement attaches literal ranges to all eight cells per
                method. Most cells lie outside those ranges. A range-conforming
                synthetic control is correctly rejected, so the checker does
                not return “falsified” for every input. The broader qualitative
                advantage is a different claim.
                """
            ),
            mo.ui.table(table2, pagination=False, selection=None),
            mo.md(
                r"""
                <img
                  src="https://raw.githubusercontent.com/MachineLearning-Nerd/icml26-logdiff-boolean-guidance-audit/main/reports/claim-by-claim/images/table2-range-audit.png"
                  alt="Cell-by-cell range audit for Table 2"
                  style="width: 100%; border-radius: 12px;"
                />
                """
            ),
        ]
    )
    return


@app.cell
def _(claims, mo):
    claim_picker = mo.ui.dropdown(
        options={f"Claim {row['claim']}: {row['topic']}": row["claim"] for row in claims},
        value="Claim 1: Proposition 3.1",
        label="Inspect one claim",
    )
    claim_picker
    return (claim_picker,)


@app.cell
def _(claim_picker, claims, mo):
    selected = next(row for row in claims if row["claim"] == claim_picker.value)
    mo.callout(
        mo.md(
            f"""
            **{selected['topic']} — {selected['verdict']}**

            Paper: {selected['paper_result']}

            Evidence: {selected['observed']}
            """
        ),
        kind=(
            "success"
            if selected["verdict"] == "VERIFIED"
            else "danger"
            if selected["verdict"] == "FALSIFIED"
            else "warn"
        ),
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why BLOCKED is a useful result

    Claim 3 needs three author-equivalent CelebA checkpoints and the exact
    5,000-image clean-fid path. Claim 4 needs complete LoGDiff and DualDiff
    32-ligand campaigns plus GRM5/RRM1 docking results. Four distinct
    verification routes were completed for each. A public proxy model and
    96 partial molecular payloads were rejected as non-equivalent evidence.

    <img
      src="https://raw.githubusercontent.com/MachineLearning-Nerd/icml26-logdiff-boolean-guidance-audit/main/reports/claim-by-claim/images/blocked-claims.png"
      alt="Four verification routes and remaining blockers for Claims 3 and 4"
      style="width: 100%; border-radius: 12px;"
    />

    Missing resources, partial campaigns, and proxy models cannot verify or
    falsify an exact empirical contract. The supported conclusion is
    therefore **6/10**, pending any future live-judge assessment.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Reproduce the bounded verification

    The formal evidence uses one deterministic CPU worker and seeds 0–24:

    ```bash
    uv sync --frozen
    uv run python repro/src/run_logdiff.py \
      --output-dir .openresearch/artifacts --seeds 25
    ```

    Read the
    [illustrated report](https://github.com/MachineLearning-Nerd/icml26-logdiff-boolean-guidance-audit/blob/main/reports/claim-by-claim/report.md)
    or start from the
    [canonical evaluator page](https://github.com/MachineLearning-Nerd/icml26-logdiff-boolean-guidance-audit/blob/main/candidate_space/pages/current-cumulative-verification/page.md)
    for contracts, raw CSV/JSON evidence, independent checker outputs,
    negative controls, and limitations.
    """)
    return


if __name__ == "__main__":
    app.run()
