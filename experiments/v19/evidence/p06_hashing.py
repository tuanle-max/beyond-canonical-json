"""Core hashing formulas of the canon-drift commitment pipeline (P00.4, step 1.1).

Every function returns the raw 32-byte SHA-256 digest and accepts ``bytes`` or ``str`` inputs
(strings are UTF-8 encoded, bytes are used as given unless a fixed width is required).

Formulas (domain-separated pre-images, ``H`` = SHA-256)::

    leaf_legacy(seq, h, receipt_hash, status)
        H(0x00 || JCS({"seq": seq, "h": h, "r": receipt_hash, "status": status}))
        (RFC 8785 JCS sorts the members lexicographically: h, r, seq, status)

    internal_node(left, right)
        H(0x01 || left || right)                       left/right are 32-byte digests

    root_chain(j, r_prev, merkle_root)
        H(0x02 || j:int64-be || r_prev || merkle_root)  r_prev/merkle_root are 32-byte digests

    leaf_v2(pid_32, canonical_bytes)
        H(0x00 || 0x02 || pid_32 || canonical_bytes)

    s2_leaf_v1(cred_id, status_nonce)
        H(0x00 || cred_id || status_nonce)

    s2_leaf_v2(epid_32, cred_id, status_nonce)
        H(0x00 || 0x02 || epid_32 || LP(cred_id) || LP(status_nonce))
        (LP = 2-byte big-endian length prefix + payload)

Notes
-----
* ``json.dumps`` must never be used for the leaf pre-image — it is not JCS-compatible and the
  P00.2 source guard fails the build if it appears anywhere under ``py/canon``. JCS comes from the
  pinned ``rfc8785`` wheel (0.1.3).
* ``leaf_legacy`` treats ``bytes`` arguments as **UTF-8 text** (the pilot encodes the identifiers
  as hex strings); this mirrors the "auto-encode utf-8" rule of the task. Binary fields that must
  stay raw (``left``/``right``/``pid_32``/``epid_32``) take exactly 32 bytes.
"""

from __future__ import annotations

import hashlib
from typing import Final

import rfc8785

HASH_SIZE: Final[int] = 32
MAX_LP_PAYLOAD: Final[int] = 65535

_DOMAIN_LEAF: Final[bytes] = b"\x00"
_DOMAIN_INTERNAL: Final[bytes] = b"\x01"
_DOMAIN_ROOT: Final[bytes] = b"\x02"
_TAG_V2: Final[bytes] = b"\x02"


def _to_bytes(value: bytes | bytearray | memoryview | str, field: str) -> bytes:
    """Return ``value`` as bytes; ``str`` is UTF-8 encoded."""
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("utf-8")
    raise TypeError(f"{field}: expected bytes or str, got {type(value).__name__}")


def _fixed(value: bytes | str, size: int, field: str) -> bytes:
    """Return ``value`` as a byte string of exactly ``size`` bytes."""
    data = _to_bytes(value, field)
    if len(data) != size:
        raise ValueError(f"{field}: expected {size} bytes, got {len(data)}")
    return data


def _text(value: bytes | str, field: str) -> str:
    """Return ``value`` as text for JSON canonicalisation (bytes are decoded as UTF-8)."""
    if isinstance(value, str):
        return value
    try:
        return _to_bytes(value, field).decode("utf-8")
    except UnicodeDecodeError as exc:  # pragma: no cover - defensive
        raise ValueError(f"{field}: bytes are not valid UTF-8 text") from exc


def _length_prefixed(value: bytes | str, field: str) -> bytes:
    """Encode ``value`` as ``uint16_be(len) || payload``."""
    data = _to_bytes(value, field)
    if len(data) > MAX_LP_PAYLOAD:
        raise ValueError(f"{field}: payload exceeds {MAX_LP_PAYLOAD} bytes")
    return len(data).to_bytes(2, "big") + data


def leaf_legacy_pre_image(seq: int, h: bytes | str, receipt_hash: bytes | str, status: bytes | str) -> bytes:
    """Pre-image of ``leaf_legacy``: ``0x00 || JCS({seq, h, r, status})``."""
    if not isinstance(seq, int) or isinstance(seq, bool):
        raise TypeError("seq: expected int")
    payload = {
        "seq": seq,
        "h": _text(h, "h"),
        "r": _text(receipt_hash, "receipt_hash"),
        "status": _text(status, "status"),
    }
    return _DOMAIN_LEAF + rfc8785.dumps(payload)


