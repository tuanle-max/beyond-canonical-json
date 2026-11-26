# Verifying the Public Artifacts

## v1.0.0-artifact.6

curl -L -O https://github.com/tuanle-max/beyond-canonical-json/releases/download/v1.0.0-artifact.6/BCJ_V21_FINAL_AUTHOR_HANDOVER.zip
curl -L -O https://github.com/tuanle-max/beyond-canonical-json/releases/download/v1.0.0-artifact.6/BCJ_V21_FINAL_AUTHOR_HANDOVER.zip.sha256
sha256sum -c BCJ_V21_FINAL_AUTHOR_HANDOVER.zip.sha256

Expected public SHA-256: e9d64eec4cbf1a484400ed36ad18d9bfb49b00163c6446a74af28ded8f3a48c7

The historical local container digest (ced5a3d1b577d32cddeccff8370c28d329433930734171b537c20cf726144ced) refers to a different
container serialization with identical member contents (46/46 identical
member paths, sizes and digests).

## v1.0.0-artifact.7

curl -L -O https://github.com/tuanle-max/beyond-canonical-json/releases/download/v1.0.0-artifact.7/BCJ_V22_FINAL_INTEGRITY_QA_REVIEW.zip
sha256sum BCJ_V22_FINAL_INTEGRITY_QA_REVIEW.zip

Expected SHA-256: 9fc3b4525fa357c4ddaa3696f018482838b888668bc628c9257ddb32da19aba0

## Scope

Byte identity relative to published
digests only. Not independent third-party replication, universal correctness,
complete source-to-binary provenance, or corrected-engine KAT execution.
