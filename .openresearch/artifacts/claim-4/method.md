# Claim 4 historical-evidence audit

The verifier scans every preserved bucket JSON file and re-derives slice
identity from its path. For each terminal slice it validates the SUCCESS-last
record, SHA-256 of the slice manifest, common source/input/environment binding,
eight distinct sample indices, sample seed mapping, 1,000-step CPU command,
SHA-256 of each sample SUCCESS record, and SHA-256 of each FILES manifest.

It separately audits the bucket listing for raw payload presence. Payload
contents are not downloaded or loaded at this route because the campaign is
already incomplete before that costly gate.

Completeness is evaluated against the literal contract: eight experiments,
32 ligands per experiment, both conditions, and both LOGDIFF and DualDiff.
The current historical route contains only LOGDIFF. A synthetic negative
control supplies all methods, conditions, experiments, raw payloads, and
docking rows; the completeness classifier must then return
`READY_FOR_CLAIM_CHECK`.

The public-source route separately resolves the historical FKC upstream commit
and enumerates its tree, then checks the author-declared NEC repository and
Hugging Face title searches. This route is deliberately independent of the
bucket audit. Its positive control finds the exact FKC commit and 440-entry
tree; its target searches do not recover the missing LoGDiff molecular
implementation.

The mandatory falsification route admits only a complete exact-method
campaign. It verifies that the quoted comparisons match the paper tables and
that a synthetic reversed-order table would be detected. The 96 undocked
LoGDiff payloads are rejected as a counterexample because they do not satisfy
the domain and quantifiers.
