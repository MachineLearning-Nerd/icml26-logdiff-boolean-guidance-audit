# OAM first-wave CPU slice readiness audit

Audit timestamp: `2026-07-20T13:03:34Z`

## Outcome

All four first-wave `cpu-upgrade` slices are still naturally `RUNNING`. None is
terminal, and none has a durable sample payload, terminal report,
`SLICE_MANIFEST.json`, or SUCCESS-last marker. Each immutable prefix currently
contains only an 83-byte `ATTEMPTS.json`, SHA-256
`91b43f8e80be3dedd1b8ede8fbfbf38b79c6e890c283fc3658657e5d20f043f7`,
showing attempt 1 for indices 0-7.

Consequently the measured evidence does **not** authorize a next wave now.
The current four Jobs already consume the route's maximum four OAM
concurrency slots, and no first-wave terminal scientific evidence exists to
validate. Partial logs and attempt ledgers are operational state only.

## Frozen route and preflight

- Contract SHA-256:
  `cadf91302ece71c558af1622617dab09ddad52e8080dc9a459616580a25d39e3`
- Input archive SHA-256:
  `a0bbb9678f72cb2239fb1dec62fc8decb8ee0706a97e19e0ec6a59983c7c3958`
- Source manifest SHA-256:
  `525fa2347e421ba669ce5068664939b0fabb9efd57e5451f7a7faed1ba3df55b`
- Runner SHA-256:
  `ce6b6a67f6e9f39bed4287b64c6c209b8398ba494ed3871fb8fedcabef783249`
- Bootstrap SHA-256:
  `db7c74ce867c6634362e98e95d6c9ff1e270c266f130805073481977d34b9eb4`
- Requirements SHA-256:
  `adfbefd63f4da5981b62b9c1702ae93470b13a9e69e67e5a73cec1913346bd2f`

The local source manifest passes. The route preflight Job
`DineshAI/6a5e0c1fbee6ee1cf4ed24ba` completed naturally. Its immutable report
SHA-256 is `d80c3bad...6f64`; SUCCESS SHA-256 is `c67d7f9f...c871`; SUCCESS
binds the report hash exactly. The report binds the frozen contract, input,
sources, and environment fingerprint `eeaeb6c...b9970`.

The measured 147.814-second probe projects one eight-sample slice at
`2.771509668 h / USD 0.08314529`, below the `5.25 h / USD 0.18` gates. The
current preflight projection for all fourteen campaigns is 155.205 job-hours
and USD 4.65614. These estimates are execution-feasibility evidence, not
scientific evidence.

## First-wave live state

| Logic | Seed | Job | Running seconds | Immutable prefix state |
| --- | ---: | --- | ---: | --- |
| `logdiff_and` | 1 | `6a5e0d94...24cd` | 3,753 | `ATTEMPTS.json` only |
| `logdiff_and_not` | 1 | `6a5e0dad...35af` | 3,727 | `ATTEMPTS.json` only |
| `logdiff_and` | 2 | `6a5e0dc6...24cf` | 3,703 | `ATTEMPTS.json` only |
| `logdiff_and_not` | 2 | `6a5e0de1...24d1` | 3,672 | `ATTEMPTS.json` only |

All four have the exact contract, route, logic, seed, `s00`, image, command,
source mounts, and canonical writable bucket. Their recent logs show only
successful environment installation followed by the silent long-running
generation phase. Nothing indicates terminal success or failure yet.

## Terminal validation before advancement

After each Job ends naturally:

1. Read its terminal HF status. `COMPLETED` is necessary for a successful
   slice but is not sufficient by itself.
2. Re-read the exact immutable prefix. A complete slice must have terminal
   `SUCCESS.json` written after `SLICE_MANIFEST.json`, eight ordered sample
   namespaces, and every sample's `FILES.json` plus SUCCESS-last marker.
3. Verify the SUCCESS/manifest digest, exact logic/seed/slice binding, stable
   input/source/environment binding, complete path inventory, and every file
   hash.
4. Independently load all eight `sample.pt` files and verify CPU execution,
   fixed sample seeds, finite 1,000-step FP32 trajectories, reconstruction,
   and tensor hashes.
5. If only `REPORT.json` exists, classify it literally as
   `checkpointed_partial` or `exhausted`. It is not slice success and must not
   authorize scientific interpretation.

## Conditional next wave

The next four disjoint `s00` identities in seed order are the two logics for
seeds 3 and 4. They are **not reserved or authorized now**.

The shared ledger has an authorized USD 40 cap, USD 5.93 billed/committed, and
USD 34.07 uncommitted. Thus four future USD 0.18 ceilings would fit
arithmetically, but all four exact reserved-not-submitted rows must exist and
the live aggregate must be rechecked immediately before any approved launch.

Only validated natural completion of the current wave, acceptable measured
runtime, zero active OAM slots, four exact new reservations, live account
reinspection, and the external authorization gates can make that next wave
eligible. This audit grants no launch authority and performed no submission.

## Protected local processes

PID 476 and PID 40427 are both alive with their expected commands. PID 476 is
the protected seed-0 `logdiff_and` controller; PID 40427 is the postprocess
queue waiting on it. Neither was signaled, reprioritized, stopped, or otherwise
modified. The replicate contract says local processes are not route launch
blockers, but they remain protected and must not be touched.

No test suite, publication, job mutation, or process mutation was performed.
