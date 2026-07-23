#!/usr/bin/env bash
set -euo pipefail

if [[ "${OAM_REPLICATE_LAUNCH_LOCK_HELD:-}" != "1" ]]; then
  exec python3 - "/tmp/oam-replicates-cpu-v1.launch.lock" "$0" "$@" <<'PY'
import fcntl
import os
import sys
from pathlib import Path

descriptor = os.open(sys.argv[1], os.O_CREAT | os.O_RDWR, 0o600)
fcntl.flock(descriptor, fcntl.LOCK_EX)
os.set_inheritable(descriptor, True)
environment = dict(os.environ)
environment["OAM_REPLICATE_LAUNCH_LOCK_HELD"] = "1"
os.execvpe("bash", ["bash", str(Path(sys.argv[2]).resolve()), *sys.argv[3:]], environment)
PY
fi

stage="${1:-}"
shift || true
logic=""
run_seed=""
slice_id=""
if [[ "${stage}" == "slice" ]]; then
  logic="${1:-}"
  run_seed="${2:-}"
  slice_id="${3:-}"
  shift 3 || true
elif [[ "${stage}" != "preflight" ]]; then
  echo "usage: launch_oam_replicate_cpu_slice.sh preflight [--dry-run] | slice LOGIC RUN_SEED SLICE_ID [--dry-run]" >&2
  exit 2
fi

dry_run=0
if [[ "${1:-}" == "--dry-run" ]]; then
  dry_run=1
  shift
fi
if [[ "$#" -ne 0 ]]; then
  echo "unexpected launcher arguments" >&2
  exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
paper_root="$(cd "${script_dir}/.." && pwd)"
manifest="${script_dir}/oam_replicate_cpu_sources.sha256"
ledger="${paper_root}/../../icml-2026-reproduction-challenge/HF_JOBS_BUDGET.md"
contract="${paper_root}/repro/configs/oam_hf_cpu_replicates_v1.json"
input_dir="${paper_root}/outputs/molecular-recovery/colab-cuda-handoff"
input_archive="${input_dir}/oam-colab-cuda-input.tar.gz"
bucket_id="DineshAI/OAM1jJsMGp-artifacts"
bucket_uri="hf://buckets/${bucket_id}"
route_uri="${bucket_uri}/hf-jobs/oam-replicates-cpu-v1"
image="ghcr.io/astral-sh/uv:python3.12-bookworm"

python3 - "${paper_root}" "${manifest}" <<'PY'
import hashlib
import sys
from pathlib import Path

root, manifest = Path(sys.argv[1]), Path(sys.argv[2])
if not manifest.is_file():
    raise SystemExit("source integrity manifest is missing")
for number, line in enumerate(manifest.read_text().splitlines(), start=1):
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    digest, relative = line.split(maxsplit=1)
    path = root / relative.lstrip("*")
    if not path.is_file():
        raise SystemExit(f"source missing at line {number}: {relative}")
    observed = hashlib.sha256(path.read_bytes()).hexdigest()
    if observed != digest:
        raise SystemExit(f"source hash mismatch at line {number}: {relative}")
PY

contract_values="$(python3 - "${contract}" "${stage}" "${logic}" "${run_seed}" "${slice_id}" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

path, stage, logic, raw_seed, slice_id = Path(sys.argv[1]), *sys.argv[2:]
contract = json.loads(path.read_text())
if contract.get("paper") != "OAM1jJsMGp" or contract.get("route_id") != "oam-replicates-cpu-v1":
    raise SystemExit("contract identity mismatch")
if contract.get("launch_authorized") is not False:
    raise SystemExit("contract must not self-authorize")
digest = hashlib.sha256(path.read_bytes()).hexdigest()
if stage == "preflight":
    print(digest, "-", "-", "-")
else:
    if logic not in contract["scientific_scope"]["allowed_logics"]:
        raise SystemExit("unsupported logic")
    try:
        seed = int(raw_seed)
    except ValueError as error:
        raise SystemExit("run seed must be an integer") from error
    if seed == 0 or seed not in contract["scientific_scope"]["allowed_run_seeds"]:
        raise SystemExit("run seed must be in 1..7; seed 0 is forbidden")
    rows = [row for row in contract["slices"] if row["slice_id"] == slice_id]
    if len(rows) != 1:
        raise SystemExit("unknown slice")
    print(digest, rows[0]["sample_start"], rows[0]["sample_stop"], f"{seed:02d}")
PY
)"
read -r contract_sha256 sample_start sample_stop run_seed_02 <<< "${contract_values}"

observed_input_sha256="$(shasum -a 256 "${input_archive}" | awk '{print $1}')"
expected_input_sha256="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["frozen_input"]["sha256"])' "${contract}")"
if [[ "${observed_input_sha256}" != "${expected_input_sha256}" ]]; then
  echo "refusing launch: frozen input archive drift" >&2
  exit 3
fi

if [[ "${stage}" == "preflight" ]]; then
  timeout="1h"
  max_cost_usd="0.03"
  job_name="oam-replicates-cpu-preflight-v1"
  expected_ledger_id="pending-oam-replicates-cpu-preflight-v1"
  phase="preflight"
