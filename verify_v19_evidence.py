#!/usr/bin/env python3
"""Read-only archival checks for BCJ-V19; not a fresh experimental reproduction."""
import argparse
import base64
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

ARCHIVES = {
    'P01_CLOSURE_REVIEW': 'b8e3d23bd61dd6e7bc6e22d9ac91c4ac7b155b9dd7b935310ac421d117f468b7',
    'P02_R4A_REVIEW': '3513e3c926a29c6e6cc3d0dcd461b27cdee47c45cfa5e4c0bb92ef4b59a4aca3',
    'P03_FINAL_QA_CLOSED_REVIEW': '45053224dc25c314a0e305324ccb087020f3832b4fa00b569833aad18c122761',
    'P04_FINAL_MEASURED_REVIEW': '2900ffb2bca0ac91ad33d6661bcbd457976f19256b1266ca7a9e6e3f457e204b',
    'P05_FINAL_MEASURED_REVIEW': '719db8c483a40a437f7e7cfeb7797bfd1fdcd9ca1fb2bd28cd24cb4dd18a4834',
    'P05_CORRECTIVE_R2B_FINAL_REVIEW': '9abff431c6ec5d1887596ebf86de2d9ad694f536cb2842b3018b785e597f576f',
    'P07_FINAL_CONSOLIDATED_REVIEW': 'ec0e5448be666ace8ac63aa12102e18da53603230b78993077d3c2d7a1beed09',
    'P07_R1_FINAL_CORRECTIVE_REVIEW': 'b53daa567527fe2b7828a38dfb8a1732fc48081b9c6c8526a63641d2382b9d03',
}

def require(test, message):
    if not test:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(z, suffix):
    matches = [n for n in z.namelist() if n == suffix or n.endswith('/' + suffix)]
    require(len(matches) == 1, f'Expected one member {suffix}, found {matches}')
    return z.read(matches[0]).decode('utf-8-sig')


def jl(z, suffix):
    return [json.loads(x) for x in read(z, suffix).splitlines() if x.strip()]


def index(rows, key):
    out = {}
    for r in rows:
        k = key(r)
        require(k not in out, f'Duplicate key {k}')
        out[k] = r
    return out


def root(leaves):
    if not leaves:
        return sha(b'\x02\x00')
    if len(leaves) == 1:
        return leaves[0]
    k = 1 << ((len(leaves)-1).bit_length()-1)
    return sha(b'\x01' + bytes.fromhex(root(leaves[:k])) + bytes.fromhex(root(leaves[k:])))


