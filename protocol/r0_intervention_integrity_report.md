# Study-S v2 R0 intervention-integrity audit

Final status: **READY_FOR_CANARY**

This audit validates the scientific instrument only. It made zero model/API calls and did not read or analyze model predictions.

## Frozen design

- RCA100 v1.1: 16 development incidents and 87 fixed confirmatory incidents.
- Conditions: S0/S1/P1/P2/P3 topology-on and S2/S3/P4/P5/P6 topology-off.
- Permutation seeds: 20260901, 20260902, 20260903.
- Planned models: qwen3.7-plus-2026-05-26 and deepseek-v4-pro.
- Bootstrap seed/count frozen prospectively: 20260905 / 10000.

## Cardinalities

- Confirmatory incidents: 87
- Ownership case-seed rows: 261
- Topology-specific audit rows: 522
- Model-agnostic condition rows: 870
- Planned model request rows: 1740

## Integrity gates

- candidate_surface_equal: 522/522 PASS
- candidate_order_equal: 522/522 PASS
- nonlabel_payload_equal: 522/522 PASS
- label_multiset_equal: 261/261 PASS
- ownership_bijection: 261/261 PASS
- typed_wrong_holder: 261/261 PASS
- gold_firewall: PASS
- api_calls: 0
- other_project_files_modified: 0

No case, seed, gold record, or candidate was altered to obtain these results.
