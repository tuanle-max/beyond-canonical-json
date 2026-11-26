# BCJ-V19 — Final Experiment Lead Master Evidence Report

**Beyond Canonical JSON: Semantic Interoperability Assurance for Tamper-Evident Commitment Pipelines**  
**Ngày:** 25/11/2026 | **Revision:** Master SSOT 1.0 | **Audience:** Author Lead / manuscript v19.tex  
**Disposition:** SCIENTIFICALLY CLOSED WITH REPRODUCIBILITY QUALIFICATIONS

## 0. Quyền hạn, phạm vi và cách sử dụng

Báo cáo này là bản diễn giải tổng hợp có truy xuất nguồn của hồ sơ freeze cuối cùng; không thay thế raw evidence, normative contract hoặc JSON SSOT đã chốt. Dùng cho việc viết Results, Methods, Discussion, Threats to Validity và Appendix của v19.tex. Không phải quyết định chấp nhận của IEEE Access. Không có thực nghiệm mới trong quá trình soạn báo cáo này.

Thứ tự ưu tiên: (1) `BCJ_V19_FINAL_SCIENTIFIC_SSOT.json` và `BCJ_V19_FINAL_CLAIM_RESTRICTIONS.md`; (2) quyết định Experiment Lead và raw evidence đã freeze; (3) normative specifications và execution records tương ứng; (4) derived reports; (5) bản thảo cũ. Nếu derived report mâu thuẫn với SSOT, không dùng derived report để ghi đè SSOT. Sai lệch mới phải được lập change record, không sửa ngầm raw data. Các số liệu ngoài JSON SSOT bên dưới được phân loại là evidence bổ trợ/legacy, không tự động nâng thành headline claim.

| Trạng thái | Giá trị |
|---|---|
| Scientific development | CLOSED |
| Scientific results | ACCEPTED |
| P07 headline reconciliation | ACCEPTED |
| Engineering QA | PARTIAL_WITH_DOCUMENTED_LIMITATIONS |
| Consolidated Docker clean-room | NOT_EXECUTED |
| New experiments required | false |
| Manuscript finalization authorized | true |
| Submission authorized | false_pending_final_manuscript_review |

Administrative commit được Agent báo cáo: `dc3634179bd3028ab78ff06a991f5851101bb4f1`. Final corrective commit: `fb67aefb74632e92b43318f74ad2f9be0bf199ba`. Không kiểm tra trực tiếp Git working tree trong lần tổng hợp này. Các archive và source reports được đọc từ bản đính kèm; bảng checksum cuối báo cáo được tính trực tiếp từ các ZIP hiện có. Các tuyên bố về execution lịch sử dựa trên execution artifacts và các quyết định review trước, không phải fresh execution hôm nay.

## 1. Executive scientific summary

| Phase | Đơn vị / phạm vi | Kết quả chốt | Ý nghĩa |
|---|---|---|---|
| P00 | Manuscript và evidence inventory | v18 identity fixed | Không trộn revision/campaign |
| P01 | 330 units, 630 occurrences | 600/600 coverage; 150/150 EQ; 150/150 NEQ; 30/30 abstain | Admission-aware metrics, legacy simulator |
| P02 | K-v2 contract, 31/71/21 suites kế thừa | R4a 21/21; R4 regression 71/71; compatibility 630/630 | Explicit semantics, rule-derived oracle |
| P03 | 2 implementations; E1–E4 | 630/630 admission/reason; 600/600 bytes/leaves; 18/18 batch outcomes | Cross-language interoperability under fixed contract |
| P04 | 100 units × 4 arms | 45/75/55/85 correct; +40 pp | Incremental guards, 15 shared misses |
| P05 | 40 units × 2 arms | 15/40 vs 40/40; +62.5 pp | Structural consistency ≠ authorization |
| P05 corrective | Same 40 units × 2 | 0 differences; 39/39 applicable states | Post-exposure regression, not new sample |
| P06 | 30 historical batches | Eq.6 30/30 vs campaign 0/30 | Construction mismatch reproduction |
| P07 | Consolidated evidence QA | P04 reconciliation accepted; engineering partial | Traceable results, no full clean-room claim |

Không cộng số unit của P01/P03, hoặc first-pass/corrective P05, hoặc performance repetitions với primary sample. J01 được tái sử dụng; các suites có thể trùng template/record. Các tần suất là descriptive trên purposive fixtures, không phải xác suất lỗi trong production.

## 2. Scientific thesis, RQs và formal model

### 2.1. Thesis

Deterministic serialization (JCS, RFC 8785) không tự giải quyết application semantics. Hai record cùng ý nghĩa có thể có canonical bytes khác nhau; normalization quá mạnh có thể xóa phân biệt nghiệp vụ hoặc hợp thức hóa dữ liệu malformed. Ngay cả khi canonical bytes đồng nhất, khác construction có thể tạo root khác. Ngay cả root/proof internally consistent, verifier chưa chắc được phép tin root đó. Bài báo đánh giá các nghĩa vụ bổ sung qua các tầng, không đề xuất hash, signature hoặc canonicalization primitive mới.

### 2.2. Research questions — giữ định nghĩa từ `v19_P00_P03.tex`

- RQ1: What do deterministic-byte conformance and explicit construction identity establish, and what do they leave unresolved?
- RQ2: Can a complete payment contract support admission-aware semantic agreement and distinction preservation in separately coded implementations, and which defects emerge during evaluation?
- RQ3: Can the implementations reconstruct identical commitments and localize observable divergence by pipeline stage, and what additional assurance remains unvalidated?

Author Lead có thể cập nhật phần cuối RQ3 để phản ánh P04/P05 đã thực hiện, nhưng không tự động thay bằng năm RQs từ P07 handover. P07 là cross-cutting evidence. RQ1 được hỗ trợ bởi legacy JCS và P06; RQ2 bởi P01–P03; RQ3 bởi P03 E4/attribution, P04 và P05. Đây là mapping đề xuất, không phải RQ mới.

### 2.3. Formal definitions

D_K+ = admissible records; D_K− = malformed or prohibited; D_K? = underspecified. β_K(d) là business interpretation trên D_K+. F_j(d) = JCS(E_j(T_j(d))) nếu accepted, ngược lại ⊥ (không phải bytes). Ba quan hệ: business equivalence (β equality), canonical-input equivalence (eligible JSON equality), full commitment-input equivalence (bytes plus profile, construction, ordered occurrences and auxiliary context).

| Obligation | Normative requirement | Empirical evidence |
|---|---|---|
| O1 | All admissible inputs have defined bytes | P01/P03 coverage |
| O2 | Nonadmissible records yield no bytes | P01 underspecified; P02/P03 boundary/adversarial |
| O3 | Equivalent admissible records yield identical bytes | EQ pair success |
| O4 | Distinct admissible records yield different bytes | NEQ pair success |
| O5 | Separate implementations agree under same contract | P03 per-occurrence exact comparisons |

O1+O3+O4 imply a well-defined injective representation on the quotient of D_K+ by business equivalence. This is a conditional proposition, not a proof of universal implementation correctness. O5 remains separate. Identical ordered leaf preimages, identical topology and auxiliary context imply identical roots by determinism; converse does not follow from finite hash equality. Neither proposition proves inventory completeness, business truth, signer authorization or source authenticity.

### 2.4. Metric conventions

Coverage Cov_U = number of unique admissible inputs accepted / all unique expected-admissible inputs. Occurrence coverage is reported separately. S_E = pairs with both legs accepted and equal bytes / all labeled admissible EQ pairs. S_D = pairs with both legs accepted and unequal bytes / all labeled admissible NEQ pairs. Rejection/abstention are never equal-byte successes. Zero denominator => N/A. Decision categories: ACCEPT, REJECT_MALFORMED, REJECT_PROHIBITED, ABSTAIN_UNDERSPECIFIED; INTERNAL_ERROR and TIMEOUT are execution failures, not successful rejection. Exact reason agreement is additional diagnostic evidence, not identical to O1–O5.

P04 objective is safe release, not semantic admission; P05 objective is authorization, not structural consistency. Do not reuse a common binary classifier across those objectives.

## 3. P00 — Provenance and historical campaign

**Purpose:** freeze authoritative manuscript identity, reconcile historical numerical claims and preserve source variants. `MANUSCRIPT_DRIFT_REPORT.md` documents four manuscript candidates; `MANUSCRIPT_FREEZE_ATTESTATION.json` records Author Lead approval. `tex/v18.tex` SHA-256 `68d8c56078d8342785d882301e0703f4116d6c71381de1518a5afe099a85abf7`, freeze commit `40376dad1f0cf9ed75838aad84695a1cbfd139f5`, 82,567 bytes, LF. The LNNS manuscript and prior IEEE Access SSOT were preserved separately. Do not treat them as additional independent datasets. P00 inventory/approval details not all available as a standalone archive; this section is based on P01/P02/P03 retained records and intermediate manuscript.

P01 was executed before formal phase approval. The process deviation was preserved and retrospectively accepted; do not describe P01 as prospectively preregistered. P00–P02 reconcile archival provenance, not third-party verification.

### 3.1. Historical evidence (legacy; not new v19 validation)

Source: `v18(1).tex` / `v19_P00_P03.tex` historical sections and archived P01 evidence. The original legacy raw corpus and full campaign execution are not freshly rerun in this report. Historical claims should carry archival labels; priority is new frozen P03–P06 evidence.

| Legacy metric | Historical result | Scope |
|---|---|---|
| Three JCS backends common cases | 20/20 | Do not confuse with separate canonicalization-drift paper's 102 cases |
| Golden vectors | 200/200 | Reported legacy check |
| Sealed synthetic pairs | 7,900 | 7,750 schema-accepted; 150 syntactically invalid |
| Resolved equivalent / unresolved among accepted | 7,250 / 500 | Corpus composition, not incidence |
| J01 | 150 EQ +150 NEQ +30 ambiguous | 330 units, 630 occurrences |
| J02 raw JCS A0 EQ failure | 150/150 | Diagnostic only |
| J02 typed baseline EQ failures | 0/150 | Simulator-level |
| J02 raw JCS ambiguous admission | 30/30 | Typed alternatives abstained 30/30 |
| J02 profile mismatch / regression signals | 20/20 and 10/10 | Mixed historical guard/passive scope; not matched causal proof |
| G2 | 140 selected units | Shared transform plus third-party JCS |
| G2 digest agreement | 220/220 | 100 EQ legs +100 NEQ legs +10 profile +10 regression; 20 ambiguous no bytes |
| G2 structural proofs / tampered proofs | 70/70 accepted; 5/5 rejected | Supplied-root structural verification only |
| G2 known-answer leaf/root | 6/6 | Historical construction |
| Legacy performance 5,000 events | 0.893 s vs 1.184 s mean; 2.78 MiB each | Unmatched boundary, not v3 overhead |

Legacy semantic manifest minimal: drtea-payment, v1.0, timestamp-iso8601-utc-required, amount-decimal-2-round-half-up, unicode-nfc. Historical pid prefix `d7deab47`, construction label `b5642feb` (four bytes). Legacy v2 leaf = H(0x0002 || pid_sem[32] || v_commit[4] || canonical_bytes). A four-byte construction identity is not a full cryptographic-strength digest. Historical v2 unchanged; normative v3 is distinct. Null/absent and alias rules were partly implicit in legacy simulator.

