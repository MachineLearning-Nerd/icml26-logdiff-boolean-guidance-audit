# Campaign command ledger

This ledger records the exact commands that changed campaign state, produced
scientific evidence, queried primary evidence sources, or enforced release
gates. Read-only formatting and file-inspection commands are preserved in the
session transcript; they do not alter the scientific result.

## Startup and source audit

```text
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs b9dd34be-c3e8-4d56-badc-224106c43fff
orx project view b9dd34be-c3e8-4d56-badc-224106c43fff
git branch --show-current
git rev-parse HEAD
git rev-parse main
git rev-parse origin/main
git status --short
git branch -a
df -h .
env
curl -L --fail --silent --show-error -A 'OpenResearch-Reproduction-Audit/1.0 (+https://github.com/MachineLearning-Nerd/icml26-repro-OAM1jJsMGp-logdiff-exact-boolean-guidance)' https://ar5iv.labs.arxiv.org/html/2602.05549 -o /tmp/oam-paper.html
orx paper 2602.05549 --full
```

The `env` inspection retained names only; no environment values, tokens, or
generated wrappers were printed into evidence.

## Fixed verifier and experiment orchestration

Every launched node used this exact inherited command:

```text
uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25
```

The tree was created and run with:

```text
orx create-experiment b9dd34be-c3e8-4d56-badc-224106c43fff --title "Frozen cumulative baseline" --run-command "uv sync --frozen && uv run python repro/src/run_logdiff.py --output-dir .openresearch/artifacts --seeds 25"
orx exp run c3284853-d298-48e8-9981-f5d184b5c135 --backend local
orx exp wait c3284853-d298-48e8-9981-f5d184b5c135 --timeout 480
orx create-experiment b9dd34be-c3e8-4d56-badc-224106c43fff --title "CelebA exact claim audit" --parent c3284853-d298-48e8-9981-f5d184b5c135
orx exp run 12b39aa0-befc-42ab-9e5a-94a1ce4e6920 --backend local
orx exp wait 12b39aa0-befc-42ab-9e5a-94a1ce4e6920 --timeout 480
orx create-experiment b9dd34be-c3e8-4d56-badc-224106c43fff --title "Molecular evidence recovery audit" --parent c3284853-d298-48e8-9981-f5d184b5c135
orx exp run d7768386-2460-439c-91f0-a8971781b5e1 --backend local
orx exp wait d7768386-2460-439c-91f0-a8971781b5e1 --timeout 480
orx create-experiment b9dd34be-c3e8-4d56-badc-224106c43fff --title "CelebA evaluator-visible evidence" --parent 12b39aa0-befc-42ab-9e5a-94a1ce4e6920
orx exp run f597538d-6a1a-40b1-a8a8-21d81b73fc48 --backend local
orx exp wait f597538d-6a1a-40b1-a8a8-21d81b73fc48 --timeout 480
orx create-experiment b9dd34be-c3e8-4d56-badc-224106c43fff --title "Molecular evaluator-visible evidence" --parent d7768386-2460-439c-91f0-a8971781b5e1
orx exp run 6936a3f8-b852-4dbb-b1e5-b850c4722a34 --backend local
orx exp wait 6936a3f8-b852-4dbb-b1e5-b850c4722a34 --timeout 480
orx create-experiment b9dd34be-c3e8-4d56-badc-224106c43fff --title "Cumulative exact-claim release candidate" --parent 6936a3f8-b852-4dbb-b1e5-b850c4722a34
orx exp run f90e1a54-324c-491f-89bd-3631024508da --backend local
orx exp wait f90e1a54-324c-491f-89bd-3631024508da --timeout 480
orx create-experiment b9dd34be-c3e8-4d56-badc-224106c43fff --title "Evaluator-visible cumulative artifact" --parent f90e1a54-324c-491f-89bd-3631024508da
orx exp run 1005e61e-2df8-4143-8fca-448d809b9c95 --backend local
orx exp wait 1005e61e-2df8-4143-8fca-448d809b9c95 --timeout 480
orx create-experiment b9dd34be-c3e8-4d56-badc-224106c43fff --title "CSV-aware evaluator release audit" --parent 1005e61e-2df8-4143-8fca-448d809b9c95
orx exp run de592fdd-01f9-40d0-b9f2-05a9f2225ae5 --backend local
orx exp wait de592fdd-01f9-40d0-b9f2-05a9f2225ae5 --timeout 480
orx create-experiment b9dd34be-c3e8-4d56-badc-224106c43fff --title "Publication surface and illustrated report" --parent de592fdd-01f9-40d0-b9f2-05a9f2225ae5
orx exp run 32c60687-2c23-4116-b455-18dd9884b087 --backend local
orx exp wait 32c60687-2c23-4116-b455-18dd9884b087 --timeout 480
orx create-experiment b9dd34be-c3e8-4d56-badc-224106c43fff --title "Final release metadata and provenance" --parent 32c60687-2c23-4116-b455-18dd9884b087
```

