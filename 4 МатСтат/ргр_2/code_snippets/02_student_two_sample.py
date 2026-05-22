from scipy import stats
import numpy as np


def test_equal_means_student(x1: np.ndarray, x2: np.ndarray, alpha: float = 0.05):
    # Классический двухвыборочный t-критерий Стьюдента (equal_var=True)
    t_stat, p_value = stats.ttest_ind(x1, x2, equal_var=True, alternative="two-sided")

    n1, n2 = len(x1), len(x2)
    s1_sq = np.var(x1, ddof=1)
    s2_sq = np.var(x2, ddof=1)
    sp_sq = ((n1 - 1) * s1_sq + (n2 - 1) * s2_sq) / (n1 + n2 - 2)

    df = n1 + n2 - 2
    t_crit = stats.t.ppf(1 - alpha / 2, df)

    return t_stat, p_value, sp_sq, df, t_crit