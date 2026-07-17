# STATUS — LOGDIFF (`OAM1jJsMGp`)

**Session:** autoloop. **Last updated:** 2026-07-17. **State:** locally complete; publication queued.

## Source audit

- Paper: arXiv 2602.05549; OpenReview `OAM1jJsMGp`.
- Official code: `TanjaBien/LogDiff` pinned at
  `94ef35bafd4b4239e9832d8295128c09e8fc1472`.
- Full image/protein experiments require training, but both official challenge
  claims are exact calculus claims. Proposition C.3 gives a discrete equivalent
  suitable for exhaustive CPU verification without a proxy scale reduction.

## Evidence

- Exhausted all 254 nontrivial Boolean events on three binary variables across
  25 posterior settings: 6,350/6,350 formulas agree with direct enumeration.
- Maximum posterior error `2.22e-16`; analytic score error `3.33e-16`;
  finite-difference score error `5.21e-10`.
- All 100 primitive Table-1 rule checks agree at floating-point roundoff.
- 12/12 tests pass; all 3 assumption-violation controls are rejected.
- Trackio logbook is complete, tagged, pinned, command-captured, and secret-scanned.

## Next

- Create and verify the descriptive public GitHub repository. Publish the completed
  Trackio logbook to `DineshAI/OAM1jJsMGp` after the daily Space quota resets.