## 4. P01 — Admission-aware legacy replay

Source P01 closure archive: `results/P01/REPORT.md`, `results/P02/P01_CLOSURE_REPORT.md`, per-leg JSONL, derived J01 metrics. Run label NEW_LEGACY_REPLAY, K-v1 via `scripts/jcommon.py`. Same legacy machinery informed expected and observed semantics; Level S (simulator), not separately implemented external adjudication.

J01 five families: timestamp/precision, amount/units, Unicode/identifiers, null/defaults, aliases. Each 30 EQ and 30 NEQ pairs; additionally 30 underspecified singles across corpus. 600 pair legs +30 singles = 630 occurrences. 630 distinct recorded reconstructed serialization digests, not original captured transport bytes. 600 admissible, 0 malformed/prohibited, 30 underspecified.

| Metric | Numerator/denominator | Meaning |
|---|---|---|
| M1 unique valid coverage | 600/600 | All expected valid accepted |
| M2 EQ success | 150/150 | Both accepted, bytes equal |
| M3 NEQ success | 150/150 | Both accepted, bytes unequal |
| M4 malformed/prohibited rejection | N/A (0 cases) | No coverage of this category |
| M5 underspecified abstention | 30/30 | No commitment |
| M6 unsafe admission | 0/30 | Underspecified controls only |
| M7 false rejection | 0/600 | Valid domain |
| Internal errors | 0 recorded | Not universal error freedom |

Degenerate controls: reject-all gives coverage 0, S_E=0, S_D=0; constant output gives coverage 100%, S_E=100%, S_D=0, unsafe admission 30/30. These validate metric design, not scientific competing baselines. P01 closure corrected stale checksum/status entry and added incorrect-pair-relationship mutation control; raw evidence preserved. SHA of reconstructed source corpus recorded as `f8154681e4a2f1e65c7dd6d3477a357837856278939282a2e483b8353bb899e2`. No original raw-byte capture. `raw_sha256` was sha256 of `json.dumps(doc, sort_keys=True)`.

## 5. P02 — Normative K-v2, oracle design, and commitment identity

### 5.1. Effective semantics (abridged; normative source takes precedence)

| Field/rule | Effective contract |
|---|---|
| Event ID | ASCII letters/digits/underscore/hyphen, 1–256; exact, no normalization |
| Timestamp | Integer epoch-ms or supported timestamp string with seconds, timezone; 1–6 fractional digits; offset minute 00/15/30/45; years 0001–9999; leap seconds rejected; floor toward −∞ including pre-epoch; safe integer range |
| Amount | Exact decimal lexeme, string or supported raw number; no exponent/grouping/positive sign; 16 integer digits, 6 fractional, length ≤24; negative including −0 prohibited; quantized payable minor units |
| Currency | Exact uppercase USD/EUR scale 2, VND scale 0; scale must match registry; no FX inference |
| Beneficiary | Required; NFC Unicode 15.0.0; no trim/case folding; empty, malformed Unicode, C0/C1 controls rejected |
| Obligation reference | Optional printable ASCII 1–256; exact; absent and null map to null |
| Aliases | Validate all supplied forms; conflicts prohibited; normalization cannot excuse malformed originals |
| Parser/schema | Strict UTF-8, duplicate members rejected, closed fields; raw numeric lexemes; no implicit binary64 rounding |
| Diagnostic precedence | malformed > prohibited > underspecified; fixed within-category reason order |

Eligible business object contains eid, t, minor, cur, bc, ref. q_s(x)=floor(10^s x+1/2) for permitted nonnegative lexeme. Safe minor units ≤2^53−1. Example USD 2.675→268, 2.674999→267. This is contract-relative quantized business identity, not general financial semantics. Do not claim all Unicode, timestamps or currencies supported.

### 5.2. Contract and construction freeze

- pid_sem_v2 = SHA256(JCS(semantic_manifest)) = `caa2f3e561edbac1f73ec2926bea8009cce176ba8b8c7f900ebc7e8de454b429`.
- construction_digest = SHA256(JCS(construction_manifest)) = `d1e46eb5c6e0688b03c085ce5ed83ba134fffc6638a5fc0df8ed143b12aaf91d`.
- Normative manifest binds contract, field semantics, taxonomy, registry and other listed normative artifacts; validate referenced bytes. Software provenance identity separate; digest binding does not establish implementation conformance.
- v3 leaf L_i = SHA256(0x0003 || pid[32] || cd[32] || F(d_i)). Internal H(0x01 || left || right). Empty H(0x0200). Singleton returns leaf. For n>1, split at largest power of two strictly below n (RFC 9162 recursive tree shape, not whole protocol).
- Batch ordered, duplicate occurrences retained, nonaccepted excluded and accounted. Required membership is multiset inclusion: for every required ID x, m_supplied(x)≥m_required(x); failure gives no successful root. Extra supplied records allowed; supplied invalid record differs from missing record. Empty root itself does not bind identities; signed checkpoint must bind context separately.

### 5.3. Corrective chronology

R1–R3 draft contract and candidate manifests; R3 boundary 25 cases and 12 pairs, J01 compatibility checked; no authority to start measured P03 at draft stage. R4 expanded boundary/adversarial control; R4a repaired oracle: unpaired surrogate handling, fullmatch lexical rules, independent monetary grammar, scale/resource bounds, timestamp calendar boundaries, unique sentinel, expected/observed separation and provenance. Old R4 oracle reproduced 12/21 corrective defects. Repaired R4a passed 21/21 and R4 regression 71/71; 0 exceptions reported. J01 independently coded adjudicator vs observed: 630/630 admission/reason/business/eligible/canonical and unchanged 150 EQ,150 NEQ,30 abstain. Expected/repair developed by same agent sequentially; earlier R4 chronology shared commit; not blind or external human adjudication. P03 preflight taxonomy sync changed candidate digests; only final IDs above authoritative. Final KAT suite 10 descriptors, 28 leaves,19 internal nodes; exact domain separation and odd tree handling; not a measured production sample.

## 6. P03 — Cross-language interoperability and defect discovery

### 6.1. Implementation environment and separation

Python 3.12.9, Unicode data 15.0.0, `rfc8785==0.1.3`; Go 1.23.12 on linux/amd64 Docker image `golang@sha256:167053a2bb901972bf2c1611f8f52c44d5fe7e762e5cab213708d82c421614db`, `golang.org/x/text v0.19.0`, `github.com/gowebpki/jcs v1.0.1`, normalization version 15.0.0. Windows Application Control blocked native compile.exe; Docker resolved the blocker for Go. The Unicode 15 NormalizationTest corpus (`fb9ac8cc154a80cad6caac9897af55a4e75176af6f4e2bb6edc2bf8b1d57f326`) had 19,074 listed records and 95,370 NFC assertions per implementation passing; not exhaustive Unicode conformance. Implementation workspaces received contract and development materials, not evaluator-owned J01 expected outputs under procedural isolation; no independent authorship or adversarial blinding claim.

Initial Python commit `8bcad2914b1e0d277dde873e2176af90d6520278`; Go `f34220d7765812fd611b7c9413cf6e90c38bcf08`. Final source digests under CRLF rendering: Python `2b6924010d528f39c05ac1f5d332ecee814e2d6a09fa3e38425daa97d119355f`; Go `493102b2265996b734f2d67931ed07547d69026af09d0ea0dbe9f1a98467a5fa`. LF digests differ; use exact variants in P04 lock. P03 final QA commit `deac7e74b643adac229e877a5a20c723909b9ba0`.

### 6.2. E1 — J01 replay under K-v2 (both final implementations)

| Outcome | Python | Go | Cross-language / qualification |
|---|---|---|---|
| Admission vs expected | 630/630 | 630/630 | 630/630 agreement |
| Reason vs expected | 630/630 | 630/630 | 630/630 agreement |
| Admissible coverage | 600/600 | 600/600 | Same 600 occurrences |
| Typed objects | 600/600 | 600/600 | Exact agreement |
| Eligible JSON | 600/600 | 600/600 | Exact agreement |
| Canonical bytes | 600/600 | 600/600 | Exact byte agreement, not just hash |
| Commitment leaves | 600/600 | 600/600 | Digest agreement; preimages rechecked in prior review |
| EQ pairs | 150/150 | 150/150 | Both legs accepted |
| NEQ pairs | 150/150 | 150/150 | Both legs accepted |
| Abstention | 30/30 | 30/30 | No bytes |
| Unsafe admission | 0/30 | 0/30 | Not a population estimate |
| False rejection/nonadmission | 0/600 | 0/600 | Valid occurrence scope |

E1 is a regression on reconstructed historical units, not unseen evaluation. Separate per-implementation comparisons to locked expected evidence and cross-implementation comparisons must be reported distinctly.

### 6.3. E2/E3 — Boundary/adversarial first pass and corrected regression

| Suite | Size | Python first pass | Go first pass (reported suite totals) | Final Python / Go |
|---|---:|---:|---:|---:|
| E2 boundary | 31 | 31/31 | 30/31 | 31/31 each |
| E3 R4 | 71 | 71/71 | 69/71 | 71/71 each |
| E3 R4a | 21 | 21/21 | 20/21 | 21/21 each |
| E2 pair register | 12 | 12/12 | one pair affected by alias error | 12/12 |

Historical first-pass report lists five discrepant cases (four unsafe admissions, one reason-only discrepancy): R4-29/B04/B06 alias conflicts admitted; M05 negative scale admitted; S05 malformed event_id surrogate had incorrect reason precedence. **Caution:** the suite aggregate deficits 1+2+1=4 do not reconcile with five case-level discrepancies in the narrative. Do not state “five failures out of 123” as a frozen aggregate without reconciling exact admission-vs-reason metrics and repeated case IDs. Safe manuscript wording: initial Go evaluation exposed alias-conflict, negative-scale, and surrogate-diagnostic defects; final regression matched all three suite expectations. Preserve historical discrepant outputs; post-exposure repair, not generalization.

Additional diagnostic defects: both implementations initially used set membership instead of multiset completeness; M01 expected A,A,B supplied A,B and M03 expected A,A,A,B supplied A,B should fail. M02 complete control passes. Malformed-Unicode sentinel collision: literal U+FFFD vs escaped unpaired surrogate in beneficiary alias could yield identical admitted canonical/leaf in initial Go (leaf `c2d0f9411d5264f3430299e6ef63ce0334a13fb6480202c8fab035ce9b5184da`); this is unsafe precommitment collapse, not SHA collision. Corrections enforce multiplicity and malformed-before-conflict precedence. Preserve counterexamples; no new independent samples.

### 6.4. E4 — Batch reconstruction

18 batch descriptors, including varied cardinalities (1,2,3,4,5,7,8,16,31,32), duplicates, ordering and membership controls. Both implementations matched expected batch status, leaf sequence, internal nodes and root outcome for 18/18 descriptors. 131 recorded leaf occurrences and 114 internal-node occurrences per implementation; 131/131 leaf and 114/114 node digest checks per implementation in accepted evidence. Cross roots 18/18 descriptor outcomes. Expected failed batches must not be counted as successful roots; say “18/18 batch-root outcomes” unless restricting to successful-root subset. Root equality does not show independent business truth or complete inventory.

