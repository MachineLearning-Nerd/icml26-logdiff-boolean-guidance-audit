# Claim 5 evaluation contract

The fixed command writes per-seed CSV files and a negative-control JSON.
`summary.json` must report 20,650 independent-group events, 6,350 taxonomy
events, floating-point-level errors below `1e-14`, and a rejected invalid
overlap. Any count, numerical, or control failure exits nonzero.

Limitations: the certificate is exhaustive over the specified finite domains
and is scoped accordingly.