def leaf_legacy(seq: int, h: bytes | str, receipt_hash: bytes | str, status: bytes | str) -> bytes:
    """Legacy Merkle leaf: ``H(0x00 || JCS({seq, h, r, status}))``."""
    return hashlib.sha256(leaf_legacy_pre_image(seq, h, receipt_hash, status)).digest()


def internal_node_pre_image(left: bytes | str, right: bytes | str) -> bytes:
    """Pre-image of ``internal_node``: ``0x01 || left || right``."""
    return _DOMAIN_INTERNAL + _fixed(left, HASH_SIZE, "left") + _fixed(right, HASH_SIZE, "right")


def internal_node(left: bytes | str, right: bytes | str) -> bytes:
    """Internal Merkle node: ``H(0x01 || left || right)``."""
    return hashlib.sha256(internal_node_pre_image(left, right)).digest()


def root_chain_pre_image(j: int, r_prev: bytes | str, merkle_root: bytes | str) -> bytes:
    """Pre-image of ``root_chain``: ``0x02 || j:uint64_be || r_prev || merkle_root``."""
    if not isinstance(j, int) or isinstance(j, bool) or j < 0 or j >= 1 << 64:
        raise ValueError("j: expected an unsigned 64-bit integer")
    return (
        _DOMAIN_ROOT
        + j.to_bytes(8, "big")
        + _fixed(r_prev, HASH_SIZE, "r_prev")
        + _fixed(merkle_root, HASH_SIZE, "merkle_root")
    )


def root_chain(j: int, r_prev: bytes | str, merkle_root: bytes | str) -> bytes:
    """Root chain step: ``H(0x02 || j:uint64_be || r_prev || merkle_root)``."""
    return hashlib.sha256(root_chain_pre_image(j, r_prev, merkle_root)).digest()


def leaf_v2_pre_image(pid_32: bytes | str, canonical_bytes: bytes | str) -> bytes:
    """Pre-image of ``leaf_v2``: ``0x00 || 0x02 || pid_32 || canonical_bytes``."""
    return (
        _DOMAIN_LEAF
        + _TAG_V2
        + _fixed(pid_32, HASH_SIZE, "pid_32")
        + _to_bytes(canonical_bytes, "canonical_bytes")
    )


def leaf_v2(pid_32: bytes | str, canonical_bytes: bytes | str) -> bytes:
    """v2 leaf: ``H(0x00 || 0x02 || pid_32 || canonical_bytes)``."""
    return hashlib.sha256(leaf_v2_pre_image(pid_32, canonical_bytes)).digest()


def s2_leaf_v1_pre_image(cred_id: bytes | str, status_nonce: bytes | str) -> bytes:
    """Pre-image of ``s2_leaf_v1``: ``0x00 || cred_id || status_nonce``."""
    return _DOMAIN_LEAF + _to_bytes(cred_id, "cred_id") + _to_bytes(status_nonce, "status_nonce")


def s2_leaf_v1(cred_id: bytes | str, status_nonce: bytes | str) -> bytes:
    """S2 status leaf v1: ``H(0x00 || cred_id || status_nonce)``."""
    return hashlib.sha256(s2_leaf_v1_pre_image(cred_id, status_nonce)).digest()


def s2_leaf_v2_pre_image(epid_32: bytes | str, cred_id: bytes | str, status_nonce: bytes | str) -> bytes:
    """Pre-image of ``s2_leaf_v2``: ``0x00 || 0x02 || epid_32 || LP(cred_id) || LP(status_nonce)``."""
    return (
        _DOMAIN_LEAF
        + _TAG_V2
        + _fixed(epid_32, HASH_SIZE, "epid_32")
        + _length_prefixed(cred_id, "cred_id")
        + _length_prefixed(status_nonce, "status_nonce")
    )


def s2_leaf_v2(epid_32: bytes | str, cred_id: bytes | str, status_nonce: bytes | str) -> bytes:
    """S2 status leaf v2: ``H(0x00 || 0x02 || epid_32 || LP(cred_id) || LP(status_nonce))``."""
    return hashlib.sha256(s2_leaf_v2_pre_image(epid_32, cred_id, status_nonce)).digest()
