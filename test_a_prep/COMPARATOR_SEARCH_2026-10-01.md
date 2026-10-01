# Backup arrest comparator search

2026-10-01. Read-only search, delegated to a research agent, for **human fibroblast RNA-seq with contact inhibition or serum withdrawal, arrest measured near RNA collection, and documented biological replication**. It covered 554 GEO series, ArrayExpress and the linked papers' methods. No data was downloaded or scored.

I checked the top pick myself: the GEO sample and series records, and the preprint's methods, read in a browser. I also checked every candidate against SenFlag's 151 cited or supplementary accessions (the circularity check).

## Result: no dataset fully documents arrest on the sequenced quiescent samples

| Rank | Accession | Cells | Quiescence | Arrest measured | Replication | Senescent arm | Data | Used by SenFlag? |
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
- **Why it helps Test A (interpretation):**
  - It is independent of all four baseline signatures (submitted 2025, after HS 2017, CellAge 2019 and SenMayo 2022, and not in SenFlag).
  - Its arrest mechanism, contact inhibition, differs from GSE162175's serum withdrawal.
  - Its arrest evidence is stronger than any other candidate's.
- **Limits:**
  - **Cell line:** it is the same line as GSE162175 (IMR-90), so a cross-dataset test checks lab, protocol and mechanism, not cell source.
  - **Replication:** n = 3.
  - **Status:** the preprint is unreviewed.
  - **Arrest evidence:** EdU is described per model, not per sequenced replicate.
  - **SA-βgal:** quiescent cells were SA-βgal positive, so SA-βgal can't separate the states here.
  - **Heat-shock design:** the heat-shock samples must be excluded.

## Implication for the decision-tree conditions (interpretation)
GSE162175 (serum withdrawal) and GSE307082 (contact inhibition) together could meet C2 (two non-senomorphic arrest mechanisms) and C4 (one derives, the other is held out, neither used by any baseline). C1 and C3 are partly met: arrest is shown by EdU at model level in GSE307082 and by protocol only in GSE162175, and replication is 3–4 cultures from one cell line. Whether that suffices is a judgment for the analysis plan and for expert feedback.
