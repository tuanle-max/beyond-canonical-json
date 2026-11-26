# Release Validation Report

## Level 1 (AUTHORITATIVE verify_v19_evidence.py, executed)
exit=0
{
  "scope": "archival checks only; no new execution, no third-party replication",
  "archive_sha256_and_crc": 8,
  "P03": {
    "admission_reason": "630/630 per implementation vs archived oracle",
    "canonical_and_leaf": "600/600",
    "EQ": 150,
    "NEQ": 150,
    "batch_outcomes": 18,
    "leaves_per_implementation": 131,
    "nodes_per_implementation": 114
  },
  "P04": {
    "correct": {
      "A1": 45,
      "A1+PID": 75,
      "A1+CI": 55,
      "A2": 85
    },
    "unsafe_release": {
      "A1": 55,
      "A1+PID": 25,
      "A1+CI": 45,
      "A2": 15
    },
    "benign": {
      "A1": 40,
      "A1+PID": 40,
      "A1+CI": 40,
      "A2": 40
    },
    "paired_A1_A2": [
      45,
      0,
      40,
      15
    ]
  },
  "P05": {
    "first_pass_and_corrective": [
      15,
      40
    ],
    "paired": [
      15,
      0,
      25,
      0
    ],
    "matched_differences": 0,
    "applicable_states": 39,
    "missing_state_control": 1
  },
  "P06": {
    "recorded_digest_matches_eq6": 30,
    "recorded_digest_matches_campaign": 0,
    "formula_reexecution": false,
    "onchain_verification": false
  }
}


Historical result preserved at `experiments/v19/verify_v19_evidence_result.historical.json`; new run at `verify_v19_evidence_result_PUBLICATION.json`.

## Overall: BLOCKED (pending explicit approval + GitHub auth)