def p03(z):
    expected = index(jl(z, 'results/P02/J01_INDEPENDENT_EXPECTED.R4A.jsonl'), lambda r: r['case_id']+':'+r['leg_id'])
    require(len(expected) == 630, 'P03 expected count')
    py, go = [index(jl(z, 'results/P03/repro_e1/e1_'+s+'.jsonl'), lambda r: r['record_id']) for s in ('py','go')]
    require(py.keys() == go.keys() == expected.keys(), 'P03 E1 membership')
    accepted = 0
    for k, e in expected.items():
        a,b = py[k],go[k]
        for r in (a,b):
            require(r['execution_status']=='OK', f'P03 execution {k}')
            require(r['admission']==e['expected_admission'] and r['reason_code']==e['expected_reason_code'], f'P03 decision {k}')
            if r['admission']=='ACCEPT':
                v=bytes.fromhex(r['canonical_bytes_hex'])
                require(v==base64.b64decode(e['expected_canonical_bytes_b64']), f'P03 canonical {k}')
                require(r['typed_business_object']==e['expected_business_object'] and r['eligible_json']==e['expected_eligible_json'], f'P03 representation {k}')
                pre=b'\x00\x03'+bytes.fromhex(r['semantic_profile_digest'])+bytes.fromhex(r['construction_digest'])+v
                require(pre.hex()==r['leaf_preimage_hex'] and sha(pre)==r['leaf_digest'],f'P03 leaf {k}')
            else:
                require(r.get('canonical_bytes_hex') is None and r.get('leaf_digest') is None, f'P03 nonadmissible {k}')
        if a['admission']=='ACCEPT':
            accepted+=1
            require(a['leaf_digest']==b['leaf_digest'],f'P03 cross-language leaf {k}')
    require(accepted==600,'P03 accepted count')
    for rset in (py,go):
        for prefix, equal in [('EQ-',True),('NEQ-',False)]:
            keys=[k for k in rset if k.startswith(prefix) and k.endswith(':A')]
            require(len(keys)==150,'P03 pair count')
            for k in keys:
                a,b=rset[k],rset[k[:-1]+'B']
                require(a['admission']==b['admission']=='ACCEPT' and (a['canonical_bytes_hex']==b['canonical_bytes_hex'])==equal,f'P03 pair {k}')
    batch=[index(jl(z,'results/P03/P03_E4_'+s+'_RESULTS.jsonl'),lambda r:r['batch_id']) for s in ('PYTHON','GO')]
    require(batch[0].keys()==batch[1].keys() and len(batch[0])==18,'P03 E4 membership')
    for rows in batch:
        leaves=nodes=0
        for k,r in rows.items():
            require(r['status']==batch[0][k]['status'] and r['root']==batch[0][k]['root'],'P03 E4 cross agreement')
            ls=r['leaf_digests'] or []; ns=r['internal_nodes'] or []
            leaves+=len(ls);nodes+=len(ns)
            if r['status']=='OK': require(root(ls)==r['root'],f'P03 E4 root {k}')
            for n in ns:
                pre=b'\x01'+bytes.fromhex(n['left'])+bytes.fromhex(n['right'])
                require(pre.hex()==n['preimage_hex'] and sha(pre)==n['digest'],f'P03 E4 node {k}')
        require((leaves,nodes)==(131,114),'P03 E4 totals')
    return {'admission_reason': '630/630 per implementation vs archived oracle', 'canonical_and_leaf': '600/600', 'EQ':150,'NEQ':150,'batch_outcomes':18,'leaves_per_implementation':131,'nodes_per_implementation':114}


def membership(rows, units, arms, uid):
    r=index(rows, lambda x:(x[uid],x['arm']))
    require(set(r)=={(u,a) for u in units for a in arms},'Unit-arm membership mismatch')
    for (u,a),v in r.items(): require(v['_key']==u+':'+a,'Inconsistent row key')
    return r


def paired(correct, units, a,b):
    c=collections.Counter((correct[u,a],correct[u,b]) for u in units)
    return [c[True,True],c[True,False],c[False,True],c[False,False]]


def p04(z):
    units=index(jl(z,'p04_evaluator/P04_MEASURED_CORPUS.jsonl'),lambda r:r['unit_id'])
    oracle=index(jl(z,'p04_evaluator/P04_EVALUATOR_ORACLE.jsonl'),lambda r:r['unit_id'])
    require(units.keys()==oracle.keys() and len(units)==100,'P04 inventory')
    require(sum(u['fault_present'] is True for u in units.values())==60,'P04 adverse count')
    arms=['A1','A1+PID','A1+CI','A2']
    rows=membership(jl(z,'results/P04/P04_MEASURED_RAW.jsonl'),units,arms,'evaluation_unit_id')
    correct={}; unsafe=collections.Counter(); benign=collections.Counter()
    for (u,a),r in rows.items():
        require(type(r['artifact_released']) is bool,'P04 release type')
        ok=r['runtime_error'] is False and r['timeout'] is False
        if units[u]['fault_present']:
            correct[u,a]=ok and not r['artifact_released']
            unsafe[a]+=r['artifact_released']
        else:
            correct[u,a]=ok and r['artifact_released'] and r['canonical_digest']==oracle[u]['expected_canonical']
            benign[a]+=correct[u,a]
    totals={a:sum(correct[u,a] for u in units) for a in arms}
    pair=paired(correct,units,'A1','A2')
    require(list(totals.values())==[45,75,55,85] and pair==[45,0,40,15] and [unsafe[a] for a in arms]==[55,25,45,15] and all(benign[a]==40 for a in arms),'P04 frozen headline discrepancy')
    return {'correct':totals,'unsafe_release':dict(unsafe),'benign':dict(benign),'paired_A1_A2':pair}