### 6.5. L0–L7 diagnostic attribution

L0 admission; L1 typed business transformation; L2 eligible mapping; L3 canonical serialization; L4 identity metadata; L5 leaf encoding/digest; L6 batch ordering/context; L7 tree structure/root. Eleven original controlled in-memory perturbations: 10 observable divergences, 9/11 exact first-stage matches, one canonical serialization no effect, one batch ordering expected L6 observed L5. Two corrective targeted controls pass 2/2 separately (positive L3, corrected L5/L6). Do not pool as 11/11 or claim universal fault localization.

### 6.6. Final QA and limits

Fresh extraction ran with two WindowsPath+str orchestration fixes and per-suite resumes; no uninterrupted historical run-all evidence. Reported 15/15 listed provenance matches and 8/8 mutations, but independent aggregation and mutation execution records incomplete. Final Experiment Lead review performed frozen-evidence reaggregation and recorded-leaf/node reconstruction; not fresh cross-language pipeline execution. F01–F05 remain qualified as specified in final register. P03 scientific results accepted, implementations frozen; no additional standalone run.

## 7. P04 — Matched incremental execution-assurance evaluation

### 7.1. Objective and design

Research question: with the same frozen K-v2 semantic engine, JCS and v3 commitment construction, what incremental protection does identity checking and a finite regression guard provide against unsafe artifact release? This is not a comparison of different normalization algorithms. P04 A1 is a strong baseline with the same typed parser, transforms, commitment and membership validation as A2. Four measured configurations differ only in enabled mechanisms.

| Arm | Common pipeline | Additional mechanism | Role |
|---|---|---|---|
| A0 | Raw JCS | None | Diagnostic only, not in 400 measured observations |
| A1 | Frozen Python K-v2 + JCS + v3 | None | Strong matched baseline |
| A1+PID | Same | Provisioned expected semantic/construction identity comparison | Identity ablation |
| A1+CI | Same | Finite regression checks at build/deployment boundary | Behavioral ablation |
| A2 | Same | Both guards | Combined architecture |
| N0/N1 | Reject-all / constant output | — | Metric-design controls, not competing measured systems |

Identity checking compares declared identifiers and bound configuration artifacts against expected identity; it does not establish that executable behavior actually follows them, and it does not authenticate a checkpoint. CI detects only regressions exercised by the frozen finite suite. A guard alarm is not equivalent to a prevented release. Passive digest divergence is not an alarm. A crash/timeout is not successful detection or prevention.

Corpus: 100 purposively designed units, four groups of 25 (15 adverse, 10 benign per group); 60 adverse,40 benign. Each unit evaluated under four arms: 400 unique unit-arm observations. Frozen synthetic, not blinded or third-party. Separate development D_DEV, regression D_CI, historical D_HIST, evaluator D_EVAL, performance D_PERF. Exact raw overlaps with dev/CI reported zero for 142 unique evaluator raw instances; template/operator and canonical/historical exposure comparisons incomplete. Do not call these unseen mechanism families.

| Group | Fault family | Operators (frozen examples) | Expected guard boundary |
|---|---|---|---|
| G1 | Semantic profile mismatch | g1_normative_artifact, g1_semantic_version, g1_unicode_fields | Identity-visible |
| G2 | Construction mismatch | g2_empty_root, g2_leaf_formula, g2_tree_policy | Identity-visible |
| G3 | Semantic transformation regression | g3_rounding_half_down, g3_scale_registry, g3_ts_plus1ms | Finite CI exercised |
| G4 | Hidden encoding/batch regression | g4_leaf_prefix, g4_node_prefix, g4_tree_topology | Outside evaluated guard coverage |

R3 development 24 observations (6×4); R4 development 48 observations (12×4), development only. R2 preregistration; CR-0011 preserved unrelated working-tree drift and recovered only necessary R2 artifacts into separate worktree. R3 proof-of-concept accepted; R4 strengthened operator coverage, A0 diagnostic, structured alarms, actual harness and metrics. Final R4A Go cross-check on 143 occurrences (142 unique) and 16 batch units reported no mismatches across compared admission/reason/canonical/leaf/batch/root fields. Same-team reference corroboration; not a second measured 400-observation experiment. Null vs empty-array serialization was normalized in batch comparison. Final measured commit `d293c4423a6f81debda6ee84d4b46f6df0b6278d`, run `p04d:40301435501d43d6`. Final lock report digest `37180cfafa394feb6138931e9ccb384236573c77224ebd5f331c2d5159fb0a0a`. Corpus/oracle/fault manifest hashes in Appendix B.

### 7.2. Primary metric — normative safe end-to-end release

For each unit u and configuration a, C(u,a)=1 if execution completed without failure AND either (i) adverse fixture and artifact not released, or (ii) benign fixture and artifact released with expected canonical digest; otherwise 0. This is the frozen operational objective for constructed fixtures, not full general-purpose verification of all commitment fields. Fault fixture any release counts unsafe. Do not treat semantic ACCEPT alone as success or guard blocking alone as false nonadmission. Missing observations/invalid execution cannot receive credit. All arms must have exact planned unit membership. Primary paired comparison A1 vs A2 explicitly, not sorted arm order.

### 7.3. Final frozen results

| Arm | Correct /100 | Correct adverse /60 | Unsafe releases /60 | Correct benign /40 |
|---|---:|---:|---:|---:|
| A1 | 45 | 5 | 55 | 40 |
| A1+PID | 75 | 35 | 25 | 40 |
| A1+CI | 55 | 15 | 45 | 40 |
| A2 | 85 | 45 | 15 | 40 |

| Group | A1 | A1+PID | A1+CI | A2 |
|---|---:|---:|---:|---:|
| G1 | 10/25 | 25/25 | 10/25 | 25/25 |
| G2 | 10/25 | 25/25 | 10/25 | 25/25 |
| G3 | 15/25 | 15/25 | 25/25 | 25/25 |
| G4 | 10/25 | 10/25 | 10/25 | 10/25 |

Paired A1/A2: both correct 45; A1 only 0; A2 only 40; neither correct 15. Effect (40−0)/100=+0.40 = 40 percentage points. Unsafe-release reduction (55−15)/55=72.727% relative, or 66.667 pp among adverse fixtures (91.667% to 25%). A2 prevents unsafe release in 45/60 adverse fixtures (75%), five of which were already correctly rejected by A1; incremental prevention =40. All arms preserve 40/40 benign controls. Recorded runtime failures 0. No production prevalence or statistical generalization; the unit pairing is descriptive.

### 7.4. Secondary observations (original measured evidence; qualified)

Original report: identity guard 30/30 applicable faults alarmed; CI 15/15 applicable faults alarmed; 0 benign false alarms among 40 controls. CI adds only 10 correct outcomes because A1 already rejects five scale violations (G3-F03/F06/F09/F12/F15). A2 identity guard can block before CI: original raw records showed 30 identity blocks, CI executed on 70 remaining units (15 applicable adverse,15 nonapplicable adverse,40 benign); the absent 30 executions are NOT_EXECUTED, not detector true negatives. Absent detectors N/A. Do not pool confusion matrices across arms or use complete negative denominators from P07-R1, which were incomplete. Retain 15 G4 shared misses as a substantive negative finding. Their identity declarations remain unchanged and finite record-level CI does not cover those mutations. Do not infer generalized fault activation from the manifest alone; predicted and observed activation differ. P04 attribution secondary metrics remain scoped, no universal localization claim.

### 7.5. Performance (original P04 measured CSV, not P07-R1 re-derived)

Batch sizes 100,1,000,5,000; 3 warmups+10 measured per arm/size; 36 warmups +120 measured =156 rows; seed42. `perf_counter_ns` timing; Python tracemalloc peak allocated bytes, NOT RSS. Actual combined processing and guard path; no component timing isolation, no startup cost or lifecycle-wide overhead claim. Table is the original archived summary, not fresh independent recomputation in this report.

| Arm | Batch size | Median ms | Q1 ms | Q3 ms | Median peak allocated bytes |
|---|---:|---:|---:|---:|---:|
| A1 | 100 | 31.982 | 30.376 | 35.519 | 64,859 |
| A1 | 1,000 | 322.623 | 303.450 | 353.804 | 751,079 |
| A1 | 5,000 | 1,635.914 | 1,548.204 | 1,806.976 | 3,823,883 |
| A1+PID | 100 | 32.116 | 29.323 | 39.603 | 68,752 |
| A1+PID | 1,000 | 332.861 | 302.162 | 370.283 | 752,871 |
| A1+PID | 5,000 | 1,726.139 | 1,626.988 | 1,778.916 | 3,817,768 |
| A1+CI | 100 | 30.220 | 28.750 | 34.998 | 69,783 |
| A1+CI | 1,000 | 329.043 | 307.351 | 380.210 | 756,166 |
| A1+CI | 5,000 | 1,613.850 | 1,569.026 | 1,704.577 | 3,822,096 |
| A2 | 100 | 32.656 | 29.320 | 39.223 | 71,316 |
| A2 | 1,000 | 305.797 | 297.716 | 325.686 | 754,787 |
| A2 | 5,000 | 1,807.601 | 1,594.384 | 1,955.181 | 3,816,765 |

A2 vs A1 median combined differences +2.11%, −5.22%, +10.49%. IQR overlap; do not infer statistically significant speedup at 1,000 or isolated guard cost. Actual runner processed common pipeline then checked guards; does not benchmark early blocking or deployment lifecycle. P07-R1 failed to recognize `duration_ns` and output NO_LATENCY_COLUMN; use original summary only with attribution or omit performance from main claims. Source: final measured ZIP `results/P04/P04_PERFORMANCE_RAW.csv`, `P04_PERFORMANCE_SUMMARY.csv`, `P04_PERFORMANCE_META.json`.

### 7.6. P04 closure and P07 reconciliation

P04 science CLOSED, QA qualified; F24–F30 transferred. Original P07 classifier used observed admission vs expected semantic admission, producing A1 94, PID64, CI84, A2 54. Those numbers are invalid as common-objective correctness; prior P07 compared alphabetical A1/A1+CI rather than A1/A2. P07-R1 restored safe-release classifier, exact 400 keys and explicit paired comparison; 45/75/55/85 and 45/0/40/15 agreed with accepted reference. Final Experiment Lead separately reaggregated original raw evidence in previous review. Quarantine obsolete tables and narratives. P07-R1 trace field `commitment_correct` compares canonical digest only; no claim of exhaustive leaf/root correctness in P04 metric.

## 8. P05 — Authenticated trusted-reference verification

### 8.1. Objective, threat model and mechanism

Distinguish internal structural consistency from authorization under independently provisioned trust context. V1 checks record-to-leaf, supported construction, proof path/index/tree size and supplied root. V2 shares the structural code and adds authenticated reference, authorized signer/checkpoint, context matching and sequence-based freshness. V1 acceptance of internally consistent unauthorized evidence is not a defect under its own contract.

