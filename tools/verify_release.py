#!/usr/bin/env python3
"""Publication wrapper (NOT the Lead-supplied verify_v19_evidence.py, which was absent).
Verifies archive identities + recomputes P04/P05/P06 headline from frozen raw vs the final SSOT."""
import csv, hashlib, json, pathlib, sys, zipfile
BASE = pathlib.Path(__file__).resolve().parents[1]
V = BASE / "experiments" / "v19"
EXP = {"BCJ_V19_P01_CLOSURE_REVIEW.zip":"b8e3d23bd61dd6e7bc6e22d9ac91c4ac7b155b9dd7b935310ac421d117f468b7",
"BCJ_V19_P02_R4A_REVIEW.zip":"3513e3c926a29c6e6cc3d0dcd461b27cdee47c45cfa5e4c0bb92ef4b59a4aca3",
"BCJ_V19_P03_FINAL_QA_CLOSED_REVIEW.zip":"45053224dc25c314a0e305324ccb087020f3832b4fa00b569833aad18c122761",
"BCJ_V19_P04_FINAL_MEASURED_REVIEW.zip":"2900ffb2bca0ac91ad33d6661bcbd457976f19256b1266ca7a9e6e3f457e204b",
"BCJ_V19_P05_FINAL_MEASURED_REVIEW.zip":"719db8c483a40a437f7e7cfeb7797bfd1fdcd9ca1fb2bd28cd24cb4dd18a4834",
"BCJ_V19_P05_CORRECTIVE_R2B_FINAL_REVIEW.zip":"9abff431c6ec5d1887596ebf86de2d9ad694f536cb2842b3018b785e597f576f",
"BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW.zip":"ec0e5448be666ace8ac63aa12102e18da53603230b78993077d3c2d7a1beed09",
"BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW.zip":"b53daa567527fe2b7828a38dfb8a1732fc48081b9c6c8526a63641d2382b9d03"}
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def jl(p): return [json.loads(l) for l in open(p,encoding="utf-8") if l.strip()]
def main():
    problems=[]; info={}
    for n,e in EXP.items():
        p=V/n
        if not p.is_file(): problems.append("MISSING "+n); continue
        g=sha(p); info[n]={"sha":g,"match":g==e}
        if g!=e: problems.append("SHA "+n)
        zf=zipfile.ZipFile(p)
        if zf.testzip() is not None: problems.append("CRC "+n)
        names=zf.namelist()
        if len(names)!=len(set(names)): problems.append("DUP "+n)
        if any(x.startswith("/") or ".." in x for x in names): problems.append("UNSAFE "+n)
    ev=V/"evidence"
    ssot=json.loads((V/"BCJ_V19_FINAL_SCIENTIFIC_SSOT.json").read_text(encoding="utf-8"))
    raw=jl(ev/"P04_MEASURED_RAW.jsonl"); corp={r["unit_id"]:r for r in jl(ev/"P04_MEASURED_CORPUS.jsonl")}; orc={r["unit_id"]:r for r in jl(ev/"P04_EVALUATOR_ORACLE.jsonl")}
    arms=["A1","A1+PID","A1+CI","A2"]; cs={a:set() for a in arms}
    for r in raw:
        u=r["_key"].split(":")[0]; f=corp[u]["fault_present"]; rel=bool(r["artifact_released"]); rf=bool(r.get("runtime_error")) or bool(r.get("timeout"))
        ok=False if rf else ((not rel) if f else (rel and r.get("canonical_digest")==orc[u].get("expected_canonical")))
        if ok: cs[r["arm"]].add(u)
    p4={a:len(cs[a]) for a in arms}
    exp4={a:int(ssot["P04"]["common_end_to_end_correctness"][a].split("/")[0]) for a in arms}
    if p4!=exp4: problems.append("P04 %s != %s"%(p4,exp4))
    raw5=jl(ev/"P05_R2B_RAW_OBSERVATIONS.jsonl"); orc5={r["unit_id"]:r for r in jl(ev/"P05_EVALUATOR_ORACLE.jsonl")}
    s={"V1":set(),"V2":set()}
    for r in raw5:
        u=r["unit_id"]; a=r["arm"]; auth=bool(orc5[u]["authorized"])
        if r["decision"] in ("ACCEPT","REJECT") and not r.get("runtime_error") and not r.get("timeout"):
            if ((r["decision"]=="ACCEPT") if auth else (r["decision"]=="REJECT")): s[a].add(u)
    if len(s["V1"])!=int(ssot["P05"]["V1"].split("/")[0]): problems.append("P05 V1")
    if len(s["V2"])!=int(ssot["P05"]["V2"].split("/")[0]): problems.append("P05 V2")
    rows=list(csv.DictReader(open(ev/"p06_repro_eq6_fresh.csv",encoding="utf-8",newline="")))
    eq6=sum(1 for r in rows if r["eq6_match"]=="true"); camp=sum(1 for r in rows if r["campaign_match"]=="true")
    if eq6!=30 or camp!=0: problems.append("P06 %d/%d"%(eq6,camp))
    out={"archives":info,"P04":p4,"P05":{"V1":len(s["V1"]),"V2":len(s["V2"])},"P06":{"eq6":eq6,"campaign":camp},"problems":problems}
    print(json.dumps(out,indent=2))
    return 0 if not problems else 1
if __name__=="__main__":
    sys.exit(main())
