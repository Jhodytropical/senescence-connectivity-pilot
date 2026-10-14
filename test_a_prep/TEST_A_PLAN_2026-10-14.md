# Test A plan (pre-registration): does a genotoxic-senescence-vs-quiescence contrast transfer between two IMR-90 datasets?

**Status: PLAN v1.0, 2026-10-14, committed to this repository and tagged `test-a-plan-v1`. Nothing has been scored and no group comparison has been run.** The only data inspection so far is file structure (columns, identifiers, integer check, library sizes), the GEO sample labels, and public dates. The commit is the timestamp. All thresholds freeze at this commit. A change before scoring needs a new dated plan version (v2) committed before any scoring, with the reason stated.

## 1. Question and scope
**Question.** If a gene-expression contrast that separates DNA-damage-induced senescent from quiescent IMR-90 fibroblasts is learned in one dataset, does it separate senescent from quiescent samples in an independent dataset made by a different lab with a different arrest method?

**This is a methods test of a signature.** It is not a drug ranking, uses no L1000 or other drug library, and says nothing about senolysis, toxicity, other cell types or tissues. Both datasets' senescent arms are genotoxic (see section 3), so a pass would show transfer of a **DNA-damage-response senescence contrast across labs and arrest methods within one cell line**, not a general senescence signature.

## 2. Should this run at all?
- It runs only on an explicit go from Jean, given after this plan is committed.
- The likely most useful result is modest. Existing readouts (for example the Hernandez-Segura 55 genes) may already separate these states, in which case the honest outcome is "existing readouts suffice; nothing new to build" (Outcome B).
- Preparation is not evidence that the run is worth doing. If it is not wanted, the plan stays unrun.

## 3. Datasets and roles (fixed)
| Role | Dataset | Samples used |
|---|---|---|
| **Derivation** | GSE162175 (IMR90, RNA-seq, serum-withdrawal quiescence) | Parental IMR90 only. Senescent: doxorubicin, etoposide, irradiation, 4 each (12). Quiescent: `IMR90_Quiesc_1-4` (4). Proliferating: `IMR90_Control_1-4` (4). |
| **Test** | GSE307082 (IMR-90, RNA-seq, contact-inhibition quiescence; unreviewed preprint) | Non-heat-shock samples only: proliferating P1, P7, P13; quiescent P2, P8, P14; senescent (doxorubicin) P3, P9, P15 (GSM9215490, -96, -84; -91, -97, -85; -92, -98, -86). |

- **Roles do not swap.** GSE162175 derives and GSE307082 tests. The trade-off is explicit: GSE162175 has more samples, so it supports derivation, but testing on n = 3 per state caps the exact permutation p-value at 0.05. The reverse direction has 12 vs 4 samples and finer resolution, but is barred from rescuing a failed primary.
- **Both senescent arms are genotoxic.** Doxorubicin, etoposide and irradiation are all DNA-damaging, and the test arm is doxorubicin. In GSE307082 the untreated quiescent and proliferating arms have no vehicle control, so "senescent" is fully confounded with drug exposure. The only non-genotoxic inducer, ER:RAS, is excluded from primary derivation (an engineered line) and enters only sensitivity S2.
- **Excluded from derivation:** palbociclib (CDK4/6 inhibition confounds arrest with senescence) and the ER:RAS arms.
- **Heat-shock exclusion.** Test A targets conditions without an additional acute heat-shock perturbation, so the 9 heat-shock samples in GSE307082 are excluded. They are not used for QC thresholds, tuning or scoring.
- **Reverse direction** (derive on GSE307082, test on GSE162175) is a pre-specified secondary analysis, reported in full whatever it shows. It cannot rescue a failed primary or be used to choose between signatures.
- **Culture confounds, acknowledged.** In GSE162175 the quiescent cells are in 0.5% serum and all others in 10%; the same-direction rule across both contrasts only partly cancels pure serum genes. In GSE307082 quiescent cells sit at high density for 10 days while proliferating controls were seeded 24 h before harvest, so density and culture time differ; E2 and E3 are most affected. The test set's arrest evidence is stronger than GSE162175's published protocol-level evidence only in a relative sense: EdU is described per model and the quiescent cells are SA-βgal positive.

## 4. Data handling before scoring
Allowed: file checksums, column-to-sample mapping, library sizes, gene-ID handling, replicate-structure and label-consistency checks. **Not allowed before this plan is committed:** any comparison between states, any PCA coloured by state, any differential expression or score.

