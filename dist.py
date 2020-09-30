import numpy as np


def pareto(size, alpha=1.16, lower=1.):
    s = np.random.pareto(alpha, size) + lower
    return s


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    a = 1.16
    m = 1.
    s = pareto(1000, alpha=a, lower=m)

    print(np.mean(s))
    print(np.max(s))
    print(np.min(s))
    # print(np.count_nonzero(s < 2.))

    count, bins, ignored = plt.hist(s, 100)
    fit = a * m**a / bins**(a + 1)
    plt.plot(bins, max(count) * fit / max(fit), linewidth=2, color='r')
    plt.show()
