"""Read-only GEO search: drug-treated senescent human cells with proliferating/quiescent controls."""
import requests, time, json
E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
QUERIES = {
 "senescent+quiescent+treatment": '(senescen*[All Fields]) AND (quiescen*[All Fields]) AND (treat*[All Fields] OR drug[All Fields] OR compound[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type]',
 "senolytic/senomorphic expression": '(senolytic*[All Fields] OR senomorphic*[All Fields] OR senotherap*[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type]',
 "senescent+proliferating+drug screen": '(senescen*[All Fields]) AND (proliferating[All Fields]) AND (screen*[All Fields] OR "drug treatment"[All Fields]) AND "Homo sapiens"[Organism] AND gse[Entry Type]',
}
out = {}
for name, q in QUERIES.items():
    r = requests.get(f"{E}/esearch.fcgi", params={"db": "gds", "term": q, "retmax": 200, "retmode": "json"}, timeout=60).json()
    ids = r["esearchresult"]["idlist"]; time.sleep(0.4)
    recs = []
    for i in range(0, len(ids), 100):
        s = requests.get(f"{E}/esummary.fcgi", params={"db": "gds", "id": ",".join(ids[i:i+100]), "retmode": "json"}, timeout=60).json()["result"]
        recs += [{"gse": "GSE" + s[k]["gse"], "title": s[k]["title"], "n": s[k]["n_samples"], "type": s[k]["gdstype"],
                  "summary": s[k]["summary"][:600]} for k in s.get("uids", [])]
        time.sleep(0.4)
    out[name] = recs
    print(f"{name}: {r['esearchresult']['count']} hits")
json.dump(out, open("dataset_search/geo_hits.json", "w"), indent=1)