else
  timeout="6h"
  max_cost_usd="0.18"
  job_name="oam-${logic}-seed${run_seed_02}-${slice_id}-cpu-v1"
  expected_ledger_id="pending-oam-replicates-${logic}-seed${run_seed_02}-${slice_id}-v1"
  phase="slice"
fi

if [[ "${dry_run}" -eq 1 ]]; then
  printf 'stage=%s paper=OAM1jJsMGp campaign=oam-replicates-cpu-v1 flavor=cpu-upgrade timeout=%s max_cost_usd=%s\n' "${stage}" "${timeout}" "${max_cost_usd}"
  printf 'contract_sha256=%s input_sha256=%s bucket=%s\n' "${contract_sha256}" "${expected_input_sha256}" "${bucket_id}"
  if [[ "${stage}" == "slice" ]]; then
    printf 'logic=%s run_seed=%s slice_id=%s sample_range=[%s,%s)\n' "${logic}" "${run_seed}" "${slice_id}" "${sample_start}" "${sample_stop}"
  fi
  printf 'requires=OAM_HF_REPLICATES_AUTHORIZED=1 OAM_HF_BUDGET_RESERVED=1 ledger_id=%s\n' "${expected_ledger_id}"
  exit 0
fi

if [[ "${OAM_HF_REPLICATES_AUTHORIZED:-}" != "1" ]]; then
  echo "refusing launch: explicit OAM replicate-route authorization is absent" >&2
  exit 4
fi
if [[ "${OAM_HF_BUDGET_RESERVED:-}" != "1" ]]; then
  echo "refusing launch: USD ${max_cost_usd} must be reserved in the shared ledger first" >&2
  exit 5
fi

python3 - "${ledger}" "${expected_ledger_id}" "${max_cost_usd}" <<'PY'
import re
import sys
from pathlib import Path

ledger, expected_id, maximum = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
text = ledger.read_text()
if "Authorized cap: **USD 40.00**" not in text:
    raise SystemExit("shared aggregate cap is not exactly USD 40.00")
matches = [line for line in text.splitlines() if line.startswith("|") and f"`{expected_id}`" in line]
if len(matches) != 1:
    raise SystemExit(f"shared ledger must contain exactly one reservation for {expected_id}")
row = matches[0]
if "`cpu-upgrade`" not in row or "reserved; not submitted" not in row:
    raise SystemExit("ledger row is not an unsubmitted cpu-upgrade reservation")
if f"<=USD {maximum}" not in row:
    raise SystemExit(f"ledger row does not reserve exact ceiling <=USD {maximum}")
balance = re.search(r"Uncommitted balance: \*\*USD ([0-9]+(?:\.[0-9]+)?)\*\*", text)
if balance is None or float(balance.group(1)) < 0:
    raise SystemExit("shared ledger has no nonnegative uncommitted balance")
PY

command -v hf >/dev/null
command -v jq >/dev/null
hf auth whoami --format json | jq -e '.user == "DineshAI"' >/dev/null
rate="$(hf jobs hardware --format json | jq -r '.[] | select(.name == "cpu-upgrade") | .["cost/hour"]')"
if [[ "${rate}" != '$0.03' ]]; then
  echo "refusing launch: expected cpu-upgrade rate USD 0.03/hour, observed ${rate}" >&2
  exit 6
fi

if [[ "${stage}" == "slice" ]]; then
  temporary_dir="$(mktemp -d)"
  trap 'rm -rf "${temporary_dir}"' EXIT
  preflight_uri="${route_uri}/preflight/contract-${contract_sha256}"
  hf cp "${preflight_uri}/PREFLIGHT.json" "${temporary_dir}/PREFLIGHT.json"
  hf cp "${preflight_uri}/SUCCESS.json" "${temporary_dir}/SUCCESS.json"
  python3 - "${temporary_dir}" "${contract}" "${manifest}" "${paper_root}" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

root, contract_path, manifest_path, paper_root = map(Path, sys.argv[1:])
contract_sha = hashlib.sha256(contract_path.read_bytes()).hexdigest()
report = json.loads((root / "PREFLIGHT.json").read_text())
success = json.loads((root / "SUCCESS.json").read_text())
if report.get("status") != "passed" or report.get("scientific_evidence") is not False:
    raise SystemExit("contract-bound remote preflight has not passed")
if success.get("report_sha256") != hashlib.sha256((root / "PREFLIGHT.json").read_bytes()).hexdigest():
    raise SystemExit("remote preflight success hash mismatch")
binding = report.get("binding", {})
if binding.get("contract_sha256") != contract_sha:
    raise SystemExit("remote preflight contract mismatch")
if binding.get("input_archive_sha256") != json.loads(contract_path.read_text())["frozen_input"]["sha256"]:
    raise SystemExit("remote preflight input mismatch")
