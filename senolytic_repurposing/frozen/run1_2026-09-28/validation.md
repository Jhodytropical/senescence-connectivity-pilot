# Validation: do known drugs rank where biology says they should?

AUC = chance a known drug outranks a random drug (0.5 = no signal, 1.0 = perfect).

| Drug class | n | Score | AUC | p-value |
|---|---|---|---|---|
| senolytic | 22 | sasp_score | 0.53 | 0.66 |
| senolytic | 22 | reversal_score | 0.46 | 0.57 |
| senomorphic | 13 | sasp_score | 0.60 | 0.21 |
| senomorphic | 13 | reversal_score | 0.47 | 0.73 |
| senescence_inducer | 7 | sasp_score | 0.20 | 0.0068 |
| senescence_inducer | 7 | reversal_score | 0.01 | 7.6e-06 |
