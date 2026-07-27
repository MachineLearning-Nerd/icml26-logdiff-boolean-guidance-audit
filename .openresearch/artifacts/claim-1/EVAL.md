# Claim 1 evaluation contract

Run the fixed project command. Current output is written to this directory and
the complete summary, Git SHA, seed list, visible CPU allocation, and runtime
are printed to the OpenResearch run log. `summary.json` must report
`claim_1.status = VERIFIED` and `verifier.status = PASS`; otherwise the process
exits nonzero.

Limitations: this is exhaustive over the declared finite certificate domain,
not a proof certificate for every continuous diffusion model.
