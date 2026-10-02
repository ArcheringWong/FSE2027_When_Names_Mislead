# Confirmatory interpretive supplement

Status: `POST_HOC_DESCRIPTIVE_SUPPLEMENT_COMPLETE`

This supplement uses only frozen responses and mappings. It adds no model calls and does not modify the registered SQ1/SQ2 decisions.

## Holder references

| Provider | Topology | Permuted | Semantic | Opaque | Perm.-Sem. (pp) | Perm.-Opaque (pp) | Permuted cases |
|---|---:|---:|---:|---:|---:|---:|---:|
| QWEN | on | 45/261 | 2/261 | 1/261 | 16.48 | 16.86 | 30 |
| DEEPSEEK | on | 7/261 | 1/261 | 1/261 | 2.30 | 2.30 | 5 |
| QWEN | off | 33/261 | 2/261 | 1/261 | 11.88 | 12.26 | 22 |
| DEEPSEEK | off | 6/261 | 1/261 | 1/261 | 1.92 | 1.92 | 4 |

The semantic comparison aligns one semantic response per incident to three seed-specific destinations. It is descriptive and does not replace the registered opaque-reference estimator.

## Semantic starting state of permuted holder selections

| Provider | Topology | Correct -> holder | Other wrong -> holder | Already holder | Unknown/invalid -> holder |
|---|---:|---:|---:|---:|---:|
| QWEN | on | 17 rows / 10 cases | 27 rows / 19 cases | 1 rows / 1 cases | 0 rows / 0 cases |
| DEEPSEEK | on | 1 rows / 1 cases | 5 rows / 3 cases | 1 rows / 1 cases | 0 rows / 0 cases |
| QWEN | off | 13 rows / 8 cases | 19 rows / 13 cases | 1 rows / 1 cases | 0 rows / 0 cases |
| DEEPSEEK | off | 2 rows / 1 cases | 3 rows / 2 cases | 1 rows / 1 cases | 0 rows / 0 cases |

## Strict-switch opportunities

| Provider | Topology | Eligible rows | Eligible cases | Strict switches | Strict cases | Strict from correct start |
|---|---:|---:|---:|---:|---:|---:|
| QWEN | on | 68 | 23 | 6 | 4 | 0 |
| DEEPSEEK | on | 140 | 47 | 0 | 0 | 0 |
| QWEN | off | 74 | 25 | 4 | 3 | 0 |
| DEEPSEEK | off | 143 | 48 | 0 | 0 | 0 |

## Input scale

| Measure | N | Min | Median | Max |
|---|---:|---:|---:|---:|
| candidate_entities | 87 | 253 | 275 | 1951 |
| evidence_units | 87 | 51 | 60 | 67 |
| candidate_entity_types | 87 | 16 | 20 | 20 |
| topology_nodes | 87 | 32 | 32 | 32 |
| topology_edges | 87 | 0 | 4 | 14 |

No row-level predictions, case IDs, roots, or holder IDs are written by this supplement.
