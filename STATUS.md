# STATUS — LOGDIFF (`OAM1jJsMGp`)

> **2026-07-22 continuation:** exact live-job and bucket reconciliation found
> all four OAM C4 s01 jobs COMPLETED with terminal slice manifests and 8/8
> sample successes each. Together with s00, 8/56 slices and 64/448 seed-1--7
> ligands are durably preserved. Four independent `cpu-upgrade` s02 slices
> (samples 16–23) are active: AND seed 1 `6a6102e7`, AND-NOT seed 1
> `6a6102f7`, AND seed 2 `6a610307`, and AND-NOT seed 2 `6a610320`. No partial
> result is claim evidence. The protocol remains incomplete until every
> condition/seed has all 32 ligands and the terminal importer/docking/audit
> passes.
> Seed 0 is now separately complete for both conditions. The independent
> auditor accepts both full 32-ligand roots with complete provenance: AND has
> mean paired docking product `59.57176296875`; AND-NOT has 31 valid-unique
> ligands (one deterministic disconnected-fragment rejection) and mean directed
> separation `0.6097096774193547`. These single-experiment values are not the
> required eight-experiment result.
> The exact claim scope was rechecked against ar5iv HTML
> (`https://ar5iv.labs.arxiv.org/html/2602.05549`, Section 4.2, Tables 5--6):
> 32 size-23 ligands across 8 experiments, with paired `A*B` for AND and
> directed `Delta(A,B)` for AND-NOT (GRM5 on-target, RRM1 off-target).

**Session:** full-score campaign. **Last updated:** 2026-07-22. **State:** in progress; official score 6/10 and exact molecular runs active. The scoped four-ligand checkpoint remains the published interim evidence; the completed seed-0 roots have not been published because the preregistered terminal gate requires all eight experiments per condition.

