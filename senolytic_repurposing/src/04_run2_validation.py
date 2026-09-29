"""Run 2 — validation, implemented exactly as PREREGISTRATION_run2.md (sha256 7aa761a2…). Run 1 frozen files are read-only inputs.
One-sided Fisher (greater) is computed as the hypergeometric survival function (identical p-values, vectorised)."""
import json, re, itertools, numpy as np, pandas as pd
from scipy.stats import hypergeom, mannwhitneyu, spearmanr
rng = np.random.default_rng(20260929)
OUT = "results/run2"; import os; os.makedirs(OUT, exist_ok=True)

# ---------- library ----------
lib = {}
for line in open("data/LINCS_L1000_Chem_Pert_Consensus_Sigs.gmt"):
    f = line.rstrip("\n").split("\t"); m = re.match(r"^(.*)\s+(up|down)$", f[0], re.I)
    lib.setdefault(m[1].strip(), {})[m[2].lower()] = {g for g in f[2:] if g}
drugs = sorted(lib); UNI = set().union(*(s for d in lib.values() for s in d.values())); NU = len(UNI)
UP = [lib[d].get("up", set()) for d in drugs]; DN = [lib[d].get("down", set()) for d in drugs]

def nlp(q, sets):
    q = q & UNI; a = np.array([len(q & s) for s in sets]); K = np.array([len(s) for s in sets])
    return -np.log10(np.clip(hypergeom.sf(a - 1, NU, K, len(q)), 1e-300, 1)), a / max(len(q), 1)

gs = lambda n: set(json.load(open(f"data/{n}.json"))[n]["geneSymbols"])
cell = pd.read_csv("data/cellsig/signatures1.csv", sep=";"); cell["p_value"] = pd.to_numeric(cell.p_value, errors="coerce")
def cellage_query(N, exclude=frozenset()):
    c = cell[~cell.gene_symbol.isin(exclude)]
    return (set(c[c.ovevrexp == 1].nsmallest(N, "p_value").gene_symbol), set(c[c.underexp == 1].nsmallest(N, "p_value").gene_symbol))
SENMAYO = set(json.load(open("data/query_signature.json"))["senmayo"])
PROLIF = gs("HALLMARK_E2F_TARGETS") | gs("HALLMARK_G2M_CHECKPOINT")
INFLAM = gs("HALLMARK_INFLAMMATORY_RESPONSE")

def reversal(up, dn, stat=0):
    return nlp(up, DN)[stat] + nlp(dn, UP)[stat] - nlp(up, UP)[stat] - nlp(dn, DN)[stat]
def signed(q, stat=0):  # positive = drug switches the gene set OFF
    return nlp(q, DN)[stat] - nlp(q, UP)[stat]

# ---------- mechanism classes from the Repurposing Hub ----------
norm = lambda s: re.sub(r"[^a-z0-9]", "", str(s).lower())
hub = pd.read_csv("data/repurposing_drugs.txt", sep="\t", comment="!")
moa = {norm(r.pert_iname): set(str(r.moa).split("|")) for r in hub.itertuples() if str(r.moa) != "nan"}
D = pd.DataFrame({"drug": drugs}); D["moa"] = [moa.get(norm(d), set()) for d in drugs]
print(f"Hub MoA matched for {sum(bool(m) for m in D.moa)}/{len(D)} library drugs")
CLASSES = {"MDM inhibitor": ["MDM inhibitor"], "CDK inhibitor": ["CDK inhibitor"],
           "tubulin (comparator)": ["tubulin polymerization inhibitor"],
           "senolytic": ["BCL inhibitor", "HSP inhibitor", "Na/K-ATPase inhibitor"],
           "senomorphic": ["mTOR inhibitor", "JAK inhibitor", "p38 MAPK inhibitor"],
           "mTOR inhibitor": ["mTOR inhibitor"], "JAK inhibitor": ["JAK inhibitor"], "p38 MAPK inhibitor": ["p38 MAPK inhibitor"],
           "EXPL glucocorticoid": ["glucocorticoid receptor agonist"], "EXPL MEK": ["MEK inhibitor"], "EXPL SYK": ["SYK inhibitor"],
           "EXPL BTK": ["Bruton's tyrosine kinase (BTK) inhibitor"], "EXPL PI3K": ["PI3K inhibitor"], "EXPL HMGCR": ["HMGCR inhibitor"]}
member = {c: D.moa.map(lambda m, L=L: bool(m & set(L))).values for c, L in CLASSES.items()}

def auc(score, mask):
    k, r = score[mask], score[~mask]
    if len(k) < 2: return np.nan, np.nan, np.nan, np.nan
    u, p = mannwhitneyu(k, r, alternative="two-sided"); a = u / (len(k) * len(r))
    rr = np.sort(r); bs = []
    for _ in range(2000):
        kb = rng.choice(k, len(k)); bs.append((np.searchsorted(rr, kb, "left") + np.searchsorted(rr, kb, "right")).sum() / 2 / (len(kb) * len(rr)))
    return a, p, *np.percentile(bs, [2.5, 97.5])

# ---------- scores ----------
run1 = pd.read_csv("frozen/run1_2026-09-28/drug_scores_all.csv").set_index("drug").reindex(drugs)
F = (gs("FRIDMAN_SENESCENCE_UP") - set(cell.gene_symbol)) & UNI
S = pd.DataFrame(index=drugs)
S["T1_fridman_indep_senlike"] = -signed(F)                       # higher = more senescence-like
up_pf, dn_pf = cellage_query(150, exclude=PROLIF)
S["T2_reversal_prolif_free"] = reversal(up_pf, dn_pf)
S["prolif_arrest"] = nlp(PROLIF, DN)[0]
X = np.c_[np.ones(len(S)), S.prolif_arrest]; y = run1.reversal_score.values
S["T2_reversal_residualised"] = y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
S["run1_reversal"] = y; S["run1_sasp"] = run1.sasp_score.values
S["T3_inflam_comparator"] = signed(INFLAM)
print(f"T1 query: {len(F)} Fridman genes, none in CellAge. T2: {len(up_pf)} up / {len(dn_pf)} down after removing {len(PROLIF)} E2F/G2M genes")
print("corr(run1 reversal, prolif_arrest) = %.2f" % np.corrcoef(y, S.prolif_arrest)[0, 1])

