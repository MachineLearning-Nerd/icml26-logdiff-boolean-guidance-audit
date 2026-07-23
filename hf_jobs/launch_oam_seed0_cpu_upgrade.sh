#!/usr/bin/env bash
set -euo pipefail

if [[ "${OAM_CPU_LAUNCH_LOCK_HELD:-}" != "1" ]]; then
  exec python3 - "/tmp/oam-seed0-cpu-migration-v1.launch.lock" "$0" "$@" <<'PY'
import fcntl
import os
import sys
from pathlib import Path

descriptor = os.open(sys.argv[1], os.O_CREAT | os.O_RDWR, 0o600)
fcntl.flock(descriptor, fcntl.LOCK_EX)
os.set_inheritable(descriptor, True)
environment = dict(os.environ)
environment["OAM_CPU_LAUNCH_LOCK_HELD"] = "1"
os.execvpe("bash", ["bash", str(Path(sys.argv[2]).resolve()), *sys.argv[3:]], environment)
PY
fi

stage="${1:-}"
shift || true
dry_run=0
if [[ "${1:-}" == "--dry-run" ]]; then
  dry_run=1
  shift
fi
if [[ "${stage}" != "preflight" && "${stage}" != "full" ]] || [[ "$#" -ne 0 ]]; then
  echo "usage: bash hf_jobs/launch_oam_seed0_cpu_upgrade.sh {preflight|full} [--dry-run]" >&2
  exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
paper_root="$(cd "${script_dir}/.." && pwd)"
manifest="${script_dir}/oam_seed0_cpu_upgrade_sources.sha256"
ledger="${paper_root}/../../icml-2026-reproduction-challenge/HF_JOBS_BUDGET.md"
input_dir="${paper_root}/outputs/molecular-recovery/colab-cuda-handoff"
input_archive="${input_dir}/oam-colab-cuda-input.tar.gz"
input_sha256="a0bbb9678f72cb2239fb1dec62fc8decb8ee0706a97e19e0ec6a59983c7c3958"
cutover_dir="${paper_root}/outputs/molecular-recovery/hf-cpu-upgrade/seed0-migration-v1/staging"
bucket_id="DineshAI/OAM1jJsMGp-artifacts"
bucket_uri="hf://buckets/${bucket_id}"
remote_root="${bucket_uri}/hf-jobs/seed0-cpu-migration-v1"
image="ghcr.io/astral-sh/uv:python3.12-bookworm"

if [[ "${stage}" == "preflight" ]]; then
  timeout="1h"
  max_cost_usd="0.03"
  job_name="oam-seed0-cpu-upgrade-preflight-v2"
  expected_ledger_id="pending-oam-seed0-cpu-upgrade-preflight-v2"
else
  timeout="6h"
  max_cost_usd="0.18"
  job_name="oam-seed0-cpu-upgrade-full-v1"
  expected_ledger_id="pending-oam-seed0-cpu-upgrade-full-v1"
fi

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
    observed = hashlib.sha256(path.read_bytes()).hexdigest()
    if observed != digest:
        raise SystemExit(f"source hash mismatch at line {number}: {relative}")
    print(f"{relative}: OK")
PY

observed_input_sha256="$(shasum -a 256 "${input_archive}" | awk '{print $1}')"
if [[ "${observed_input_sha256}" != "${input_sha256}" ]]; then
  echo "refusing launch: frozen scientific input archive drift" >&2
  exit 3
fi

if [[ "${dry_run}" -eq 1 ]]; then
  printf 'stage=%s flavor=cpu-upgrade timeout=%s max_cost_usd=%s\n' "${stage}" "${timeout}" "${max_cost_usd}"
  printf 'bucket=%s remote_root=%s\n' "${bucket_id}" "${remote_root}"
  printf 'input_sha256=%s\n' "${input_sha256}"
  printf 'requires_budget_reservation=OAM_HF_BUDGET_RESERVED=1\n'
  if [[ "${stage}" == "full" ]]; then
    printf 'requires_cutover=OAM_HF_CUTOVER_AUTHORIZED=1 and validated staged checkpoint\n'
  fi
  exit 0
fi

if [[ "${OAM_HF_BUDGET_RESERVED:-}" != "1" ]]; then
  echo "refusing launch: root must reserve USD ${max_cost_usd} in the shared HF budget ledger first" >&2
  exit 4
fi
python3 - "${ledger}" "${expected_ledger_id}" "${max_cost_usd}" <<'PY'
import sys
from pathlib import Path

ledger, expected_id, maximum = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
matches = []
for line in ledger.read_text().splitlines():
    if line.startswith("|") and f"`{expected_id}`" in line:
        matches.append(line)
if len(matches) != 1:
    raise SystemExit(f"shared ledger must contain exactly one reserved row for {expected_id}")
row = matches[0]
if "`cpu-upgrade`" not in row or "reserved; not yet submitted" not in row:
    raise SystemExit(f"shared ledger row is not a pending cpu-upgrade reservation: {expected_id}")
if f"<=USD {maximum}" not in row:
    raise SystemExit(f"shared ledger row does not reserve the exact USD {maximum} ceiling")
PY

active_local="$(ps -axo pid=,ppid=,command= | python3 -c '
import json, os, sys
rows=[]
for line in sys.stdin:
    parts=line.strip().split(maxsplit=2)
    if len(parts)!=3: continue
    pid,ppid,command=int(parts[0]),int(parts[1]),parts[2]
    if pid == os.getpid(): continue
    if "run_parallel_molecular_protocol.py --logic logdiff_and --run-seed 0" in command or ("compose_sample_score.py" in command and "full-protocol-shards/logdiff_and/run-seed-00" in command):
        rows.append({"pid":pid,"ppid":ppid,"command":command})
