# CelebA C3 fail-closed readiness audit

Audit date: 2026-07-20. Scope: static preparation only. No local or Hugging Face
training/generation job was launched, no test suite was run, and protected PIDs
476 and 40427 were not modified.

## Bottom line

The independent public-model route is now preregistered and guarded, but it is
**not execution-ready evidence yet**. The asset gate passes. The evidence gate
correctly fails until two full, independent classifiers exist. The existing
`classifier-smoke` checkpoint is excluded: it trained for one epoch on only two
examples and reports zero validation accuracy for both heads.

Even a successful future run cannot reproduce the paper's Table 3 values. The
paper used an unavailable 64 px latent SiT and unavailable author classifiers;
this route uses a public 32 px unconditional DDPM and newly trained pixel-space
classifiers. Its strongest valid conclusion is directional support (or
contradiction) for LOGDIFF versus constant negation on this independent model.

## Official claim and present verdict

The judged C3 claim is that CelebA NOT guidance lowers FID from 32.87 for the
constant baseline to 23.61 for LOGDIFF while retaining comparable conformity.
The official verdict at Space SHA
`38daa9517ef7af65d409ffd0325cba289e969014`, judged
`2026-07-20T01:09:46+00:00`, is `inconclusive`: the table transcription matches,
but no empirical generation run exists. The pinned release has none of its nine
declared checkpoints, references a missing dataset config, and computes
TorchMetrics FID even though the paper specifies clean-fid.
The released results writer also multiplies the already-total 5,000 target by
batch size and records 500,000 samples under the default batch of 100; this
route binds counts to the actual PNG inventory instead.

Primary-source protocol facts used here:

- CelebA FID is computed independently per compositional task.
- Each task has 5,000 generated images: 100 images for each of 50 queries.
- The paper specifies clean-fid.
- The released evaluator uses all 162,770 CelebA training images as its real FID
  distribution. This route retains that reference distribution and changes only
  the implementation to the paper-specified clean-fid.

## Frozen inputs

The source of truth is
`repro/configs/celeba_c3_public_negation.json`. Its canonical JSON SHA-256 must
be embedded in every classifier, generation, and evaluation manifest.

| Input | Pin / SHA-256 |
|---|---|
| Author source | `TanjaBien/LogDiff@94ef35bafd4b4239e9832d8295128c09e8fc1472` |
| Released classifier models | `ff5f6b3f2bcf6b4b3c3a5e654eed4c527631808712b2ee1a58f619871b3a7c61` |
| Released CelebA dataset loader | `98483f0fd65326bac2d5c6cdc486f736a9d6a3d1832a5d3904f94b565285f4d2` |
| Released CelebA inference config | `28c2ff8b5c88b966cf1ebe35fd6a819f9b25a7f7513d5855ba64a4a95d8b1142` |
| Public DDPM Hub revision | `shalpin87/diffusion_celeba@91d0ff096e031c21b8313bd5877316a52900d4ec` |
| Public DDPM weights | `930f28acfcad1137c5c38f0cf0aaeebc61dc607c6e54369c3da7df9309f90ced` |
| CelebA image archive, 1,443,490,838 bytes | `46fb89443c578308acf364d7d379fe1b9efb793042c0af734b6112e4fd3a8c74` |
| CelebA attributes | `f0e5da289d5ccf75ffe8811132694922b60f2af59256ed362afa03fefba324d0` |
| CelebA partitions | `fc955bcb3ef8fbdf7d5640d9a8693a8431b5f2ee291a5c1449a1549e7e073fe7` |

The preflight recomputes these hashes and derives both raw partition counts
(`162770/19867/19962`) and released single-hair-label counts
(`100247/12459/12186`) rather than trusting prose. A remote run must transfer the
pinned archive and metadata and extract them fresh; an unverified remote cache
is not accepted.

## Fail-closed execution contract

Two classifiers are mandatory:

1. Guidance: released noise-aware `MultiheadClassifier(ResNet18,[2,5])`, seed
   42, 100 full epochs.
2. Judge: released clean-image `MultiLabelClassifier(ResNet18,[2,5])`, seed
   314159, 10 full epochs.

