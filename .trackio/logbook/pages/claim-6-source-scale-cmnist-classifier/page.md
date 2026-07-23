# Source-scale CMNIST classifier


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_26911a0d4863", "created_at": "2026-07-19T18:56:36+00:00", "title": "Exact upstream classifier trained on the full source split"}
-->
The missing noise-aware CMNIST composition classifier was rebuilt using the pinned author trainer, its 50-epoch configuration, all 60,000 training examples, and the expected epoch=49-step=2950 checkpoint. SHA-256: a77cafc37a7be88eaec5aead5ffe024a995fbf2421d736ff009b3c9dd96d36ba.

A deterministic audit evaluates all 10,000 test examples at fixed diffusion times.

| t | Digit accuracy | Colour accuracy |
| ---: | ---: | ---: |
| 0 | 97.56 percent | 100.00 percent |
| 50 | 97.20 percent | 100.00 percent |
| 100 | 96.38 percent | 99.98 percent |
| 250 | 83.67 percent | 97.15 percent |
| 500 | 33.89 percent | 48.82 percent |
| 750 | 13.09 percent | 15.28 percent |
| 999 | 10.64 percent | 10.79 percent |

The decay toward chance at maximum noise is expected and is now measured rather than hidden inside one random-timestep average.


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_dcefa55cd18a", "created_at": "2026-07-19T21:13:04+00:00", "title": "Independent full-test judge completed"}
-->
The clean independent judge used the same released ResNet-18 two-head architecture, all 60,000 CMNIST training examples, batch 1,024, and 50 epochs. Its expected epoch=49-step=2950 checkpoint has SHA-256 `ff8dbb5253278ad46e0033959045f9558927b0e814cd04f98fc747d6629adfb6`.

A deterministic evaluation over all 10,000 clean test images measured digit accuracy **98.14%**, colour accuracy **100.00%**, digit NLL **0.0867544**, and colour NLL **0.0000258573**. This judge is independent of the composition checkpoint (`a77cafc3...`) and provides a separate full-split readout rather than reusing the model being evaluated.
