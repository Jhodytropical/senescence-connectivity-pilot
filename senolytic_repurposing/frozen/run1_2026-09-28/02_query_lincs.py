"""Query SigCom LINCS (L1000 chemical perturbations) for drugs that reverse the senescence signature.
Query A: full CellAge signature (up + down) -> drugs whose effect is the opposite of senescence.
Query B: SenMayo SASP genes (up only) -> drugs that switch off the senescence secretome (senomorphics)."""
import json, requests, pandas as pd
API = "https://maayanlab.cloud/sigcom-lincs"
q = json.load(open("data/query_signature.json"))

def gene_ids(symbols):
    r = requests.post(f"{API}/metadata-api/entities/find", json={"filter": {
        "where": {"meta.symbol": {"inq": symbols}}, "fields": ["id", "meta.symbol"]}}, timeout=120)
    r.raise_for_status()
    return [e["id"] for e in r.json()]

def enrich(up, down=None, limit=1000):
    body = {"up_entities": up, "limit": limit, "database": "l1000_cp"}
    if down:
        body["down_entities"] = down
        url = f"{API}/data-api/api/v1/enrich/ranktwosided"
    else:
        body = {"entities": up, "limit": limit, "database": "l1000_cp"}
        url = f"{API}/data-api/api/v1/enrich/rank"
    r = requests.post(url, json=body, timeout=600); r.raise_for_status()
    return r.json()["results"]

def annotate(results):
    ids = [x["uuid"] for x in results]
    meta = {}
    for i in range(0, len(ids), 200):
        r = requests.post(f"{API}/metadata-api/signatures/find", json={"filter": {
            "where": {"id": {"inq": ids[i:i+200]}}}}, timeout=120); r.raise_for_status()
        meta.update({m["id"]: m["meta"] for m in r.json()})
    rows = []
    for x in results:
        m = meta.get(x["uuid"], {})
        rows.append({**{k: v for k, v in x.items() if not isinstance(v, (dict, list))},
                     "drug": m.get("pert_name"), "cell_line": m.get("cell_line"),
                     "dose": m.get("pert_dose"), "time": m.get("pert_time")})
    return pd.DataFrame(rows)

up_ids, down_ids = gene_ids(q["up"]), gene_ids(q["down"])
print(f"resolved {len(up_ids)}/{len(q['up'])} up, {len(down_ids)}/{len(q['down'])} down")
a = annotate(enrich(up_ids, down_ids)); a.to_csv("results/A_full_signature_raw.csv", index=False)
print("A:", a.shape, list(a.columns)); print(a.head(8).to_string())
sasp_ids = gene_ids(q["senmayo"])
b = annotate(enrich(sasp_ids)); b.to_csv("results/B_sasp_raw.csv", index=False)
print("B:", b.shape, list(b.columns)); print(b.head(8).to_string())
