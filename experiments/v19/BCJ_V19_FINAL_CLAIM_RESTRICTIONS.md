# BCJ-V19 Final Claim Restrictions

Mandatory wording constraints for manuscript finalization. Scope: frozen V19 corpora; same-team evidence.

## Must NOT claim
- Full consolidated Docker clean-room execution.
- Complete production integration QA.
- Complete immutable execution-lock enforcement.
- Universal fail-closed behavior.
- Independent third-party replication.
- Real-world attack prevalence.
- Universal semantic correctness or security.
- Independently verified historical blockchain transactions.

## Required characterizations
- **P07 fresh-process result** = *aggregation re-execution*, NOT full experimental reproduction.
- **P03 Experiment Lead verification** = *frozen-evidence reaggregation and recorded commitment reconstruction*, NOT fresh execution of both semantic implementations.
- **P06** = *reproduction of recovered historical evidence*; delivered CSV has empty tx_id/block → no on-chain verification.

## Secondary-metric caveats (do NOT claim independently reconstructed by P07-R1)
- **P04 F25 detector negative denominators are incomplete in the R1 output.** Detector confusion figures are not a complete independent reconstruction.
- **P04 F27 performance medians and IQR were not re-derived by the R1 code** (the actual `duration_ns` column was not recognized). Performance remains "combined processing + guard", no component isolation.

## Preserve unresolved obligations
All unresolved engineering obligations remain PARTIAL or documented limitations (e.g., P03 deep per-input reconstruction, Docker clean-room, F05 missing logs). Do not upgrade these to RESOLVED.
