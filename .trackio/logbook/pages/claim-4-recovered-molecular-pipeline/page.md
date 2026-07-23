# Claim 4 - recovered molecular pipeline


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_86bff2c868db", "created_at": "2026-07-19T18:56:33+00:00", "title": "Recovered full-scale inputs and real docking"}
-->
LOGDIFF does not release its molecular implementation. The paper states that this experiment follows the FKC setup, so the independent recovery pins martaskrt/fkc-diffusion at aa6f5ed4a0ebb91329d4cd5823cc7e77c5e196e6 and the DualDiff dataset revision 84be04b28bdb1856fe5d9bbbf2dc5858b6b8c921.

The exact challenge pair is present: dataset index 29 is GRM5 P41594 and index 371 is RRM1 P23921. All ligand, 10A pocket, protein, and cleaned-protein files are present. Three released artifacts are SHA-256 verified: the 2.84M-parameter diffusion model, 2.55M-parameter property model, and regression parameters.

Real execution gates passed:
- TargetDiff loaded the released checkpoint and ran its actual SO(3)-equivariant graph sampler on the GRM5 pocket.
- AutoDock Vina scored, minimized, and docked both released reference complexes.
- GRM5 reference docked at -5.050 kcal/mol in the low-exhaustiveness smoke gate.
- RRM1 reference docked at -7.587 kcal/mol in the low-exhaustiveness smoke gate.

The 32-ligand, 1,000-step, beta 2.0 replication is retained as active work until its generated-ligand metrics are available.


---
<!-- trackio-cell
{"type": "code", "id": "cell_32edec61d690", "created_at": "2026-07-20T01:05:24+00:00", "title": "Four-ligand full-step checkpoint: paired Vina evaluation", "command": [".venv/bin/python", "repro/src/summarize_molecular_progress.py", "outputs/molecular-recovery/full-protocol-shards/logdiff_and/run-seed-00", "outputs/molecular-recovery/outputs/full-protocol-partial4-logdiff-and", "--results-csv", "outputs/molecular-recovery/outputs/full-protocol-partial4-logdiff-and/29/371/results.csv", "--output", "outputs/molecular-recovery/outputs/full-protocol-partial4-logdiff-and/partial_checkpoint.json"], "exit_code": 0, "duration_s": 3.695}
-->
````bash
$ .venv/bin/python repro/src/summarize_molecular_progress.py outputs/molecular-recovery/full-protocol-shards/logdiff_and/run-seed-00 outputs/molecular-recovery/outputs/full-protocol-partial4-logdiff-and --results-csv outputs/molecular-recovery/outputs/full-protocol-partial4-logdiff-and/29/371/results.csv --output outputs/molecular-recovery/outputs/full-protocol-partial4-logdiff-and/partial_checkpoint.json
````

exit 0 · 3.7s


