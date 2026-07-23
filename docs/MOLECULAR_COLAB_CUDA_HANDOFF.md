# OAM molecular Colab CUDA handoff

## Status and scientific boundary

This is a prepared, fail-closed handoff for the fourteen missing molecular
experiments: seeds 1--7 for `logdiff_and` and seeds 1--7 for
`logdiff_and_not`. It has **not** been launched. No paid compute is authorized.
The active local seed-0 work remains read-only and is not present in either the
input or return bundle.

CUDA is conditionally supported by the recovered stack. The sampler already
selects `cuda:0`; model weights and inputs move to that device; and the CUDA
graph path uses the upstream `torch-cluster` and `torch-scatter` kernels rather
than the Apple-MPS fallback. The equations, recovered weights, FP32 precision,
and paper protocol remain fixed. CUDA results are not expected to be bitwise
identical to the local CPU seed-0 result because the kernels and random-number
implementations differ. Consequently, the final eight-run aggregate is
hardware-heterogeneous even though AND and AND-NOT remain strictly separated.

There is no local CUDA device, so scientific execution is blocked until all
three remote gates pass on the pinned runtime:

1. exact runtime, package, source, input, GPU, CUDA-kernel, and model-load
   preflight;
2. one compiled one-step forward compatibility probe;
3. one compiled 20-step timing calibration.

The last two probes are labeled non-evidence. A changed GPU model, runtime,
package, source, plan, or input manifest invalidates resume and requires the
gates to be rerun. This is intentional.

## Pinned basis

- Google Colab runtime version: `2026.04`
- Ubuntu: `22.04.5 LTS`
- Python: `3.12.13`
- NumPy: `2.0.2`
- PyTorch: `2.10.0+cu128`; CUDA `12.8`
- Official runtime listing: <https://research.google.com/colaboratory/runtime-version-faq.html>
- Exact official environment snapshot: <https://github.com/googlecolab/backend-info/tree/77d5dbef56d73b96db5efef2280679cb548c9bd9>
- Official PyG installation guidance: <https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html>
- Exact PyTorch 2.10 / CUDA 12.8 extension wheels: <https://data.pyg.org/whl/torch-2.10.0+cu128.html>
- Colab runtime limitations: <https://research.google.com/colaboratory/faq.html>

The driver requires exactly one GPU, compute capability at least 7.0, and at
least 8 GiB VRAM. It records `nvidia-smi`, driver, device, runtime, package,
source, plan, and input identities. Colab GPU type and availability are not
guaranteed, and free runtimes are generally limited to at most twelve hours.

## Transport artifacts

All paths below are relative to this paper directory.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `outputs/molecular-recovery/colab-cuda-handoff/oam-colab-cuda-input.tar.gz` | `63,049,318` | `a0bbb9678f72cb2239fb1dec62fc8decb8ee0706a97e19e0ec6a59983c7c3958` |
| `outputs/molecular-recovery/colab-cuda-handoff/oam-colab-cuda-input.tar.gz.sha256` | `94` | `b8187134567b536a1472df92abab80a0cdfbb84a63784cce9e4d1bcee1cc2df9` |
| `outputs/molecular-recovery/colab-cuda-handoff/COLAB_PLAN.json` | `45,085` | `096d1703bbeb52f1ebf116a063d48c1bf5969f2b02473e56fd5b8d159f5f1dec` |
| `outputs/molecular-recovery/colab-cuda-handoff/COLAB_INPUT_MANIFEST.json` | `24,209` | `cebadd2ffd0342e8a8bd4bb1a700f6620775d7d6583017a630316fe6d9b14e55` |
| `outputs/molecular-recovery/colab-cuda-handoff/BUNDLE_INFO.json` | `926` | `caf4c60ef7849981c131b465b1bf0247e526b368537638d2452936d5a661e753` |
| `repro/colab/oam_colab_driver.py` | `54,307` | `e19ed6c4a438bb4f200320c7fc268abf48d617181733f8837bdc00ea5ef3f3d3` |
| `repro/colab/requirements-2026.04.txt` | `376` | `e8f4cc0c226c6fe235fde0c960a2eec8a9953b0673f6d3cc9ba6fa15e89c7f40` |
| `repro/src/build_oam_colab_bundle.py` | `15,426` | `277a52e8ea5d26418f6fadf9942bc0ba8cda1a2a004df434ca622a3e13edba61` |
| `repro/src/verify_oam_colab_return.py` | `21,607` | `3d0597421ae14f77299a276eee73d5aacfa1c1aa3348150dafbbbeef89d19105` |

The archive is deterministic, contains `91` payload files and no
seed-0 path, and has an external `.sha256` sidecar plus `BUNDLE_INFO.json`.
Every archived file has a size, SHA-256, and role in the input manifest. The
plan binds the paper/PDF identity, exact vendor commits, all recovered weight
hashes, source hashes, fourteen condition/seed identities, protocol, and Drive
checkpoint semantics. Extraction rejects absolute paths, parent traversal,
duplicates, links, non-regular members, an unexpected member set, and any
content mismatch before installation.

## Colab run instructions

In Colab, select **Runtime > Change runtime type**, choose a GPU, and select
runtime version `2026.04`. Place these three files in
`MyDrive/OAM-Colab-CUDA/input/`:

