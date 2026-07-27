# Claim 3 limitations and deviations

- No author-equivalent CelebA checkpoint is present in the pinned release.
- No independent CelebA generation or FID campaign is claimed at this node.
- The current author release postdates the paper and contains only three Git
  commits; this audit makes no claim about unreleased author state.
- Table transcription validates what the paper reports, not whether the
  reported samples or measurements can be independently regenerated.
- Missing files, a broken config, and a metric implementation mismatch are
  reproducibility blockers—not valid counterexamples to the empirical result.
- The public Diffusers CelebA UNet is a deliberately rejected reconstruction
  candidate, not a substitute for the paper's SiT and classifier states.
- Four materially different routes were completed. None yields the exact
  images, model state, or clean-fid measurements required to resolve the
  empirical claim.
