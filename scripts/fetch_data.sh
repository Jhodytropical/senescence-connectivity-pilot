#!/usr/bin/env bash
# Re-download every input. Nothing here is redistributed in this repository.
set -euo pipefail
cd "$(dirname "$0")/../senolytic_repurposing/data"

# CellAge senescence signatures + DrugAge (Human Ageing Genomic Resources)
curl -sLO https://genomics.senescence.info/cells/cellSignatures.zip && unzip -oq cellSignatures.zip -d cellsig
curl -sL -o drugage.zip https://genomics.senescence.info/drugs/dataset.zip && unzip -oq drugage.zip -d drugage

# MSigDB gene sets
for G in FRIDMAN_SENESCENCE_UP FRIDMAN_SENESCENCE_DN HALLMARK_E2F_TARGETS HALLMARK_G2M_CHECKPOINT HALLMARK_INFLAMMATORY_RESPONSE; do
  curl -sL -o "$G.json" "https://www.gsea-msigdb.org/gsea/msigdb/human/download_geneset.jsp?geneSetName=$G&fileType=json"
done
curl -sL -o senmayo.json "https://www.gsea-msigdb.org/gsea/msigdb/human/download_geneset.jsp?geneSetName=SAUL_SEN_MAYO&fileType=json"

# LINCS L1000 consensus drug signatures (Enrichr library, Ma'ayan Lab)
curl -sL -o LINCS_L1000_Chem_Pert_Consensus_Sigs.gmt \
  "https://maayanlab.cloud/Enrichr/geneSetLibrary?mode=text&libraryName=LINCS_L1000_Chem_Pert_Consensus_Sigs"

# Broad Drug Repurposing Hub annotations (mechanism-of-action classes)
curl -sLO https://s3.amazonaws.com/data.clue.io/repurposing/downloads/repurposing_drugs_20200324.txt
mv repurposing_drugs_20200324.txt repurposing_drugs.txt

# Test A data preparation: GEO processed counts (structure checks only; see test_a_prep/)
mkdir -p ../../test_a_prep/data && cd ../../test_a_prep/data
curl -sLO https://ftp.ncbi.nlm.nih.gov/geo/series/GSE162nnn/GSE162175/suppl/GSE162175_Rawcounts.txt.gz
curl -sLO https://ftp.ncbi.nlm.nih.gov/geo/series/GSE329nnn/GSE329184/suppl/GSE329184_included_samples_counts.csv.gz
curl -sLO https://ftp.ncbi.nlm.nih.gov/geo/series/GSE307nnn/GSE307082/suppl/GSE307082_CellStates_count_matrix.txt.gz
# SenMayo paper, Supplementary Data 1 (Saul et al. 2022), for test_a_prep/baselines/check_senmayo.py
curl -sL -o SenMayo_SuppData1_MOESM4.xlsx "https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-022-32552-1/MediaObjects/41467_2022_32552_MOESM4_ESM.xlsx"
echo "done — now run scripts/verify_inputs.sh to compare against the files the pilot used"
