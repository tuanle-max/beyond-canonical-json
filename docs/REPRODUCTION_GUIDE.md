## Level 1 (AUTHORITATIVE)
`python verify_v19_evidence.py experiments/v19` (exit 0 = frozen evidence + headline agree).
`tools/verify_release.py` is an OPTIONAL supplementary checker (not the Lead checker).

# Reproduction Guide (BCJ-V19 artifact)

Three verification levels. Read the scope of each before citing any result.

## Level 1 - Frozen-evidence verification (SUPPORTED here)
The Lead-supplied `verify_v19_evidence.py` was NOT present in the source workspace, so it is recorded as a
missing dependency. This repository ships a clearly-labelled publication wrapper:

```
python verify_v19_evidence.py experiments/v19
```

It verifies: the 8 principal archive SHA-256 values, detached checksums, ZIP CRC, unique members, safe member
paths, internal SHA256SUMS where present, and recomputes the P04/P05/P06 headline metrics from the frozen raw
evidence against `BCJ_V19_FINAL_SCIENTIFIC_SSOT.json`.
Exit 0 = all integrity + headline checks agree. Non-zero = a discrepancy (do not edit expectations to pass).
Limits: Level 1 is archival verification, not re-execution of the scientific experiments.
Required Python: 3.12.x; standard library only (no external packages). Environment tested: 3.12.9.

## Level 2 - Phase-specific experimental re-execution (PARTIAL)
Accepted archives are archival evidence. Executable re-execution requires the phase source trees (Python/Go) and
dependency locks. `reproduction/` documents what is available; where a runner/dependency is not published it is
listed as unavailable. Do not invent commands.

| Phase | Principal archive | Executable runner in repo? | Notes |
|---|---|---|---|
| P01 | BCJ_V19_P01_CLOSURE_REVIEW.zip | inside archive | archival verification only |
| P02 | BCJ_V19_P02_R4A_REVIEW.zip | inside archive | normative contract |
| P03 | BCJ_V19_P03_FINAL_QA_CLOSED_REVIEW.zip | inside archive | Python+Go; needs Go toolchain + JCS deps |
| P04 | BCJ_V19_P04_FINAL_MEASURED_REVIEW.zip | inside archive | frozen corpus+oracle+raw |
| P05 | BCJ_V19_P05_FINAL_MEASURED_REVIEW.zip / ..._CORRECTIVE_R2B_FINAL_REVIEW.zip | inside archive | verifier + corpus |
| P06 | P07 archives + evidence/ | evidence/p06_* | reproduction, not on-chain |
| P07 | BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW.zip | inside archive | aggregation + handover |

Any rerun MUST write to a new scratch directory. Never overwrite frozen raw observations.

## Level 3 - Clean-room environment
`Full consolidated Docker clean-room execution: NOT_EXECUTED`
A Dockerfile/targets are referenced from the P07 archives; providing them is not a demonstration of Docker
reproduction. Docker cleanroom status = NOT_EXECUTED.
