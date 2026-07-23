#!/usr/bin/env bash
set -euo pipefail

stage="${1:-}"
if [[ "${stage}" != "preflight" && "${stage}" != "slice" ]]; then
  echo "usage: bootstrap_oam_replicate_cpu_slice.sh preflight | slice LOGIC RUN_SEED SLICE_ID" >&2
  exit 2
fi
shift

runner=/workspace/hf/run_oam_replicate_cpu_slice.py
requirements=/workspace/hf/requirements-cpu-upgrade.txt
contract=/workspace/configs/oam_hf_cpu_replicates_v1.json
sources_manifest=/workspace/hf_jobs/oam_replicate_cpu_sources.sha256
bootstrap=/workspace/hf_jobs/bootstrap_oam_replicate_cpu_slice.sh
input=/workspace/input/oam-colab-cuda-input.tar.gz
repository=/workspace/oam-repository
route_root=/hf-bucket/hf-jobs/oam-replicates-cpu-v1
contract_sha256="$(sha256sum "${contract}" | awk '{print $1}')"
preflight_root="${route_root}/preflight/contract-${contract_sha256}"

common=(
  --contract "${contract}"
  --input-archive "${input}"
  --repository "${repository}"
  --runner-path "${runner}"
  --requirements-path "${requirements}"
  --bootstrap-path "${bootstrap}"
  --sources-manifest-path "${sources_manifest}"
)

python3 "${runner}" extract "${common[@]}"

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
export PYTHONHASHSEED=0

if [[ "${stage}" == "preflight" ]]; then
  if [[ "$#" -ne 0 ]]; then
    echo "preflight takes no additional arguments" >&2
    exit 2
  fi
  exec /workspace/.venv/bin/python "${runner}" preflight \
    "${common[@]}" \
    --preflight-root "${preflight_root}"
fi

if [[ "$#" -ne 3 ]]; then
  echo "slice requires LOGIC RUN_SEED SLICE_ID" >&2
  exit 2
fi
logic="$1"
run_seed="$2"
slice_id="$3"

read -r sample_start sample_stop < <(
  python3 - "${contract}" "${logic}" "${run_seed}" "${slice_id}" <<'PY'
import json
import sys
contract = json.load(open(sys.argv[1]))
logic, seed, slice_id = sys.argv[2], int(sys.argv[3]), sys.argv[4]
if logic not in contract["scientific_scope"]["allowed_logics"]:
    raise SystemExit("unsupported logic")
if seed == 0 or seed not in contract["scientific_scope"]["allowed_run_seeds"]:
    raise SystemExit("run seed must be in 1..7; seed 0 is forbidden")
matches = [row for row in contract["slices"] if row["slice_id"] == slice_id]
if len(matches) != 1:
    raise SystemExit("unknown slice")
print(matches[0]["sample_start"], matches[0]["sample_stop"])
PY
)

printf -v run_seed_02 '%02d' "${run_seed}"
printf -v sample_start_03 '%03d' "${sample_start}"
printf -v sample_stop_03 '%03d' "${sample_stop}"
slice_root="${route_root}/campaigns/${logic}/run-seed-${run_seed_02}/slice-${slice_id}-samples-${sample_start_03}-${sample_stop_03}/contract-${contract_sha256}"

exec /workspace/.venv/bin/python "${runner}" slice \
  "${common[@]}" \
  --preflight-root "${preflight_root}" \
  --slice-root "${slice_root}" \
  --logic "${logic}" \
  --run-seed "${run_seed}" \
  --slice-id "${slice_id}"
