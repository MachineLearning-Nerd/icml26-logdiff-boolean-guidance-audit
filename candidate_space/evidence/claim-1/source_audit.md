# Claim 1 source audit

Source retrieved from `https://ar5iv.labs.arxiv.org/html/2602.05549` on
2026-07-27 at 11:45:56 UTC with User-Agent
`OpenResearch-Reproduction-Audit/1.0 (+https://github.com/MachineLearning-Nerd/icml26-repro-OAM1jJsMGp-logdiff-exact-boolean-guidance)`.
The 753,729-byte response has SHA-256
`67336441b284337c309cd66e2aee8d3a6bd01da716c145debe1319387b9c321a`.

The exact theorem is Proposition 3.1 at HTML anchor `#S3.SS1.1`. It quantifies
over every `t ∈ (0,T]` and every `x ∈ X`. At each conjunction node the two
events must be conditionally independent given `X_t=x`. At each disjunction
node they must be conditionally independent or mutually exclusive. Every
subformula posterior must be exact, differentiable, and strictly between zero
and one. Under those hypotheses, the recursively computed posterior and
logical score equal the true values.

This executable certificate does not claim to prove the continuous theorem.
It exhausts the complete stated finite semantic domain used by the certificate,
with smooth posteriors and exact gradients, and uses a full-joint oracle plus
finite differences. The result is rigorous for that finite domain and
corroborates the theorem under its assumptions.
