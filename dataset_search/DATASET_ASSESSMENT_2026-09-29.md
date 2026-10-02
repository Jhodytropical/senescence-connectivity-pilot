# Dataset availability check (before deciding on Run 3), 2026-09-29

**Current status:** Run 3 remains on hold, with methodological feedback first. The initial assessment and first verdict below are retained as history and superseded by “Refinements (2026-09-29)” at the end. Test A is feasible, not validated; Test B currently lacks an interpretable survival endpoint.

**Required design:** drug-treated **senescent** cells with matched **proliferating** and **quiescent/arrested** controls, plus **viability** measurements.
**Search:** NCBI GEO E-utilities with 3 queries → 190 unique human series (`geo_hits.json`, `geo_search.py`). Series were flagged by design keywords, then the top candidates were read by hand. The search is read-only, and nothing was downloaded beyond metadata.

## Best match: GSE329184 (public 2026-09-23, PMID 42754596; RNA-seq counts matrix available)
- Dermal (NHDF) and lung (NHLF) fibroblasts, 2 donors each, mostly 4 replicates per condition, 240 samples.
- **Proliferating:** untreated, and DMSO vehicle.
- **Arrested, not senescent:** rapamycin 10 µM and nocodazole. The authors describe tool compounds that induce *quiescence*; which compound plays which role needs confirming in the paper.
- **Senescent:** bleomycin-induced, palbociclib-induced, and late passage (replicative).
- **Senolytic:** navitoclax at 0.1 and 1 µM, given to both senescent and non-senescent cells.
- **Viability:** the study pairs RNA-seq with Cell Painting imaging. Per-well cell counts are **not** in GEO and must be checked in the paper's supplement.
- **Limits:** only one senolytic, and no senomorphic applied to senescent cells (rapamycin is used as an arrest control here). Palbociclib induces senescence in this dataset, so it must be excluded from any inducer test built on it (circularity).

## Supporting datasets
| Series | Design | Gap |
|---|---|---|
| GSE162175 (IMR90, n=32) | Several forms of senescence vs **growing and quiescent** cells | Induction only, no drug on senescent cells; useful as a **second-lab replication** of a senescence-vs-arrest signature |
| GSE210020 (HDF, n=40) | Senescent and non-senescent × ABT263, nintedanib, sunitinib, MP470, triplicates; viability in the paper | No quiescent control |
| GSE146575 (BJ, n=12) | Rapamycin/DOT1L inhibitor across young-quiescent → senescent | n = 1 per condition |

## What this means for Run 3
Suitable data **does exist**, but it can **validate**, not **screen**. GSE329184 (+ GSE162175) could supply:
1. A signature of **senescent vs arrested** cells (not vs proliferating), built from experiments separate from CellAge. This addresses both the proliferation confound and the independence problem.
2. A real senolytic response in senescent vs non-senescent cells, which could test whether the L1000 approach can ever separate senolytic response from general toxicity.

A Run 3 limited to that scope looks worthwhile. It should be plan-first, with the plan deposited somewhere independent and timestamped before scoring, and it should exclude every compound used to build the signature. It's not started; it needs Jean's go, and ideally method feedback first.

---

# Verification against the paper (added 2026-09-29, after reading the full text)
Source: Tan Y, Liu A, Larkin E, Wani R, Dick A, Patassini S, Erlmann P. "Deciphering senescence-associated mechanisms through cell painting & transcriptomics." *npj Aging* 2026. doi:10.1038/s41514-026-00500-8, PMC13586382 (open access). Local copy: `paper_PMC13586382.xml`.

## Correction to the assessment above
**Wrong:** I listed nocodazole as an arrest control. The authors state that in the repeat experiment — the one deposited in GEO — nocodazole-treated cells "remained in a proliferative phenotype reflected in nuclei counts and morphology", and they "did not regard nocodazole as senescence-like condition in the downstream analysis." Nocodazole is neither a senescence condition nor a quiescence control here. The GEO metadata alone ("Tool compounds were used to induce quiescence or senescence") does not say this. The error came from inferring roles from compound names.

