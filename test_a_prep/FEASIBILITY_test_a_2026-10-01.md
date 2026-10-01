# Test A data feasibility — GSE162175 and GSE329184

2026-10-01, revised the same day after review. **Preparation only.** No expression comparison, signature, score or drug ranking was computed. Inputs were the GEO sample records, the two public count files (structure only: columns, identifiers, integer check, library sizes) and the two papers' methods. Run 3 remains on hold pending methodological feedback. Interpretation is unresolved; this file is not for publication until reviewed.

Files: `sample_manifest.csv` (272 samples, one row each), `structure_checks.json`, `build_manifest.py` (re-runs both). The count files are in `data/` and are not redistributed.

Labels: **[GEO]** = sample record, **[PAPER]** = published methods, **[FILE]** = count file, **[INFERENCE]** = my reading, not stated by the authors.

## 1. Proposed Test A groups

| Series | Senescent | Arrest comparator | Proliferating reference | Excluded from Test A |
|---|---|---|---|---|
| GSE162175 (IMR90, n = 4 each) | doxorubicin, etoposide, irradiation, RAS-induced (4OHT) — 16 | quiescent, 0.5% FBS d3–8 — 4 | growing DMSO; ER:RAS non-induced — 8 | palbociclib — 4 |
| GSE329184 (NHDF/NHLF) | bleomycin, late passage — 32 (27 in counts) | **none confirmed.** Rapamycin-treated samples (16; 12 in counts) are labelled "rapamycin-treated; arrest at RNA collection unconfirmed", not quiescent controls | untreated, DMSO vehicle — 32 | navitoclax arms (Test B), nocodazole, palbociclib — 160 |

Palbociclib is excluded in both because CDK4/6 inhibition confounds arrest with senescence (decision 2026-09-29). Nocodazole is excluded because the authors report it stayed proliferative in the repeat experiment [PAPER].

## 2. Usable expression files and gene identifiers

- **Both usable as raw integer counts** [FILE]: no non-integer cells, no duplicate IDs, unversioned Ensembl gene IDs throughout.
- GSE162175: 57,232 genes × 32 samples; every count column maps to a GSM. The column names differ slightly from the GEO titles (`IMR90_iRas_*` vs `iRas_*`); the manifest maps them. GEO says hg19 + Rsubread, but the Ensembl release is not stated. Library sizes run from 23.5M to 57.7M (a 2.5× spread), so normalisation matters.
- GSE329184: 58,051 genes × 230 samples (Ensembl 86, GRCh38) [GEO]. Ten GEO samples are absent from the processed file: two failed sequencing QC (0010, 0235) and eight were dropped over Cell Painting plate concerns [GEO]. Those eight are late-passage NHLF (4) and rapamycin-treated NHLF (4). Raw reads for all 240 exist in SRA but would need re-alignment.
- 51,686 gene IDs are shared between the two files; the rest are unique to one or the other (5,546 and 6,365).
- **Default: analyse the two series separately.** They differ in genome build, annotation, read layout (SE50 vs PE ~2×101) and cell source (fetal vs adult fibroblasts). Whether they can also be compared beyond direction — for example after harmonising annotations — is for the analysis plan to decide, not this report.

## 3. Donor and batch confounding

**GSE162175**
- A single cell line, so the comparison has **no between-donor variation**. That does not rule out confounding: passage, culture history and experimental batch could still differ between conditions, and nothing in the record shows they don't.
- The paper's methods say in-vitro replicates "represent independent experiments" [PAPER]. That is a general statement for the paper, not a statement about these RNA-seq samples. **Replicate provenance is unconfirmed**: until it is established, the four replicates should not be treated as independent experiments, and whether replicate index marks a shared batch across conditions is unknown.

**GSE329184**
- Two donors per tissue. The authors observed **donor-specific batch effects** in the transcriptomics and corrected for them per cell type [PAPER]. Every donor has every Test A condition [GEO], so donor can be modelled as a blocking factor.
- **Replicates are wells, not independent experiments.** Each sample is one well position pooled from two technical plates [PAPER], and the four samples per condition per donor come in two adjacent-number pairs [GEO]. Effective biological replication is at most 2 donors per tissue [INFERENCE].
- **Late-passage donor labels are ambiguous** [GEO]: `NHDF1` (3 in counts), `NHDF1_2` (4) and `NHLF_1and2` (4 in counts; 4 more dropped by the authors). These may be pooled or mixed donors.
- **Rapamycin-treated NHLF is thin**: one pair of wells per donor remains after the authors' exclusions.
- If sample numbers follow RNA-extraction plate order (96 per plate), donor and extraction plate partly coincide [INFERENCE; the numbering-to-plate mapping is not confirmed].

## 4. Documented arrest confirmation

| Samples | Published evidence | Gap |
|---|---|---|
| GSE162175 quiescent (0.5% FBS, d3–8, harvest d8) | Protocol only in GEO. The paper's quiescence imaging used a different setup (0.1% FBS, vector + 4OHT, day 6) [PAPER]. No per-sample proliferation assay is published for the sequenced samples. | Published evidence is protocol-level only. |
| GSE329184 rapamycin-treated (10 µM, 48 h from day 1; medium refreshed at 48 h; harvest day 7) | Selected in the initial setup for "cell cycle arrest with immediate proliferation after compound removal" [PAPER]. Day-7 Cell Painting shows a distinct rapamycin-dominated "quiescence-like" cluster [PAPER]. Condition-level live imaging only. | **Arrest at RNA collection is unconfirmed.** The methods say the medium was refreshed at 48 h; they do not say whether rapamycin was removed or replenished. *If* it was removed, the authors' own description implies proliferation could have resumed during the ~4 days before RNA collection [INFERENCE, conditional]. Rapamycin is also senomorphic (addendum 2026-09-29). |

## 5. Feasibility (agent interpretation)

- **GSE329184 currently has no confirmed arrest comparator.** Its rapamycin-treated arm cannot be used as a quiescent control until the timing question is answered. Its senescent and proliferating arms remain usable.
- **GSE162175 is the only candidate source of a senescent-vs-quiescent contrast**, with n = 4 quiescent samples from one cell line, replicate provenance unconfirmed and protocol-level published arrest evidence. That is thinner than the protocol assumed.
- **Open question for the dataset authors:** was rapamycin removed or replenished at the 48 h medium change, and were the rapamycin wells still non-proliferating at day 7?
- A separate review of existing signatures (SenFlag, Hernandez-Segura, CellAge, SenMayo) is under way. It may identify an existing readout or a better comparator dataset.
- Nothing here changes the hold: Run 3 waits for methodological feedback.
