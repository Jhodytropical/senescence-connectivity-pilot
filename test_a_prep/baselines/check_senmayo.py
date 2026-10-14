"""Reproduce the SenMayo gene-count check: MSigDB SAUL_SEN_MAYO (B2) against the paper's Supplementary Data 1 (human sheet).

Run from the repository root after scripts/fetch_data.sh:
    .venv/bin/python test_a_prep/baselines/check_senmayo.py
Reads two third-party files that are fetched, never committed. Prints counts and the full set differences.
"""
import json
import openpyxl

msigdb = set(json.load(open("senolytic_repurposing/data/senmayo.json"))["SAUL_SEN_MAYO"]["geneSymbols"])
ws = openpyxl.load_workbook("test_a_prep/data/SenMayo_SuppData1_MOESM4.xlsx", read_only=True)["human"]
paper = {str(r[0]).strip() for r in list(ws.iter_rows(values_only=True))[1:] if r and r[0]}
print(f"MSigDB SAUL_SEN_MAYO: {len(msigdb)} distinct symbols")
print(f"Paper, Supplementary Data 1 (human): {len(paper)} distinct symbols")
print("In paper, not in MSigDB:", sorted(paper - msigdb))
print("In MSigDB, not in paper:", sorted(msigdb - paper))