## Answers to the three open questions
**1. Are the arrest controls suitable? — Yes, for rapamycin; there is only one.**
Rapamycin (10 µM, 2 days) was chosen "for its quiescent-like phenotype (cell cycle arrest with immediate proliferation after compound removal)", so the role is stated and the phenotype is measured (reversibility on washout, plus a distinct mitochondrial morphology cluster). Senescence conditions are bleomycin, palbociclib and late passage. So the design gives **one** quiescence-like control, not a panel, and that control is a single compound with its own mTOR-specific effects on gene expression.

**2. Can expression samples be matched to viability? — No, not at sample level, and there is no viability assay.**
- Methods: "Technical triplicates were prepared for each assay, (1) Live imaging & SA-β-galactosidase, (2) CP, (3) RNA extraction." The three readouts are **separate plates**, so RNA-seq wells are not the wells that were imaged. GEO says samples were excluded over "experimental concerns on the separate CellPainting plate with matched experimental plate layout."
- The word "viability" does not appear in the paper. The survival proxy is **nuclei count**.
- Matching is therefore **condition-level** (cell type × inducer × senolytic dose), not per sample.

**3. What counts as a senolytic response? — The dataset does not establish selective killing.**
The authors' own reading of their survival proxy is ambiguous in both directions: a rare morphology cluster shows "either active mitosis or fragmented nuclei from ongoing apoptosis", and after navitoclax "we see an increase in the number of nuclei ... which is also supportive of increased mitosis or apoptosis". Nuclei counts go **up**, and the response "differs between cell type and chemical inducer" — for palbociclib-induced senescence in dermal fibroblasts, navitoclax "does not shift nuclei count" at all.

## Verdict: the senolytic half of Run 3 is not answerable with this dataset
The central question — does expression separate selective senolysis from general toxicity — needs survival measured **alongside** expression in the same wells. This dataset has no viability assay, an ambiguous proxy, and readouts on separate plates. Expression in surviving cells here could equally reflect selective loss of senescent cells or a shift in which cells remain. **This half stays on hold**, pending either the authors' per-well data or a dataset with paired viability.

The **senescent-vs-arrested signature** half remains supported: rapamycin is a stated, phenotyped quiescence-like control, and GSE162175 (separate lab) offers replication. Keep the two tests distinct, as advised.

## Incidental finding relevant to our pilot
The authors report that **SenMayo "was only partially enriched for chemically induced senescence-like conditions but not LP [late passage]"** cells, while the Hernandez-Segura in-vitro fibroblast signature did match. Our pilot's `sasp_score` is built on SenMayo. Independent evidence that SenMayo underperforms in cultured fibroblasts is a further reason not to treat that score as a senescence-specific readout.

---

# Refinements (2026-09-29)
1. **Test B wording.** The verdict above ("needs survival measured alongside expression in the same wells") overstated the requirement. Properly matched parallel plates can support a condition-level comparison if the viability assay, replication and matching are adequate. **The main reason Test B stays paused is the lack of an interpretable survival endpoint** (no viability assay; nuclei count read by the authors as mitosis *or* apoptosis), not the separate plates alone. Status: "The currently identified measurements do not support a reliable test of selective senolysis versus general toxicity. We welcome advice on whether additional measurements or supplements make that comparison possible."
2. **Test A is feasible, not validated.** Senescent vs rapamycin-arrested cells may separate senescence from *rapamycin's specific effects* rather than from arrest in general. Checked GSE162175 (Wagner et al., *Nat Commun* 2026, PMC13254117; local copy `paper_PMC13254117.xml`): its quiescence is by **serum withdrawal** (GEO growth protocol: DMEM 0.5% FBS, days 3–8; 4 replicates), which is a different arrest mechanism, as required. Open points: no explicit arrest phenotyping of the *sequenced* quiescent samples was found; the paper's imaging arm used 0.1% FBS, so the conditions may differ; and palbociclib-induced senescence is in both datasets, so palbociclib must be excluded from inducer tests.
3. **SenMayo.** Its partial enrichment is a **coverage** question (limited sensitivity or context dependence in cultured fibroblasts), not by itself a specificity finding. Specificity would need a test of whether it responds in non-senescent conditions such as ordinary inflammation.