expected = {
    "runner": paper_root / "repro/hf/run_oam_replicate_cpu_slice.py",
    "requirements": paper_root / "repro/hf/requirements-cpu-upgrade.txt",
    "bootstrap": paper_root / "hf_jobs/bootstrap_oam_replicate_cpu_slice.sh",
    "sources_manifest": manifest_path,
}
observed = binding.get("source_files", {})
for name, path in expected.items():
    if observed.get(name) != hashlib.sha256(path.read_bytes()).hexdigest():
        raise SystemExit(f"remote preflight source drift: {name}")
projection = report.get("projection", {})
if float(projection.get("slice_hours", 99)) > 5.25:
    raise SystemExit("remote measured slice projection exceeds 5.25 hours")
if float(projection.get("slice_cost_usd_at_0.03_per_hour", 99)) > 0.18:
    raise SystemExit("remote measured slice projection exceeds USD 0.18")
PY

  printf -v sample_start_03 '%03d' "${sample_start}"
  printf -v sample_stop_03 '%03d' "${sample_stop}"
  slice_uri="${route_uri}/campaigns/${logic}/run-seed-${run_seed_02}/slice-${slice_id}-samples-${sample_start_03}-${sample_stop_03}/contract-${contract_sha256}"
  if hf cp "${slice_uri}/SUCCESS.json" "${temporary_dir}/SLICE_SUCCESS.json" 2>/dev/null; then
    hf cp "${slice_uri}/SLICE_MANIFEST.json" "${temporary_dir}/SLICE_MANIFEST.json"
    python3 - "${temporary_dir}" "${logic}" "${run_seed}" "${slice_id}" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

root, logic, raw_seed, slice_id = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
preflight = json.loads((root / "PREFLIGHT.json").read_text())
success = json.loads((root / "SLICE_SUCCESS.json").read_text())
manifest_path = root / "SLICE_MANIFEST.json"
manifest = json.loads(manifest_path.read_text())
seed = int(raw_seed)
if success.get("status") != "complete":
    raise SystemExit("existing slice SUCCESS has invalid status")
if success.get("logic") != logic or success.get("run_seed") != seed or success.get("slice_id") != slice_id:
    raise SystemExit("existing slice SUCCESS identity mismatch")
if success.get("binding") != preflight.get("binding") or manifest.get("binding") != preflight.get("binding"):
    raise SystemExit("existing slice has mixed source/environment binding")
if success.get("slice_manifest_sha256") != hashlib.sha256(manifest_path.read_bytes()).hexdigest():
    raise SystemExit("existing slice manifest digest mismatch")
raise SystemExit("refusing launch: this exact condition/seed/slice is already successful")
PY
  fi
fi

read_active_jobs() {
  hf jobs list --status RUNNING,SCHEDULING --limit 0 --format json
}

guard_exact_duplicate() {
  local active_json="$1"
  OAM_ACTIVE_JOBS_JSON="${active_json}" python3 - "${stage}" "${logic}" "${run_seed}" <<'PY'
import json
import os
import sys

stage, logic, run_seed = sys.argv[1:]
jobs = json.loads(os.environ["OAM_ACTIVE_JOBS_JSON"])
duplicates = []
for job in jobs:
    labels = job.get("labels", {})
    if labels.get("paper") != "OAM1jJsMGp" or labels.get("campaign") != "oam-replicates-cpu-v1":
        continue
    if stage == "preflight":
        duplicate = labels.get("phase") == "preflight"
    else:
        duplicate = labels.get("logic") == logic and labels.get("run_seed") == run_seed
    if duplicate:
        duplicates.append({
            "id": job.get("id"), "status": job.get("status"),
            "flavor": job.get("flavor"), "labels": labels, "url": job.get("url"),
        })
if duplicates:
    raise SystemExit("refusing launch: exact OAM condition/seed work is active: " + json.dumps(duplicates, sort_keys=True))
PY
}

guard_exact_duplicate "$(read_active_jobs)"

command=(
  hf jobs run
  --detach
  --name "${job_name}"
  --label paper=OAM1jJsMGp
  --label campaign=oam-replicates-cpu-v1
  --label phase="${phase}"
  --label contract_sha256="${contract_sha256}"
  --flavor cpu-upgrade
  --timeout "${timeout}"
  --volume "${paper_root}/repro/hf:/workspace/hf:ro"
  --volume "${paper_root}/repro/configs:/workspace/configs:ro"
  --volume "${paper_root}/hf_jobs:/workspace/hf_jobs:ro"
  --volume "${input_dir}:/workspace/input:ro"
  --volume "${bucket_uri}:/hf-bucket:rw"
)
if [[ "${stage}" == "slice" ]]; then
  command+=(
    --label logic="${logic}"
    --label run_seed="${run_seed}"
    --label slice_id="${slice_id}"
  )
fi
command+=(
  --
  "${image}"
  /bin/bash /workspace/hf_jobs/bootstrap_oam_replicate_cpu_slice.sh
  "${stage}"
)
if [[ "${stage}" == "slice" ]]; then
  command+=("${logic}" "${run_seed}" "${slice_id}")
fi

# The second read narrows the check-to-submit race. Unrelated Jobs are only
# observed and never blocked, cancelled, paused, killed, or relabelled.
guard_exact_duplicate "$(read_active_jobs)"
exec "${command[@]}"
