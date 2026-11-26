# BCJ-V19 Final Author Handover

Administrative handover for manuscript finalization. No experiments were rerun; no frozen evidence or manuscript was modified.

## Authorized / not authorized
- manuscript_finalization_authorized = **true**
- submission_authorized = **false_pending_final_manuscript_review**
- NEW experiments / corpora / verification arms / P07-R2 / P08 = **NOT authorized**

## Canonical numbers to use
Use `BCJ_V19_FINAL_SCIENTIFIC_SSOT.json` as the single source of truth:
- P03: 630/630; 600/600; 150/150; 150/150; 18/18; 131 leaves/impl; 114/114 nodes/impl.
- P04: A1 45 / A1+PID 75 / A1+CI 55 / A2 85 (of 100); paired A1 vs A2 45/0/40/15; unsafe A1 55/60, A2 15/60; benign 40/40 per arm.
- P05: V1 15/40; V2 40/40; paired 15/0/25/0; authorized 11/11 per arm; unauthorized V1 25/25, V2 0/25; coordinated V1 6/6, V2 0/6; decision agreement 40/40; state 39/39 +1 N/A; 80 corrective obs; zero first-pass/corrective differences.
- P06: artifact Eq.6 30/30; campaign 0/30; divergence batch 0; reproduction only.

## Research questions
Do NOT adopt the auto-generated five-RQ mapping. **Preserve the manuscript's existing research questions.** Treat P07 as cross-cutting reproducibility evidence. Final RQ wording is the Author Lead's responsibility.

## Claim restrictions
Apply `BCJ_V19_FINAL_CLAIM_RESTRICTIONS.md` verbatim. In particular: no Docker clean-room claim; no "production integration QA / complete lock enforcement / universal fail-closed"; P07 = aggregation re-execution; P03 = reaggregation of frozen evidence; F25 negative denominators incomplete; F27 medians/IQR not re-derived by R1; no third-party / prevalence / universal-security claim; no on-chain verification.

## Preserved artifacts (do not overwrite)
- Commit `fb67aefb74632e92b43318f74ad2f9be0bf199ba`
- `BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW.zip` — `b53daa567527fe2b7828a38dfb8a1732fc48081b9c6c8526a63641d2382b9d03`
- `BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW.zip` — `ec0e5448be666ace8ac63aa12102e18da53603230b78993077d3c2d7a1beed09`
- All P00–P06 accepted archives, frozen corpora, and raw observations.

## Handover documents
- `P07_EXPERIMENT_LEAD_FINAL_DISPOSITION.md`
- `BCJ_V19_FINAL_SCIENTIFIC_SSOT.json`
- `BCJ_V19_FINAL_CLAIM_RESTRICTIONS.md`
- `BCJ_V19_FINAL_AUTHOR_HANDOVER.md` (this file)
