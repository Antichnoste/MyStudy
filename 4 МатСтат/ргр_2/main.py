import csv
from dataclasses import dataclass

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


ALPHA = 0.05
MU0_X3 = 75.24
LAMBDA_X4 = 0.106


@dataclass
class TTestResult:
    statistic: float
    p_value: float
    critical_value: float
    reject_h0: bool
    df: float


@dataclass
class ChiSquareResult:
    statistic: float
    p_value: float
    critical_value: float
    reject_h0: bool
    df: int
    bounds: np.ndarray
    observed: np.ndarray
    expected: np.ndarray


def read_columns(path: str) -> dict[str, np.ndarray]:
    columns = {"X1": [], "X2": [], "X3": [], "X4": []}
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            for key in columns:
                columns[key].append(float(row[key]))
    return {key: np.asarray(values, dtype=float) for key, values in columns.items()}

# Двухвыборочный тест Стьюдента для X1 и X2
def test_equal_means_student(x1: np.ndarray, x2: np.ndarray, alpha: float) -> TTestResult:
    statistic, p_value = stats.ttest_ind(x1, x2, equal_var=True, alternative="two-sided")
    n1, n2 = len(x1), len(x2)
    df = n1 + n2 - 2
    critical_value = stats.t.ppf(1 - alpha / 2, df)
    reject_h0 = abs(statistic) > critical_value
    return TTestResult(statistic, p_value, critical_value, reject_h0, float(df))

# Одновыборочный тест Стьюдента для X3
def test_mean_x3(x3: np.ndarray, mu0: float, alpha: float) -> TTestResult:
    statistic, p_value = stats.ttest_1samp(x3, popmean=mu0, alternative="two-sided")
    df = len(x3) - 1
    critical_value = stats.t.ppf(1 - alpha / 2, df)
    reject_h0 = abs(statistic) > critical_value
    return TTestResult(statistic, p_value, critical_value, reject_h0, float(df))


def test_mann_whitney(x1: np.ndarray, x2: np.ndarray) -> tuple[float, float]:
    statistic, p_value = stats.mannwhitneyu(x1, x2, alternative="two-sided")
    return float(statistic), float(p_value)


# Кртиерий Пиросона
def pearson_exp_gof(x4: np.ndarray, lam: float, alpha: float, intervals_count: int = 5) -> ChiSquareResult:
    n = len(x4)
    probs = np.linspace(0.0, 1.0, intervals_count + 1)
    bounds = stats.expon.ppf(probs, scale=1 / lam)
    bounds[0] = 0.0

    observed = np.zeros(intervals_count, dtype=int)
    for i in range(intervals_count):
        left = bounds[i]
        right = bounds[i + 1]
        if i < intervals_count - 1:
            observed[i] = np.sum((x4 >= left) & (x4 < right))
        else:
            observed[i] = np.sum(x4 >= left)

    expected = np.full(intervals_count, n / intervals_count, dtype=float)
    statistic = np.sum((observed - expected) ** 2 / expected)
    df = intervals_count - 1
    critical_value = stats.chi2.ppf(1 - alpha, df)
    p_value = 1 - stats.chi2.cdf(statistic, df)
    reject_h0 = statistic > critical_value

    return ChiSquareResult(statistic, p_value, critical_value, reject_h0, df, bounds, observed, expected)


def print_sample_stats(name: str, x: np.ndarray) -> None:
    print(f"{name}: n={len(x)}, mean={np.mean(x):.6f}, var={np.var(x, ddof=1):.6f}")


def main() -> None:
    data = read_columns("data.csv")
    x1, x2, x3, x4 = data["X1"], data["X2"], data["X3"], data["X4"]

    print("Исходные описательные статистики")
    print_sample_stats("X1", x1)
    print_sample_stats("X2", x2)
    print_sample_stats("X3", x3)
    print_sample_stats("X4", x4)

    print("\n1) Проверка H0: mu1 = mu2 (классический two-sample t-test Стьюдента, двусторонняя альтернатива)")
    res1 = test_equal_means_student(x1, x2, ALPHA)
    print(f"t = {res1.statistic:.6f}")
    print(f"df = {res1.df:.6f}")
    print(f"t_crit = ±{res1.critical_value:.6f}")
    print(f"p-value = {res1.p_value:.6f}")
    print("Решение:", "отклоняем H0" if res1.reject_h0 else "нет оснований отклонить H0")

    print(f"\n2) Проверка H0: mu = {MU0_X3} для X3 (one-sample t-test)")
    res2 = test_mean_x3(x3, MU0_X3, ALPHA)
    print(f"t = {res2.statistic:.6f}")
    print(f"df = {res2.df:.0f}")
    print(f"t_crit = ±{res2.critical_value:.6f}")
    print(f"p-value = {res2.p_value:.6f}")
    print("Решение:", "отклоняем H0" if res2.reject_h0 else "нет оснований отклонить H0")

    print("\n3) Непараметрическая проверка: Манн-Уитни для X1 и X2")
    u_stat, u_p = test_mann_whitney(x1, x2)
    print(f"U = {u_stat:.6f}")
    print(f"p-value = {u_p:.6f}")
    print("Решение:", "отклоняем H0" if u_p < ALPHA else "нет оснований отклонить H0")

    print(f"\n4) Проверка H0: X4 ~ Exp(lambda={LAMBDA_X4}) (критерий Пирсона)")
    res3 = pearson_exp_gof(x4, LAMBDA_X4, ALPHA, intervals_count=5)
    print(f"chi2 = {res3.statistic:.6f}")
    print(f"df = {res3.df}")
    print(f"chi2_crit = {res3.critical_value:.6f}")
    print(f"p-value = {res3.p_value:.6f}")
    print("Решение:", "отклоняем H0" if res3.reject_h0 else "нет оснований отклонить H0")

    print("\nИнтервалы для критерия Пирсона (равновероятные):")
    for i in range(len(res3.observed)):
        left = res3.bounds[i]
        right = res3.bounds[i + 1]
        right_text = f"{right:.6f}" if np.isfinite(right) else "+inf"
        print(
            f"{i + 1}: [{left:.6f}, {right_text}) | "
            f"n_obs={res3.observed[i]:2d}, n_exp={res3.expected[i]:.2f}"
        )

    # График: гистограмма X4 + экспоненциальная плотность
    x_min, x_max = float(x4.min()), float(x4.max())
    x_grid = np.linspace(0.0, max(x_max, x_min + 1e-6), 500)
    pdf = stats.expon.pdf(x_grid, scale=1 / LAMBDA_X4)

    plt.figure(figsize=(7, 4))
    plt.hist(x4, bins=5, density=True, alpha=0.4, color="gray", edgecolor="black", label="Гистограмма X4")
    plt.plot(x_grid, pdf, color="crimson", linewidth=2, label=f"Exp(λ={LAMBDA_X4})")
    plt.title("X4 и экспоненциальная плотность")
    plt.xlabel("x")
    plt.ylabel("Плотность")
    plt.legend()
    plt.tight_layout()
    plt.savefig("x4_exp_overlay.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    main()