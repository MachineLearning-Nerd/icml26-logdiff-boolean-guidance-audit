# Claim 3 release-integrity method

The verifier reads a pinned, complete Git tree manifest of the current author
release. It checks every declared CelebA checkpoint path, resolves the exact
Hydra dataset target, and compares the paper's sample and FID contract with
the executable evaluation path.

The independent checker re-derives those predicates from the raw JSON rather
than trusting the headline status. The negative control injects all required
paths and a matching clean-fid protocol; the same decision function must then
refuse to label the release BLOCKED.

This is an executability audit, not a substitute generation experiment.

The public provenance route uses independent GitHub and Hugging Face API
responses preserved under `public-checkpoint-search/`. It rejects unrelated
generic-name results. The reconstruction route positively resolves a public
CelebA DDPM revision and its model tree, then rejects it as non-equivalent
because the paper requires a different diffusion state plus composition and
judge classifiers.

The mandatory falsification route admits only exact-method image sets evaluated
with the paper's 5,000-sample clean-fid protocol. It confirms the Table 3
transcription and checks a synthetic reversed-FID control. Missing checkpoints
and a different public DDPM are not treated as counterexamples.
