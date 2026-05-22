import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv('data.csv', sep=',')
    x = df['x'].values
    y = df['y'].values
    n = len(x)

    b_lin, a_lin = np.polyfit(x, y, 1)
    y_pred_lin = a_lin + b_lin * x
    
    c_quad, b_quad, a_quad = np.polyfit(x, y, 2)
    y_pred_quad = a_quad + b_quad * x + c_quad * (x**2)
    
    b_pow, ln_a_pow = np.polyfit(np.log(x), np.log(y), 1)
    a_pow = np.exp(ln_a_pow)
    y_pred_pow = a_pow * (x**b_pow)

    tss = np.sum((y - np.mean(y))**2)

    def calc_metrics(y_pred):
        rss = np.sum((y - y_pred)**2)
        r2 = 1 - rss / tss
        rmse = np.sqrt(rss / n)
        mask = y != 0
        a_err = np.mean(np.abs((y[mask] - y_pred[mask]) / y[mask])) * 100
        return rss, r2, rmse, a_err

    rss_lin, r2_lin, rmse_lin, a_lin_err = calc_metrics(y_pred_lin)
    rss_quad, r2_quad, rmse_quad, a_quad_err = calc_metrics(y_pred_quad)
    rss_pow, r2_pow, rmse_pow, a_pow_err = calc_metrics(y_pred_pow)

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

    x_star = 1207.9904
    y_star_lin = a_lin + b_lin * x_star
    y_star_quad = a_quad + b_quad * x_star + c_quad * (x_star**2)
    y_star_pow = a_pow * (x_star**b_pow)

    print("=== ДАННЫЕ ===")
    print(f"n = {n}")
    print("\n[Уравнения моделей]")
    print(f"Линейная:      a = {a_lin:.4f}, b = {b_lin:.4f}")
    print(f"Квадратичная:  a = {a_quad:.4f}, b = {b_quad:.4f}, c = {c_quad:.6f}")
    print(f"Степенная:     ln(a) = {ln_a_pow:.4f}, a = {a_pow:.4f}, b = {b_pow:.4f}")
    
    print("\n[Сравнение моделей]")
    print(f"Линейная:      R^2 = {r2_lin:.4f}, RMSE = {rmse_lin:.4f}, Ошибка A = {a_lin_err:.2f}%")
    print(f"Квадратичная:  R^2 = {r2_quad:.4f}, RMSE = {rmse_quad:.4f}, Ошибка A = {a_quad_err:.2f}%")
    print(f"Степенная:     R^2 = {r2_pow:.4f}, RMSE = {rmse_pow:.4f}, Ошибка A = {a_pow_err:.2f}%")

    print("\n[Статистика линейной модели]")
    print(f"RSS = {rss_lin:.4f}")
    print(f"Дисперсия (s^2) = {s2:.4f}, s = {s:.4f}")
    print(f"Дов. интервал a: ({ci_a[0]:.4f}; {ci_a[1]:.4f})")
    print(f"Дов. интервал b: ({ci_b[0]:.4f}; {ci_b[1]:.4f})")
    print(f"t-набл (для b) = {t_stat_b:.4f}, t-крит = {t_crit:.4f}")

    print(f"\n[Прогноз для x* = {x_star}]")
    print(f"Линейная:     {y_star_lin:.4f}")
    print(f"Квадратичная: {y_star_quad:.4f}")
    print(f"Степенная:    {y_star_pow:.4f}")
    print("======================================")

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='gray', label='Фактические данные', alpha=0.7)
    
    x_plot = np.linspace(min(x), max(x), 200)
    plt.plot(x_plot, a_lin + b_lin * x_plot, label='Линейная', color='red')
    plt.plot(x_plot, a_quad + b_quad * x_plot + c_quad * x_plot**2, label='Квадратичная', color='blue')
    plt.plot(x_plot, a_pow * (x_plot**b_pow), label='Степенная', color='green')
    
    plt.xlabel('Скорость чтения, МБ/с (x)')
    plt.ylabel('Скорость записи, МБ/с (y)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.title('Диаграмма рассеяния и регрессионные модели')
    plt.tight_layout()
    plt.savefig('plot.png', dpi=300)
    print("График успешно сохранен в файл 'plot.png'.")

if __name__ == "__main__":
    main()