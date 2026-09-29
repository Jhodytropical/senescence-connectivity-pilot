# Senescence Connectivity Screen: exploratory pilot

## Status (after Run 2 validation, 2026-09-29)
> **This exploratory screen recovered known senescence inducers and generated candidate compounds for further testing. It did not demonstrate significant discrimination of known senolytics or senomorphics.** A prospectively specified follow-up validation (Run 2) found that **the screen did not demonstrate senescence specificity beyond proliferation arrest**. The inducer signal did not replicate on a second senescence gene set (which is not fully independent; see T1), and the SASP score overlaps substantially with **general inflammation suppression**.
>
> This is an **informative negative result about this particular pipeline**. It does not show that connectivity mapping fails in general. It can be shared with a lab as a transparent pilot, to ask for feedback on the method. The candidate list must not be presented as validated.

Nothing here is evidence of benefit in humans or advice to take any drug.

## Corrections to the first write-up (2026-09-28)
| Claim made | Correction |
|---|---|
| Control lists "fixed BEFORE looking at their ranks" | **False for the inducer list.** It was written after the output showed palbociclib and the MDM2 inhibitors as top mimickers. The Run 1 inducer AUC of 0.01 is circular and **withdrawn**. The other lists were written after the top SASP hits had been printed. |
| "The method finds drugs that calm/prevent senescence" | Unsupported. Senomorphics had AUC 0.60, p = 0.21 in Run 1 and AUC 0.51, Holm p = 1.0 in Run 2. Failing to detect senolytics does not validate a different class. |
| Local Fisher scoring gives "the same results" as a LINCS signature query | Unsupported. Consensus gene sets with overlap tests are a different analysis from per-signature (cell line, dose, time) querying. Equivalence was never tested. |
| Rilmenidine is "the strongest lead"; fostamatinib is "novel" | Withdrawn. Rilmenidine's worm-lifespan result (Bennett et al., *Aging Cell* 2023) is prior convergence, not validation of this screen. "Novel" would need a dedicated literature search, which hasn't been done. |
| "Nothing similar exists" | That check covered only Jean's own project folders. It says nothing about scientific novelty. |

## Method (Run 1, frozen in `frozen/run1_2026-09-28/`, SHA256SUMS)
- **Query:** the CellAge senescence meta-signature (Chatsirisupachai et al. 2019; 150 genes up and 150 down) and SenMayo SASP (Saul et al. 2022).
- **Drugs:** 5,425 LINCS L1000 *consensus* signatures (Enrichr library), scored locally with one-sided Fisher overlap tests.
- **Scores:** `reversal_score` = reversal overlaps minus mimicry overlaps. `sasp_score` = SASP genes switched off minus SASP genes switched on.
- **Candidate score:** 70% SASP percentile + 30% reversal percentile. **This weighting is arbitrary.** Run 2 T5 tests how much it matters.

## Run 2: prospectively specified follow-up
The plan is in `PREREGISTRATION_run2.md` (sha256 `7aa761a2…`). The existing project record states that it was made read-only and logged before Run 2 scoring. Run 1 results were already visible when this follow-up was planned, so it is not a blinded or wholly independent confirmation. A hash identifies the exact file contents; it does not prove when the file was written. A timestamped, independently preserved record would strengthen evidence of timing. The original plan is retained unchanged as a historical record. Control classes are defined mechanically from Broad Repurposing Hub MoA labels, which match 3,331 of the 5,425 drugs. Script: `src/04_run2_validation.py`. Outputs: `results/run2/`.