Checkpoint binds checkpoint_id, publisher_id, semantic_profile_digest, construction_digest, root, batch_id, tree_size, checkpoint_sequence. Signing preimage: `b"BCJ-V19-P05-CHECKPOINT\x00\x01" || JCS(checkpoint)`; Ed25519. Trust context supplied independently of untrusted evidence envelope, including trusted key/publisher, expected identity and batch/checkpoint selection constraints, sequence floor and state. Embedded key is not trust authority. Distinguish signature validity, signer authorization, reference authorization, evidence/context consistency, freshness. Exact replay accepted under matching authorized checkpoint ID, sequence and checkpoint digest; equal-sequence conflict rejected; stale/rollback below floor or last sequence rejected. State advances only after all required checks pass; rejected evidence does not advance state. Missing-state control rejects and leaves state absent. Synthetic deterministic keys (seed `P05-R2A-SEED-42`) reproducible; signing/verifier interface separation, not secure key custody or OS sandbox guarantee. Threat model excludes compromised authorized signer, compromised provisioning, wall-clock freshness, distributed consensus, business truth.

Logical abstraction (not proof of code): V1(e)=S(e); V2(e,c,T,s)=S(e)∧SigValid(c,T)∧Authorized(c,T)∧Consistent(e,c,T)∧Fresh(c,T,s). Acceptance by V2 implies structural acceptance under this shared contract; converse not generally true. P05 provides 25 evaluated counterexamples.

### 8.2. Design, groups, inventory

Prereg R1 initially 10 benign/30 adverse; final approved inventory after exact-replay decision is 11 authorized/29 adverse, 40 total. Two arms per unit =80 primary observations. All units synthetic purposive. Within each adverse fixture, correct outcome is actual REJECT, not INTERNAL_ERROR/TIMEOUT/INVALID_CONFIG or absent output; authorized requires actual ACCEPT. Own structural correctness evaluated separately. Do not equate absence of authorization functionality with structural implementation error.

| Group | N | Definition | V1 correct | V2 correct |
|---|---:|---|---:|---:|
| G1 | 10 | Authorized valid controls | 10 | 10 |
| G2 | 6 | Coordinated structurally consistent unauthorized substitutions | 0 | 6 |
| G3 | 4 | Unauthorized declared semantic-profile identifiers | 0 | 4 |
| G4 | 4 | Unauthorized declared construction identifiers | 0 | 4 |
| G5 | 4 | Structurally invalid root/proof fixtures | 4 | 4 |
| G6 | 4 | Signature/key/publisher authorization violations | 0 | 4 |
| G7 | 4 | Missing trusted-reference conditions incl missing state | 0 | 4 |
| G8 | 4 | Sequence/freshness/replay including one authorized exact replay | 1 | 4 |
| Total | 40 | 11 authorized,29 adverse | 15 | 40 |

G2 six variants: amount, timestamp, beneficiary, alternative membership, duplicate and reordered evidence; supplied replacements internally consistent, original authenticated checkpoint retained. Not a hash collision. G3/G4 use unauthorized declared IDs with same actual K-v2/v3 engine; not independently implemented alternate profiles/algorithms. G6 not exclusively invalid signatures. G8 authorized replay belongs to authorized denominator.

### 8.3. First-pass frozen scientific results

| Metric | V1 | V2 |
|---|---:|---:|
| Common authorization-objective correctness | 15/40 (37.5%) | 40/40 (100%) |
| Own structural contract (V1) | 40/40 | N/A as separate arm metric |
| Authorized acceptance | 11/11 | 11/11 |
| Structurally invalid rejection | 4/4 | 4/4 |
| Structurally valid unauthorized acceptance | 25/25 | 0/25 |
| Coordinated substitution acceptance | 6/6 | 0/6 |
| False rejection of authorized controls | 0/11 | 0/11 |
| Recorded execution failures | 0 | 0 |

Paired both correct 15, V1 only 0, V2 only 25, neither0; +62.5 percentage points. Do not report 100% generalized security. First-pass measured commit `9e9f952acaf3bf196306dc81b877d5583a25a185`; run `p05d:24ca93148824a83c`. Historical reason-category agreement 80/80 (against historical expected reasons, not independent reason oracle). V2 reason categories reported: ACCEPT_AUTHORIZED11; EVIDENCE_INCONSISTENT6; PROFILE_MISMATCH4; CONSTRUCTION_MISMATCH4; MISSING_TRUSTED_REFERENCE4; ROOT_MISMATCH3; INVALID_SIGNATURE2; STALE_SEQUENCE2; PROOF_INVALID1; UNTRUSTED_KEY1; UNKNOWN_PUBLISHER1; SEQUENCE_CONFLICT1. Counts sum40; labels characterize fixtures, not distinct attack families or detection coverage.

### 8.4. Corrective chronology and independent decision corroboration

First-pass accepted with qualifications, corrective validation mandatory. F40 strict input parsing; F41 separately coded checker; F42 scope for declared identifiers; F43 exact state aggregation; F44 prospective execution lock; F45 actual QA; F46 retrospective consolidated spec; F47 deterministic key scope; F48 dependency closure. Partial R2B commit `edce1a46b40747be623f57219235443ed5242f46` delivered separate decision checker; V2 partial `d1e7eb9fae6ce7ef7c854723f7c9a70fa4c7013b` exact state audit. Checker independently implements leaf/node/path/preimage/signature/trust/freshness, reuses frozen P03 semantic adapter and standard cryptographic libraries, no import of production verification implementation. 40/40 decision agreement with historical oracle; not exact reason reconstruction or independent full inventory reconstruction. Same-team post-exposure; not blind/third-party. Broad exception handling caveat preserved.

Exact state audit: all 40 initial states match frozen inputs; 39/39 applicable final states exact; 1 missing-state N/A (`P05-G7-04`) correctly rejected without creating state. Earlier first-pass report 40/40 state transitions is superseded; use 39/39 +1 N/A. State correctness is not simply counting accepted units. Corrective run after input-validation hardening used same corpus 40×2=80, label POST_EXPOSURE_REGRESSION_VALIDATION, lock `f5eb6b589d06268d3fbd4b624b4d5bc2ec61c8f6b35bd26dd6c1d87055bd5d08`; final commit `8ad0afa5b124eee9fbcfa1a3e021fd6011b68030`. 15/40 vs40/40, same paired table, authorized and unauthorized counts unchanged, 39/39 applicable states +1 N/A, reason agreement 80/80, zero recorded errors. Across 80 matched first-pass/corrective keys: zero decision, reason, initial-state and final-state differences (previous Experiment Lead comparison of original raw evidence). Do not pool repeated observations as 80 independent units or claim generalization to new inputs.

### 8.5. Corrective QA and limitations

Agent recorded 24/24 conditions; some were standalone assertions rather than production integration tests. Strict raw parser exists but full transport integration/state schema incomplete; partial lock enforcement, runner chronology and bounded timeout integration not completely established. Source audits found failure accounting expression `(decision == "ACCEPT") == authorized` can credit errors as adverse rejection; P07-R1 corrected primary aggregation to require actual ACCEPT/REJECT without failures. No observed errors in delivered corpus, so headline results unchanged. F49–F55 carryover covers residual F40/44/45/48 without duplicating IDs. First-pass and corrective archives preserved separately. P05 SCIENTIFIC CLOSED; no universal fail-closed, production-ready or fully independent replication claim.

## 9. P06 — Reproduction of historical construction discrepancy (CR-0006)

Initially blocked because historical inputs/formulas not located. Recovered in P07 repository search; original manifest and two formula sources identified, fresh reproduction reported. 30 batches, seed42, 30×1,681 regenerated events, ordering j=0..29, one randint per batch as recorded in inventory. Raw 32-byte leaves and lowercase hex published roots. Historical tree leaf H(0x00||d), node H(0x01||L||R), odd leaf duplicated. This is a different historical tree rule from v3 recursive split.

Artifact Eq.6: r_j = MerkleRoot([r_(j−1)] + B_j). Campaign: r_j = H(0x02 || uint64_be(j) || r_(j−1) || MerkleRoot(B_j)). The recovered inventory specifies exact serialization and ordering; original code is authoritative. First divergence at j=0. Manifest root `6860e20e18c2ca15c0c4c8e15c50fe6655f45e05a98449108bb2386dd80b1b48`; campaign root `243b7c29a7ad371aa040374b0603f37bdbf5432420e21169aa61feadd8f14a32`.

| Outcome | Result |
|---|---:|
| Artifact Eq.6 matches historical manifest | 30/30 |
| Campaign alternative matches historical manifest | 0/30 |
| Fresh output agrees with historical derived CSV | 30/30 |
| Independent on-chain verification | NOT ESTABLISHED |

Evidence path: P07 original consolidated ZIP `p07/p06/P06_RECOVERY_INVENTORY.json`, `repro_eq6_fresh.csv`, `P06_FINAL_DISPOSITION.md` and logs. Source manifest `docs/drtea_mainnet_manifest_REAL.json` hash `f5dbc2fe037db808885d35648c4e2dd84df32e684c3e98b9056a41da181e9e3b`. Campaign source `py/canon/hashing.py`; artifact reproduction `scripts/drtea_eq6_repro.py`; historical CSVs `derived/legacy_validation_real.csv`, `derived/legacy_validation_real_eq6.csv`. Source digests listed in Appendix B. Original source/manifest bytes not included in the final consolidated ZIP reviewed here; source identities are inventory records. Fresh CSV tx_id and block blank; no blockchain transaction verification, no production dataset claim. P07-R1 p06() reports existing counts rather than rerunning formulas; use original fresh reconstruction evidence, not a second independent reconstruction. Scientific result accepted with provenance scope. Label REPRODUCTION_OF_HISTORICAL; not newly discovered mismatch, not SHA collision or JCS failure. Demonstrates construction identity matters independently of semantic normalization.

## 10. P07 — Consolidated QA, corrections and final administrative closure

P07 initial commit `529630219663f511b4b80ee7489604ad125d9d8f`. Agent reported 14/14 mutation/integration tests, fresh-directory P05 execution, no Docker clean-room. Scientific blocker P04 wrong metric (see §7.6), P03 pass-flag recount not independent raw reconstruction, P05 classifier failure-accounting issue. P07-R1 commit `fb67aefb74632e92b43318f74ad2f9be0bf199ba` corrected P04, P05 primary aggregation, reported fresh-process aggregation. Agent status 11 resolved/4 resolved-as-limitation/4 partial does not supersede Experiment Lead assessment. Final prior review independently reaggregated original P03/P04/P05 frozen evidence; no new semantic implementation execution. P06 counts forwarded in R1. Administrative commit `dc3634179bd3028ab78ff06a991f5851101bb4f1` records qualified closure, no new archive or workload.

### 10.1. Evidence levels / reproducibility distinctions

