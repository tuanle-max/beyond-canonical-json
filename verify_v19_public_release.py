#!/usr/bin/env python3
"""Public-release verification: 7 original archives + P03 privacy-redacted derivative (R2).
Reuses authoritative verify_v19_evidence rules unchanged."""
import argparse, hashlib, json, pathlib, sys, zipfile
import verify_v19_evidence as V
ORIG = {k: d for k, d in V.ARCHIVES.items() if k != "P03_FINAL_QA_CLOSED_REVIEW"}
DERIV = "BCJ_V19_P03_FINAL_QA_CLOSED_PUBLIC_RELEASE_R2.zip"
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("archive_directory", type=pathlib.Path); a = ap.parse_args()
    base = a.archive_directory; problems = []
    for k, d in ORIG.items():
        f = base / ("BCJ_V19_" + k + ".zip")
        if not f.is_file(): problems.append("MISSING " + k)
        elif sha(f.read_bytes()) != d: problems.append("SHA " + k)
    dp = base / DERIV
    if not dp.is_file(): print(json.dumps({"problems": problems + ["MISSING_P03_DERIV"]}, indent=2)); return 1
    man = json.loads((base.parent.parent / "docs" / "P03_PUBLICATION_DERIVATIVE_MANIFEST.json").read_text(encoding="utf-8"))
    dsha = sha(dp.read_bytes())
    if dsha != man["public_derivative_sha256"]: problems.append("DERIVATIVE_SHA")
    z = zipfile.ZipFile(dp); names = set(z.namelist())
    for r in man["retained_member_digests"]:
        if r["member"] not in names or sha(z.read(r["member"])) != r["sha256"]: problems.append("IDENTICAL_MODIFIED " + r["member"])
    for r in man["modified_members"]:
        if r["member"] not in names or sha(z.read(r["member"])) != r["redacted_sha256"]: problems.append("REDACTED_MISMATCH " + r["member"])
    if any(n.endswith(".pyc") or "/__pycache__/" in n for n in names): problems.append("BYTECODE_PRESENT")
    def op(k): return zipfile.ZipFile(base / ("BCJ_V19_" + k + ".zip"))
    res = {"scope": "public-release archival verification: 7 original archives + 1 privacy-redacted P03 derivative R2; no fresh execution",
           "original_archives_verified": len(ORIG), "p03_derivative_sha256": dsha,
           "members_identical": len(man["retained_member_digests"]), "members_redacted": len(man["modified_members"])}
    try:
        res["P03"] = V.p03(z)
        res["P04"] = V.p04(op("P04_FINAL_MEASURED_REVIEW"))
        res["P05"] = V.p05(op("P05_FINAL_MEASURED_REVIEW"), op("P05_CORRECTIVE_R2B_FINAL_REVIEW"))
        res["P06"] = V.p06(op("P07_FINAL_CONSOLIDATED_REVIEW"))
    except Exception as e:
        problems.append("SCIENTIFIC " + repr(e))
    res["problems"] = problems
    print(json.dumps(res, indent=2))
    return 0 if not problems else 1
if __name__ == "__main__":
    sys.exit(main())
