# Branch audit and normalization map

## Audit scope

The source snapshot was cloned from the public repository on 2026-08-16. It
contained one landing branch, main, and ten public experiment branches under
orx/. Every branch was inspected by tip commit, commit subject, and lineage.
The old names are retained here as provenance; the final public names remove
the OpenResearch implementation prefix and describe the branch role.

## Old-to-new mapping

| Old public branch | Tip before rewrite | Role | Final branch |
| --- | --- | --- | --- |
| orx/frozen-cumulative-baseline | a617bc04525ce55ad3477a16a7318031ca376fba | Freeze the finite C1/C2/C5 baseline and initial fail-closed contracts | baseline/frozen-claims |
| orx/celeba-exact-claim-audit | c7be7e5148e9a96bc178f23b150c07f9ec8b4800 | Add the exact CelebA release contract and source audit | audit/celeba-release |
| orx/celeba-evaluator-visible-evidence | bc8c80069855dd36a685c4d24ca2915770f007e7 | Expose the current CelebA evidence and independent checker | audit/celeba-evidence |
| orx/molecular-evidence-recovery-audit | 2b6695985ab09bca0cc6c5f71620647f2c189bfe | Recover and hash-audit the available molecular manifests | audit/molecular-recovery |
| orx/molecular-evaluator-visible-evidence | 8c8c90ae81f09b664c574a56d3fe39a96f5f36d8 | Freeze the four-route molecular blocker and controls | audit/molecular-evidence |
| orx/cumulative-exact-claim-release-candidate | ac7ad48b7dc4120acbbbbe0468f0cfa76c4591bc | Combine the current claim contracts into a release candidate | candidate/cumulative-claims |
| orx/evaluator-visible-cumulative-artifact | 391bab3175d667335fc7a39ac1019d6870a7dbd1 | Add evaluator-visible raw claim artifacts and checkers | release/evaluator-artifact |
| orx/csv-aware-evaluator-release-audit | 1d37e8b780078db415730cd50f9f138c507634b3 | Correct text-only CSV release classification and audit the upload surface | audit/csv-release |
| orx/publication-surface-and-illustrated-report | 13569ed474f2872b5827e57f4c7fbf791be4119c | Add the illustrated report, tutorial, and public landing surface | release/publication-surface |
| orx/final-release-metadata-and-provenance | 2e3caa2523de33d36b4f4f8927cb8d6240be9b26 | Record final release provenance and fast-forward main | release/final-provenance |

main is the publication surface. release/final-provenance intentionally
points to the same pre-normalization tip as main; it remains a named release
checkpoint rather than being silently deleted.

## Lineage

~~~text
baseline/frozen-claims
├── audit/celeba-release
│   └── audit/celeba-evidence
└── audit/molecular-recovery
    └── audit/molecular-evidence
        └── candidate/cumulative-claims
            └── release/evaluator-artifact
                └── audit/csv-release
                    └── release/publication-surface
                        └── release/final-provenance → main
~~~

The branch purpose is historical: these refs are experiment and publication
checkpoints, not separate scientific claims. Main contains the final docs and
the evaluator-visible surface; the descriptive branches preserve the exact
intermediate states.

## Naming and identity invariants

After normalization the public branch set must be exactly main plus the ten
final names in the mapping above. No branch may retain the orx/ prefix.
Every reachable commit must have:

- author name MachineLearning-Nerd
- author email MachineLearning-Nerd@users.noreply.github.com
- committer name MachineLearning-Nerd
- committer email MachineLearning-Nerd@users.noreply.github.com
- no Co-authored-by trailer

The recovery bundle created before history rewriting is kept outside the
repository. verify_final.py checks the branch inventory, required docs,
reachable commit identities, and evidence manifest after a fresh clone.