| Procedure | Status | Permitted wording |
|---|---|---|
| Legacy J01 simulator | Executed replay | Same legacy machinery, Level S |
| G2 third-party JCS + shared transform | Archived | Library-level evidence, not separate semantics |
| P03 Python/Go semantic implementations | Executed, corrected, frozen | Separately coded, same-team cross-language agreement |
| P03 final review | Frozen-evidence reaggregation | Recorded leaf/node/root reconstruction, not new pipeline execution |
| P04 400 observations | Measured | Matched same-contract assurance evidence |
| P05 80 primary +80 repeated | Measured, post-exposure corrective | Same 40 units, repeated regression |
| P06 fresh historical output | Recorded execution | Reproduction of recovered artifact, not on-chain |
| P07 fresh-directory P05 | Demonstrated in host environment | P05 execution only |
| P07-R1 fresh-process P04/P05/P06 | Aggregation re-execution | Not full experiment reproduction |
| Full consolidated Docker clean-room | NOT EXECUTED | Explicit limitation |
| Independent external replication | NOT PERFORMED | Prohibited claim |

### 10.2. Final 19-obligation assessment (Experiment Lead, not Agent self-report)

| ID | Final disposition / remaining limit |
|---|---|
| F01 | Scientific P03 reaggregation substantially verified in review; automation partial |
| F02 | Historical P03 mutation test execution detail partial |
| F03 | P03 root/node checks verified; provenance automation partial |
| F04 | Accepted with immutable source identity scope |
| F05 | Missing runall/resume logs; no uninterrupted historical run-all claim |
| F24 | Semantic admission vs guard blocking separation accepted |
| F25 | Detector negative denominators incomplete; no complete R1 confusion reconstruction |
| F26 | Partial first-comparable-divergence attribution; NOT_EXECUTED ≠ L0 |
| F27 | Combined processing/guard only; R1 medians/IQR not re-derived |
| F28 | Frozen synthetic; exposure/template overlap limitations |
| F29 | Go cross-check only actual compared fields; same-team |
| F30 | Headline corrected, activation reporting partial |
| F49 | Strict entry coverage partial |
| F50 | Complete immutable lock enforcement partial |
| F51 | Production integration QA partial |
| F52 | Actual verifier-path bounded timeout integration partial |
| F53 | Scientific failure accounting accepted; full validator coverage partial |
| F54 | Executable pipeline gate integration partial |
| F55 | Full dependency closure/Docker reproduction not completed |

Scientific closure ≠ engineering closure. Do not convert remaining PARTIAL statuses to RESOLVED. No P07-R2/P08/new experiment authorized. Limit claims instead. Reopen only if new evidence invalidates an accepted scientific conclusion, not to inflate status.

## 11. Claim-to-evidence matrix for v19.tex

| Claim ID | RQ | Approved scope | Evidence anchor | Forbidden inference |
|---|---|---|---|---|
| C01 | RQ1 | JCS canonical bytes do not establish application semantics | Historical J01/J02 + contract model | JCS algorithm defective |
| C02 | RQ1 | Different construction formulas reproduce 30/30 vs0/30 recorded roots | P06 fresh CSV, recovery inventory | Independent mainnet verification |
| C03 | RQ2 | K-v1 replay coverage600/600, EQ/NEQ150/150, abstain30/30 | P01 per-leg + metrics | All malformed inputs rejected |
| C04 | RQ2 | K-v2 explicitly defines semantics and reason precedence | Final normative contract and manifest | Universal payment ontology |
| C05 | RQ2 | Python/Go admission/reason630/630, bytes600/600, EQ/NEQ150/150 each | P03 corrected E1 and raw evidence | Unseen generalization or independent business oracle |
| C06 | RQ2 | Alias, scale, Unicode, multiplicity and sentinel defects exposed and corrected | P03 original failures and regression | SHA collision, aggregate five/123 without reconciliation |
| C07 | RQ3 | 18/18 batch-root outcomes, 131 leaves/114 nodes per impl | P03 E4 | All 18 successful roots, external completeness |
| C08 | RQ3 | 9/11 stage matches; two corrective controls separately2/2 | P03 attribution metrics | 11/11 original or universal localization |
| C09 | RQ3 | A2 improves safe release45/100→85/100, paired+40pp | P04 raw/oracle and P07-R1 reconciliation | Semantic admission metric, production incidence |
| C10 | RQ3 | Unsafe release55/60→15/60, benign40/40 each | P04 primary outcomes | Comprehensive guard detection |
| C11 | RQ3 | Identity/finite CI have limited complementary coverage | P04 original applicable signals | Complete confusion reconstruction by R1 |
| C12 | RQ3 | V1/V2 correctness15/40→40/40, +62.5pp | P05 first-pass | V1 structurally defective |
| C13 | RQ3 | V2 rejects25/25 structurally valid unauthorized, six coordinated substitutions, preserves11/11 authorized | P05 raw/oracle | Universal security or compromised signer protection |
| C14 | RQ3 | Separate checker40/40 decision agreement,39/39 applicable states +1 N/A | P05 R2B checker/state audit | Exact independent reason oracle |
| C15 | RQ3 | Corrective80 repeated obs no matched differences | P05 corrective comparison | 80 independent new units |
| C16 | Cross-cutting | Frozen-evidence reaggregation and limited execution shown | P07/P07-R1, final disposition | Full consolidated Docker clean-room |

## 12. Threats to validity — required language and methodological controls

Construct validity: semantic equivalence is defined by K-v2, not externally adjudicated business truth. Coverage and pair success include both-admitted condition. P04 safe release and P05 authorization are distinct objectives, not interchangeable binary labels. V1 own structural contract separate. Root equality neither external completeness nor authorization.

Internal validity: same-team AI-assisted contract, evaluator and implementations may share specification errors. Go separately coded and procedural isolation reduce but do not eliminate common-mode risk. P04 matched engine controls differences but injected faults and finite CI scope shape results. P05 shares structural implementation; separate checker reuses adapter and libraries. Historical first-pass defects and correction chronology must remain visible. P01 retrospective approval; no blanket claim of prospective preregistration. P07 metric mismatch demonstrates importance of explicit normative objectives and independent classification.

External/statistical validity: purposive synthetic fixtures, template dependence, finite fixed domain, repeated evaluations, limited currency/time/Unicode contract. Counts descriptive, no population estimates, no claim of independent random sampling. Do not use pooled binomial CIs as empirical guarantees; legacy nominal 1.98% one-sided CP upper bound from zero/150 is arithmetic conditional on i.i.d. assumptions not established here. Avoid significance testing that assumes independent templates. Paired effect is descriptive (b−c)/N with specified direction.

Security validity: assume hash binding properties, correct trust provisioning, uncompromised signer and specified sequence state. No compromised signer, external source truth, wall-clock freshness, distributed equivocation resistance, inventory authenticity or production attack prevalence. Declared ID mismatch not alternate algorithm implementation. No universal fail-closed guarantee.

Reproducibility: preserved frozen evidence and checksums, limited host execution and fresh process aggregation; original P03 run orchestration resumed; missing logs; incomplete full integration QA and lock binding; no consolidated Docker execution. Distinguish actual execution, reaggregation and reported historical provenance. Do not describe AI-assisted same-team checking as independent third-party replication.

## 13. Author Lead integration plan (no new experiments)

| Manuscript section | Required change |
|---|---|
| Abstract | Thesis and scoped P03, P04, P05, optionally P06 headline results; no performance/QA overclaim |
| Introduction | Explain representation, execution and authorization gaps as one thesis; keep 3 RQs |
| Related Work | Distinguish serialization, schemas, transparency, provenance, authenticated references; bibliographic accuracy independently verify before submission |
| Formal model | O1–O5, conditional quotient/root propositions, structural vs authorization predicates; no proof of implementation-wide security |
| Design | K-v2 full normative manifest, v3 full digests, required multiset membership, guards, signed checkpoint and state |
| Methodology | Separate legacy/J01, P03 initial and corrective, P04 matched arms, P05 two arms and repeat, P06 historical reproduction; exact metrics and denominators |
| Results | RQ1 legacy/P06; RQ2 P01/P02/P03; RQ3 E4/attribution/P04/P05; explicit shared misses and corrective defects |
| Discussion | Why guards and authorization complement, not replace semantic correctness; limits of trust |
| Threats | All limitations in §12; no unsupported claims |
| Reproducibility | Exact archive identities, scope of reaggregation, no full Docker claim; repository link only after confirmed publication/access |
| Appendix | Frozen contract/digests, artifact map, exact secondary denominators where available, correction history |
| Conclusion | Finite contract-relative interoperability and incremental assurance, no universal claim |

Suggested abstract-ready English results statement: “On 630 reconstructed record occurrences, separately coded Python and Go implementations agreed on all admission decisions and reason categories and on canonical bytes for all 600 admitted occurrences. All 150 equivalent and 150 distinct pairs satisfied their specified relationships. In a 100-unit matched execution-assurance evaluation, combining profile-identity and finite regression guards increased safe-release correctness from 45/100 to 85/100, while retaining 15 shared misses. On a separate 40-unit corpus, authenticated trusted-reference verification improved authorization-objective correctness from 15/40 to 40/40, rejecting all 25 structurally valid but unauthorized fixtures while accepting all 11 authorized controls. Historical reconstruction reproduced 30/30 recorded roots under one construction and 0/30 under an alternative construction. These results characterize bounded, contract-relative synthetic evaluations and recovered artifacts rather than universal security or independent third-party replication.”

## 14. Prohibited/superseded numerical claims checklist

- P04 94/64/84/54 as common-objective: WRONG metric, quarantined; use 45/75/55/85 with explicit arm names.
- P04 paired A1 vs alphabetical A1+CI: not primary; use A1/A2 45/0/40/15.
- P05 40/40 applicable state transitions: superseded by39/39 +1 N/A.
- P05 10 authorized/30 adverse: obsolete prereg inventory; final11/29.
- P03 five failures /123: narrative and suite deficits not reconciled; use defect classes and per-suite counts with caveat.
- P03 initial 32-bit construction identifier: legacy v2 only; final v3 two full 32-byte digests.
- P03 final18/18 roots: descriptor-level outcome, not necessarily all successful roots.
- P03 attribution original11/11: incorrect;9/11, separate corrective2/2.
- P01 malformed rejection 30/30: incorrect, 30 underspecified; malformed/prohibited denominator0 => N/A.
- 24/24 production QA or 19/19 engineering closure: unsupported; record partial limitations.
- P04 R1 independently recomputed performance/confusion: unsupported.
- P06 on-chain verification: unsupported; tx_id/block blank, regenerated workload.
- P07 full consolidated reproduction: unsupported; aggregation re-execution only plus limited P05 host execution.
- No claims of third-party replication, production prevalence, universal security, universal semantic correctness, complete lock enforcement or universal fail-closed behavior.

## 15. Final disposition and release gate

Scientific results accepted and frozen; no additional experiments required. Author Lead authorized to write v19.tex; submission pending final manuscript review. Before submission: ensure all tables trace to frozen evidence, correct old abstract/discussion statements that P04/P05 remain unvalidated, verify bibliographic references and artifact access, distinguish original and corrected outputs, preserve existing RQ definitions, and apply all claim restrictions. Do not change scientific SSOT on editorial authority alone. This report does not certify repository state or independently execute the pipelines. It records the accepted scientific evidence and qualified boundaries from supplied documents and archives.

## Appendix A — Archive inventory and current byte-level verification

