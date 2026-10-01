# Backup arrest comparator search

2026-10-01. Read-only search, delegated to a research agent, for **human fibroblast RNA-seq with contact inhibition or serum withdrawal, arrest measured near RNA collection, and documented biological replication**. It covered 554 GEO series, ArrayExpress and the linked papers' methods. No data was downloaded or scored.

I checked the top pick myself: the GEO sample and series records, and the preprint's methods, read in a browser. I also checked every candidate against SenFlag's 151 cited or supplementary accessions. That check works at the level of accession numbers only. It does not rule out reuse of the same underlying experiments or samples under other accessions.

## Result: no dataset fully documents arrest on the sequenced quiescent samples

| Rank | Accession | Cells | Quiescence | Arrest measured | Replication | Senescent arm | Data | Accession cited by SenFlag? |
|---|---|---|---|---|---|---|---|---|
| 1 | **GSE307082** | IMR-90 | Contact inhibition, 10 d | EdU (24 h) plus re-entry on replating, stated as how quiescence "was confirmed". Model-level; not explicitly tied to the sequenced inductions | 3 biological replicates, processed together | Doxorubicin DNA-damage senescence | RNA-seq count matrix on GEO. Use the 9 non-heat-shock samples (3 proliferating / 3 quiescent / 3 senescent) | no |
| 2 | GSE287058 | IMR90, BJ (+ LF1, preadipocytes) | Contact inhibition 3 d; 0.01% FBS 3 d; 20% and 3% O₂ | None documented | 3 batches | none | RNA-seq, HTSeq counts | no |
| 3 | GSE117444 | Primary dermal fibroblasts, 2 strains (Coller lab) | Contact inhibition 7 d | Protocol only | 3 matched replicates | none | RNA-seq counts | **yes (circular for SenFlag)** |
| 4 | GSE227766 | IMR90 | Contact inhibition (~100% + 4 d) | Protocol only | biological triplicate | Etoposide, IR 15 Gy | RNA-seq (raw only) | no |
| 5 | GSE328392 | Primary lung fibroblasts, 16 donors | Serum starvation (duration not in GEO) | Unknown; "not part of the primary analysis" | donor-level | IR, bleomycin | h5ad | no |
| 6 | GSE118693 | MRC-5 | Contact inhibition 9 d | Protocol only | n = 3 | none | RNA-seq counts | no |

Lower value: GSE117337 (3′ poly(A) sequencing), GSE42509 (n = 2, no assay), GSE60883 (150-day contact inhibition, drifting toward senescence), GSE60340 (TP53-mutant background, exclude), GSE93535 (no proliferating arm), GSE86867 (only a DE table). The ArrayExpress hits are microarrays only.

## GSE307082 (Watts et al., bioRxiv 2025.09.07.674107, not peer-reviewed)
- **Verified in the preprint methods:**
  - Contact-inhibited quiescence: seeded at 30,000 cells/cm² and held 10 days.
  - "Quiescence was confirmed by lack of EdU incorporation", and distinguished from senescence by re-entry on replating and no nuclear enlargement.
  - The process "was repeated to obtain three individual biological replicates".
  - Contact-inhibited quiescent cells "also stained positive for the SA-bG assay".
- **Verified in GEO:** proliferating, quiescent and senescent IMR-90, each with and without heat shock, three biological replicates, and a processed count matrix.
- **Status: a promising backup comparator, pending review of the files themselves** (count matrix, sample labels, replicate provenance).
- **Why it may help Test A (interpretation):**
  - Its accession is not cited by any of the four baseline signatures, and it post-dates HS 2017, CellAge 2019 and SenMayo 2022. Sample-level independence is not yet checked.
  - Its arrest mechanism, contact inhibition, differs from GSE162175's serum withdrawal.
  - Its arrest evidence is stronger than any other candidate's.
- **Limits:**
  - **Cell line:** it is the same line as GSE162175 (IMR-90), so a cross-dataset test checks lab, protocol and mechanism, not cell source.
  - **Replication:** n = 3.
  - **Status:** the preprint is unreviewed.
  - **Arrest evidence:** EdU is described per model, not per sequenced replicate.
  - **SA-βgal:** quiescent cells were SA-βgal positive, so SA-βgal can't separate the states here.
  - **Heat-shock design:** Test A targets conditions without an additional acute heat-shock perturbation, so the heat-shock samples are outside the intended comparison. That exclusion must be stated in a plan before any scoring.

## Implication for Test A (interpretation)
- **What the pair could provide:** GSE162175 (serum withdrawal) and GSE307082 (contact inhibition) could give Test A two arrest mechanisms, neither of them senomorphic. One dataset could derive a signature and the other test it, provided sample-level independence from the baselines holds.
- **Arrest and replication evidence is partial:** EdU at model level in GSE307082, protocol only in GSE162175, and 3–4 cultures per group.
- **Scope of a cross-test:** it would assess transfer across labs and arrest methods **within IMR-90**. It would not establish that a signature generalises to other cell types.
- **Markers:** reversible arrest and absent EdU incorporation support the quiescent label. SA-βgal positivity in the quiescent cells shows why no single marker should define the groups.
- **Before any scoring, a committed plan must fix:**
  - which dataset derives and which tests, with no swapping after seeing performance;
  - the pass criterion, including uncertainty with three replicates;
  - the heat-shock exclusion rationale;
  - whether replicate provenance and sample labels support the analysis.