rows = []
for col in S.columns:
    for c in CLASSES:
        a, p, lo, hi = auc(S[col].values, member[c])
        rows.append({"score": col, "class": c, "n": int(member[c].sum()), "AUC": a, "CI_lo": lo, "CI_hi": hi, "p": p})
R = pd.DataFrame(rows)
FAMILY = [("T1_fridman_indep_senlike", "MDM inhibitor"), ("T1_fridman_indep_senlike", "CDK inhibitor"),
          ("T2_reversal_prolif_free", "MDM inhibitor"), ("T2_reversal_prolif_free", "CDK inhibitor"),
          ("T2_reversal_residualised", "MDM inhibitor"), ("T2_reversal_residualised", "CDK inhibitor"),
          ("run1_sasp", "senomorphic")]
fam = R.set_index(["score", "class"]).loc[FAMILY].reset_index()
o = np.argsort(fam.p.values); m = len(fam); adj = np.empty(m); run = 0
for i, j in enumerate(o): run = max(run, min(1, (m - i) * fam.p.values[j])); adj[j] = run
fam["p_holm"] = adj
R.to_csv(f"{OUT}/class_tests_all.csv", index=False); fam.to_csv(f"{OUT}/confirmatory_holm.csv", index=False)
pd.set_option("display.width", 200)
print("\nCONFIRMATORY (Holm across 7)\n", fam.round(3).to_string(index=False))
show = ["MDM inhibitor", "CDK inhibitor", "tubulin (comparator)", "senolytic", "senomorphic", "mTOR inhibitor", "JAK inhibitor", "p38 MAPK inhibitor"]
print("\nALL CLASSES x SCORES (AUC)\n", R.pivot(index="class", columns="score", values="AUC").round(2).to_string())
print("\nn per class:", {c: int(member[c].sum()) for c in CLASSES})

# ---------- T5 sensitivity ----------
NAMED = ["Rilmenidine", "Y-27632", "PD-98059", "Fostamatinib", "AS-605240", "Thalidomide", "Ibrutinib", "Ponatinib",
         "Lovastatin", "Simvastatin", "Metformin", "Dexamethasone", "Hydrocortisone"]
sasp_stat = {0: signed(SENMAYO, 0), 1: signed(SENMAYO, 1)}
ranks, cfgs, base = {}, [], None
for N, st in itertools.product([50, 100, 150, 250], [0, 1]):
    u, d = cellage_query(N); rev = reversal(u, d, st); sa = sasp_stat[st]
    for w in [0.5, 0.7, 0.9, 1.0]:
        cs = w * pd.Series(sa).rank(pct=True).values + (1 - w) * pd.Series(rev).rank(pct=True).values
        filt = np.where((rev >= 0) & (sa > 0), cs, -np.inf)
        rk = pd.Series(filt, index=drugs).rank(ascending=False, method="min")
        key = f"N{N}_w{w}_{'fisher' if st == 0 else 'fraction'}"; ranks[key] = rk; cfgs.append((key, cs))
        if key == "N150_w0.7_fisher": base = (rk, cs)
brk, bcs = base
frozen_top = pd.read_csv("frozen/run1_2026-09-28/candidates_ranked.csv").drug.head(50).tolist()
assert brk.nsmallest(50).index.tolist() == frozen_top or set(brk.nsmallest(50).index) == set(frozen_top), "baseline does not reproduce Run 1"
print("\nBaseline config reproduces frozen Run 1 top 50: OK")
sens = pd.DataFrame([{"config": k, "spearman_vs_run1": spearmanr(cs, bcs)[0],
                      "top50_jaccard": len(set(ranks[k].nsmallest(50).index) & set(brk.nsmallest(50).index)) / len(set(ranks[k].nsmallest(50).index) | set(brk.nsmallest(50).index))}
                     for k, cs in cfgs])
sens.to_csv(f"{OUT}/sensitivity_configs.csv", index=False)
print(sens.describe().round(2).to_string())
RK = pd.DataFrame(ranks); top5 = len(drugs) * 0.05
rob = pd.DataFrame({"frac_configs_top5pct": (RK <= top5).mean(axis=1), "median_rank": RK.median(axis=1),
                    "best_rank": RK.min(axis=1), "worst_rank": RK.max(axis=1)})
rob["robust"] = rob.frac_configs_top5pct >= 0.8
rob["moa"] = ["|".join(sorted(m)) for m in D.moa]
rob.sort_values("median_rank").to_csv(f"{OUT}/candidate_robustness.csv")
print(f"\nNamed Run 1 candidates (top 5% = rank <= {top5:.0f} of {len(drugs)}; {len(cfgs)} configs)")
print(rob.loc[NAMED].round(2).to_string())
r = rob[rob.robust].sort_values("median_rank")
print(f"\n{len(r)} drugs robust (top 5% in >=80% of configs). Collapsed by MoA:")
g = r.assign(moa=r.moa.replace("", "(no Hub annotation)")).groupby("moa").apply(lambda x: pd.Series({"n": len(x), "drugs": ", ".join(x.index[:6])}), include_groups=False).sort_values("n", ascending=False)
g.to_csv(f"{OUT}/robust_by_moa.csv"); print(g.head(30).to_string())
