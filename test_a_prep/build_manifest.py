"""Test A data preparation: sample manifest + structural checks for GSE162175 and GSE329184.

Scope (2026-10-01, Jean): inventory and feasibility only. This script reads GEO sample
metadata and the *structure* of the public count files (columns, identifiers, library
sizes). It computes no group comparison, signature, score or drug ranking.

Inputs:  ../dataset_search/GSE*.gsm.txt (GEO SOFT sample records, fetched 2026-09-28)
         data/GSE162175_Rawcounts.txt.gz, data/GSE329184_included_samples_counts.csv.gz
Outputs: sample_manifest.csv, structure_checks.json
"""
import collections
import csv
import gzip
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
META = HERE.parent / "dataset_search"
DATA = HERE / "data"


def parse_soft(path):
    samples, cur = [], None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if line.startswith("^SAMPLE"):
            cur = collections.defaultdict(list)
            cur["acc"] = [line.split("=", 1)[1].strip()]
            samples.append(cur)
        elif cur is not None and line.startswith("!Sample_") and " = " in line:
            k, v = line[8:].split(" = ", 1)
            cur[k].append(v)
    return samples


def chars(s):
    return dict(c.split(": ", 1) for c in s["characteristics_ch1"])


def read_counts_structure(path, sep):
    with gzip.open(path, "rt") as fh:
        header = next(fh).rstrip("\n").split(sep)
        cols = header[1:]
        totals = [0] * len(cols)
        ids, non_int, rows = [], 0, 0
        for line in fh:
            parts = line.rstrip("\n").split(sep)
            ids.append(parts[0])
            rows += 1
            for i, v in enumerate(parts[1:]):
                try:
                    totals[i] += int(v)
                except ValueError:
                    non_int += 1
    id_kinds = collections.Counter(
        "ensembl_versioned" if re.fullmatch(r"ENSG\d{11}\.\d+", x)
        else "ensembl" if re.fullmatch(r"ENSG\d{11}", x)
        else "other" for x in ids)
    return {
        "columns": cols,
        "n_genes": rows,
        "gene_id_kinds": dict(id_kinds),
        "duplicate_gene_ids": rows - len(set(ids)),
        "non_integer_cells": non_int,
        "library_size": dict(zip(cols, totals)),
    }


rows = []

# ---------------- GSE162175 (Wagner et al., Nat Commun 2026; IMR90) ----------------
G1_ROLE = {
    "growing": ("proliferating_reference", ""),
    "quiescent": ("ARREST_COMPARATOR", "serum withdrawal 0.5% FBS d3-d8"),
    "doxorubicin": ("SENESCENT", ""),
    "etoposide": ("SENESCENT", ""),
    "irradiation": ("SENESCENT", ""),
    "4OHT": ("SENESCENT", "oncogene-induced (RAS); paired control = iRas_neg"),
    "palbociclib": ("EXCLUDE", "CDK4/6 inhibitor: arrest and senescence confounded (decision 2026-09-29)"),
}
G1_DOSE = {
    "doxorubicin": ("0.5 uM", "24 h"), "etoposide": ("50 uM", "48 h"),
    "palbociclib": ("1 uM", "continuous"), "irradiation": ("10 Gy", "single dose"),
    "4OHT": ("100 nM", "continuous"), "0.5percent FBS": ("0.5% FBS", "day 3 to day 8"),
    "DMSO": ("vehicle", "to day 8"),
}
g1 = parse_soft(META / "GSE162175.gsm.txt")
g1_struct = read_counts_structure(DATA / "GSE162175_Rawcounts.txt.gz", "\t")
for s in g1:
    c = chars(s)
    title = s["title"][0]
    treat = c["treatment"]
    key = c["cell state"] if c["cell state"] in ("growing", "quiescent") else treat
    if title.startswith("iRas_neg"):
        key = "growing"
    role, note = G1_ROLE[key]
    if title.startswith("iRas_neg"):
        note = "ER:RAS line, not induced; paired control for 4OHT arm"
    count_col = "IMR90_" + title if title.startswith("iRas") else title
    dose, dur = G1_DOSE.get(treat, ("", ""))
    arrest = ""
    if key == "quiescent":
        arrest = "published: protocol only (no per-sample proliferation assay published)"
    rows.append({
        "series": "GSE162175", "gsm": s["acc"][0], "title": title,
        "count_column": count_col if count_col in g1_struct["columns"] else "MISSING",
        "in_processed_counts": count_col in g1_struct["columns"],
        "cell_line": "IMR90 ER:RAS" if title.startswith("iRas") else "IMR90",
        "tissue": "fetal lung fibroblast", "donor": "IMR90 (single donor line)",
        "treatment": treat, "dose": dose, "duration": dur,
        "harvest": "day 8",
        "replicate": title.rsplit("_", 1)[1] + " (provenance unconfirmed: independent experiment vs technical)",
        "assay": "RNA-seq SE50, HiSeq 2500, hg19, Rsubread counts",
        "documented_arrest_confirmation": arrest,
        "proposed_role": role, "note": note,
    })

