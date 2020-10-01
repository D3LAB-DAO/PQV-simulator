import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint


if __name__ == "__main__":
    with open("./log/simul-heatmap.txt", 'r') as f:
        lines = f.readlines()
        lines = [line.split('\t')[:-1] for line in lines]

    dict_PQV_vs_equal = dict()
    dict_PQV_vs_plain = dict()
    dict_PQV_vs_QV = dict()

    for line in lines:
        k = (int(line[0]), int(line[1]))
        dict_PQV_vs_equal[k] = float(line[2])
        dict_PQV_vs_plain[k] = float(line[3])
        dict_PQV_vs_QV[k] = float(line[4])

    dicts_ = [dict_PQV_vs_equal, dict_PQV_vs_plain, dict_PQV_vs_QV]
    names_ = ["PQV_vs_equal", "PQV_vs_plain", "PQV_vs_QV"]
    for dict_, name_ in zip(dicts_, names_):
        ser = pd.Series(list(dict_.values()),
                        index=pd.MultiIndex.from_tuples(dict_.keys()))
        df = ser.unstack().fillna(0)
        df.shape

        ax1 = sns.heatmap(df, cmap='GnBu', vmin=0, vmax=100)
        ax1.set_xlabel('Agents')
        ax1.set_ylabel('Policies')
        # plt.show()
        plt.savefig("./plots/" + name_ + '.png', format='png', dpi=300)
        plt.close()