**Prospectively specified tests (Holm-corrected across 7; prior Run 1 results were known):**
| Test | Class (n) | AUC [95% CI] | Holm p | Plan-specified verdict |
|---|---|---|---|---|
| T1 second gene set (Fridman senescence-UP, 50 genes, **no overlap with CellAge; not independent evidence**) | MDM inhibitors (8) | 0.53 [0.43–0.66] | 1.0 | **Fail.** No signal on this second gene set; nonoverlapping genes do not establish independent experiments or cohorts |
| | CDK inhibitors (27) | 0.60 [0.48–0.70] | 0.43 | Fail |
| T2a reversal with E2F/G2M proliferation genes removed | MDM inhibitors | 0.15 [0.01–0.31] | 0.004 | Pass |
| | CDK inhibitors | 0.24 [0.15–0.34] | <0.001 | Pass |
| T2b reversal residualized on a proliferation-arrest score | MDM inhibitors | 0.55 [0.33–0.77] | 1.0 | **Fail.** Signal disappears |
| | CDK inhibitors | 0.51 [0.38–0.63] | 1.0 | Fail |
| T3 senomorphics (mTOR, JAK, p38) on the SASP score | 67 | 0.51 [0.44–0.58] | 1.0 | **Fail** |
| T4 senolytics (BCL, HSP, Na/K-ATPase), expected null | 21 | 0.67 on SASP, 0.38 on reversal | — | No discrimination in the useful direction |

**What this means:**
- The Run 1 reversal score correlates **−0.73** with a plain proliferation-arrest score, indicating **substantial overlap**. Inducers still separate after E2F/G2M genes are removed (T2a), but the adjusted score does not significantly distinguish them after residualizing on proliferation arrest (T2b). These results do not establish that arrest causes the signal or quantify its causal contribution. Senescence includes arrest, so this adjustment is conservative. The plan required both tests to pass, and T2b failed: **the screen did not demonstrate senescence specificity beyond proliferation arrest**.
- The SASP score correlates **0.48** with a generic inflammatory-response score (HALLMARK), and 25 of the 124 SenMayo genes are in that set. Exploratory classes that looked strong on SASP also score high on generic inflammation: MEK inhibitors 0.85 on SASP vs 0.77 on inflammation, statins (HMGCR) 0.72 vs 0.75. That pattern points to **general anti-inflammatory activity**, not senescence specificity. These classes were seen in Run 1, so this is exploratory only.
- **Cytotoxicity is uncontrolled.** Consensus signatures carry no viability data.

**T5, ranking sensitivity (32 configurations: N ∈ {50, 100, 150, 250} × SASP weight ∈ {0.5, 0.7, 0.9, 1.0} × Fisher or overlap fraction):**
- The overall ranking is stable: Spearman 0.90–1.00 against Run 1, median 0.95.
- The top 50 is only moderately stable: Jaccard median 0.54, range 0.16–1.00.
- 12 of the 13 named Run 1 candidates stay in the top 5% in at least 80% of configurations. The exception is simvastatin (44%).
- **Stability is not validity.** These drugs rank robustly *on a score that failed validation*.

## Candidate list: status
`results/run2/candidate_robustness.csv` and `robust_by_moa.csv` hold 125 drugs that are robust to scoring choices. By mechanism, they cluster in anti-inflammatory classes (glucocorticoids, COX inhibitors, TGF-β receptor inhibitors, PDE inhibitors), plus known toxins (potassium dichromate, erastin). That pattern fits the general-inflammation interpretation. Treat the list as **hypotheses for testing**, not leads.

## What would move this forward
1. **Freeze this version and seek methodological feedback first.** Share it as a transparent pilot and an informative negative result about this pipeline, with an unvalidated candidate list.
2. **Check whether suitable datasets exist before deciding on Run 3.** Look for drug-treated senescent-cell expression data with matched proliferating and quiescent (resting) controls, plus survival/viability measurements. Let data availability and methodological feedback determine whether another run is worthwhile.
3. **Validate any revised readout.** Measuring senescent cells alone does not remove growth-arrest confounding. Matched controls and viability measurements are needed to distinguish senescence-specific effects from growth arrest, general inflammation suppression, broad transcriptional suppression and cell death. Score penalties for these effects would themselves require validation.

## Reproduce
```bash
cd ~/Claude_Projects/Longevity_Research/senolytic_repurposing
../.venv/bin/python src/01_signature.py
../.venv/bin/python src/02_score_local.py
../.venv/bin/python src/03_validate_and_rank.py   # Run 1 (its control-list validation is superseded)
../.venv/bin/python src/04_run2_validation.py     # Run 2, prospectively specified follow-up
```
