import numpy as np
import scipy.stats as stats

# Расчет метрик качества моделей (R^2, RMSE, Средняя ошибка аппроксимации)
tss = np.sum((y - np.mean(y))**2)

def calc_metrics(y_pred):
    rss = np.sum((y - y_pred)**2)
    r2 = 1 - rss / tss
    rmse = np.sqrt(rss / n)
    mask = y != 0
    a_err = np.mean(np.abs((y[mask] - y_pred[mask]) / y[mask])) * 100
    return rss, r2, rmse, a_err

# Вычисляем метрики для всех моделей
rss_lin, r2_lin, rmse_lin, a_lin_err = calc_metrics(y_pred_lin)
rss_quad, r2_quad, rmse_quad, a_quad_err = calc_metrics(y_pred_quad)
rss_pow, r2_pow, rmse_pow, a_pow_err = calc_metrics(y_pred_pow)

print("Сравнение моделей:")
print(f"Линейная:      R² = {r2_lin:.4f}, RMSE = {rmse_lin:.4f}, Ошибка A = {a_lin_err:.2f}%")
print(f"Квадратичная:  R² = {r2_quad:.4f}, RMSE = {rmse_quad:.4f}, Ошибка A = {a_quad_err:.2f}%")
print(f"Степенная:     R² = {r2_pow:.4f}, RMSE = {rmse_pow:.4f}, Ошибка A = {a_pow_err:.2f}%")

# Статистический анализ линейной модели
mean_x = np.mean(x)
S_xx = np.sum((x - mean_x)**2)
s2 = rss_lin / (n - 2)
s = np.sqrt(s2)

se_b = s / np.sqrt(S_xx)
se_a = s * np.sqrt(1/n + (mean_x**2) / S_xx)

t_crit = stats.t.ppf(0.975, n - 2)
ci_a = (a_lin - t_crit * se_a, a_lin + t_crit * se_a)
ci_b = (b_lin - t_crit * se_b, b_lin + t_crit * se_b)
t_stat_b = b_lin / se_b

print("\nСтатистика линейной модели:")
print(f"RSS = {rss_lin:.4f}")
print(f"Дисперсия (s²) = {s2:.4f}, s = {s:.4f}")
print(f"Дов. интервал a: ({ci_a[0]:.2f}; {ci_a[1]:.2f})")
print(f"Дов. интервал b: ({ci_b[0]:.4f}; {ci_b[1]:.4f})")
print(f"t-набл (для b) = {t_stat_b:.4f}, t-крит = {t_crit:.4f}")