All listed archive digests recomputed in this report from local uploaded bytes. Detached comparison where matching companion file exists; CRC tested by ZIP reader. Intermediate archives are historical records, not additional scientific samples. Internal SHA256SUMS was not reverified across every intermediate archive in this report.

| Archive | SHA-256 | Detached | Members | CRC |
|---|---|---|---:|---|
| `BCJ_V19_P01_CLOSURE_REVIEW.zip` | `b8e3d23bd61dd6e7bc6e22d9ac91c4ac7b155b9dd7b935310ac421d117f468b7` | MATCH | 39 | OK |
| `BCJ_V19_P01_R2_REVIEW.zip` | `9bd563acbd8d44b4d3cdfa5eeab502bcefe448c20c689d3207b1aabf25b86436` | MATCH | 51 | OK |
| `BCJ_V19_P02_R1_DRAFT_REVIEW.zip` | `f17a6114635c606fa8490d4768a03cf62ea3d299ccb6e0f7702318f6a34a6d8a` | MATCH | 14 | OK |
| `BCJ_V19_P02_R2_REVIEW.zip` | `c7a5177a89341625681df3c5d263974b36f7757e91d6653ae79c4a1655180e85` | MATCH | 37 | OK |
| `BCJ_V19_P02_R3_REVIEW.zip` | `3b6f887be029cf562184ffc2e86b80489e1af14cd495893cdd68a2f834a10024` | MATCH | 57 | OK |
| `BCJ_V19_P02_R4A_REVIEW.zip` | `3513e3c926a29c6e6cc3d0dcd461b27cdee47c45cfa5e4c0bb92ef4b59a4aca3` | MATCH | 117 | OK |
| `BCJ_V19_P02_R4_REVIEW.zip` | `8d6a48a6332fd1127af51c99213b4e30902623a30111c67be7846ad08878192c` | MATCH | 37 | OK |
| `BCJ_V19_P03_CLOSED_REPRODUCTION_REVIEW.zip` | `228bb6afaea94f1145e4752e660fb69ff3a3ad9ccdb5f94461e58170cb9daffa` | MATCH | 506 | OK |
| `BCJ_V19_P03_FINAL_QA_CLOSED_REVIEW.zip` | `45053224dc25c314a0e305324ccb087020f3832b4fa00b569833aad18c122761` | MATCH | 529 | OK |
| `BCJ_V19_P03_FINAL_REPRODUCED_REVIEW.zip` | `910b409f11dfe55adef5ff36242a53dbc335c4e77fdab251347ccea6562db812` | MATCH | 477 | OK |
| `BCJ_V19_P03_PREFLIGHT_R1_REVIEW(1).zip` | `a6e48a8f49bb90608c74beff65bb6918d75c214f97ddbbc4d0d5e0f533f5bf6e` | MATCH | 125 | OK |
| `BCJ_V19_P03_PREFLIGHT_R1_REVIEW(2).zip` | `f672d3d0c63ecb1aaff0c32a64c3b5159ebb6e2f2b3dcfe57e3966489a681031` | MATCH | 136 | OK |
| `BCJ_V19_P03_PREFLIGHT_R1_REVIEW(3).zip` | `68e29bbd449502b71e3f14f4155b72e7c7716ac6eb5482145ad36ed59bab7a64` | MATCH | 143 | OK |
| `BCJ_V19_P03_PREFLIGHT_R1_REVIEW(4).zip` | `a838ac382fcbe1744a2aa45cc27bc5390ada688769e696b2d87f795cbff21184` | MATCH | 146 | OK |
| `BCJ_V19_P03_PREFLIGHT_R1_REVIEW.zip` | `a6e48a8f49bb90608c74beff65bb6918d75c214f97ddbbc4d0d5e0f533f5bf6e` | MATCH | 125 | OK |
| `BCJ_V19_P03_R1_REVIEW.zip` | `f7a905af3ea640bc6fb7fab59f54c2e8364311e38016f92bbbca433baf758b22` | MATCH | 203 | OK |
| `BCJ_V19_P03_STAGE1_R1_REVIEW.zip` | `d29f34190657dca563db7fef19c839158d905ca4f28b30800442581d34b5fec4` | MATCH | 228 | OK |
| `BCJ_V19_P03_STAGE1_R2_REVIEW.zip` | `bd8f4beb79b243f9166ea12dd70651a3b2fc07bd85c2631fee6ac8dcfd8dbad7` | MATCH | 360 | OK |
| `BCJ_V19_P03_STAGE1_R3A_FINAL_REVIEW.zip` | `59e93c27835744bffc61a1cda99d9734a6586b0f1cb638f21ae264f7724e05a1` | MATCH | 456 | OK |
| `BCJ_V19_P03_STAGE1_R3_REVIEW.zip` | `337024bbf3fcd07ed5aee4ea413537e715e41c2e3b669a501e1a445929db726e` | MATCH | 422 | OK |
| `BCJ_V19_P04_DEVELOPMENT_READINESS_R3_REVIEW.zip` | `bd862cbcdf2007256edaa6a2ac260116ed456065497b974d59d7422596a45599` | MATCH | 40 | OK |
| `BCJ_V19_P04_EXECUTION_READINESS_R4_REVIEW.zip` | `ebb1d824c1f895e98736b1eda808d5c84c2f6e62b3cf061113cbb4759d67e39b` | MATCH | 63 | OK |
| `BCJ_V19_P04_FINAL_MEASURED_REVIEW.zip` | `2900ffb2bca0ac91ad33d6661bcbd457976f19256b1266ca7a9e6e3f457e204b` | MATCH | 110 | OK |
| `BCJ_V19_P04_PREREG_R2_REVIEW.zip` | `828a3f44eb52304c6481e9aa9ee39519e93c674cf69a0948ccec0f3a5f7202ea` | MATCH | 16 | OK |
| `BCJ_V19_P05_CORRECTIVE_R2B_FINAL_REVIEW.zip` | `9abff431c6ec5d1887596ebf86de2d9ad694f536cb2842b3018b785e597f576f` | MATCH | 40 | OK |
| `BCJ_V19_P05_CORRECTIVE_R2B_REVIEW.zip` | `4150a108bd1dfebaf3a39f752287f90520dbcd8edbd6ef70d89fe56d53767ccb` | MATCH | 11 | OK |
| `BCJ_V19_P05_CORRECTIVE_R2B_V2_PARTIAL_REVIEW.zip` | `93aaade3d0afcd1a58669604d731f43df2998c9344e585bb34d23ce077dc3346` | MATCH | 20 | OK |
| `BCJ_V19_P05_FINAL_MEASURED_REVIEW.zip` | `719db8c483a40a437f7e7cfeb7797bfd1fdcd9ca1fb2bd28cd24cb4dd18a4834` | MATCH | 53 | OK |
| `BCJ_V19_P05_PREREG_R1_REVIEW.zip` | `477fa2c73eb4203b29bc86700a86b38bcca9ff10bf2e75c7341f4ed8c593d5f2` | MATCH | 24 | OK |
| `BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW.zip` | `ec0e5448be666ace8ac63aa12102e18da53603230b78993077d3c2d7a1beed09` | MATCH | 43 | OK |
| `BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW.zip` | `b53daa567527fe2b7828a38dfb8a1732fc48081b9c6c8526a63641d2382b9d03` | MATCH | 37 | OK |

### Administrative files and manuscript identities (computed locally)

| File | SHA-256 |
|---|---|
| `BCJ_V19_FINAL_AUTHOR_HANDOVER.md` | `9cf6408d12ad74068e76432976bd8589e23b0730a6d5d1289a4e85d42edb8ec7` |
| `BCJ_V19_FINAL_CLAIM_RESTRICTIONS.md` | `76de78f9d1ebd7d2790bbda19a4b5b6e4948dfd8db98bc601d55e78281afdf31` |
| `BCJ_V19_FINAL_SCIENTIFIC_SSOT.json` | `7a8015b7fec23f066a07f122e1b8327bba2e2d6ecb30dabc4e59cb8e6f56b36f` |
| `P07_EXPERIMENT_LEAD_FINAL_DISPOSITION.md` | `2f26a33772b8a81fd388f23ee44706a5276496889f91c2e7fc9564498cdea385` |
| `v18(1).tex` | `68d8c56078d8342785d882301e0703f4116d6c71381de1518a5afe099a85abf7` |
| `v18(2).tex` | `68d8c56078d8342785d882301e0703f4116d6c71381de1518a5afe099a85abf7` |
| `v19_P00_P03.tex` | `65f2422879a110010d1e4bde6c40ccef3b277f8d6507bbae7b2a1403323d3cd1` |

## Appendix B — Exact source-member anchors and locked identifiers

The following archived records provide authoritative detail for the report. Archive path plus member path identifies the source; member SHA-256 recomputed here. Historical source digests inside records are reported identities, not independently computed where source bytes are absent.

### BCJ_V19_P01_CLOSURE_REVIEW.zip

| Member | SHA-256 |
|---|---|
| `results/P01/derived/J01_METRICS.json` | `9a4685b9ef3b9c7c9b67d7f8285c51d5e169068bc24ce95b45f592f2cbbaf752` |
| `results/P01/MANUSCRIPT_DRIFT_REPORT.md` | `c30ee8e24a4189e838bdce8f9f066875bda0eaefd6495b0853af57f841a1a9f9` |
| `results/P01/PROCESS_DEVIATION_REPORT.md` | `81f5b3f4d37483b205a0a6f0520a0163c414455093cb92ad8f1cfe0dab6d0cbf` |
| `results/P01/raw/J01_PER_LEG_RESULTS.jsonl` | `ef210c68a75bac5901094a92fa9c11495d9ef1600d75581e413b89af1caf2188` |
| `results/P01/REPORT.md` | `351fedb513d544a3be520f458117ea410e4d88734926abb5c38ad6176e44f50b` |
| `results/P02/P01_CLOSURE_REPORT.md` | `3b21778ec635d244fc786685e9c7bb52e4b48f297b27ed8a523e8feab9b65948` |

### BCJ_V19_P02_R4A_REVIEW.zip

| Member | SHA-256 |
|---|---|
| `results/P02/K_V1_TO_K_V2_IMPACT_REPORT.md` | `2386b8e21cee9e019743d39542baf39ba5a72a3e0b60333a6d2114c1eb473955` |
| `results/P02/R4A_ORACLE_REPAIR_REPORT.md` | `5f079fd50089528d5eec2cd11d84a18650c13af3178f040fd3e53f88e5ea9179` |

### BCJ_V19_P03_FINAL_QA_CLOSED_REVIEW.zip