Each must see all 100,247 filtered training examples per epoch and finish above
the preregistered validation thresholds (gender 0.90, hair 0.75). The generator
will not accept the smoke model, an arbitrary checkpoint path, a hash mismatch,
or a guidance checkpoint without matching provenance. The evaluator accepts
only the independent judge checkpoint.

Generation is fixed at two methods, 50 identical queries per method, 100 images
per query, 1,000 DDPM steps, batch 10, guidance scale 1.0, LOGDIFF odds clip 3.0,
and seed 2026. The two methods reuse the same starting noise and stochastic
scheduler stream. Each completed query is promoted atomically, records all PNG
hashes, and may be reused only through `--resume` after its hashes and run-state
identity pass. Dirty output directories, partial promoted queries, missing
records, and any count other than exactly 5,000 images per method are rejected.

Evaluation starts only in a new empty directory. It re-hashes all 10,000
generated PNGs, revalidates the protocol and judge checkpoint, builds the
162,770-image training reference by hard links (copy fallback), and requires
clean-fid 0.1.35 in `clean` mode. This prevents old aggregate/reference images
from contaminating FID, which the previous evaluator allowed.

The independent result passes its preregistered directional gate only if:

- both methods have all 5,000 paired images;
- LOGDIFF pooled clean-FID is strictly below constant pooled clean-FID; and
- LOGDIFF's independent-judge negated-event violation rate is no higher than
  constant's.

Passing does **not** justify the wording “Table 3 reproduced” or comparison of
the resulting absolute FIDs to 23.61/32.87 as if architectures matched.

## Preregistered commands (do not run on the busy local host)

Run these from the paper root on one persistent remote filesystem:

```bash
python repro/src/preflight_public_celeba_c3.py --stage assets
python repro/src/train_public_celeba_classifier.py --role guidance --device cuda --num-workers 4
python repro/src/train_public_celeba_classifier.py --role judge --device cuda --num-workers 4
python repro/src/preflight_public_celeba_c3.py --stage classifiers
python repro/src/run_public_celeba_negation.py --device cuda --output-dir outputs/celeba-public/negation-c3-v1
python repro/src/evaluate_public_celeba_negation.py --generation-dir outputs/celeba-public/negation-c3-v1 --device cuda --fid-device cuda --output-dir outputs/celeba-public/evaluation-c3-v1
```

On interruption, rerun a classifier with only its exact role-local
`--resume .../training_state.pt`, or rerun generation with `--resume`. Never
change the protocol JSON between attempts. Persist the entire
`outputs/celeba-public` tree after every classifier epoch and completed query.

## Compute route and budget

Use an HF `t4-medium` job (1 x T4 16 GB, 8 vCPU, 30 GB RAM, 100 GB ephemeral
disk) attached to a private persistent bucket/volume. The live HF hardware quote
on 2026-07-20 is USD 0.60/hour. `t4-small` has enough VRAM but only 15 GB system
RAM and 50 GB disk, below this preregistration's conservative 24 GB RAM gate.
`cpu-upgrade` is unsuitable for the classifier-gradient and 10-million
image-step generation workload.

Without a measured T4 calibration, wall time is necessarily a range. Static
workload accounting gives roughly 11.0 million classifier training examples
(100 guidance epochs plus 10 judge epochs), 10,000,000 image-denoising steps,
and two clean-FID passes against 162,770 real images. Reserve **18-36 T4 hours**
(USD **10.80-21.60**) and impose a USD 24 route cap, leaving headroom inside the
user's USD 30 balance. Before the evidence job, run a separately labelled timing
calibration that cannot write into evidence directories; refine the reservation
from measured images/second. Do not start if another account-wide T4 job would
be displaced or if persistence is unavailable.

## Remaining blockers and strongest next action

1. No full guidance classifier exists.
2. No independent clean judge exists.
3. No paired 10,000-image generation exists.
4. No clean-fid result exists.
5. Absolute Table 3 parity remains impossible without the missing author
   checkpoint stack; this route can only supply independent directional evidence.

The strongest next action is to package the pinned minimal inputs plus these
scripts onto a private persistent HF volume, run the asset preflight, perform a
non-evidence T4 timing calibration, and launch the two classifier stages only
after reserving the resulting capped budget. Generation must remain blocked
until both classifier provenance gates pass.