- `oam-colab-cuda-input.tar.gz`
- `oam-colab-cuda-input.tar.gz.sha256`
- `oam_colab_driver.py`

Mount Drive in the first cell:

```python
from google.colab import drive
drive.mount("/content/drive")
```

Verify the standalone extraction driver before using it:

```bash
sha256sum /content/drive/MyDrive/OAM-Colab-CUDA/input/oam_colab_driver.py
# must be: e19ed6c4a438bb4f200320c7fc268abf48d617181733f8837bdc00ea5ef3f3d3
```

Safely verify and extract the input bundle:

```bash
python /content/drive/MyDrive/OAM-Colab-CUDA/input/oam_colab_driver.py extract \
  --archive /content/drive/MyDrive/OAM-Colab-CUDA/input/oam-colab-cuda-input.tar.gz \
  --expected-sha256 a0bbb9678f72cb2239fb1dec62fc8decb8ee0706a97e19e0ec6a59983c7c3958
```

Install only the pinned dependencies and CUDA extensions:

```bash
python -m pip install --no-cache-dir -r \
  /content/drive/MyDrive/OAM-Colab-CUDA/repository/repro/colab/requirements-2026.04.txt
python -m pip install --no-cache-dir \
  torch_scatter==2.1.2+pt210cu128 \
  torch_cluster==1.6.3+pt210cu128 \
  -f https://data.pyg.org/whl/torch-2.10.0+cu128.html
```

Run the three gates in order:

```bash
python /content/drive/MyDrive/OAM-Colab-CUDA/repository/repro/colab/oam_colab_driver.py preflight
python /content/drive/MyDrive/OAM-Colab-CUDA/repository/repro/colab/oam_colab_driver.py compatibility-probe
python /content/drive/MyDrive/OAM-Colab-CUDA/repository/repro/colab/oam_colab_driver.py calibrate
```

Inspect the measured extrapolation before authorizing the full free-GPU run:

```bash
cat /content/drive/MyDrive/OAM-Colab-CUDA/repository/outputs/molecular-recovery/colab-cuda/ledgers/CUDA_CALIBRATION.json
```

If and only if all gates pass and the calibration is acceptable, run one
campaign at a time:

```bash
python /content/drive/MyDrive/OAM-Colab-CUDA/repository/repro/colab/oam_colab_driver.py run \
  --max-wall-hours 10 --max-campaigns 1
```

Repeat that command in later sessions. Omitting `--max-campaigns 1` lets the
driver continue through campaigns until the ten-hour checkpoint. It never
interrupts an active sample. Each sample runs in `/content` scratch, is
validated locally, copied to Drive using `.incoming`, rehashed, and receives
`SUCCESS.json` last. Resume revalidates every sample hash. A failed sample gets
up to ten attempts; failures are recorded and independent campaigns continue,
while merge, Vina, summary, and audit phases reject incomplete dependencies.
Vina remains full mode with exhaustiveness 32, seed 1, and two CPU workers.

After all fourteen campaigns report complete, package the hash-manifested return:

```bash
python /content/drive/MyDrive/OAM-Colab-CUDA/repository/repro/colab/oam_colab_driver.py package-return
```

Retrieve both files from `MyDrive/OAM-Colab-CUDA/return/`:

- `oam-colab-cuda-return.tar.gz`
- `oam-colab-cuda-return.tar.gz.sha256`

## Independent local return verification

The verifier is read-only unless `--extract-to` is explicitly supplied. It
checks the transport digest, safe member set, input/plan/source/vendor/weight
bindings, GPU gates, all 448 raw shard identities and hashes, exact commands,
fourteen merge manifests, Vina outputs, condition-separated summaries, and
independent per-campaign audits.

```bash
.venv/bin/python repro/src/verify_oam_colab_return.py \
  /path/to/oam-colab-cuda-return.tar.gz \
  --sidecar /path/to/oam-colab-cuda-return.tar.gz.sha256 \
  --output outputs/molecular-recovery/colab-cuda-handoff/RETURN_VERIFICATION.json
```

Only after accepting that verification should the returned seeds be installed,
using a new explicit destination rather than this paper root first:

```bash
.venv/bin/python repro/src/verify_oam_colab_return.py \
  /path/to/oam-colab-cuda-return.tar.gz \
  --sidecar /path/to/oam-colab-cuda-return.tar.gz.sha256 \
  --extract-to /an/explicit/empty/review-directory
```

After reviewed artifacts are deliberately integrated, rerun the independent
molecular auditor across local CPU seed 0 plus verified CUDA seeds 1--7 for each
condition. Do not pool AND with AND-NOT, and retain the hardware-backend caveat.

## Runtime and storage planning

The measured first-eight local CPU mean is `13,350.65` seconds per sample. The
remaining fourteen experiments project to `415.35` wall hours at four local
workers, generation only. No CUDA runtime has been measured yet. The initial
engineering envelope is **20--120 GPU hours** for generation, not a performance
claim; `CUDA_CALIBRATION.json` becomes the authoritative estimate before the
full run. Environment setup, Drive transfers, merging, and CPU Vina docking are
additional.

Plan for **1.6--2.4 GiB** of working Drive storage and **1.0--1.8 GiB** for the
return archive. The input archive is about 63 MB. Multiple free Colab sessions
are likely.
