# Existing senescence signatures vs Test A's purpose

2026-10-01. Read-only literature review; no data was scored. Delegated to a research agent. These points were spot-checked against the primary sources: SenFlag full text (quiescence-exclusion marker, NFIA, Lenain 2017 quiescent cells, GSE213323, "No new sequencing data"), GSE75643 sample titles (3 × "Quiescent Serum Starvation"), and the E-MTAB-5403 SDRF (Quiescence and Proliferation samples present). Other claims are as reported by the agent, with its sources.

## Comparison

| Signature | Quiescent comparator? | Cell types | Independent validation | Availability | Fit for Test A |
|---|---|---|---|---|---|
| **SenFlag** (Demaria group, EMBO J 2026, [PMC13433995](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433995/)) | Yes, in derivation. Tig3 serum-starved (0% FBS, 10 d; Lenain 2017) and HUVEC contact-inhibited (GSE213323). How arrest was confirmed: not reported. | WI-38, BJ, IMR90, Tig3, HUVEC, macrophages; mouse and human in vivo scRNA-seq | Aging atlases, irradiation, senolytics, p16 ablation, LPS. No held-out quiescent test and no AUC found. | ~20 genes in Methods; R code in the paper's supplement | The only one built to exclude quiescence (NFIA low as the exclusion marker; CCND1 up in senescence, down in quiescence). It is a single-cell percentile rule, so it would need adapting for bulk data. |
| **Hernandez-Segura 2017** (55 core genes, Curr Biol) | Yes. HCA2 fibroblasts in 0.2% FBS for 48 h; genes shared with quiescence were removed. Arrest confirmation for the quiescent arm: not found in the main text. | HCA2, BJ, 5 fibroblast strains from GEO, keratinocytes, melanocytes, astrocytes | Limited (qPCR in BJ; one lymphoblast set; IPF lung) | Data S2F; E-MTAB-5403 | Removes arrest-shared genes, but from one short serum-starved fibroblast set. Never tested for discrimination. |
| **CellAge 1,259** (Chatsirisupachai et al., Aging Cell 2019, [PMC6826163](https://pmc.ncbi.nlm.nih.gov/articles/PMC6826163/)) | None found. Replicative senescence vs young cells. | 20 replicative-senescence microarray sets (supplement not accessible) | Overlap with GTEx/TCGA only | Table S2; genomics.senescence.info | Senescence vs proliferation only. Consistent with Run 1 tracking arrest. |
| **SenMayo** (Saul et al., Nat Commun 2022, [PMC9381717](https://pmc.ncbi.nlm.nih.gov/articles/PMC9381717/)) | None | Curated from the literature; validated in bone, brain, marrow, adipose | Strong in vivo work (aged cohorts, INK-ATTAC, D+Q trial) | Supplementary Data 1; MSigDB `SAUL_SEN_MAYO` | SASP-weighted; does not address arrest. |

Correction to earlier project notes: the CellAge expression signature is Chatsirisupachai et al. 2019, not 2021.

## Candidate comparator datasets (senescent + serum-starved quiescent)

| Accession | Cells | Senescent | Quiescent | Arrest confirmation |
|---|---|---|---|---|
| GSE75643 | Tig3 lung fibroblasts (hTERT-immortalised) | BRAF V600E OIS d4/d10, n = 3 each (+ bypass) | 0% FBS 10 d, n = 3 | Paper describes BrdU assays; not confirmed for the quiescent samples |
| E-MTAB-5403 | HCA2 primary foreskin fibroblasts | IR 10 Gy d4/10/20 | 0.2% FBS 48 h | Not found for the quiescent arm |
| GSE213323 | HUVEC | none | contact inhibition, low serum | Not checked; usable only as a specificity check |

## Implications (agent interpretation)

- **No existing signature does Test A's job in bulk fibroblast data.** SenFlag comes closest by design, but its quiescence exclusion was not tested on independent quiescent data.
- **SenFlag is the closest existing answer to Test A's question**, so it should be examined in depth before anything new is built.
- **GSE75643 and E-MTAB-5403 have a plain serum-starved quiescent arm**, which makes them better held-out tests than GSE329184's rapamycin-treated arm. Neither documents arrest confirmation for its quiescent samples.
- **Scoring SenFlag or the 55 genes on GSE162175 as baselines would be analysis.** That belongs in a Run 3 plan, committed before scoring, and is not done here.

## Correction: training-data overlap (added 2026-10-01, same day)

The comparator suggestion above is **withdrawn for testing SenFlag or the 55 genes.** A follow-up check of each signature's derivation data found:

| Candidate test set | SenFlag | Hernandez-Segura 2017 | CellAge 2019 | SenMayo |
|---|---|---|---|---|
| GSE162175 | not used | not used | not used | not used |
| GSE329184 | not used | not used | not used | not used |
| GSE75643 | **derivation** (its quiescent arm) | not used | not used | not used |
| E-MTAB-5403 (= PRJEB19157) | **derivation** | **derivation** | not used | not used |
| GSE213323 | **derivation** (supports the NFIA/CCND1 quiescence markers) | not used | not used | not used |

Evidence:
- **Cited in the SenFlag text:** GSE75643, PRJEB19157 and GSE213323 all appear in the SenFlag full text (PMC13433995). ENA maps PRJEB19157 to E-MTAB-5403.
- **Absent from SenFlag's supplement:** GSE162175 and GSE329184 appear nowhere among the 151 accessions in SenFlag's supplementary files, which include the per-gene results of its pooled bulk analysis.
- **Hernandez-Segura 2017** derived its signature from its own E-MTAB-5403.
- **CellAge** derived from 20 replicative-senescence microarray series (Table S2), none of them the candidates, and has no quiescent arm.
- **SenMayo** derived from the literature, with no expression data.

Implications:
- **Circular for SenFlag:** scoring SenFlag on GSE75643, E-MTAB-5403 or GSE213323 would test it on its own training data. The same holds for scoring the 55 genes on E-MTAB-5403. Use them only for sanity checks or training.
- **The independent test sets for all four signatures are GSE162175 and GSE329184.** GSE329184's rapamycin arm is still "arrest at RNA collection unconfirmed", so in practice GSE162175's serum-starved arm is the only independent, protocol-documented quiescent comparator.