def p05(z, corrective):
    o=index(jl(z,'p05_evaluator/P05_EVALUATOR_ORACLE.jsonl'),lambda r:r['unit_id'])
    require(len(o)==40 and sum(r['authorized'] is True for r in o.values())==11,'P05 inventory')
    a=['V1','V2']; sets=[]
    for arc,path in [(z,'p05_evaluator/P05_RAW_OBSERVATIONS.jsonl'),(corrective,'p05_r2b/P05_R2B_RAW_OBSERVATIONS.jsonl')]:
        r=membership(jl(arc,path),o,a,'unit_id'); sets.append(r)
        c={(u,arm):v['runtime_error'] is False and v['timeout'] is False and v['decision']==('ACCEPT' if o[u]['authorized'] else 'REJECT') for (u,arm),v in r.items()}
        require([sum(c[u,arm] for u in o) for arm in a]==[15,40] and paired(c,o,'V1','V2')==[15,0,25,0],'P05 headline discrepancy')
        require(all(v['decision']==o[u]['expected_'+arm.lower()+'_decision'] for (u,arm),v in r.items()),'P05 archived arm oracle disagreement')
    for k,r in sets[0].items():
        require(all(r[f]==sets[1][k][f] for f in ('decision','reason','initial_state','final_state')),'P05 regression difference '+str(k))
    state=index(jl(corrective,'p05_r2b/P05_FIRST_PASS_STATE_REAUDIT.jsonl'),lambda r:r['unit_id'])
    require(state.keys()==o.keys(),'P05 state membership')
    applicable=0
    for u,r in state.items():
        actual=sets[0][u,'V2']; require(actual['initial_state']==r['expected_initial_state'] and actual['final_state']==r['expected_final_state'] and actual['decision']==r['expected_decision'],'P05 state mismatch '+u)
        if r['state_applicable']: applicable+=1
        else: require(actual['decision']=='REJECT' and actual['initial_state'] is None and actual['final_state'] is None,'P05 missing state')
    require(applicable==39,'P05 state denominator')
    return {'first_pass_and_corrective':[15,40],'paired':[15,0,25,0],'matched_differences':0,'applicable_states':39,'missing_state_control':1}


def p06(z):
    rows=list(csv.DictReader(io.StringIO(read(z,'p07/p06/repro_eq6_fresh.csv'))))
    require([int(r['j']) for r in rows]==list(range(30)),'P06 batch membership')
    a=sum(r['r_chained_manifest']==r['r_chained_reproduced_eq6'] for r in rows)
    b=sum(r['r_chained_manifest']==r['r_campaign_h02'] for r in rows)
    require((a,b)==(30,0),'P06 recorded digest discrepancy')
    require(all(not r['tx_id'] and not r['block'] for r in rows),'P06 transaction metadata unexpected')
    return {'recorded_digest_matches_eq6':a,'recorded_digest_matches_campaign':b,'formula_reexecution':False,'onchain_verification':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('archive_directory',type=Path);args=parser.parse_args()
    z={}
    try:
        for key,digest in ARCHIVES.items():
            path=args.archive_directory/('BCJ_V19_'+key+'.zip')
            require(sha(path.read_bytes())==digest,'Archive digest mismatch: '+str(path))
            arc=zipfile.ZipFile(path);z[key]=arc
            require(len(arc.namelist())==len(set(arc.namelist())) and arc.testzip() is None,'ZIP integrity: '+str(path))
        result={'scope':'archival checks only; no new execution, no third-party replication','archive_sha256_and_crc':len(z),'P03':p03(z['P03_FINAL_QA_CLOSED_REVIEW']),'P04':p04(z['P04_FINAL_MEASURED_REVIEW']),'P05':p05(z['P05_FINAL_MEASURED_REVIEW'],z['P05_CORRECTIVE_R2B_FINAL_REVIEW']),'P06':p06(z['P07_FINAL_CONSOLIDATED_REVIEW'])}
        print(json.dumps(result,indent=2))
    finally:
        for arc in z.values(): arc.close()

if __name__=='__main__': main()
