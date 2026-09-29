"""Validate the scoring against drugs already known to act on senescent cells, cross-check DrugAge, and rank candidates.
CORRECTION 2026-09-29: these lists were NOT fixed before seeing results — the inducer list was written after the mimicker output. See README + PREREGISTRATION_run2.md; Run 2 uses Hub MoA classes instead."""
import pandas as pd
from scipy.stats import mannwhitneyu

t = pd.read_csv("results/drug_scores_all.csv")
KNOWN = {
    "senolytic": ["Dasatinib", "Quercetin", "Fisetin", "Navitoclax", "ABT-737", "Piperlongumine", "Alvespimycin",
                  "Tanespimycin", "17-AAG", "Geldanamycin", "Ganetespib", "NVP-AUY922", "Luteolin", "Curcumin",
                  "Digoxin", "Ouabain", "Bufalin", "Proscillaridin", "Digitoxin", "Lanatoside-C", "Panobinostat",
                  "Azithromycin"],
    "senomorphic": ["Sirolimus", "Temsirolimus", "Everolimus", "Torin-1", "Torin-2", "Metformin", "Ruxolitinib",
                    "Resveratrol", "SB-203580", "Losmapimod", "Apigenin", "Kaempferol", "Simvastatin"],
    "senescence_inducer": ["Palbociclib", "Nutlin-3", "RG-7388", "SAR405838", "AMG-232", "Olaparib", "Bortezomib"],
}
t["known_class"] = ""
for cls, drugs in KNOWN.items():
    t.loc[t.drug.isin(drugs), "known_class"] = cls

lines = ["# Validation: do known drugs rank where biology says they should?\n",
         "AUC = chance a known drug outranks a random drug (0.5 = no signal, 1.0 = perfect).\n",
         "| Drug class | n | Score | AUC | p-value |", "|---|---|---|---|---|"]
for cls in KNOWN:
    k = t[t.known_class == cls]; rest = t[t.known_class != cls]
    for col in ("sasp_score", "reversal_score"):
        u, p = mannwhitneyu(k[col], rest[col], alternative="two-sided")
        lines.append(f"| {cls} | {len(k)} | {col} | {u / (len(k) * len(rest)):.2f} | {p:.2g} |")
open("results/validation.md", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))

# DrugAge: compounds that significantly extended average lifespan in any species
da = pd.read_csv("data/drugage/drugage.csv")
sig = da[da.avg_lifespan_significance.astype(str).str.upper() == "S"]
agg = sig.groupby(sig.compound_name.str.lower()).agg(
    drugage_species=("species", lambda s: "; ".join(sorted(set(s)))[:120]),
    drugage_best_lifespan_pct=("avg_lifespan_change_percent", "max"),
    drugage_mouse=("species", lambda s: any("Mus musculus" in x for x in s)))
t = t.merge(agg, left_on=t.drug.str.lower(), right_index=True, how="left").drop(columns="key_0", errors="ignore")
t["in_drugage"] = t.drugage_species.notna()

# Candidate ranking: strong SASP suppression, and not pushing cells toward senescence
t["pct_sasp"] = t.sasp_score.rank(pct=True); t["pct_rev"] = t.reversal_score.rank(pct=True)
t["candidate_score"] = 0.7 * t.pct_sasp + 0.3 * t.pct_rev
cand = t[(t.reversal_score >= 0) & (t.sasp_score > 0)].sort_values("candidate_score", ascending=False)
cols = ["drug", "candidate_score", "sasp_score", "reversal_score", "n_sasp_turned_off", "known_class",
        "in_drugage", "drugage_best_lifespan_pct", "drugage_mouse", "sasp_genes_off"]
cand[cols].to_csv("results/candidates_ranked.csv", index=False)
t.to_csv("results/drug_scores_all.csv", index=False)
print(f"\n{len(cand)} candidates; {int(cand.head(100).in_drugage.sum())} of top 100 already in DrugAge")
print(cand.head(40)[cols[:9]].round(2).to_string(index=False))
print("\nKnown drugs, rank among all 5425 by SASP score:")
t["sasp_rank"] = t.sasp_score.rank(ascending=False).astype(int)
print(t[t.known_class != ""].sort_values("sasp_rank")[["drug", "known_class", "sasp_rank", "sasp_score", "reversal_score"]].round(1).to_string(index=False))
