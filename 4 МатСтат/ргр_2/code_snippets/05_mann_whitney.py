from scipy import stats
import numpy as np


def mann_whitney_test(x1: np.ndarray, x2: np.ndarray):
    u_stat, p_value = stats.mannwhitneyu(x1, x2, alternative="two-sided")
    return u_stat, p_value
