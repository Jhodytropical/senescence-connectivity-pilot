# Run 2: Validation of the Run 1 screen (pre-registered 2026-09-29, before any Run 2 scoring)

Run 1 outputs are frozen in `frozen/run1_2026-09-28/` (see `SHA256SUMS`). Nothing in Run 2 may modify them.

## Disclosure about Run 1
- The "senescence_inducer" control list in Run 1 was written **after** the Run 1 output showed palbociclib, RG-7388, SAR405838 and AMG-232 as top mimickers. Its AUC 0.01 is **circular** and is withdrawn as evidence.
- The senolytic and senomorphic lists were written after the top SASP hits had been printed. Glucocorticoids, MEK, SYK, BTK, PI3K and HMGCR inhibitors were **seen** as Run 1 hits. Any class test on those mechanisms is exploratory, never confirmatory.

## Control classes: defined mechanically by the Broad Drug Repurposing Hub `moa` field (exact label match)
Drug names are matched after lowercasing and removing non-alphanumerics. The match rate is reported.
| Role | Hub MoA labels | Status |
|---|---|---|
| Senescence inducer (primary) | `MDM inhibitor` | confirmatory (class chosen by mechanism, not by rank) |
| Senescence inducer (secondary) | `CDK inhibitor` | confirmatory |
| Antiproliferative comparator | `tubulin polymerization inhibitor` | confirmatory (mitotic arrest, mostly not senescence) |
| Senolytic | `BCL inhibitor`, `HSP inhibitor`, `Na/K-ATPase inhibitor` | expected null (pre-stated) |
| Senomorphic | `mTOR inhibitor`, `JAK inhibitor`, `p38 MAPK inhibitor` | confirmatory |
| Seen in Run 1 | `glucocorticoid receptor agonist`, `MEK inhibitor`, `SYK inhibitor`, `Bruton's tyrosine kinase (BTK) inhibitor`, `PI3K inhibitor`, `HMGCR inhibitor` | exploratory only |

## Tests
AUC = P(class drug scores higher than a non-class drug), two-sided Mann-Whitney. Confidence intervals come from a 2,000-draw bootstrap that resamples class members, which accounts for small class sizes. Holm correction is applied across the confirmatory tests of T1–T3.

- **T1, independent signature.** Query = FRIDMAN_SENESCENCE_UP (MSigDB; Fridman & Tainsky 2008) **minus every gene in the CellAge signature** (so no gene overlaps Run 1). Score = −log10 p(query ∩ drug-UP) − (−log10 p(query ∩ drug-DOWN)), meaning "senescence-like".
  *Pass:* MDM inhibitors have AUC > 0.5 with Holm p < 0.05.
- **T2, proliferation control.** Remove every HALLMARK_E2F_TARGETS and HALLMARK_G2M_CHECKPOINT gene from the Run 1 CellAge query (N = 150/direction as before), then recompute `reversal_score`. Also report a proliferation-arrest score (E2F+G2M ∩ drug-DOWN), and the Run 1 reversal score residualized on it (OLS).
  *Pass:* MDM inhibitors have AUC < 0.5 with Holm p < 0.05 on the proliferation-free reversal score **and** on the residualized score. The tubulin comparator is reported alongside. If tubulin inhibitors score as strongly as MDM inhibitors, the signal is interpreted as growth arrest.
- **T3, senomorphics.** Senomorphic classes on the Run 1 `sasp_score` and on the SASP score with HALLMARK_INFLAMMATORY_RESPONSE genes as a comparator query.
  *Pass:* AUC > 0.5 with Holm p < 0.05 on `sasp_score`. If the inflammatory-response comparator scores equally, it is interpreted as generic anti-inflammation, not senescence-specific.
- **T4, senolytics.** Reported with CIs; the expected result is null.
- **T5, sensitivity of the candidate ranking.** Grid: N ∈ {50, 100, 150, 250} × SASP weight w ∈ {0.5, 0.7, 0.9, 1.0} × statistic ∈ {Fisher −log10 p, overlap fraction}. Report Spearman ρ against the Run 1 ranking and the top-50 Jaccard. A named candidate is **robust** only if it sits in the top 5% in ≥ 80% of configurations. Top candidates are reported collapsed by Hub MoA so that related drugs are not counted as independent hits.

## Pre-stated interpretation
- If T1 or T2 fails, the inducer result is not evidence for senescence-specific detection.
- If T3 fails, the screen does not demonstrate senomorphic discrimination, and candidates remain unvalidated hypotheses.
- Cytotoxicity cannot be controlled with the available data (no viability data in L1000 consensus signatures). This remains an open limitation.
- Signature-level LINCS querying (per cell line, dose and time) is not done here. Run 1 and Run 2 results are **not** claimed to be equivalent to it.
