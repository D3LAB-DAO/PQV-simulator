# PQV-simulator
Probabilistic Quadratic Voting Simulator.

# Run
```
$ sh simul-1.sh [--option=value, ...]
$ sh simul-2.sh [--option=value, ...]
```

# Visualization

```
$ python visualization.py
```

### Pareto dist. of ballots

![](./plots/pareto.png)

### Similarity among equal, plain and QV versus PQV (1)

* exponent  : `seq 1.0 0.5 3.05`  # 3.0

![](./plots/graph.png)

<!--
txWindow    : Graph : `seq 10 10 100` [%]
-->

### Similarity among equal, plain and QV versus PQV (2)

Using the best hyperparameters from simulation 1 (Grid Search) .

* nPolicies : `seq 2 1 16`
* nAgents   : `seq 30 30 300`

![](./plots/heatmap_PQV_vs_equal.png)
![](./plots/heatmap_PQV_vs_plain.png)
![](./plots/heatmap_PQV_vs_QV.png)
