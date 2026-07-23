#!/usr/bin/env bash
set -euo pipefail

stage="${1:-}"
if [[ "${stage}" != "preflight" && "${stage}" != "full" ]]; then
  echo "usage: bootstrap_oam_seed0_cpu_upgrade.sh {preflight|full}" >&2
  exit 2
fi

runner=/workspace/hf/run_oam_seed0_cpu_upgrade.py
requirements=/workspace/hf/requirements-cpu-upgrade.txt
input=/workspace/input/oam-colab-cuda-input.tar.gz
repository=/workspace/oam-repository
bucket_root=/hf-bucket/hf-jobs/seed0-cpu-migration-v1

python3 "${runner}" extract \
  --input-archive "${input}" \
  --repository "${repository}"

uv venv /workspace/.venv --python 3.12
uv pip install --python /workspace/.venv/bin/python \
  --index-url https://download.pytorch.org/whl/cpu \
  'torch==2.9.0+cpu'
uv pip install --python /workspace/.venv/bin/python -r "${requirements}"
uv pip install --python /workspace/.venv/bin/python \
  --find-links 'https://data.pyg.org/whl/torch-2.9.0+cpu.html' \
  'torch_scatter==2.1.2+pt29cpu' \
  'torch_cluster==1.6.3+pt29cpu'

export WANDB_MODE=disabled
export WANDB_SILENT=true
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1

if [[ "${stage}" == "preflight" ]]; then
  exec /workspace/.venv/bin/python "${runner}" preflight \
    --input-archive "${input}" \
    --repository "${repository}" \
    --bucket-root "${bucket_root}"
fi

exec /workspace/.venv/bin/python "${runner}" full \
  --input-archive "${input}" \
  --repository "${repository}" \
  --bucket-root "${bucket_root}" \
  --cutover-archive /workspace/cutover/oam-seed0-cutover.tar.gz \
  --cutover-manifest /workspace/cutover/CUTOVER.json \
  --workers 8 \
  --max-wall-hours 5.25