One evaluator-visible run exited nonzero because `.csv` was not yet classified
as a text upload suffix. That branch was preserved; its child corrected the
release audit and passed.

## Claim 3 primary-source routes

```text
uv run python repro/src/check_claim3_release.py .openresearch/artifacts
curl -A 'OpenResearch-Reproduction-Audit/1.0' -sS 'https://api.github.com/repos/TanjaBien/LogDiff/branches?per_page=100'
curl -A 'OpenResearch-Reproduction-Audit/1.0' -sS 'https://api.github.com/repos/TanjaBien/LogDiff/releases?per_page=100'
curl -A 'OpenResearch-Reproduction-Audit/1.0' -sS 'https://huggingface.co/api/models?search=TanjaBien&limit=100'
curl -A 'OpenResearch-Reproduction-Audit/1.0' -sS 'https://huggingface.co/api/models?search=epoch_epoch%3D589-step_step%3D750000.ckpt&limit=100'
curl -A 'OpenResearch-Reproduction-Audit/1.0' -sS 'https://huggingface.co/api/models/shalpin87/diffusion_celeba/revision/91d0ff0'
curl -A 'OpenResearch-Reproduction-Audit/1.0' -sS 'https://huggingface.co/api/models/shalpin87/diffusion_celeba/tree/91d0ff096e031c21b8313bd5877316a52900d4ec?recursive=true&expand=false'
```

## Claim 4 primary-source routes

```text
uv run python repro/src/check_claim4_evidence.py .openresearch/artifacts
curl -A 'OpenResearch-Reproduction-Audit/1.0' -sS https://api.github.com/repos/nec-research/Logical-Guidance-for-the-Exact-Composition-of-Diffusion-Models
git ls-remote https://github.com/martaskrt/fkc-diffusion.git
curl -A 'OpenResearch-Reproduction-Audit/1.0' -sS https://api.github.com/repos/martaskrt/fkc-diffusion/commits/aa6f5ed4a0ebb91329d4cd5823cc7e77c5e196e6
curl -A 'OpenResearch-Reproduction-Audit/1.0' -sS 'https://api.github.com/repos/martaskrt/fkc-diffusion/git/trees/aa6f5ed4a0ebb91329d4cd5823cc7e77c5e196e6?recursive=1'
curl -A 'OpenResearch-Reproduction-Audit/1.0' -sS 'https://huggingface.co/api/models?search=Logical%20Guidance%20Exact%20Composition%20Diffusion%20Models&limit=100'
orx lit 'DualDiff dual-target molecular generation GRM5 RRM1 diffusion'
orx lit 'FKC diffusion molecular generation martaskrt'
```

## Presentation and release checks

```text
rsvg-convert -w 1600 -o reports/claim-by-claim/images/headline-verdicts.png reports/claim-by-claim/images/headline-verdicts.svg
rsvg-convert -w 1600 -o reports/claim-by-claim/images/table2-range-audit.png reports/claim-by-claim/images/table2-range-audit.svg
rsvg-convert -w 1600 -o reports/claim-by-claim/images/theorem-certificates.png reports/claim-by-claim/images/theorem-certificates.svg
rsvg-convert -w 1600 -o reports/claim-by-claim/images/blocked-claims.png reports/claim-by-claim/images/blocked-claims.svg
marimo check --strict notebooks/logdiff_reproduction.py
git diff --check
```

The exact Hugging Face commit-API upload, post-publication clone, manifest
verification, and `git ls-remote` commands are appended to the dashboard copy
of this ledger only after they have actually executed.
