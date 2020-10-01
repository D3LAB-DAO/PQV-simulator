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

exponent  : Graph : `seq 1.0 0.5 3.1  # 3.0`

TODO

<!--
txWindow  : Graph : `seq 10 10 100` [%]

TODO
-->

### Similarity among equal, plain and QV versus PQV (2)

Using the best hyperparameters from simulation 1 (Grid Search) .

* nPolicies : `seq 2 1 16`
* nAgents   : `seq 30 30 300`

<!--Heatmap-->
TODO
