# Repro — LOGDIFF Exact Boolean Guidance (ICML 2026)

Reproduction of *Logical Guidance for the Exact Composition of Diffusion Models*
([arXiv:2602.05549](https://arxiv.org/abs/2602.05549), OpenReview `OAM1jJsMGp`)
for the ICML 2026 Agent Reproduction Challenge.

## Claims

1. **Exact score-based logical guidance — verified.** Every nontrivial Boolean
   event over three independent binary categorical variables is compiled into the
   paper's CI-conjunction / ME-disjunction circuit and checked against independent
   full-joint enumeration. With 25 posterior settings this covers 6,350 compiled
   formulas.
2. **Sufficient conditions and Boolean calculus — verified.** Negation,
   conditionally-independent conjunction and disjunction, and mutually-exclusive
   disjunction are each checked directly. Analytic scores are also triangulated
   using finite differences.

Three fail-closed controls deliberately violate conditional independence or use
the constant-weight OR baseline; every invalid construction is rejected.

## Reproduce

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python numpy pytest
source .venv/bin/activate
python repro/src/run_logdiff.py --output-dir outputs --seeds 25
python -m pytest repro/tests -q
```

Official source: `TanjaBien/LogDiff`, pinned commit
`94ef35bafd4b4239e9832d8295128c09e8fc1472`.

