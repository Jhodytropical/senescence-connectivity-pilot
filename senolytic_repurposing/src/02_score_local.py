"""Connectivity scoring against LINCS L1000 consensus drug signatures (Enrichr library, downloaded locally).
The SigCom LINCS data API was down on 2026-09-28 and Enrichr's API rate-limited us, so we run Fisher tests locally.

Per drug, four one-sided Fisher overlap tests:
  reversal: senescence-UP vs drug-DOWN, senescence-DOWN vs drug-UP
  mimicry:  senescence-UP vs drug-UP,   senescence-DOWN vs drug-DOWN
reversal_score = sum(-log10 p reversal) - sum(-log10 p mimicry)
sasp_score     = -log10 p(SenMayo vs drug-DOWN) - -log10 p(SenMayo vs drug-UP)"""
import json, math, re, pandas as pd
from scipy.stats import fisher_exact

def read_gmt(path):
    sets = {}
    for line in open(path):
        f = line.rstrip("\n").split("\t")
        sets[f[0]] = {g.split(",")[0] for g in f[2:] if g}
    return sets

lib = read_gmt("data/LINCS_L1000_Chem_Pert_Consensus_Sigs.gmt")
universe = set().union(*lib.values())
q = json.load(open("data/query_signature.json"))
Q = {k: set(q[k]) & universe for k in ("up", "down", "senmayo")}
print(f"{len(lib)} signatures, universe {len(universe)} genes; query in universe:",
      {k: len(v) for k, v in Q.items()})

drugs = {}
for term, genes in lib.items():
    m = re.match(r"^(.*)\s+(up|down)$", term, re.I)
    drugs.setdefault(m[1].strip(), {})[m[2].lower()] = genes

N = len(universe)
def nlp(query, gs):
    a = len(query & gs)
    p = fisher_exact([[a, len(gs) - a], [len(query) - a, N - len(gs) - len(query) + a]], alternative="greater")[1]
    return -math.log10(max(p, 1e-300)), a

rows = []
for d, s in drugs.items():
    U, D = s.get("up", set()), s.get("down", set())
    r1, n1 = nlp(Q["up"], D); r2, n2 = nlp(Q["down"], U)
    m1, _ = nlp(Q["up"], U); m2, _ = nlp(Q["down"], D)
    so, ns = nlp(Q["senmayo"], D); sn, _ = nlp(Q["senmayo"], U)
    rows.append({"drug": d, "reversal_score": r1 + r2 - m1 - m2, "sasp_score": so - sn,
                 "rev_upVSdown": r1, "rev_downVSup": r2, "mim_upVSup": m1, "mim_downVSdown": m2,
                 "n_sen_up_turned_off": n1, "n_sen_down_turned_on": n2, "n_sasp_turned_off": ns,
                 "sasp_genes_off": ";".join(sorted(Q["senmayo"] & D)),
                 "sen_up_genes_off": ";".join(sorted(Q["up"] & D))})
t = pd.DataFrame(rows).sort_values("reversal_score", ascending=False)
t.to_csv("results/drug_scores_all.csv", index=False)
print(f"{len(t)} drugs scored")
cols = ["drug", "reversal_score", "sasp_score", "n_sen_up_turned_off", "n_sen_down_turned_on", "n_sasp_turned_off"]
print("\nTOP REVERSERS\n", t.head(20)[cols].round(1).to_string(index=False))
print("\nTOP MIMICKERS (push cells toward senescence)\n", t.tail(10)[cols].round(1).to_string(index=False))
print("\nTOP SASP SUPPRESSORS\n", t.sort_values("sasp_score", ascending=False).head(20)[cols].round(1).to_string(index=False))
