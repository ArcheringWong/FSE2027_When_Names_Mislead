# Study-S v2 Confirmatory Analysis Report

- Status: `CONFIRMATORY_ANALYSIS_FROZEN_READY_FOR_INTERPRETATION`
- Analysis / protocol: `CONFIRMATORY_ANALYSIS_001` / `STUDY_S_V2_CONFIRMATORY_PROTOCOL_2_3`
- Population/join: 87 incidents; 261 typed-holder rows; 1740 frozen primary outcomes
- SQ1 primary: `CROSS_MODEL_SEMANTIC_BENEFIT_NOT_CONFIRMED`; replication: `CROSS_MODEL_SEMANTIC_BENEFIT_CONFIRMED`
- SQ2 primary: `CROSS_MODEL_REPAIRED_TYPED_HOLDER_ATTRACTION_NOT_CONFIRMED`; replication: `CROSS_MODEL_REPAIRED_TYPED_HOLDER_ATTRACTION_NOT_CONFIRMED`
- Bootstrap: 10,000 base-incident resamples; seed 20260905
- Exclusions/replacements/fuzzy recovery/partial recovery/v1 holder use/API calls: 0/0/0/0/0/0

## SQ1

- QWEN on: semantic 13/87; opaque 1/87; delta 0.137931; 95% CI [0.068966, 0.218391]; McNemar p=0.000488281
- QWEN off: semantic 14/87; opaque 2/87; delta 0.137931; 95% CI [0.057471, 0.218391]; McNemar p=0.00183105
- DEEPSEEK on: semantic 4/87; opaque 1/87; delta 0.034483; 95% CI [0.000000, 0.080460]; McNemar p=0.25
- DEEPSEEK off: semantic 5/87; opaque 1/87; delta 0.045977; 95% CI [0.011494, 0.091954]; McNemar p=0.125

## SQ2

- QWEN on: permuted holder 45/261; opaque holder 1/261; delta 0.168582; 95% CI [0.114943, 0.226054]; new/strict 44/6; `REPAIRED_TYPED_HOLDER_ATTRACTION_CONFIRMED`
- QWEN off: permuted holder 33/261; opaque holder 1/261; delta 0.122605; 95% CI [0.076628, 0.176245]; new/strict 32/4; `REPAIRED_TYPED_HOLDER_ATTRACTION_CONFIRMED`
- DEEPSEEK on: permuted holder 7/261; opaque holder 1/261; delta 0.022989; 95% CI [0.003831, 0.049808]; new/strict 6/0; `REPAIRED_TYPED_HOLDER_ATTRACTION_NOT_CONFIRMED`
- DEEPSEEK off: permuted holder 6/261; opaque holder 1/261; delta 0.019157; 95% CI [0.000000, 0.045977]; new/strict 5/0; `REPAIRED_TYPED_HOLDER_ATTRACTION_NOT_CONFIRMED`