print(json.dumps(rows))
')"

if [[ "${stage}" == "full" ]]; then
  if [[ "${OAM_HF_CUTOVER_AUTHORIZED:-}" != "1" ]]; then
    echo "refusing full launch: explicit root cutover authorization is absent" >&2
    exit 5
  fi
  if [[ "${active_local}" != "[]" ]]; then
    echo "refusing full launch: local seed-0 processes remain active and were not modified" >&2
    echo "${active_local}" >&2
    exit 6
  fi
  python3 - "${cutover_dir}" "${input_sha256}" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

root, expected_input = Path(sys.argv[1]), sys.argv[2]
manifest = root / "CUTOVER.json"
archive = root / "oam-seed0-cutover.tar.gz"
sidecar = root / "oam-seed0-cutover.tar.gz.sha256"
for path in (manifest, archive, sidecar):
    if not path.is_file():
        raise SystemExit(f"cutover artifact missing: {path}")
value = json.loads(manifest.read_text())
if value.get("local_processes_absent") is not True or value.get("launch_authorized") is not False:
    raise SystemExit("cutover process/authorization invariant failed")
if value.get("completed_count", 0) < 16 or value.get("completed_count", 0) >= 32:
    raise SystemExit("cutover completed count is outside migration range")
if value.get("frozen_scientific_input", {}).get("sha256") != expected_input:
    raise SystemExit("cutover input binding mismatch")
observed = hashlib.sha256(archive.read_bytes()).hexdigest()
recorded = sidecar.read_text().split()[0]
if observed != recorded:
    raise SystemExit("cutover archive sidecar mismatch")
print(json.dumps({"cutover_completed": value["completed_count"], "cutover_archive_sha256": observed}, sort_keys=True))
PY
  temporary_dir="$(mktemp -d)"
  trap 'rm -rf "${temporary_dir}"' EXIT
  hf cp "${remote_root}/reports/PREFLIGHT.json" "${temporary_dir}/PREFLIGHT.json"
  python3 - "${temporary_dir}/PREFLIGHT.json" "${input_sha256}" <<'PY'
import json, sys
value=json.load(open(sys.argv[1]))
if value.get("stage") != "preflight" or value.get("status") != "passed":
    raise SystemExit("remote CPU preflight has not passed")
if value.get("input_archive_sha256") != sys.argv[2]:
    raise SystemExit("remote CPU preflight input binding mismatch")
PY
fi

command -v hf >/dev/null
command -v jq >/dev/null
hf auth whoami --format json >/dev/null
rate="$(hf jobs hardware --format json | jq -r '.[] | select(.name == "cpu-upgrade") | .["cost/hour"]')"
if [[ "${rate}" != '$0.03' ]]; then
  echo "refusing launch: expected cpu-upgrade rate USD 0.03/hour, observed ${rate}" >&2
  exit 7
fi

read_active_jobs() {
  hf jobs list --status RUNNING,SCHEDULING --limit 0 --format json
}

guard_active_jobs() {
  local active_json="$1"
  OAM_ACTIVE_JOBS_JSON="${active_json}" python3 - "${job_name}" <<'PY'
import json, os, sys
name=sys.argv[1]
jobs=json.loads(os.environ["OAM_ACTIVE_JOBS_JSON"])
cpu=[{"id":j.get("id"),"status":j.get("status"),"flavor":j.get("flavor"),"labels":j.get("labels",{}),"url":j.get("url")} for j in jobs if j.get("flavor")=="cpu-upgrade"]
duplicates=[j for j in jobs if j.get("labels",{}).get("name")==name or (j.get("labels",{}).get("paper")=="OAM1jJsMGp" and j.get("labels",{}).get("campaign")=="seed0-cpu-migration-v1")]
if duplicates:
    print("refusing launch: an OAM seed-0 migration job is already active: "+json.dumps(duplicates,sort_keys=True),file=sys.stderr)
    raise SystemExit(8)
if cpu:
    print("deferring launch: account-wide cpu-upgrade is in use; existing jobs were not modified: "+json.dumps(cpu,sort_keys=True),file=sys.stderr)
    raise SystemExit(9)
PY
}

guard_active_jobs "$(read_active_jobs)"

command=(
  hf jobs run
  --detach
  --name "${job_name}"
  --label paper=OAM1jJsMGp
  --label campaign=seed0-cpu-migration-v1
  --label phase="${stage}"
  --flavor cpu-upgrade
  --timeout "${timeout}"
  --volume "${paper_root}/repro/hf:/workspace/hf:ro"
  --volume "${paper_root}/hf_jobs:/workspace/hf_jobs:ro"
  --volume "${input_dir}:/workspace/input:ro"
)
if [[ "${stage}" == "full" ]]; then
  command+=(--volume "${cutover_dir}:/workspace/cutover:ro")
fi
command+=(
  --volume "${bucket_uri}:/hf-bucket:rw"
  --
  "${image}"
  /bin/bash /workspace/hf_jobs/bootstrap_oam_seed0_cpu_upgrade.sh "${stage}"
)

# A second read narrows the shared-account check-to-submit race. No existing
# job is cancelled, paused, killed, relabelled, or otherwise mutated.
guard_active_jobs "$(read_active_jobs)"
exec "${command[@]}"
