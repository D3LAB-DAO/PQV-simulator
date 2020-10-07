import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np


def draw_heatmap(filename, show=False):
    with open(filename, 'r') as f:
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

        if show:
            plt.show()
        else:
            plt.savefig("./plots/heatmap_" + name_ + '.png', format='png', dpi=300)
            plt.close()


def draw_graph(filename, show=False):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = [line.split('\t')[:-1] for line in lines]

    keys = []
    PQV_vs_equal, PQV_vs_plain, PQV_vs_QV = [], [], []

    for line in lines:
        keys.append(float(line[0]))
        PQV_vs_equal.append(float(line[1]))
        PQV_vs_plain.append(float(line[2]))
        PQV_vs_QV.append(float(line[3]))

    fig, ax1 = plt.subplots()

    lists_ = [PQV_vs_equal, PQV_vs_plain, PQV_vs_QV]
    names_ = ["PQV_vs_equal", "PQV_vs_plain", "PQV_vs_QV"]
    for list_, name_ in zip(lists_, names_):
        ax1.plot(keys, list_, label=name_)

    ax1.set_xlabel('Exponents')
    ax1.set_ylabel('Similarities')
    ax1.set_xlim((keys[0], keys[-1]))
    ax1.set_ylim((0, 100.))

    plt.legend(
        loc='lower center',
        bbox_to_anchor=(0.5, 1.00),
        ncol=3
    )

    if show:
        plt.show()
    else:
        plt.savefig("./plots/graph.png", format='png', dpi=300)
        plt.close()


def get_medium_graph(file_name, input_path='./log', output_path='./log'):
    path_s = os.listdir(input_path)
    num_dirs = 0

    res = dict()

    for path_ in path_s:
        if os.path.isdir(input_path + '/' + path_):
            num_dirs += 1

            with open(input_path + '/' + path_ + file_name, 'r') as f:
                lines = f.readlines()
                lines = [line.split('\t')[:-1] for line in lines]

            for line in lines:
                key = float(line[0])
                values = np.array([float(line[1]), float(line[2]), float(line[3])])
                if key in res:
                    # res[key] += values  # Avg.
                    res[key] = np.append(res[key], [values], axis=0)  # Median.
                else:
                    # res[key] = values  # Avg.
                    res[key] = np.array([values])  # Median.

    for k, v in res.items():
        # res[k] = list(v / num_dirs)  # Avg.
        res[k] = np.median(res[k], axis=0)  # Median.

    with open(input_path + '/' + file_name, 'w') as f:
        for k, v in res.items():
            f.write(str(k) + '\t' + '\t'.join([str(s) for s in v]) + '\t')
            f.write('\n')


def get_medium_heatmap(file_name, input_path='./log', output_path='./log'):
    path_s = os.listdir(input_path)
    num_dirs = 0

    res = dict()

    for path_ in path_s:
        if os.path.isdir(input_path + '/' + path_):
            num_dirs += 1

            with open(input_path + '/' + path_ + file_name, 'r') as f:
                lines = f.readlines()
                lines = [line.split('\t')[:-1] for line in lines]

            for line in lines:
                key = (int(line[0]), int(line[1]))
                values = np.array([float(line[2]), float(line[3]), float(line[4])])
                if key in res:
                    # res[key] += values  # Avg.
                    res[key] = np.append(res[key], [values], axis=0)  # Median.
                else:
                    # res[key] = values  # Avg.
                    res[key] = np.array([values])  # Median.

    for k, v in res.items():
        # res[k] = list(v / num_dirs)  # Avg.
        res[k] = np.median(res[k], axis=0)  # Median.

    with open(input_path + '/' + file_name, 'w') as f:
        for k, v in res.items():
            f.write('\t'.join([str(s) for s in k]) + '\t' + '\t'.join([str(s) for s in v]) + '\t')
            f.write('\n')


if __name__ == "__main__":
    get_medium_graph("/simul-power.txt")
    draw_graph("./log/simul-power.txt", show=False)

    get_medium_heatmap("/simul-heatmap.txt")
    draw_heatmap("./log/simul-heatmap.txt", show=False)