Public Space: [DineshAI/OAM1jJsMGp](https://huggingface.co/spaces/DineshAI/OAM1jJsMGp) at current and judged revision `1fd04429cb112e90be5fa2bb7a19b827667922bf`.

**Historical protected-chain update (2026-07-20 20:29 IST):** the seed-0 AND
controller released naturally after all `32/32` shard `SUCCESS.json` markers
were present. The persistent post-processing queue (PID `40427`) independently
validated the existing generation, completed its merge on the first attempt,
and started full `vina_full` docking (child PID `48191`, four workers,
exhaustiveness 32). AND summary, AND-NOT generation/merge/docking, and the
combined summary remain pending. This is runtime telemetry only: no docked
metric, claim verdict, publication, or process intervention is implied.

**Read-only in-run progress observation:** the same protected
AND docking controller has persisted results for `55/64` generated-ligand ×
target evaluations with `0` recorded failures. All four worker processes remain
CPU-active. This does not establish any molecular metric or claim outcome; the
queue must complete its existing AND and AND-NOT phases naturally before a
terminal evidence audit is eligible.

**Protected AND terminal receipt (2026-07-20 21:07 IST):** the queue's first
attempt completed full seed-0 AND docking (`32/32` samples; `64/64` generated
ligand-target evaluations; two reference evaluations; zero recorded failures).
`parallel_docking/COMPLETE.json` binds `results.csv` to SHA-256
`bcf5c333676116320ce13c8a4d1ced9c7c71f24357e53c7b85cc4755ffd36f29`.
The queue-generated per-condition summary reports valid-unique `1.0`, diversity
`0.8599261972`, quality fraction `0.25`, and AND product `59.57176296875` for
this single run. These are not a paper-level result: no AND-NOT condition or
multi-seed mean/std exists yet. The protected queue has now advanced naturally
to the separate seed-0 AND-NOT generation phase; no manual rerun, audit,
publication, or claim inference was performed.

Fresh official verdict: **6/10**, high quality, at judged Space SHA `1fd04429cb112e90be5fa2bb7a19b827667922bf`; C1/C5 are verified, C2 is falsified, and C3/C4 remain inconclusive. The C4 feedback cites the published 4/32 scope, the below-target `64.53` product, and the then-unstarted AND-NOT campaign. The unpublished seed-0 completion resolves those immediate execution gaps but not the required eight-experiment mean/std.

GitHub remains `MachineLearning-Nerd/icml26-repro-OAM1jJsMGp-logdiff-exact-boolean-guidance` at `6449752`; the current campaign changes are intentionally uncommitted.

## Anchored evidence

- C1 Proposition 3.1: verified by exhaustive finite-state oracles and real trained-UNet algebra checks.
- C2 CMNIST/Shapes3D Table 2 range statement: falsified as written by the paper table itself; only 2/8 LOGDIFF and 5/8 constant-baseline cells fall inside the stated ranges.
- C3 CelebA Table 3: table transcription matches, but the pinned author release lacks all nine declared checkpoints, has a broken config reference, and uses a different FID implementation/protocol.
- C4 GRM5/RRM1 Tables 5-6: exact targets, all three checkpoint hashes, the real TargetDiff sampler, and AutoDock Vina are recovered; seed 0 is complete for both conditions and seeds 1-7 remain active/incomplete.
- C5 Proposition C.2: verified over 20,650 independent-product events and 6,350 taxonomy events, with invalid overlap rejected.

## Source-scale runs

- Exact upstream CMNIST composition classifier completed 50 epochs on the full 60,000-example split.
- Fixed-timestep evaluation completed over the full 10,000-example test split at seven timesteps.
- Independent exact upstream clean-judge training and full 10,000-example evaluation completed. The checkpoint SHA-256 is `ff8dbb5253278ad46e0033959045f9558927b0e814cd04f98fc747d6629adfb6`; digit/colour accuracies are `0.9814/1.0` and digit/colour NLLs are `0.0867544/0.000025857`.
- Molecular recovery includes verified DualDiff data, the exact GRM5/RRM1 target pair, pretrained weights, the real sampler, and full Vina. Both 32 x 1,000-step seed-0 conditions are now generated, hash-merged, docked, summarized, and independently audited as full provenance-complete experiments. AND has 32 valid-unique ligands. AND-NOT has 31; sample 19 deterministically reconstructs as disconnected fragments and is retained as an explicit null docking row. The existing four-ligand partial merge (`b0cf5223...`) remains the only published molecular checkpoint until the full sixteen-root gate passes.
- The measured HF `cpu-upgrade` migration preflight passed without modifying the local controller or any pre-existing HF job. Attempt 1 (`6a5de41d...`) exposed a missing transitive `lmdb` dependency and ended `ERROR`; attempt 2 (`6a5de599...`) added only `lmdb==2.3.0`, then completed after 139 running seconds. Its 20-step probe took `122.218544` seconds, produced result SHA-256 `70ecc737...`, and ran with PyTorch `2.9.0+cpu`, no CUDA runtime, 64 visible CPUs, and 529,681,592,320 bytes (493.30 GiB) RAM. The persisted non-scientific gate report is `outputs/molecular-recovery/hf-cpu-upgrade/seed0-migration-v1/PREFLIGHT.json` (1,340 bytes; SHA-256 `cedeaccc...`), bound to frozen input SHA-256 `a0bbb967...`. The seed-0 full HF job was never launched because the protected local seed-0 chain completed.
- A restartable parallel Vina wrapper is prepared for complete 32-ligand experiments. It preserves the upstream target anchors, `vina_full` mode, exhaustiveness 32, and seed 1 while checkpointing each ligand/target pair, rejecting mismatched protocol caches, retrying failures up to ten times, and emitting a results table compatible with the upstream summarizer. A fail-closed postprocessing queue now validates every one of the 32 seed-0 shard hashes, merges and docks AND, independently generates/merges/docks AND-NOT, and writes separate plus joint seed-0 reports. Independent conditions continue after a failed branch; dependent phases never consume partial artifacts. Queue session `22687` / PID `40427` is waiting by native process inspection on the exact active AND parent PID `476`, then each phase receives up to ten 24-hour restartable attempts. This completes one of the paper's eight experiments per condition; seeds 1--7 remain required for paper-level mean/std replication.
- The four-ligand checkpoint completed paired `vina_full` docking at exhaustiveness 32: 8/8 generated-ligand target evaluations succeeded; mean GRM5/RRM1 affinities are `-8.00375/-8.06675` kcal/mol, mean AND product is `64.53267625`, diversity is `0.887054`, valid-unique fraction is `1.0`, and paper-defined quality fraction is `0.5`. Same-run reference affinities are `-5.866/-7.640`. The product is below the paper's LOGDIFF `73.20 +/- 3.18` and DualDiff `71.87 +/- 3.33`, so it is published as a partial execution checkpoint rather than headline verification. AND-NOT separation is not inferred from AND samples.
- An independent non-pandas evidence auditor now validates the merged sample and every source shard hash, exact GRM5/RRM1 identities, canonical-SMILES uniqueness, reporting-source hashes, and (for restartable complete docking) the results-manifest hash. It independently reproduces the four-ligand product `64.53267625`, reports a deterministic pair-breaking control and target-swap sign control, forbids pooling AND with AND-NOT, and correctly leaves full readiness false until eight complete 32-ligand experiments exist for each condition. See `docs/MOLECULAR_EVIDENCE_AUDIT.md`.
- A fail-closed continuation is prepared, but not launched, for the remaining seeds 1--7 of AND and AND-NOT. Its deterministic plan contains 14 exclusive campaigns and 72 commands, protects every seed-0 output from writes, revalidates exact paper/protocol/source/vendor/weight identities, continues independent campaigns after a failure, and exposes ten materially different escalation routes while forbidding “unable” before all ten have evidence. The latest dry run passed static integrity and correctly remained blocked on the four live OAM/CVM/qIO chain PIDs plus the 4 GiB memory gate. See `docs/MOLECULAR_REPLICATE_CONTINUATION.md`.
- A deterministic Colab-2026.04 CUDA handoff is also prepared, but not launched, for those same fourteen missing campaigns. CUDA compatibility is conditional rather than claimed: the remote driver must pass exact runtime/package/source/GPU checks, CUDA scatter/k-NN and checkpoint-load gates, a compiled one-step forward, and a 20-step timing calibration before it can run. Each campaign has exclusive Drive paths; seed 0 is absent and protected; every sample is scratch-validated and hash-checkpointed; conditions remain separate; and the independent local return verifier binds all 448 raw shards through merge, Vina, summary, and audit evidence. The CPU seed-0/CUDA seed-1--7 backend heterogeneity is explicit. See `docs/MOLECULAR_COLAB_CUDA_HANDOFF.md`.
- A disjoint HF `cpu-upgrade` route for seeds 1-7 is executing under its frozen contract. It rejects seed 0 at five independent boundaries and splits all fourteen campaigns into 56 fixed eight-sample slices with unique condition/seed/slice/contract prefixes, atomic hash manifests, and SUCCESS-last immutability. The paid preflight and eight s00/s01 slices have terminal verified receipts (64/448 ligands); four disjoint s02 slices for AND/AND-NOT seeds 1-2 are active. The content-addressed importer still requires all 56 slices and 448 unique samples and rejects partial, extra, seed-0, or mixed-contract/source/environment identities. Merge/full docking/audit remain terminal work after import. See `docs/OAM_HF_CPU_REPLICATES.md`.
- A final-only challenge-C4 terminal import and existing-Space repair are prepared but not executed. They reject a seed-0-only checkpoint and require the independent auditor's full sixteen condition/seed campaigns, eight provenance-complete 32-ligand experiments per condition, no pooling, and zero readiness blockers. The importer reruns the auditor and requires exact report-byte identity before exposing only JSON/CSV evidence; the repair refetches the exact official verdict, pins the existing Space parent, stages additive evidence only, and requires separate literal root approval for apply. Full completion reports reproduced means/std exactly and does not predetermine verification. See `docs/C4_TERMINAL_HANDOFF.md`.
- Official CelebA is complete and verified at 202,599 images; the released clean-filter splits contain 100,247 train, 12,459 validation, and 12,186 test images. Public DDPM `shalpin87/diffusion_celeba@91d0ff0` is pinned locally and clean-fid 0.1.35 is installed for the independent C3 route.

## Publication and verification

- Static Space is public and RUNNING; Hub and app return HTTP 200.
- Exactly the intended 11-page hierarchy is present, with Conclusion last.
- Required tags, pinned executive summary/poster, artifact cell, and public evidence bucket are present.
- Local structural validation passes except the pre-existing legacy Space-name rule requiring a new `repro-*` identifier; no duplicate Space was created.
- Remote secret and absolute-path leakage scans pass.
- The independent CMNIST judge page was synced and read back at current Space SHA `93d90f36`; its remote SHA-256 exactly matches the local page (`840c7bef...`).
- The Claim 4 checkpoint page was synced and byte-for-byte read back at public Space SHA `38daa951`; local and remote SHA-256 are both `7ac3c77c...`. The public checkpoint artifact also read back with matching SHA-256 `c44cd570...`; its unauthenticated download endpoint returns a public Xet redirect.

## Next

Let the four active s02 jobs terminate naturally, verify their exact bucket receipts, and continue at most four disjoint OAM slices concurrently without rerunning any successful slice. Preserve unrelated Jobs. Import only after all 56 slice successes and 448 unique samples exist under the one frozen contract; then merge, run full Vina, summarize each experiment separately, and execute the sixteen-root independent audit. Publish only if that audit is blocker-free and the additive exact-parent Space repair passes; until then retain the judged 6/10 baseline. See `docs/OAM_HF_CPU_REPLICATES.md` and `docs/C4_TERMINAL_HANDOFF.md`.
