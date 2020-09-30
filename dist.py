import numpy as np


def pareto(size, alpha=1.16, lower=1., upper=None):
    s = np.random.pareto(alpha, size) + lower
    if upper != None:
        s = s[s < upper]  # kill outliers
    return s


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from math import floor

    totalBallots = 100000

    a = 1.16
    m = 1.
    size = 300
    ps = pareto(size, alpha=a, lower=m)
    # print(np.mean(s))
    # print(np.max(s))
    # print(np.min(s))
    # print(np.count_nonzero(s < 2.))

    ps = [floor(p * (totalBallots / sum(ps))) for p in ps]
    ps[-1] = totalBallots - sum(ps[:-1])
    ps = np.array(ps)
    ps = ps[ps < 1000.]  # xlim

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Ballots')
    ax1.set_ylabel('Voters')

    count, bins, ignored = ax1.hist(ps, 100)
    fit = a * m**a / bins**(a + 1)
    ax1.plot(bins, max(count) * fit / max(fit), linewidth=2, color='r')
    plt.show()
