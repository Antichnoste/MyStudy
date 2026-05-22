from scipy import stats
import numpy as np


def pearson_exp_gof(x4: np.ndarray, lam: float = 0.106, alpha: float = 0.05):
    n = len(x4)
    probs = np.linspace(0.0, 1.0, 6)
    bounds = stats.expon.ppf(probs, scale=1 / lam)
    bounds[0] = 0.0

    observed = np.zeros(5, dtype=int)
    for i in range(5):
        left, right = bounds[i], bounds[i + 1]
        if i < 4:
            observed[i] = np.sum((x4 >= left) & (x4 < right))
        else:
            observed[i] = np.sum(x4 >= left)

    expected = np.full(5, n / 5, dtype=float)
    chi2 = np.sum((observed - expected) ** 2 / expected)
    df = 4
    chi2_crit = stats.chi2.ppf(1 - alpha, df)
    p_value = 1 - stats.chi2.cdf(chi2, df)

    return chi2, p_value, df, chi2_crit