| Member | SHA-256 |
|---|---|
| `results/P02/ERROR_TAXONOMY.yaml` | `9beac72e5eb1e5f7927e3f79bb98ed3daaead820e31c2101ecd4b87b3f39a64d` |
| `results/P02/K_V2_FREEZE_ATTESTATION.json` | `1dd1509ccde358f4dcde96e68bed48d7dde98e56b65635cd1624a148a99627fe` |
| `results/P02/MANUSCRIPT_FREEZE_ATTESTATION.json` | `a397775ee11af98603f1043df71951c6d6c2f790c5d79611c2a2cdc9b3a5f397` |
| `results/P02/NORMATIVE_CONTRACT.R4.md` | `9869794d90bb5b3991a45eea25e4eefe4e7443e2610657312fba98047724142e` |
| `results/P02/P03_E1_METRICS.CORRECTED.json` | `f8ec57335de5873502e6bb8f00562aac54b3576cb1ffde96308685ce52507e36` |
| `results/P03/E2_E3_REPORT.md` | `7be23421fcde6413e269118c20fa59b8709ef83b6f7737225a87388ee1e5c3f8` |
| `results/P03/FINAL_STATUS.json` | `9304fdb2e80f3644f809ecc05a0694430c032efab4ba8bfbeef3a52fd9bd9fad` |
| `results/P03/P03_E4_OCCURRENCE_METRICS.json` | `245469ea81f1e36935b02c44751bac12b6e56813c3a5c9ace15782e2f1b28871` |
| `results/P03/P03_STAGE_ATTRIBUTION_METRICS.json` | `d21ff422295aa71a85d079079a1e76dc8b3ebe2188d266b76cd5d7467c1eee0b` |
| `results/P03/P03_STAGE_ATTRIBUTION_METRICS.R3C.json` | `caa8fc0a734ba38da82de36b23390df634642a734f941216c3d021b40cad84a5` |
| `results/P03/QA_B_REPORT.md` | `d4732528f3bf3dc51282a07332caa6e4b42421c18feb96e876736ad598cbd239` |
| `results/P03/R3_REGRESSION_REPORT.md` | `0d992c3fdd58d88e3effc3967c94ec3ed416a8f55c4bb991ba7d6fd915b90a11` |
| `results/P03/SENTINEL_CORRECTION_REPORT.md` | `b4ce9a72c467103c29bb3335c16b6b9f3115badcfb7e9e0624c6efb590a88cb8` |
| `implementations/go-dev/ERROR_TAXONOMY.yaml` | `9beac72e5eb1e5f7927e3f79bb98ed3daaead820e31c2101ecd4b87b3f39a64d` |
| `implementations/go-dev/NORMATIVE_CONTRACT.R4.md` | `9869794d90bb5b3991a45eea25e4eefe4e7443e2610657312fba98047724142e` |
| `implementations/python-dev/ERROR_TAXONOMY.yaml` | `9beac72e5eb1e5f7927e3f79bb98ed3daaead820e31c2101ecd4b87b3f39a64d` |
| `implementations/python-dev/NORMATIVE_CONTRACT.R4.md` | `9869794d90bb5b3991a45eea25e4eefe4e7443e2610657312fba98047724142e` |

### BCJ_V19_P04_FINAL_MEASURED_REVIEW.zip

| Member | SHA-256 |
|---|---|
| `BCJ_V19_P04_FINAL_MEASURED_REVIEW/_p04_meta_final/REPORT.md` | `da08a31212f9a5d22584fddd5ec68cf3ecdae2c0fa5a778e9cb4a438f3fe9cd4` |
| `BCJ_V19_P04_FINAL_MEASURED_REVIEW/p04_evaluator/P04_EVALUATOR_ORACLE.jsonl` | `71e49d342eacd9ef4294433c0d97f474f606cad76aa2f0971b699de90597be1f` |
| `BCJ_V19_P04_FINAL_MEASURED_REVIEW/p04_evaluator/P04_FAULT_MANIFEST.jsonl` | `f6d4cd35ca2944bfe1aa17a1653373b919c441ec8fc2ac59516464853c0cef4c` |
| `BCJ_V19_P04_FINAL_MEASURED_REVIEW/p04_evaluator/P04_FINAL_SSOT_LOCK.json` | `ce06256f19c11e68654e7a18d8c903c58fc999c0c1ce973e453d4968a9f06524` |
| `BCJ_V19_P04_FINAL_MEASURED_REVIEW/p04_evaluator/P04_MEASURED_CORPUS.jsonl` | `88321938b29f7a3f031a4e9c5a0a0f18a0b1c4511ab672669c6b378f86f6e0c9` |
| `BCJ_V19_P04_FINAL_MEASURED_REVIEW/p04_prereg_r2/P04_METRIC_DICTIONARY.yaml` | `1fc5c0c7214c7299761eb028b07ba190d7dcc569a40074ce3596fba7c6a900a6` |
| `BCJ_V19_P04_FINAL_MEASURED_REVIEW/p04_prereg_r3/P04_METRIC_DICTIONARY.yaml` | `7732128d885ecb652df4ba94920576584d6942eb8d30cfbd92ff99d59f0fc090` |
| `BCJ_V19_P04_FINAL_MEASURED_REVIEW/results/P04/P04_PERFORMANCE_RAW.csv` | `0b47c453107331bb4490c9667f9bd62cc970b4f5b18383954d0d53f6db91a67a` |
| `BCJ_V19_P04_FINAL_MEASURED_REVIEW/results/P04/P04_PERFORMANCE_SUMMARY.csv` | `84cadd38951e88f98a6e06fc785c80f0019d40855a88da7f6495ba6f439d17f9` |

### BCJ_V19_P05_FINAL_MEASURED_REVIEW.zip

| Member | SHA-256 |
|---|---|
| `BCJ_V19_P05_FINAL_MEASURED_REVIEW/_p05_meta_final/REPORT.md` | `9417df2402890190857987721eb656f24345690efb2a810a36143e19f5d853e1` |
| `BCJ_V19_P05_FINAL_MEASURED_REVIEW/p05_evaluator/P05_RAW_OBSERVATIONS.jsonl` | `a00d6dfcd41b6eafd73cdba3ddea8d96aa184e76f4abc8b09741942b2df6298c` |
| `BCJ_V19_P05_FINAL_MEASURED_REVIEW/p05_prereg_r1/P05_TRUST_PROVISIONING_SPEC.md` | `b3a09adfb3c4aca3bc6f893d6447ab0bb47772c659293d34829bb93f6675d64b` |
| `BCJ_V19_P05_FINAL_MEASURED_REVIEW/p05_prereg_r1/REPORT.md` | `b3a6e4b5aa2f36e13a065eb600a7ae5f3599d727b2f39da7950eaf85619937df` |

### BCJ_V19_P05_CORRECTIVE_R2B_FINAL_REVIEW.zip

| Member | SHA-256 |
|---|---|
| `BCJ_V19_P05_CORRECTIVE_R2B_FINAL_REVIEW/p05_r2b/P05_FIRST_PASS_STATE_REAUDIT_SUMMARY.json` | `2d9eac0e03f0b3c0f68602ec67708bd0e4b4e75e577f97da326c46c6872ca020` |
| `BCJ_V19_P05_CORRECTIVE_R2B_FINAL_REVIEW/p05_r2b/P05_FIRST_PASS_VS_R2B_COMPARISON.csv` | `6114de46064da80aed91f93dd06976378283d659acd319a90bb4cad8618c2155` |
| `BCJ_V19_P05_CORRECTIVE_R2B_FINAL_REVIEW/p05_r2b/P05_R2B_EXECUTION_LOCK.json` | `f2774cdaa16ebc99116846229d19403f0221832e1bf51acecedb087b7c3e94b1` |
| `BCJ_V19_P05_CORRECTIVE_R2B_FINAL_REVIEW/p05_r2b/P05_R2B_FINALIZE_SUMMARY.json` | `1eddcef2339ea36239595e3e72803904709b09b471c5ee9b78b35659fcb218bd` |
| `BCJ_V19_P05_CORRECTIVE_R2B_FINAL_REVIEW/p05_r2b/P05_R2B_INDEPENDENT_ORACLE_V2.jsonl` | `bb2e96033ecbe136a91693c38542d5a35e433b64c9a748c78adbcd6f7d3fa150` |
| `BCJ_V19_P05_CORRECTIVE_R2B_FINAL_REVIEW/p05_r2b/P05_R2B_SPEC.md` | `8967eba7c745d00156992ae341da953372329b4de8ed58a9e8953b78929e459a` |

### BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW.zip

| Member | SHA-256 |
|---|---|
| `BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW/p07/P07_CLEANROOM_STATUS.json` | `4e99336b3d815419ca9b3596cd3316343085404b8231eaed63c9a658e337fc3e` |
| `BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW/p07/p06/P06_FINAL_DISPOSITION.md` | `9dbad4e004521dd8255c8f84af66a67c50617c02e56910ce8372d2ed9ffa32ef` |
| `BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW/p07/p06/P06_RECOVERY_INVENTORY.json` | `bb35daf41e88d84e9a22518ce319fe0e3eeeaafa52c3cab97436d6dd244bec26` |
| `BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW/p07/p06/repro_eq6_fresh.csv` | `35cdca9e5e7046544ac7412065e6d9eb107798869956df8a4f2bf85a1f7c6c3c` |

### BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW.zip

| Member | SHA-256 |
|---|---|
| `BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW/p07_r1/P05_R1_CORRECTED_AGGREGATION.json` | `96b1a2be79ceea522384f77504cede1f3d5ea29bd15854948eddf1ae8e8f5e6f` |
| `BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW/p07_r1/P07_R1_19_OBLIGATION_REGISTER.json` | `06643c98fa450196c6f813a5b2fa6c097e40cf50b65fb9026b802033fd93c764` |
| `BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW/p07_r1/P07_R1_CONSOLIDATED_REPRO.json` | `baf2d8e33c143f0e48a1e68f460653619075bae54d78c67b2c04b8239ce2c33f` |
| `BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW/p07_r1/P07_R1_P04_CLASSIFICATION_TRACE.jsonl` | `bcb182aab9f851bd93f1836059b3283b686e5a012fa060d858a4bbac34f1ce9e` |
| `BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW/p07_r1/P07_R1_P04_F24_F30.json` | `ccbef622d3ad64655a5a05ca8b1dbec1de6401a3eaf462029dc0310182a4e5c5` |
| `BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW/p07_r1/P07_R1_P04_METRIC_RECONCILIATION.md` | `41ce1f13ed3f5c95d569158bf5068e627b4c63d47ace25be5cb05c37723d6637` |

### Locked identifiers / historical recovery provenance (verbatim records)

**P04_FINAL_SSOT_LOCK.json**

