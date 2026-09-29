"""Connectivity search via Enrichr's LINCS L1000 consensus drug signatures (Maayan Lab).
(The SigCom LINCS data API was down on 2026-09-28; src/02_query_lincs.py is kept for when it returns.)

For every drug we test four overlaps:
  senescence-UP genes  vs drug-DOWN genes  -> reversal
  senescence-DOWN genes vs drug-UP genes   -> reversal
  senescence-UP genes  vs drug-UP genes    -> mimicry
  senescence-DOWN genes vs drug-DOWN genes -> mimicry
reversal_score = sum(-log10 p of reversal overlaps) - sum(-log10 p of mimicry overlaps)
SASP query: SenMayo genes vs drug-DOWN genes -> drugs that switch off the senescence secretome."""
import json, re, math, requests, pandas as pd
E = "https://maayanlab.cloud/Enrichr"
LIB = "LINCS_L1000_Chem_Pert_Consensus_Sigs"
q = json.load(open("data/query_signature.json"))

def enrich(genes, desc):
    r = requests.post(f"{E}/addList", files={"list": (None, "\n".join(genes)), "description": (None, desc)}, timeout=120)
    r.raise_for_status(); uid = r.json()["userListId"]
    r = requests.get(f"{E}/enrich", params={"userListId": uid, "backgroundType": LIB}, timeout=300)
    r.raise_for_status()
    rows = r.json()[LIB]
    df = pd.DataFrame([{"term": x[1], "p": x[2], "overlap": ";".join(x[5]), "n_overlap": len(x[5])} for x in rows])
    m = df.term.str.extract(r"^(.*)\s+(up|down)$", flags=re.I)
    df["drug"], df["direction"] = m[0].str.strip(), m[1].str.lower()
    return df

def score(df):
    return df.assign(s=-df.p.clip(lower=1e-300).map(math.log10))

up, down, sasp = (score(enrich(q[k], k)) for k in ("up", "down", "senmayo"))
print("example terms:", up.term.head(3).tolist())

def pick(df, d):
    return df[df.direction == d].set_index("drug")[["s", "n_overlap", "overlap"]]

t = pd.DataFrame({
    "rev_upVSdown": pick(up, "down").s, "rev_downVSup": pick(down, "up").s,
    "mim_upVSup": pick(up, "up").s, "mim_downVSdown": pick(down, "down").s,
    "sasp_off": pick(sasp, "down").s, "sasp_on": pick(sasp, "up").s,
}).fillna(0)
t["reversal_score"] = t.rev_upVSdown + t.rev_downVSup - t.mim_upVSup - t.mim_downVSdown
t["sasp_score"] = t.sasp_off - t.sasp_on
t["sasp_genes_off"] = pick(sasp, "down").overlap
t["sen_up_genes_off"] = pick(up, "down").overlap
t.index.name = "drug"
t.sort_values("reversal_score", ascending=False).to_csv("results/drug_scores_all.csv")
print(f"{len(t)} drugs scored")
print(t.sort_values("reversal_score", ascending=False).head(15)[["reversal_score", "sasp_score"]].round(1).to_string())
print(t.sort_values("sasp_score", ascending=False).head(15)[["reversal_score", "sasp_score"]].round(1).to_string())
