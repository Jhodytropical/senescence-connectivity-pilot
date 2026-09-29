"""Build the senescence query signature from the CellAge meta-analysis (Chatsirisupachai et al. 2019)."""
import json, pandas as pd
N = 150  # genes per direction, a typical size for connectivity queries
sig = pd.read_csv("data/cellsig/signatures1.csv", sep=";")
sig["p_value"] = pd.to_numeric(sig["p_value"], errors="coerce")
up = sig[sig.ovevrexp == 1].nsmallest(N, "p_value").gene_symbol.tolist()
down = sig[sig.underexp == 1].nsmallest(N, "p_value").gene_symbol.tolist()
senmayo = json.load(open("data/senmayo.json"))["SAUL_SEN_MAYO"]["geneSymbols"]
json.dump({"up": up, "down": down, "senmayo": senmayo}, open("data/query_signature.json", "w"), indent=1)
print(f"CellAge genes: {len(sig)} total, {int(sig.ovevrexp.sum())} up, {int(sig.underexp.sum())} down")
print(f"Query: {len(up)} up, {len(down)} down; SenMayo: {len(senmayo)} genes")
print("Top up:", up[:10]); print("Top down:", down[:10])
