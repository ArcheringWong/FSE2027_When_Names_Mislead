# Dataset and Review-Use Notice

## RCA100

The study uses RCA100 v1.1 from the AgenticOpsEval materials maintained at:

<https://www.aiops.cn/gitlab/aiops-live-benchmark/agenticopseval>

The locally supplied RCA100 license is CC BY-NC-SA 4.0. Users of the original dataset
must follow its attribution, non-commercial-use, and ShareAlike terms and the dataset's
own citation instructions.

## What is included here

This anonymous package excludes licensed raw telemetry and answer-key files. It contains
the anonymous paper, frozen protocol metadata, source code defining the intervention and
evaluator, aggregate statistical outputs, hashes, and compact derived tables keyed by
case and canonical entity identifiers.

The `review_only/` directory contains evaluation-time root and typed-holder identifiers
plus frozen predictions needed to inspect endpoint construction. These files are supplied
solely for anonymous scholarly review and offline verification. They must not be used as
input to a model, prompt compiler, evidence compiler, or intervention generator.

No API credentials, provider authorization material, or raw model response text is
included. No license for broader reuse of the accompanying project code is asserted by
this review package beyond the permissions required for anonymous peer review.

