#!/usr/bin/env python3
"""Audit helper (P00.6): reproduce the DR-TEA artifact's OWN Eq. 6 from its seed.

This script does NOT implement a campaign formula. It re-implements the artifact's chaining rule
so that the real manifest can be audited:

    artifact Eq. 6 (specs/formal-model.md, services/ingestion/merkle.py):
        leaves_j = [r_{j-1}] + B_j            # predecessor root is leaf index 0
        r_j      = MerkleRoot(leaves_j)      # leaf H(0x00||d), node H(0x01||L||R)

    campaign Eq. (§6, tex/manuscript.tex eq:rootchain, py/canon/hashing.py):
        r_j = H(0x02 || j:uint64_be || r_{j-1} || MerkleRoot(B_j))

Event stream: the pilot manifest was produced by scripts/e7_preflight.py with
``random.Random(42)``, 30 batches x 1681 events, and one ``randint(0, 1680)`` draw per batch
(sample-proof index). That exact RNG consumption order is mirrored here, so the event hashes are
reproduced bit-for-bit - no pilot event data is invented.

Output: a CSV with, per batch, the manifest root, the reproduced artifact root, and the value the
campaign formula would produce from the same inputs.

Usage:
    .venv/Scripts/python scripts/drtea_eq6_repro.py \\
        --manifest docs/drtea_mainnet_manifest_REAL.json \\
        --live-csv <artifact>/results/e7_mainnet_live.csv \\
        --csv derived/legacy_validation_real_eq6.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
import random
import sys

from canon import hashing

SEED = 42
N_BATCHES = 30
BATCH_SIZE = 1681
GENESIS_PREV_ROOT = b"\x00" * 32


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def artifact_merkle_root(leaves: list[bytes]) -> bytes:
    """DR-TEA's binary Merkle tree: leaf H(0x00||d), node H(0x01||L||R), odd leaf duplicated."""
    level = [sha256(b"\x00" + leaf) for leaf in leaves]
    while len(level) > 1:
        if len(level) % 2:
            level = level + [level[-1]]
        level = [sha256(b"\x01" + level[i] + level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


def event_batches() -> list[list[bytes]]:
    """Reproduce the pilot's event hashes (seed 42, 30 x 1681, one randint per batch)."""
    rng = random.Random(SEED)
    batches = []
    for _ in range(N_BATCHES):
        batches.append([rng.randbytes(32) for _ in range(BATCH_SIZE)])
        rng.randint(0, BATCH_SIZE - 1)  # preflight draws the sample-proof index here
    return batches


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--live-csv", help="optional artifact CSV with tx_id / included_block_no")
    args = parser.parse_args(argv)

    manifest = json.loads(pathlib.Path(args.manifest).read_text(encoding="utf-8"))
    batches = manifest["batches"] if isinstance(manifest, dict) else manifest

    sidecar: dict[str, dict] = {}
    if args.live_csv and pathlib.Path(args.live_csv).is_file():
        for row in csv.DictReader(pathlib.Path(args.live_csv).open(encoding="utf-8")):
            sidecar[row.get("batch_id", "")] = row

    events = event_batches()
    rows = []
    eq6_match = ours_match = 0
    first_ours_diff = None

    for index, batch in enumerate(batches):
        prev = bytes.fromhex(batch["prev_root_hex"])
        expected = batch["root_hex"]

        reproduced = artifact_merkle_root([prev] + events[index]).hex()
        prev_ok = reproduced == expected
        eq6_match += bool(prev_ok)

        ours = hashing.root_chain(batch["batch_id"], prev, artifact_merkle_root(events[index])).hex()
        ours_ok = ours == expected
        ours_match += bool(ours_ok)
        if not ours_ok and first_ours_diff is None:
            first_ours_diff = (batch["batch_id"], expected, ours)

        companion = sidecar.get(str(batch["batch_id"]), {})
        rows.append([
            batch["batch_id"], companion.get("tx_id", ""), companion.get("included_block_no", ""),
            expected, reproduced, "true" if prev_ok else "false", ours, "true" if ours_ok else "false",
        ])

    out = pathlib.Path(args.csv)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["j", "tx_id", "block", "r_chained_manifest", "r_chained_reproduced_eq6",
                         "eq6_match", "r_campaign_h02", "campaign_match"])
        writer.writerows(rows)

    total = len(rows)
    print(f"batches                     : {total}")
    print(f"artifact Eq. 6 reproduced   : {eq6_match}/{total}")
    print(f"campaign Eq. (0x02 frame)   : {ours_match}/{total}")
    if first_ours_diff:
        j, expected, ours = first_ours_diff
        print(f"first campaign divergence  : j={j}")
        print(f"  manifest r_j    = {expected}")
        print(f"  campaign would  = {ours}")
    return 0 if eq6_match == total else 1


if __name__ == "__main__":
    raise SystemExit(main())