Order of operations: (1) gene universe, (2) expression filter, (3) model.
1. **Gene universe.** Unversioned Ensembl IDs present in both count files (30,829 IDs). About 46% of GSE162175's IDs fall outside it, mostly newer annotation (GSE307082 carries 10,427 `ENSG000003*` IDs; GSE162175 has none). This is accepted: the test uses only genes both annotations share.
2. **Duplicates and blanks.** GSE307082 has 5 blank IDs (dropped) and 29 IDs that occur on more than one row (sum the counts across rows).
3. **Expression filter.** Keep a gene if it has at least 10 counts in at least 3 samples of the set being analysed: the retained derivation samples (20 if none is dropped), or the 9 test samples. Derivation and test filters are applied separately. "Expressed in the test set" below means passing the test filter.
4. **QC rule.** A sample is excluded only for a library size below 10 million assigned reads or a file/label inconsistency. Library sizes are 48.1–60.5 M for the 9 test samples and 30.8–53.3 M for the 20 derivation samples, so none is expected to fail.
   - **A required sample that fails QC is not replaced.** If any of the nine test samples fails, the fixed 3-per-state design is broken and the outcome is D. In derivation, a failed sample is dropped, but if any state or inducer group falls below 3 samples the signature is not evaluable (D).
   - **Minimum test coverage (a judgment call, fixed in advance).** After the test-set expression filter, at least 70% of the frozen signature's genes in each direction, and at least 20 per direction, must remain. Otherwise the outcome is D.
5. **Input files** (SHA-256): `GSE307082_CellStates_count_matrix.txt.gz` 73d178823b136f721ae8cd408defa86f3f56e1a247b2e17b5b1894edafbf054e. The GSE162175 file is recorded in `scripts/TESTA_INPUT_SHA256SUMS`.

## 5. Signature derivation (GSE162175 only; test data are not touched)
1. **Normalise:** median-of-ratios size factors (geometric means over universe genes with non-zero counts in all retained derivation samples), then log2(normalised count + 1).
2. **Contrasts:** S = the retained senescent samples pooled (12 if none is dropped); Q = the retained quiescent samples; P = the retained proliferating samples. Filtering, normalisation, contrasts and the per-inducer criterion all use the retained samples only. log2FC(S vs Q) = mean(S) − mean(Q) on the log2 scale; likewise S vs P. P-values are Welch two-sample t-tests (`scipy.stats.ttest_ind`, `equal_var=False`) for S vs Q, with Benjamini-Hochberg FDR over all genes passing the filter. Replicate index is not blocked in the primary model because its provenance is unconfirmed (sensitivity S1).
3. **A gene enters the signature if all hold:** FDR < 0.05 for S vs Q; |log2FC| ≥ 1 for both S vs Q and S vs P, with the same sign; and for each inducer i separately, mean(inducer i) − mean(Q) has the same sign as the pooled S vs Q log2FC and an absolute value of at least 0.5.
4. **Select:** rank by the smaller of the two |log2FC| values and keep the top 100 up and top 100 down, ties broken by ascending Ensembl ID. If fewer than 20 genes pass in either direction, the signature is "not evaluable", which is Outcome D (inconclusive), because an inability to test is not an observed failure to transfer.
5. **Freeze:** save the gene list and its SHA-256 before any test data are scored (see section 11). Derivation p-values are not the evidence; the held-out test is.