```json
{
  "base_commit": "1c88fa9e4a466f70e539b0d92fc2de7598a340f9",
  "construction_digest": "d1e46eb5c6e0688b03c085ce5ed83ba134fffc6638a5fc0df8ed143b12aaf91d",
  "corpus_digests": {
    "P04_EVALUATOR_ORACLE.jsonl": "71e49d342eacd9ef4294433c0d97f474f606cad76aa2f0971b699de90597be1f",
    "P04_FAULT_MANIFEST.jsonl": "f6d4cd35ca2944bfe1aa17a1653373b919c441ec8fc2ac59516464853c0cef4c",
    "P04_MEASURED_CORPUS.jsonl": "88321938b29f7a3f031a4e9c5a0a0f18a0b1c4511ab672669c6b378f86f6e0c9"
  },
  "corpus_inventory_sha256": "f12aaf679ccc2dd61238b7913cd78fea6bba742d3c4e63f7d8ed4a2180f36003",
  "d_ci_file_sha256": "ffe1da6d368fab475640988c3e5f86fc054f8c2755755cfd9188015f3bedddeb",
  "d_dev_file_sha256": "b8f60a36e061f131aa4da1fe1857e91b54a070e98a183c8b4146f64d1f9f952b",
  "frozen": true,
  "go_source_sha256_crlf": "493102b2265996b734f2d67931ed07547d69026af09d0ea0dbe9f1a98467a5fa",
  "holdout_audit_sha256": "622d4280d9d54bc251b2c369ddeb3e3bfdbcc84ff21e77a2fc2d2c96b17fe779",
  "line_ending_policy": "frozen digests defined under CRLF rendering of LF-committed blobs; raw / lf / crlf digests recorded separately",
  "oracle_provenance_sha256": "dcdb9fcc5b938224c2751c0afd56e83c0a19c96192f5dfd34d68c78e24fb7af4",
  "pid_sem_v2": "caa2f3e561edbac1f73ec2926bea8009cce176ba8b8c7f900ebc7e8de454b429",
  "python_source_sha256_crlf": "2b6924010d528f39c05ac1f5d332ecee814e2d6a09fa3e38425daa97d119355f",
  "source_variants": {
    "go": {
      "crlf": "493102b2265996b734f2d67931ed07547d69026af09d0ea0dbe9f1a98467a5fa",
      "lf": "66ada97af6e39c255d90b7a9135fce011723291b0651205b9b9fc4fcd10e5fca",
      "raw": "66ada97af6e39c255d90b7a9135fce011723291b0651205b9b9fc4fcd10e5fca"
    },
    "python": {
      "crlf": "2b6924010d528f39c05ac1f5d332ecee814e2d6a09fa3e38425daa97d119355f",
      "lf": "ea81f929021a1ca39bf0bc70f5950ef5d5cc16e7602102eb77f13e7ec348a7f9",
      "raw": "ea81f929021a1ca39bf0bc70f5950ef5d5cc16e7602102eb77f13e7ec348a7f9"
    }
  }
}
```

**P06_RECOVERY_INVENTORY.json**

```json
{
  "status": "RECOVERED",
  "batches": 30,
  "artifact_eq6_match": "30/30",
  "campaign_match": "0/30",
  "fresh_reproduces_historical_csv": "30/30",
  "first_campaign_divergence": {
    "j": "0",
    "manifest_root": "6860e20e18c2ca15c0c4c8e15c50fe6655f45e05a98449108bb2386dd80b1b48",
    "campaign_would": "243b7c29a7ad371aa040374b0603f37bdbf5432420e21169aa61feadd8f14a32"
  },
  "reconstruction_plan": {
    "artifact_eq6": "r_j = MerkleRoot([r_{j-1}] + B_j); leaf H(0x00||d); node H(0x01||L||R); odd leaf duplicated",
    "campaign_h02": "r_j = H(0x02 || j:uint64_be || r_{j-1} || MerkleRoot(B_j))",
    "ordering": "batch j ascending 0..29; B_j regenerated from seed 42 (30 x 1681 events; one randint per batch)",
    "serialization": "raw 32-byte leaves; lowercase hex for published roots; manifest fields prev_root_hex/root_hex"
  },
  "evidence": {
    "real_manifest": {
      "path": "docs/drtea_mainnet_manifest_REAL.json",
      "sha256": "f5dbc2fe037db808885d35648c4e2dd84df32e684c3e98b9056a41da181e9e3b"
    },
    "campaign_formula": {
      "path": "py/canon/hashing.py",
      "sha256": "8d495ed00f61a8adcefed41f27caecfb55ead29ea70928792f85a7f6f8902095"
    },
    "repro_script": {
      "path": "scripts/drtea_eq6_repro.py",
      "sha256": "8e3f346ccb09c96237333e5ded7594cf9ff77c334c7fc58877b7b1e953783f38"
    },
    "historical_campaign_csv": {
      "path": "derived/legacy_validation_real.csv",
      "sha256": "cc989ba9dc27ee945cb731cfb0439d92ae65dd732c15964bf893e71dbd23646f"
    },
    "historical_eq6_csv": {
      "path": "derived/legacy_validation_real_eq6.csv",
      "sha256": "4332844b4746c63966dc4814daa1fc681c3ffd85586cb3dc16b66443443ba10b"
    },
    "cr_record": {
      "path": "docs/CR-0006-OPEN.md",
      "sha256": "040d5e572fab3f207250c8bd751d3aa81407fdbb5bce66a8e285b565dbcc3c2a"
    },
    "fresh_eq6_csv": {
      "path": "experiments/v19/p07/p06/repro_eq6_fresh.csv",
      "sha256": "35cdca9e5e7046544ac7412065e6d9eb107798869956df8a4f2bf85a1f7c6c3c"
    },
    "fresh_stdout": {
      "path": "experiments/v19/p07/p06/repro_stdout.log",
      "sha256": "4c58f5e1e69c9555ab5faa8847149b6c56ba73f8f0669b296d4197f7eb5af521"
    }
  },
  "evidence_level": "REPRODUCTION_OF_HISTORICAL (not a new scientific sample)",
  "environment": {
    "python": "3.12.9"
  }
}
```

## Appendix C — Exact final machine-readable SSOT (verbatim)

```json
{
  "document": "BCJ_V19_FINAL_SCIENTIFIC_SSOT",
  "program": "BCJ-V19",
  "status": {
    "scientific_development": "CLOSED",
    "scientific_results": "ACCEPTED",
    "p07_headline_reconciliation": "ACCEPTED",
    "engineering_qa": "PARTIAL_WITH_DOCUMENTED_LIMITATIONS",
    "docker_cleanroom": "NOT_EXECUTED",
    "new_experiments_required": false,
    "manuscript_finalization_authorized": true,
    "submission_authorized": "false_pending_final_manuscript_review"
  },
  "preserved": {
    "final_commit": "fb67aefb74632e92b43318f74ad2f9be0bf199ba",
    "final_archive": "BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW.zip",
    "final_archive_sha256": "b53daa567527fe2b7828a38dfb8a1732fc48081b9c6c8526a63641d2382b9d03",
    "prior_p07_archive": "BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW.zip",
    "prior_p07_archive_sha256": "ec0e5448be666ace8ac63aa12102e18da53603230b78993077d3c2d7a1beed09"
  },
  "P03": {
    "admission_and_reason_agreement": "630/630",
    "typed_objects_eligible_json_canonical_bytes_leaves": "600/600",
    "equivalent_pairs": "150/150",
    "distinct_pairs": "150/150",
    "batch_roots": "18/18",
    "recorded_leaves_per_implementation": 131,
    "internal_node_digest_checks_per_implementation": "114/114",
    "evidence_basis": "frozen-evidence reaggregation and recorded commitment reconstruction (not fresh execution of both semantic implementations)"
  },
  "P04": {
    "common_end_to_end_correctness": {
      "A1": "45/100",
      "A1+PID": "75/100",
      "A1+CI": "55/100",
      "A2": "85/100"
    },
    "paired_A1_vs_A2": {
      "both_correct": 45,
      "A1_only": 0,
      "A2_only": 40,
      "both_incorrect": 15,
      "N": 100
    },
    "unsafe_release": {
      "A1": "55/60",
      "A2": "15/60"
    },
    "benign_preservation_per_arm": "40/40",
    "metric_definition": "safe end-to-end release: fault unit correct iff not released; benign correct iff released and canonical==expected; runtime failure never correct"
  },
  "P05": {
    "V1": "15/40",
    "V2": "40/40",
    "paired": {
      "both_correct": 15,
      "v1_only": 0,
      "v2_only": 25,
      "both_incorrect": 0
    },
    "authorized_acceptance_per_arm": "11/11",
    "unauthorized_acceptance": {
      "V1": "25/25",
      "V2": "0/25"
    },
    "coordinated_substitution_acceptance": {
      "V1": "6/6",
      "V2": "0/6"
    },
    "separately_coded_decision_agreement": "40/40",
    "applicable_state_transitions": "39/39 (+1 missing-state N/A)",
    "corrective_observations": 80,
    "first_pass_vs_corrective_decision_reason_initial_final_state_differences": 0
  },
  "P06": {
    "historical_artifact_eq6": "30/30",
    "alternative_campaign_construction": "0/30",
    "first_divergence_batch": 0,
    "evidence_basis": "historical reproduction only; no independent on-chain verification"
  },
  "research_questions": "Preserve the manuscript's existing RQs; P07 is cross-cutting reproducibility evidence; final wording owned by Author Lead.",
  "references": {
    "claim_restrictions": "BCJ_V19_FINAL_CLAIM_RESTRICTIONS.md",
    "author_handover": "BCJ_V19_FINAL_AUTHOR_HANDOVER.md",
    "disposition": "P07_EXPERIMENT_LEAD_FINAL_DISPOSITION.md"
  }
}
```

## Appendix D — Mandatory claim restrictions (verbatim)

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


## Appendix E — Final administrative disposition (verbatim)

# P07 Experiment Lead Final Disposition

Administrative closure record. This disposition does not modify any frozen evidence, accepted archive, or the manuscript.

| field | value |
|---|---|
| scientific_development | CLOSED |
| scientific_results | ACCEPTED |
| p07_headline_reconciliation | ACCEPTED |
| engineering_qa | PARTIAL_WITH_DOCUMENTED_LIMITATIONS |
| docker_cleanroom | NOT_EXECUTED |
| new_experiments_required | false |
| manuscript_finalization_authorized | true |
| submission_authorized | false_pending_final_manuscript_review |

## Preserved immutable artifacts
- Final corrective commit: `fb67aefb74632e92b43318f74ad2f9be0bf199ba`
- Final corrective archive: `BCJ_V19_P07_R1_FINAL_CORRECTIVE_REVIEW.zip`
- SHA-256: `b53daa567527fe2b7828a38dfb8a1732fc48081b9c6c8526a63641d2382b9d03`
- Prior accepted archive: `BCJ_V19_P07_FINAL_CONSOLIDATED_REVIEW.zip` — `ec0e5448be666ace8ac63aa12102e18da53603230b78993077d3c2d7a1beed09`

## Independently verified by Experiment Lead
37 unique archive members; 36/36 internal checksums; detached SHA-256 agreement; ZIP CRC integrity; 400 unique P04 classification trace keys; P04 headline results reaggregated from the original measured archive; P03 raw Python/Go record-level, canonical-byte, leaf-digest, equivalent/distinct-pair, batch-root, and internal-node agreement; P05 first-pass and corrective headline results; zero P05 decision/reason/initial-state/final-state differences across matched observations.

## Scope
No P07-R2 experimental cycle, P08, new corpus, new measured experiment, or new verification arm is authorized. Scientific research program = SCIENTIFICALLY CLOSED WITH REPRODUCIBILITY QUALIFICATIONS.

## Canonical numbers
See `BCJ_V19_FINAL_SCIENTIFIC_SSOT.json`. Claim limits: `BCJ_V19_FINAL_CLAIM_RESTRICTIONS.md`. Author handover: `BCJ_V19_FINAL_AUTHOR_HANDOVER.md`.


**END OF MASTER EVIDENCE REPORT**
