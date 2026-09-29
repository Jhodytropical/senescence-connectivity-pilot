# A senescence connectivity-mapping pilot that failed its own validation

**Negative result.** I scored 5,425 LINCS L1000 consensus drug signatures against the CellAge senescence meta-signature to look for compounds that reverse cellular senescence. The screen **did not demonstrate senescence specificity beyond proliferation arrest**, and did not discriminate known senolytics or senomorphics. This repository holds the code, the failed validations, a withdrawn result, and the reasoning — so the next person can skip this particular dead end or tell me where I went wrong.

Jean Hyacinthe · independent, computational only, no lab · September 2026

> Nothing here is evidence of benefit in humans, or advice to take any compound. The candidate rankings are unvalidated and should not be treated as leads.

## The result in one table
Validation classes were defined mechanically from Broad Drug Repurposing Hub mechanism-of-action labels. Holm-corrected across 7 confirmatory tests.

| Test | Class | AUC [95% CI] | Holm p | Verdict |
|---|---|---|---|---|
| Second senescence gene set (Fridman, no shared genes) | MDM2 inhibitors (8) | 0.53 [0.43–0.66] | 1.0 | fail |
| Reversal score, proliferation genes removed | MDM2 inhibitors | 0.15 [0.01–0.31] | 0.004 | pass |
| Reversal score residualised on proliferation arrest | MDM2 inhibitors | 0.55 [0.33–0.77] | 1.0 | **fail** |
| SASP score | senomorphics: mTOR/JAK/p38 (67) | 0.51 [0.44–0.58] | 1.0 | **fail** |
| Either score | senolytics: BCL-2/HSP90/Na⁺K⁺-ATPase (21) | no discrimination | — | expected null |

- The reversal score correlates **−0.73** with a plain proliferation-arrest score.
- The SASP score correlates **0.48** with a generic HALLMARK inflammatory-response score.
- Rankings are stable across 32 scoring configurations (Spearman 0.90–1.00). **Stability is not validity** — they are stable on a score that failed validation.

## A result I withdrew
The first write-up reported AUC 0.01 (p = 7.6e-06) for senescence inducers and called it strong validation. **That was circular**: I chose the inducer control list *after* seeing palbociclib and the MDM2 inhibitors at the top of the output. It is withdrawn, and the correction is recorded in [the report](senolytic_repurposing/README.md) and in a comment on the script that produced it. The Run 2 validation exists because of that mistake.

Run 2 was specified before scoring but **after** the Run 1 results were visible — a prospectively specified follow-up, not a blind pre-registration. The plan is in [PREREGISTRATION_run2.md](senolytic_repurposing/PREREGISTRATION_run2.md), fixed before the scoring in `04_run2_validation.py` ran.

## What is here
| Path | What |
|---|---|
| [senolytic_repurposing/README.md](senolytic_repurposing/README.md) | The full report, including the corrections table |
| [senolytic_repurposing/PREREGISTRATION_run2.md](senolytic_repurposing/PREREGISTRATION_run2.md) | The validation plan, written before scoring |
| `senolytic_repurposing/src/` | Four scripts: signature → scoring → Run 1 ranking → Run 2 validation |
| `senolytic_repurposing/results/` | All scores for 5,425 drugs, class tests, sensitivity grid |
| `senolytic_repurposing/frozen/` | Run 1 and the corrected report, read-only, with SHA256SUMS |
| [dataset_search/](dataset_search/DATASET_ASSESSMENT_2026-09-29.md) | Whether public data can support a better test — and where my first assessment was wrong |
| [PROTOCOL_for_feedback_2026-09-29.md](PROTOCOL_for_feedback_2026-09-29.md) | One-page request for methodological feedback |

## Reproducing
```bash
python3 -m venv .venv && .venv/bin/pip install pandas requests scipy
scripts/fetch_data.sh                                        # re-downloads every input
.venv/bin/python senolytic_repurposing/src/01_signature.py
.venv/bin/python senolytic_repurposing/src/02_score_local.py
.venv/bin/python senolytic_repurposing/src/03_validate_and_rank.py   # Run 1 (its validation is superseded)
.venv/bin/python senolytic_repurposing/src/04_run2_validation.py     # Run 2
```
No input data is redistributed here. `scripts/fetch_data.sh` pulls CellAge and DrugAge (HAGR), MSigDB gene sets, the LINCS L1000 consensus library (Enrichr, Ma'ayan Lab) and the Broad Drug Repurposing Hub annotations from their original sources.

## Where this is going
On hold pending methodological feedback. Two candidate follow-ups, deliberately kept separate:

- **Test A — a senescent-vs-*arrested* signature.** Feasible, not yet validated. Needs at least two arrest mechanisms (rapamycin in GSE329184, serum withdrawal in GSE162175) so a result does not just reflect one compound's effects. **Known weakness:** rapamycin is itself a senomorphic, so senescent-vs-rapamycin-arrested may amount to senescent-vs-partially-suppressed-senescent. A non-senomorphic second arrest mechanism may be a precondition — see the [protocol addendum](PROTOCOL_for_feedback_2026-09-29.md#addendum-added-2026-09-29-after-the-feedback-requests-were-sent).
- **Test B — selective senolysis vs general toxicity.** Paused. The datasets I found lack an interpretable survival endpoint measured alongside expression. I would rather record that than run an analysis that cannot answer the question.

**If you work on senescence and think either test is misconceived, that is the most useful thing you could tell me.** Open an issue, or see the protocol above. A recommendation to stop will be recorded as the outcome, not quietly dropped.

Feedback requests went to three researchers on 2026-09-29. The exact protocol they were linked to is commit [`b8fb688`](../../blob/b8fb688/PROTOCOL_for_feedback_2026-09-29.md), also tagged `sent-2026-09-29`. Later thinking is appended to the protocol as a dated addendum, never edited into the body.

**Conventions.** `senolytic_repurposing/frozen/` is immutable — its `SHA256SUMS` must always verify, and any change there invalidates the record. Any future correspondence cites commit-pinned URLs rather than `main`, which drifts.

## Sources
CellAge / DrugAge: Human Ageing Genomic Resources · SenMayo: Saul et al. 2022 · Fridman senescence sets & HALLMARK: MSigDB · LINCS L1000 consensus signatures: Enrichr, Ma'ayan Lab · Drug Repurposing Hub: Broad Institute · GSE329184: Tan et al., *npj Aging* 2026, doi:10.1038/s41514-026-00500-8 · GSE162175: Wagner et al., *Nat Commun* 2026, doi:10.1038/s41467-026-71564-z

Code is MIT-licensed. Analysis run with Claude Code.