````python title=summarize_molecular_progress.py
#!/usr/bin/env python3
"""Create a publishable, path-sanitized molecular campaign checkpoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from summarize_molecular_campaign import summarize_frame


SAFE_RESULT_KEYS = (
    "sample_index",
    "sample_seed",
    "attempt",
    "wall_seconds",
    "sampling_seconds",
    "sha256",
    "bytes",
    "valid_reconstruction",
    "smiles",
    "posterior_min",
    "posterior_max",
)


def build_report(
    shard_root: Path,
    merged_root: Path,
    results_csv: Path | None = None,
) -> dict:
    progress = json.loads((shard_root / "PROGRESS.json").read_text())
    merge_manifest = json.loads(
        (merged_root / "29" / "371" / "merge_manifest.json").read_text()
    )
    completed = int(progress["completed"])
    if completed != len(progress["results"]):
        raise ValueError("progress result count mismatch")
    if int(merge_manifest["samples"]) != completed:
        raise ValueError("partial merge does not match current progress count")
    safe_results = [
        {key: row[key] for key in SAFE_RESULT_KEYS if key in row}
        for row in progress["results"]
    ]
    if not all(row.get("valid_reconstruction") for row in safe_results):
        raise ValueError("not every merged shard has a valid reconstruction")
    smiles = [row.get("smiles") for row in safe_results]
    if len(smiles) != len(set(smiles)):
        raise ValueError("partial campaign contains duplicate SMILES")

    report = {
        "paper": "OAM1jJsMGp",
        "claim": "C4: GRM5/RRM1 molecular composition",
        "status": "partial_campaign_checkpoint",
        "scope": (
            f"{completed} completed ligands from an active "
            f"{progress['samples']}-ligand AND campaign; not a replacement "
            "for the complete paper protocol"
        ),
        "protocol": {
            "logic": progress["logic"],
            "target_indices": progress["targets"]["indices"],
            "target_names": progress["targets"]["names"],
            "num_steps": progress["num_steps"],
            "inverse_temperature_beta": progress["inverse_temperature_beta"],
            "posterior_mc_samples": progress["posterior_mc_samples"],
            "num_atoms": progress["num_atoms"],
            "compile_forward": progress["compile_forward"],
            "workers": progress["workers"],
            "max_attempts_per_sample": progress["max_attempts_per_sample"],
        },
        "campaign_target_samples": int(progress["samples"]),
        "completed_samples": completed,
        "valid_reconstructions": sum(
            bool(row["valid_reconstruction"]) for row in safe_results
        ),
        "unique_smiles": len(set(smiles)),
        "campaign_elapsed_seconds_at_checkpoint": progress["elapsed_seconds"],
        "merged_sample_sha256": merge_manifest["output_sha256"],
        "results": safe_results,
    }
    if results_csv is not None:
        if not results_csv.is_file():
            raise FileNotFoundError(results_csv)
        docking = summarize_frame(
            pd.read_csv(results_csv), samples_per_run=completed
        )
        if progress["logic"] == "logdiff_and":
            docking["diagnostic_mean_rrm1_minus_grm5"] = docking.pop(
                "mean_and_not_separation"
            )
            docking["and_not_metric_status"] = (
                "not_applicable_to_and_samples; requires a separate "
                "logdiff_and_not campaign"
            )
        report["docking"] = {
            "mode": "vina_full",
            "exhaustiveness": 32,
            **docking,
        }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("shard_root", type=Path)
    parser.add_argument("merged_root", type=Path)
    parser.add_argument("--results-csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(args.shard_root, args.merged_root, args.results_csv)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

````


````json title=partial_checkpoint.json
{
  "campaign_elapsed_seconds_at_checkpoint": 12659.331600189209,
  "campaign_target_samples": 32,
  "claim": "C4: GRM5/RRM1 molecular composition",
  "completed_samples": 4,
  "docking": {
    "and_not_metric_status": "not_applicable_to_and_samples; requires a separate logdiff_and_not campaign",
    "diagnostic_mean_rrm1_minus_grm5": -0.06299999999999994,
    "diversity": 0.8870539334210088,
    "exhaustiveness": 32,
    "generated_samples": 4,
    "maximum_rrm1_docking": -7.347,
    "mean_and_product": 64.53267625000001,
    "mean_grm5_docking": -8.00375,
    "mean_rrm1_docking": -8.06675,
    "minimum_grm5_docking": -8.282,
    "mode": "vina_full",
    "quality_fraction": 0.5,
    "valid_unique_count": 4,
    "valid_unique_fraction": 1.0
  },
  "merged_sample_sha256": "b0cf5223adfc76ce5389a5253c2481e2612df31d262c7f7dc18ddad6e6f53234",
  "paper": "OAM1jJsMGp",
  "protocol": {
    "compile_forward": true,
    "inverse_temperature_beta": 2.0,
    "logic": "logdiff_and",
    "max_attempts_per_sample": 10,
    "num_atoms": 23,
    "num_steps": 1000,
    "posterior_mc_samples": 1,
    "target_indices": [
      29,
      371
    ],
    "target_names": [
      "GRM5",
      "RRM1"
    ],
    "workers": 4
  },
  "results": [
    {
      "attempt": 1,
      "bytes": 1586377,
      "posterior_max": 0.9998999834060669,
      "posterior_min": 9.999999747378752e-05,
      "sample_index": 0,
      "sample_seed": 0,
      "sampling_seconds": 12637.527888059616,
      "sha256": "9896eb58d849cffd33d2aff6079e2f91cb482788a2fd2a52a6f6ad1f1cfa16e6",
      "smiles": "O=C(O)C(CO)Cc1[nH]c2c3c1CC(F)(F)CC3(F)CCC=C2",
      "valid_reconstruction": true,
      "wall_seconds": 12659.108721017838
    },
    {
      "attempt": 1,
      "bytes": 1586761,
      "posterior_max": 0.9998999834060669,
      "posterior_min": 9.999999747378752e-05,
      "sample_index": 1,
      "sample_seed": 1,
      "sampling_seconds": 12628.873342990875,
      "sha256": "deff243d24acb8b0baf1ca665a9c195594fc10552bd114240faf2aede3fc0f2a",
      "smiles": "CC1OC2(CO)C(=O)C1(O)OC(C(O)CC1CCOC1=O)C2O",
      "valid_reconstruction": true,
      "wall_seconds": 12650.233256101608
    },
    {
      "attempt": 1,
      "bytes": 1589129,
      "posterior_max": 0.9998999834060669,
      "posterior_min": 9.999999747378752e-05,
      "sample_index": 2,
      "sample_seed": 2,
      "sampling_seconds": 12616.164033174515,
      "sha256": "c00b0e9a2459c1ba82fe20b65ad761933f7235c73887008207079242f14ff37e",
      "smiles": "O=C1CC(C(O)C2CC(CC(O)C(=O)O)C(O)C2O)CC(O)O1",
      "valid_reconstruction": true,
      "wall_seconds": 12637.701331853867
    },
    {
      "attempt": 1,
      "bytes": 1587913,
      "posterior_max": 0.9998999834060669,
      "posterior_min": 9.999999747378752e-05,
      "sample_index": 3,
      "sample_seed": 3,
      "sampling_seconds": 12614.183653116226,
      "sha256": "95663e38f1cc2e06cf9549e7d7fc0a26f22d12d6a6b971786da3e2614c5ece7b",
      "smiles": "O=C(O)c1cc(F)c2c(c1)OCN2C(=O)C1CCCCCCC1",
      "valid_reconstruction": true,
      "wall_seconds": 12635.8560359478
    }
  ],
  "scope": "4 completed ligands from an active 32-ligand AND campaign; not a replacement for the complete paper protocol",
  "status": "partial_campaign_checkpoint",
  "unique_smiles": 4,
  "valid_reconstructions": 4
}

````


````output
{
  "campaign_elapsed_seconds_at_checkpoint": 12659.331600189209,
  "campaign_target_samples": 32,
  "claim": "C4: GRM5/RRM1 molecular composition",
  "completed_samples": 4,
  "docking": {
    "and_not_metric_status": "not_applicable_to_and_samples; requires a separate logdiff_and_not campaign",
    "diagnostic_mean_rrm1_minus_grm5": -0.06299999999999994,
    "diversity": 0.8870539334210088,
    "exhaustiveness": 32,
    "generated_samples": 4,
    "maximum_rrm1_docking": -7.347,
    "mean_and_product": 64.53267625000001,
    "mean_grm5_docking": -8.00375,
    "mean_rrm1_docking": -8.06675,
    "minimum_grm5_docking": -8.282,
    "mode": "vina_full",
    "quality_fraction": 0.5,
    "valid_unique_count": 4,
    "valid_unique_fraction": 1.0
  },
  "merged_sample_sha256": "b0cf5223adfc76ce5389a5253c2481e2612df31d262c7f7dc18ddad6e6f53234",
  "paper": "OAM1jJsMGp",
  "protocol": {
    "compile_forward": true,
    "inverse_temperature_beta": 2.0,
    "logic": "logdiff_and",
    "max_attempts_per_sample": 10,
    "num_atoms": 23,
    "num_steps": 1000,
    "posterior_mc_samples": 1,
    "target_indices": [
      29,
      371
    ],
    "target_names": [
      "GRM5",
      "RRM1"
    ],
    "workers": 4
  },
  "results": [
    {
      "attempt": 1,
      "bytes": 1586377,
      "posterior_max": 0.9998999834060669,
      "posterior_min": 9.999999747378752e-05,
      "sample_index": 0,
      "sample_seed": 0,
      "sampling_seconds": 12637.527888059616,
      "sha256": "9896eb58d849cffd33d2aff6079e2f91cb482788a2fd2a52a6f6ad1f1cfa16e6",
      "smiles": "O=C(O)C(CO)Cc1[nH]c2c3c1CC(F)(F)CC3(F)CCC=C2",
      "valid_reconstruction": true,
      "wall_seconds": 12659.108721017838
    },
    {
      "attempt": 1,
      "bytes": 1586761,
      "posterior_max": 0.9998999834060669,
      "posterior_min": 9.999999747378752e-05,
      "sample_index": 1,
      "sample_seed": 1,
      "sampling_seconds": 12628.873342990875,
      "sha256": "deff243d24acb8b0baf1ca665a9c195594fc10552bd114240faf2aede3fc0f2a",
      "smiles": "CC1OC2(CO)C(=O)C1(O)OC(C(O)CC1CCOC1=O)C2O",
      "valid_reconstruction": true,
      "wall_seconds": 12650.233256101608
    },
    {
      "attempt": 1,
      "bytes": 1589129,
      "posterior_max": 0.9998999834060669,
      "posterior_min": 9.999999747378752e-05,
      "sample_index": 2,
      "sample_seed": 2,
      "sampling_seconds": 12616.164033174515,
      "sha256": "c00b0e9a2459c1ba82fe20b65ad761933f7235c73887008207079242f14ff37e",
      "smiles": "O=C1CC(C(O)C2CC(CC(O)C(=O)O)C(O)C2O)CC(O)O1",
      "valid_reconstruction": true,
      "wall_seconds": 12637.701331853867
    },
    {
      "attempt": 1,
      "bytes": 1587913,
      "posterior_max": 0.9998999834060669,
      "posterior_min": 9.999999747378752e-05,
      "sample_index": 3,
      "sample_seed": 3,
      "sampling_seconds": 12614.183653116226,
      "sha256": "95663e38f1cc2e06cf9549e7d7fc0a26f22d12d6a6b971786da3e2614c5ece7b",
      "smiles": "O=C(O)c1cc(F)c2c(c1)OCN2C(=O)C1CCCCCCC1",
      "valid_reconstruction": true,
      "wall_seconds": 12635.8560359478
    }
  ],
  "scope": "4 completed ligands from an active 32-ligand AND campaign; not a replacement for the complete paper protocol",
  "status": "partial_campaign_checkpoint",
  "unique_smiles": 4,
  "valid_reconstructions": 4
}

````


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_e179e0a0b124", "created_at": "2026-07-20T01:05:39+00:00", "title": "Interim interpretation and scope boundary"}
-->
## Interim full-step molecular evidence (4/32)

This is a scientific checkpoint, not full Claim 4 verification. Four independent AND ligands completed the recovered TargetDiff protocol at 1,000 denoising steps, beta 2.0, 23 atoms, and one posterior sample. All four trajectories were finite, all four reconstructed to valid and distinct SMILES, and all eight generated-ligand AutoDock Vina evaluations succeeded at exhaustiveness 32.

The four-ligand means are GRM5 -8.0038 kcal/mol, RRM1 -8.0668 kcal/mol, AND product 64.5327, diversity 0.8871, valid-unique fraction 1.0, and paper-defined quality fraction 0.5. Same-run reference docking was -5.866 for GRM5 and -7.640 for RRM1. The paper reports LOGDIFF AND product 73.20 +/- 3.18 and DualDiff 71.87 +/- 3.33, so this four-ligand checkpoint is below both reported means and is not treated as confirming the headline magnitude.

The AND-NOT separation metric is intentionally not inferred from these AND samples; it requires the separate logdiff_and_not campaign. The active 32-ligand AND campaign continues with restartable shards, and full Claim 4 assessment remains pending both complete AND and AND-NOT evidence.
