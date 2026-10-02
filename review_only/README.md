# Restricted Review Component

These tables expose evaluation-time root and typed-holder identifiers and therefore sit
outside the public, label-blind intervention-construction boundary.

They are included so reviewers can inspect and recompute the paper's endpoints:

- `restricted_root_mapping.csv`: one unique canonical root per confirmatory incident.
- `repaired_typed_holder_mapping.csv`: the provenance-defined same-type wrong holder for
  each incident and permutation seed, with invariant checks.
- `confirmatory_analysis_join.csv`: frozen provider predictions joined to the restricted
  root only after responses were fixed.
- `sq1_case_level.csv`: paired semantic-versus-opaque correctness rows.
- `sq2_case_seed_level.csv`: seed-specific typed-holder selections and switch indicators.

Use these files only for offline review. Do not place them in prompts, agent-visible
manifests, transformation code, or evidence-selection pipelines.

