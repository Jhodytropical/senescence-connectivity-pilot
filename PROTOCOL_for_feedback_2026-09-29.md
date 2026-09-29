# Request for methodological feedback: a connectivity-mapping pilot that failed its own validation

**Not a result. I am asking whether the proposed next test is worth running, and what would make it sound.**

Jean Hyacinthe · jeanhyacinthe@gmail.com · independent, computational only, no lab · 2026-09-29

## What I did
Scored 5,425 LINCS L1000 **consensus** drug signatures against the CellAge senescence meta-signature (150 genes up / 150 down) and SenMayo, using one-sided Fisher overlap tests, to look for compounds whose expression effect opposes senescence.

## What happened
A follow-up validation, specified before scoring but **after** the first results were visible (disclosed — not a blind pre-registration), failed its own criteria:

| Test | Result |
|---|---|
| MDM2/CDK inhibitors on a second senescence gene set (Fridman, no shared genes) | AUC 0.53 / 0.60, Holm p ≥ 0.43 — no replication |
| Same, after regressing out a proliferation-arrest score | AUC 0.55 / 0.51, p = 1.0 — signal gone |
| Known senomorphics (mTOR, JAK, p38 inhibitors) on the SASP score | AUC 0.51, p = 1.0 |
| Known senolytics (BCL-2, HSP90, Na⁺/K⁺-ATPase) | no discrimination |

The reversal score correlates **−0.73** with plain proliferation arrest; the SASP score correlates **0.48** with a generic HALLMARK inflammatory-response score. An earlier, circular control-class result (classes chosen after seeing output, AUC 0.01) has been withdrawn. Rankings are stable across 32 scoring configurations, but stability is not validity.

**My reading: this pipeline did not demonstrate senescence specificity beyond proliferation arrest.** It is an informative negative about this design — consensus signatures, mostly from proliferating cancer lines, scored with set-overlap statistics — not a claim about connectivity mapping in general.

## What I am considering next, and where I would like to be corrected
Using GSE329184 (Tan et al., *npj Aging* 2026; NHDF/NHLF fibroblasts, 2 donors, ~230 RNA-seq samples: proliferating, rapamycin quiescence-like, bleomycin / palbociclib / late-passage senescence, ± navitoclax 0.1 and 1 µM), plus GSE162175 from a different lab for replication.

**Test A — a senescent-vs-*arrested* signature (feasible, not yet validated).** Build the query from senescent vs arrested cells rather than senescent vs proliferating, then re-run the L1000 screen and repeat the failed validations. In GSE329184 the arrest comparator is rapamycin, so a signature from it alone could separate senescence from *rapamycin's specific effects* rather than from arrest in general. Replication with a **different arrest mechanism** is therefore essential: GSE162175 (Wagner et al., *Nat Commun* 2026; IMR90, 4 replicates) has quiescence by **serum withdrawal** (GEO: 0.5% FBS, days 3–8). Caveats: I found no explicit arrest phenotyping of the sequenced quiescent samples (the paper's imaging arm used 0.1% FBS, so the conditions may differ), and palbociclib-induced senescence appears in both datasets, so palbociclib must be excluded from any inducer test built on them.

- Q1: Are rapamycin-induced and serum-withdrawal quiescence together an adequate pair of arrest comparators, or is a third mechanism (e.g. contact inhibition) needed before a shared senescence-vs-arrest signature means anything?
- Q2: Is scoring L1000 consensus signatures salvageable at all, or should this move to per-signature querying with cell-line, dose and time as covariates?

**Test B — selective senolysis vs general toxicity (paused).** I had planned to compare navitoclax in senescent vs matched non-senescent cells. **The currently identified measurements do not support a reliable test of selective senolysis versus general toxicity. We welcome advice on whether additional measurements or supplements make that comparison possible.** The main reason is the lack of an interpretable survival endpoint: there is no viability assay, and the proxy (nuclei count) rises after navitoclax, which the authors themselves read as "supportive of increased mitosis **or** apoptosis"; in one arm it does not shift at all. The readouts are on separate but layout-matched plates ("Technical triplicates were prepared for each assay"). That alone need not rule out a condition-level comparison, if the survival assay, replication and matching were adequate.

- Q3: Is there a dataset with drug-treated senescent and matched non-senescent cells and an **interpretable viability endpoint** (same wells, or properly matched parallel plates) alongside expression? That seems to be the binding constraint, not analysis method.
- Q4: Given that expression is measured only in surviving cells, what design actually distinguishes selective killing from a shift in the surviving population?

**Also noted:** the same paper reports SenMayo was only partially enriched in chemically induced senescence and not in late-passage cells, while the Hernandez-Segura in-vitro fibroblast signature matched. That is a **coverage** concern (limited sensitivity, or context dependence, in cultured fibroblasts), not by itself a specificity finding. Specificity would need a test of whether SenMayo also responds in non-senescent conditions such as ordinary inflammation. My pilot's SASP score correlated 0.48 with a generic inflammatory-response score, which hints at this but was not a designed specificity test.

## What I am asking
Not for collaboration or data. Just: **is Test A worth running, and is Test B answerable at all with public data?** Please assess the two questions separately: whether the arrest comparators and phenotyping support Test A, and whether any available survival endpoint and experimental matching support Test B. A recommendation not to proceed with either test would be useful and will be reflected in the write-up.

Everything is reproducible and the failed validations are in the repository, including the withdrawn circular result. Run 1 and the corrected report are frozen with checksums. No candidate list is being presented as validated, and no compound here is a recommendation for any use.
