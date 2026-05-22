from scipy import stats
import numpy as np


def test_mean_x3(x3: np.ndarray, mu0: float = 75.24, alpha: float = 0.05):
    t_stat, p_value = stats.ttest_1samp(x3, popmean=mu0, alternative="two-sided")
    df = len(x3) - 1
    t_crit = stats.t.ppf(1 - alpha / 2, df)

    return t_stat, p_value, df, t_crit