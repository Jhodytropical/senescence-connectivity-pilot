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
echo "done"
