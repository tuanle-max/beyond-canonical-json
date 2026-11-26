# Artifact Inventory

## Principal frozen archives (identity-preserved)

| Archive | SHA-256 | bytes | CRC | unique | internal SHA256SUMS |
|---|---|---|---|---|---|
| BCJ_V19_P01_CLOSURE_REVIEW.zip | `b8e3d23bd61dd6e7bc6e22d9ac91c4ac7b155b9dd7b935310ac421d117f468b7` | 182289 | OK | True | bad=19 |
| BCJ_V19_P02_R4A_REVIEW.zip | `3513e3c926a29c6e6cc3d0dcd461b27cdee47c45cfa5e4c0bb92ef4b59a4aca3` | 334475 | OK | True | bad=0 |
| BCJ_V19_P03_FINAL_QA_CLOSED_REVIEW.zip | `45053224dc25c314a0e305324ccb087020f3832b4fa00b569833aad18c122761` | 3234152 | OK | True | bad=0 |
| BCJ_V19_P04_FINAL_MEASURED_REVIEW.zip | `2900ffb2bca0ac91ad33d6661bcbd457976f19256b1266ca7a9e6e3f457e204b` | 254324 | OK | True | bad=0 |
| BCJ_V19_P05_FINAL_MEASURED_REVIEW.zip | `719db8c483a40a437f7e7cfeb7797bfd1fdcd9ca1fb2bd28cd24cb4dd18a4834` | 79934 | OK | True | bad=0 |
| BCJ_V19_P05_CORRECTIVE_R2B_FINAL_REVIEW.zip | `9abff431c6ec5d1887596ebf86de2d9ad694f536cb2842b3018b785e597f576f` | 48469 | OK | True | bad=0 |
| BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW.zip | `ec0e5448be666ace8ac63aa12102e18da53603230b78993077d3c2d7a1beed09` | 142650 | OK | True | bad=0 |
| BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW.zip | `b53daa567527fe2b7828a38dfb8a1732fc48081b9c6c8526a63641d2382b9d03` | 39500 | OK | True | bad=0 |

## Frozen evidence subset (Level 1 reaggregation)

P04 raw/oracle/corpus; P05 first-pass + corrective raw/oracle/corpus + state re-audit; P03 E2 pairs + J01; P06 manifest/hashing/repro/derived CSVs.

## Missing dependencies (recorded, not fabricated)

- `verify_v19_evidence.py` (Lead-supplied Level-1 checker): NOT FOUND.
- `verify_v19_evidence_result.json`: NOT FOUND.
- `BCJ_V19_EXPERIMENT_LEAD_MASTER_SSOT.md`: NOT FOUND.
- v19-specific `README.md`: NOT FOUND (root README is the older canon-drift version).
- `v19.tex`: present in source (`tex/v19.tex`) but NOT published pending author approval.