# ---------------- GSE329184 (Tan et al., npj Aging 2026; NHDF/NHLF) ----------------
g2 = parse_soft(META / "GSE329184.gsm.txt")
g2_struct = read_counts_structure(DATA / "GSE329184_included_samples_counts.csv.gz", ",")
for s in g2:
    title = s["title"][0]
    lib = s["description"][0].replace("Library name: ", "")
    parts = title.split(" - ")
    line_label = parts[-1].strip()
    cond = " - ".join(parts[1:-1])
    navito = "Navitoclax" in cond
    if cond.startswith("LP"):
        base, dose, dur = "late passage (P25+)", "", "replicative"
    elif "Rapamycin" in cond:
        base, dose, dur = "rapamycin", "10 uM", "48 h, then medium refreshed"
    elif "Bleomycin" in cond:
        base, dose, dur = "bleomycin", "5 ug/mL (series text: 5-20)", "48 h, then medium refreshed"
    elif "Nocodazole" in cond:
        base, dose, dur = "nocodazole", "50 ng/mL", "48 h, then medium refreshed"
    elif "Palbociclib" in cond:
        base, dose, dur = "palbociclib", "4.5 uM", "6 d, no medium change"
    elif "DMSO" in cond:
        base, dose, dur = "vehicle DMSO", "0.225%", "6 d"
    else:
        base, dose, dur = "untreated (NTC)", "", ""
    if navito:
        m = re.search(r"Navitoclax_([\d,]+)umol", cond)
        dose = (dose + "; " if dose else "") + f"navitoclax {m.group(1).replace(',', '.')} uM from day 5 (48 h)"

    if navito:
        role, note = "EXCLUDE", "navitoclax-treated: Test B material, not Test A"
    elif base in ("late passage (P25+)", "bleomycin"):
        role, note = "SENESCENT", ""
    elif base == "rapamycin":
        role, note = ("RAPAMYCIN_TREATED_ARREST_UNCONFIRMED",
                      "rapamycin-treated; arrest at RNA collection unconfirmed. Medium refreshed at 48 h: "
                      "the record does not say whether the drug was removed or replenished. IF removed, the "
                      "paper's initial setup reports proliferation resumes on removal; RNA taken day 7. "
                      "Rapamycin is also senomorphic (addendum 2026-09-29). Not a quiescent control.")
    elif base in ("untreated (NTC)", "vehicle DMSO"):
        role, note = "proliferating_reference", ""
    elif base == "nocodazole":
        role, note = "EXCLUDE", "authors: stayed proliferative in the repeat experiment"
    else:
        role, note = "EXCLUDE", "palbociclib: arrest and senescence confounded (decision 2026-09-29)"

    donor = {"NHDF1": "NHDF donor 1", "NHDF2": "NHDF donor 2", "NHLF1": "NHLF donor 1",
             "NHLF2": "NHLF donor 2", "NHDF1_2": "UNCLEAR (label NHDF1_2)",
             "NHLF_1and2": "UNCLEAR (label NHLF_1and2; donors pooled or mixed?)"}.get(line_label, "UNCLEAR")
    rows.append({
        "series": "GSE329184", "gsm": s["acc"][0], "title": title,
        "count_column": lib if lib in g2_struct["columns"] else "MISSING",
        "in_processed_counts": lib in g2_struct["columns"],
        "cell_line": line_label, "tissue": "dermal fibroblast" if "DF" in line_label else "lung fibroblast",
        "donor": donor, "treatment": base, "dose": dose, "duration": dur,
        "harvest": "day 7", "replicate": lib,
        "assay": "RNA-seq PE ~2x101, NovaSeq 6000, GRCh38/Ensembl 86, featureCounts; "
                 "well = 2 technical plates pooled at lysis",
        "documented_arrest_confirmation": (
            "none per sample; condition-level live imaging (nuclei counts) in paper"
            if role == "RAPAMYCIN_TREATED_ARREST_UNCONFIRMED" else ""),
        "proposed_role": role, "note": note,
    })

out = HERE / "sample_manifest.csv"
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

lib = {}
for series, struct in (("GSE162175", g1_struct), ("GSE329184", g2_struct)):
    sizes = sorted(struct["library_size"].values())
    lib[series] = {k: v for k, v in struct.items() if k not in ("columns", "library_size")}
    lib[series].update(n_count_columns=len(struct["columns"]), library_size_min=sizes[0],
                       library_size_median=sizes[len(sizes) // 2], library_size_max=sizes[-1])
    known = {r["count_column"] for r in rows if r["series"] == series}
    lib[series]["count_columns_without_gsm"] = sorted(set(struct["columns"]) - known)
lib["GSE329184"]["gsm_not_in_processed_counts"] = sorted(
    r["replicate"] for r in rows if r["series"] == "GSE329184" and not r["in_processed_counts"])
roles = collections.Counter((r["series"], r["proposed_role"]) for r in rows)
lib["roles"] = {f"{a} {b}": n for (a, b), n in sorted(roles.items())}
# Design balance only (counts of samples per cell), no expression involved.
bal = collections.Counter((r["cell_line"], r["treatment"]) for r in rows
                          if r["series"] == "GSE329184" and r["proposed_role"] != "EXCLUDE"
                          and r["in_processed_counts"])
lib["GSE329184_test_a_design_cells"] = {f"{a} | {b}": n for (a, b), n in sorted(bal.items())}
json.dump(lib, open(HERE / "structure_checks.json", "w"), indent=2)
print(json.dumps(lib, indent=2))