## 6. Baselines (scored on the test set only, never tuned)
B1 Hernandez-Segura 55 core genes; B2 SenMayo; B3 CellAge up/down (all as published); B4 a bulk approximation of the SenFlag quiescence-exclusion axis, score = rank(CCND1) − rank(NFIA), explicitly **not** SenFlag as published, which is a single-cell rule (CCND1 rises in senescence and falls in quiescence; NFIA marks quiescence); B5 a proliferation control (HALLMARK E2F targets + G2M checkpoint).
- **Mapping rule.** Baseline gene symbols are mapped to Ensembl IDs through the GSE307082 annotation columns, restricted to the gene universe. A symbol that maps to several IDs keeps the ID with the highest total count across the nine eligible test samples only (never the heat-shock samples); equal totals are broken by ascending unversioned Ensembl ID. **Baseline coverage is defined on genes available for scoring:** a published gene counts as available only if it maps to an Ensembl ID in the universe and passes the test expression filter (section 4). A baseline is *evaluable* only if at least 70% of its published genes are available, and every direction it needs still has at least one available gene. A baseline that fails either test is reported "not evaluable" and cannot meet any outcome condition. B4 needs both CCND1 and NFIA to be available; if either is lost it is not evaluable.
- **Fixed baseline lists.** B2 is the MSigDB `SAUL_SEN_MAYO` set as fetched by `scripts/fetch_data.sh` (124 symbols), hashed as `senmayo.json` in `scripts/INPUT_SHA256SUMS`. The paper's own Supplementary Data 1 (human sheet) lists 125 genes; the MSigDB set contains 124 of them and lacks only CCL3L1. B2 uses the 124-gene MSigDB set, which `fetch_data.sh` reproduces; `test_a_prep/baselines/check_senmayo.py` reproduces the comparison from the hashed supplement. B3 is the CellAge `cellsig/signatures1.csv` file, likewise hashed: up = rows flagged `ovevrexp` = 1 (525 genes), down = rows flagged `underexp` = 1 (734 genes). B5 is the HALLMARK `E2F_TARGETS` and `G2M_CHECKPOINT` files, hashed. B4 is the file `test_a_prep/baselines/B4_CCND1_NFIA.tsv` (CCND1 weight +1, NFIA weight −1; SHA-256 408de6f2eac280bd7e0ac21ac2fb4083f293c18243df66be1efcf08a7c428a52, recorded in `test_a_prep/baselines/SHA256SUMS` and checked by `scripts/verify_inputs.sh`). **B1 (the Hernandez-Segura 55 core genes) is the file `test_a_prep/baselines/B1_HS2017_core55_from_Fig2B.tsv`** (23 down, 32 up; SHA-256 e6615929a16b609f8292a4978d3af9bc8d3ea400f4937f0270e0e2c9604d9ade, in `test_a_prep/baselines/SHA256SUMS`). It was transcribed from the Figure 2B heatmap labels of the author manuscript (PMC5788810), **not** from the paper's Data S2F, which could not be retrieved. Checks: 55 distinct symbols, and every gene named in the figure's panels C and D appears with the matching direction. One symbol, FAM214B, is absent from the test-set annotation and counts as unmapped under the symbol rule (54 of 55 available before expression filtering). FAM214B is the previous HGNC symbol of ATOSB (HGNC:25666; ENSG00000005238 in the test annotation); the pre-specified rule does not map aliases, and any change would be a dated version bump before scoring. The list should be compared with Data S2F if that file becomes available; any difference is a dated version bump before scoring. Lines beginning with `#` in the file are comments. "Published genes" in the coverage rule means the genes in the hashed list.
- **B5 is descriptive** and plays no part in the outcome rule.
- **Independence.** Neither dataset appears in any of the four signatures' source lists at accession level. GSE162175 became public on 15 Feb 2026 and GSE307082 on 1 Sep 2026, both after the four signatures were published, so none could have used them. Independence from the earlier studies behind the signatures cannot be fully excluded.

## 7. Scoring (test set, no recalibration)
Take within-sample percentile ranks of the raw filtered counts over the test-filtered gene universe, with average ranks for ties (a per-sample scale factor does not change within-sample ranks). Score = mean percentile rank of up genes minus mean percentile rank of down genes (one-sided sets: mean percentile rank). Read-type differences (single-end 50 bp vs paired-end) are acknowledged; they are not adjusted for.

## 8. Endpoints and decision rule (fixed before any test performance is seen)
- **E1 (primary):** AUC for senescent (n = 3) vs quiescent (n = 3), higher score = senescent; ties count 0.5. The grid is multiples of 1/9 without ties.
- **E2 (descriptive):** AUC for senescent vs proliferating; it plays no part in the outcome rule.
- **E3 (contamination flag):** AUC for quiescent vs proliferating. A value of 8/9 or above, or 1/9 or below, flags near-perfect separation of arrested from dividing cells and fails the bound. The bound is 2/9 ≤ AUC ≤ 7/9.
- **E4 (non-inferential sanity gate):** it determines eligibility for A and B but is not a significance test. Test-set calculation: median-of-ratios size factors across the nine eligible test samples (geometric means over test-universe genes with non-zero counts in all nine), then log2(normalised count + 1), then log2FC(S vs Q) = mean(S) − mean(Q). For each signature gene that passes the test expression filter, it "agrees" if the sign of that log2FC equals the sign of its derivation log2FC(S vs Q); a difference of exactly zero counts as disagreement. E4 = agreeing genes ÷ signature genes passing the filter. The gate is 70%. No p-value is used: the signature genes were selected for large derivation effects, and no fair null is available.
- **E5:** E1 and E3 for baselines B1–B4. **B5** is descriptive.

**Definitions.** The signature is *evaluable* if section 5 yields at least 20 up and 20 down genes. A baseline is *evaluable* if it meets the coverage rule of section 6 (at least 70% of its published genes available for scoring, every needed direction non-empty). The signature *meets the conditions* if it is evaluable, test coverage and QC are satisfied (section 4), E1 = 9/9, E3 is within its bound, and E4 ≥ 70%. A baseline *matches* if it is evaluable and has both E1 = 9/9 and E3 within its bound.

**Outcomes** (exhaustive and mutually exclusive; thresholds are judgment calls set without seeing test results):
- **A, transfer, no baseline matched:** the signature meets the conditions, all four of B1–B4 are evaluable, and none matches.
- **B, transfer, an existing readout also meets it:** the signature meets the conditions and at least one evaluable baseline among B1–B4 matches. Conclusion: existing readouts suffice; no new-signature claim.
- **C, no transfer in this test:** the signature is evaluable, test coverage and QC are satisfied, and E1 ≤ 6/9. This can also arise from annotation, library type or batch differences, so it means "does not transfer in this test", not "no biology".
- **D, inconclusive:** everything else. This includes a signature that is not evaluable, or test coverage or QC that fails; E1 of 7/9 or 8/9; E1 = 9/9 with E3 outside the bound or E4 below 70%; and a signature that meets the conditions when no evaluable baseline matches but one or more of B1–B4 is not evaluable (the comparison cannot establish that no existing readout matches). Not a pass. No data are added to rescue it.

The A/B split is **descriptive only**, because it can hinge on one sample pair.

**Operating characteristics (arithmetic, not a result).** With 3 vs 3 vs 3 samples there are 1,680 equally likely allocations of nine distinct ranks to the three states. If scores carry no information: E1 = 9/9 occurs in 84 of 1,680 (5.0%); E1 = 9/9 with E3 inside its bound occurs in 52 of 1,680 (3.1%), computed by enumeration because E1 and E3 share the quiescent samples and their probabilities cannot be multiplied; E1 ≤ 6/9 occurs in 1,344 of 1,680 (80%). The 3.1% is before the E4 floor and the baseline conditions, which are not modelled, and so is not the false-positive rate of the full rule. The smallest exact one-sided permutation p-value for E1 is 1/20 = 0.05 (0.10 two-sided), assuming full exchangeability and distinct scores; a test restricted within the three replicate blocks has a minimum of 1/8. P-values are reported but used in no outcome rule. A perfect E1 is borderline evidence at best: the outcome is a transfer check, not proof.

## 9. Sensitivity and stop rule
- **Sensitivity (reported; cannot change the outcome):** S1 block on replicate index; S2 add the ER:RAS arms (the only non-genotoxic check); S3 signature size 50 and 200; S4 alternative normalisation in derivation (TMM-type); S5 leave-one-inducer-out derivation; S6 the reverse direction.
- **Stop rule:** Outcomes B, C and D end Test A with a short closing note. Only Outcome A leaves a still-small follow-up question open, and it justifies no drug ranking. A failure does not reopen the repurposing screen, which was closed on 2026-10-01. It means only that this signature work is not supported further.

## 10. Replicate provenance and labels
- **GSE307082:** the 18 samples (P1–P18) form three blocks of six, each holding all six state-by-treatment combinations. This is consistent with three biological replicates processed together, as the preprint states [inference: the block structure is not stated in GEO]. All 18 count columns map to the GEO titles.
- **GSE162175:** replicate provenance is unconfirmed, and arrest evidence for the sequenced quiescent samples is protocol-level in the published record. Replicates are treated as samples, not as proven independent experiments.

## 11. Process
1. Done (2026-10-14): Jean reviewed the plan and authorised the commit.
2. Done at this commit: the plan is committed to the public repository and tagged `test-a-plan-v1`. The scripts are part of the pre-registration; the plan prevails on any conflict between plan and script.
3. **Stage 1:** commit the derivation script, run it on GSE162175 only, and commit the gene list with its hash (tag `test-a-signature-v1`).
4. **Stage 2:** commit the scoring script and run it once on GSE307082.
5. Report every outcome, including C and D, with exact values. Record any deviation in a dated section; do not change thresholds after scoring.
6. For B, C or D, write the closing note.

Each push needs Jean's explicit go.

## 12. Open items
Before scoring: optionally compare B1 with Data S2F if it becomes available (any difference is a dated version bump); a separate go from Jean to run. Already in place: the GSE307082 file is in `fetch_data.sh` and the checksum list; B1 (transcribed from Figure 2B), B2, B3, B4 and B5 are hashed; and `scripts/verify_inputs.sh` passes.
