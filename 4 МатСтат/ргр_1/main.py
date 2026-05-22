import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.cluster import KMeans
import os

os.makedirs("plots", exist_ok=True)

df = pd.read_csv("data.csv")
n = len(df)
alpha = 0.05
z_val = stats.norm.ppf(1 - alpha/2)

def sturges_rule(n):
    return int(1 + np.floor(np.log2(n)))

def freedman_diaconis_bins(data):
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    if iqr == 0:
        return sturges_rule(len(data))
    h_fd = 2 * iqr * (len(data) ** (-1/3))
    if h_fd <= 0:
        return sturges_rule(len(data))
    return max(1, int(np.ceil((np.max(data) - np.min(data)) / h_fd)))

def fit_distribution(data, dist_guess, mean, std_biased):
    if dist_guess == 'Normal':
        loc = mean
        scale = std_biased
        pdf = lambda x: stats.norm.pdf(x, loc=loc, scale=scale)
        cdf = lambda x: stats.norm.cdf(x, loc=loc, scale=scale)
        params = {'a': loc, 'sigma2': scale**2}
    elif dist_guess == 'Uniform':
        a_mmp = np.min(data)
        b_mmp = np.max(data)
        scale = b_mmp - a_mmp
        pdf = lambda x: stats.uniform.pdf(x, loc=a_mmp, scale=scale)
        cdf = lambda x: stats.uniform.cdf(x, loc=a_mmp, scale=scale)
        params = {'a': a_mmp, 'b': b_mmp}
    else:
        c_mmp = np.min(data)
        lam_mmp = 1 / (mean - c_mmp)
        pdf = lambda x: stats.expon.pdf(x, loc=c_mmp, scale=1/lam_mmp)
        cdf = lambda x: stats.expon.cdf(x, loc=c_mmp, scale=1/lam_mmp)
        params = {'c': c_mmp, 'lambda': lam_mmp}

    return params, pdf, cdf

def compute_mm_params(data, dist_guess, mean, var_biased, std_biased):
    if dist_guess == 'Normal':
        return {'a': mean, 'sigma2': var_biased}
    if dist_guess == 'Uniform':
        return {
            'a': mean - np.sqrt(3 * var_biased),
            'b': mean + np.sqrt(3 * var_biased),
        }
    lam_mm = 1 / std_biased
    return {
        'c': mean - 1 / lam_mm,
        'lambda': lam_mm,
    }

def density_from_params(x, dist_guess, params):
    if dist_guess == 'Normal':
        return stats.norm.pdf(x, loc=params['a'], scale=np.sqrt(params['sigma2']))
    if dist_guess == 'Uniform':
        return stats.uniform.pdf(x, loc=params['a'], scale=params['b'] - params['a'])
    return stats.expon.pdf(x, loc=params['c'], scale=1 / params['lambda'])

def plot_density_mm_mle(col_name, data, dist_guess, mm_params, mle_params):
    data_min, data_max = np.min(data), np.max(data)
    span = max(data_max - data_min, 1e-6)
    x_grid = np.linspace(data_min - 0.05 * span, data_max + 0.05 * span, 600)

    plt.style.use('ggplot')
    plt.figure(figsize=(9, 4))
    plt.hist(data, bins=sturges_rule(len(data)), density=True, alpha=0.25,
             color='gray', edgecolor='black', label='Эмпирическая плотность')
    plt.plot(x_grid, density_from_params(x_grid, dist_guess, mm_params),
             color='royalblue', linewidth=2, label='Плотность (ММ)')
    plt.plot(x_grid, density_from_params(x_grid, dist_guess, mle_params),
             color='crimson', linewidth=2, linestyle='--', label='Плотность (ММП)')
    plt.title(f'{col_name}: сравнение плотностей ММ и ММП')
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(f'plots/{col_name}_density_mm_mle.png', dpi=160)
    plt.close()

def plot_histogram_comparison(col_name, data, dist_guess, pdf):
    bins_sturges = sturges_rule(len(data))
    std_biased = np.std(data, ddof=0)
    h_scott = 3.5 * std_biased * (len(data) ** (-1/3))
    bins_scott = max(1, int(np.ceil((np.max(data) - np.min(data)) / h_scott))) if h_scott > 0 else bins_sturges
    bins_fd = freedman_diaconis_bins(data)

    methods = [
        ('Стерджес', bins_sturges),
        ('Скотт', bins_scott),
        ('Фридман-Диаконис', bins_fd),
    ]

    x_grid = np.linspace(np.min(data), np.max(data), 400)
    plt.style.use('ggplot')
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle(f'Сравнение правил разбиения гистограммы для {col_name}', fontsize=12)

    for ax, (label, bins_num) in zip(axes, methods):
        ax.hist(data, bins=bins_num, density=True, alpha=0.6, color='royalblue', edgecolor='black')
        ax.plot(x_grid, pdf(x_grid), color='red', linewidth=1.5, label='Теорет. плотность (ММП)')
        ax.set_title(f'{label} (bins={bins_num})', fontsize=10)
        ax.legend(fontsize=7, loc='upper right')

    plt.tight_layout()
    plt.savefig(f'plots/{col_name}_hist_compare.png', dpi=160)
    plt.close()

def plot_variation_and_cdf(col_name, data, cdf):
    x_sorted = np.sort(data)
    ecdf_y = np.arange(1, len(data) + 1) / len(data)
    x_grid = np.linspace(np.min(data), np.max(data), 400)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(np.arange(1, len(data) + 1), x_sorted, color='blue', linewidth=1.8)
    axes[0].set_title(f'Вариационный ряд {col_name}')
    axes[0].set_xlabel('Индекс (i)')
    axes[0].set_ylabel(f'Значение {col_name}(i)')

    axes[1].step(x_sorted, ecdf_y, where='post', color='blue', linewidth=1.8, label='ЭФР')
    axes[1].plot(x_grid, cdf(x_grid), 'r--', linewidth=1.6, label='Теорет. ФР')
    axes[1].set_title(f'Функция распределения {col_name}')
    axes[1].legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(f'plots/{col_name}_var_cdf.png', dpi=160)
    plt.close()

def process_column(col_name, data, dist_guess):
    print(f"\n{'='*40}\nОБРАБОТКА СТОЛБЦА {col_name} (Предполагаем: {dist_guess})\n{'='*40}")
    
    x_sorted = np.sort(data)
    mean = np.mean(data)
    var_biased = np.var(data, ddof=0)
    std_biased = np.std(data, ddof=0)
    var_unbiased = np.var(data, ddof=1)
    std_unbiased = np.std(data, ddof=1)
    median = np.median(data)
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    
    print(f"--- 4.1 Числовые характеристики ---")
    print(f"Среднее (x_bar): {mean:.4f}")
    print(f"Дисперсия смещ. (S^2): {var_biased:.4f}, Ст. откл (S): {std_biased:.4f}")
    print(f"Дисперсия несмещ. (sigma^2): {var_unbiased:.4f}, Ст. откл (sigma): {std_unbiased:.4f}")
    print(f"Медиана: {median:.4f}, Q1: {q1:.4f}, Q3: {q3:.4f}")

    mm_params = compute_mm_params(data, dist_guess, mean, var_biased, std_biased)
    params, pdf, cdf = fit_distribution(data, dist_guess, mean, std_biased)
    plot_histogram_comparison(col_name, data, dist_guess, pdf)
    plot_variation_and_cdf(col_name, data, cdf)
    plot_density_mm_mle(col_name, data, dist_guess, mm_params, params)

    k_sturges = sturges_rule(n)
    counts, bins = np.histogram(data, bins=k_sturges)

    print(f"\n--- 4.3 Оценки параметров ({dist_guess}) ---")
    if dist_guess == 'Normal':
        print(f"ММ: a = {mean:.4f}, sigma^2 = {var_biased:.4f}")
        print(f"ММП: a = {mean:.4f}, sigma^2 = {var_biased:.4f}")
    elif dist_guess == 'Uniform':
        a_mm = mean - np.sqrt(3 * var_biased)
        b_mm = mean + np.sqrt(3 * var_biased)
        a_mmp = min(data)
        b_mmp = max(data)
        print(f"ММ: a = {a_mm:.4f}, b = {b_mm:.4f}")
        print(f"ММП: a = {a_mmp:.4f}, b = {b_mmp:.4f}")
    elif dist_guess == 'Exponential':
        lam_mm = 1 / std_biased
        c_mm = mean - 1 / lam_mm
        c_mmp = params['c']
        lam_mmp = params['lambda']
        print(f"ММ: c = {c_mm:.4f}, lambda = {lam_mm:.4f}")
        print(f"ММП: c = {c_mmp:.4f}, lambda = {lam_mmp:.4f}")

    x0 = mean + std_unbiased
    p_emp = np.mean(data > x0)
    
    if dist_guess == 'Normal':
        p_param = 1 - stats.norm.cdf(x0, loc=mean, scale=std_biased)
    elif dist_guess == 'Uniform':
        a_mmp = params['a']
        b_mmp = params['b']
        p_param = (b_mmp - x0) / (b_mmp - a_mmp) if x0 < b_mmp else 0
    elif dist_guess == 'Exponential':
        c_mmp = params['c']
        lam_mmp = params['lambda']
        p_param = np.exp(-lam_mmp * (x0 - c_mmp)) if x0 > c_mmp else 1

    print(f"\n--- 4.4 Вероятности P(X > {x0:.4f}) ---")
    print(f"Эмпирическая: {p_emp:.4f}")
    print(f"Параметрическая: {p_param:.4f}")

    mids = (bins[:-1] + bins[1:]) / 2
    ex_grouped = np.sum(counts * mids) / n
    dx_grouped = np.sum(counts * (mids - ex_grouped)**2) / (n - 1)
    print(f"\n--- 4.5 Группированная выборка ---")
    print(f"EX_grp = {ex_grouped:.4f} (исх. {mean:.4f})")
    print(f"DX_grp = {dx_grouped:.4f} (исх. {var_unbiased:.4f})")

    print(f"\n--- 4.6 Доверительные интервалы (95%) ---")
    margin_asymp = z_val * std_unbiased / np.sqrt(n)
    print(f"Асимпт. ДИ для EX: ({mean - margin_asymp:.4f}, {mean + margin_asymp:.4f})")
    
    if dist_guess == 'Normal':
        t_val = stats.t.ppf(1 - alpha/2, n - 1)
        chi2_left = stats.chi2.ppf(1 - alpha/2, n - 1)
        chi2_right = stats.chi2.ppf(alpha/2, n - 1)
        
        margin_exact = t_val * std_unbiased / np.sqrt(n)
        ci_a = (mean - margin_exact, mean + margin_exact)
        ci_var = ((n - 1) * var_unbiased / chi2_left, (n - 1) * var_unbiased / chi2_right)
        
        print(f"Точный ДИ для a: ({ci_a[0]:.4f}, {ci_a[1]:.4f})")
        print(f"Точный ДИ для sigma^2: ({ci_var[0]:.4f}, {ci_var[1]:.4f})")

process_column('X1', df['X1'].values, 'Exponential')
process_column('X2', df['X2'].values, 'Uniform')
process_column('X3', df['X3'].values, 'Normal')

print(f"\n{'='*40}\nБОНУС ЗАДАНИЕ ДЛЯ X4\n{'='*40}")
x4 = df['X4'].values
x4_reshaped = x4.reshape(-1, 1)

kmeans = KMeans(n_clusters=2, random_state=42, n_init=10).fit(x4_reshaped)
labels = kmeans.labels_
cluster1, cluster2 = x4[labels == 0], x4[labels == 1]

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.hist(x4, bins=sturges_rule(n), edgecolor='black', alpha=0.7)
plt.title('Гистограмма X4 (Смесь)')

plt.subplot(1, 2, 2)
plt.hist(cluster1, alpha=0.5, label=f'Кластер 1 (n={len(cluster1)})')
plt.hist(cluster2, alpha=0.5, label=f'Кластер 2 (n={len(cluster2)})')
plt.title('Разделение на кластеры')
plt.legend()
plt.tight_layout()
plt.savefig('plots/X4_bonus.png')
plt.close()

print(f"X4 Общее среднее: {np.mean(x4):.4f}")
print(f"Кластер 1 среднее: {np.mean(cluster1):.4f}, размер: {len(cluster1)}")
print(f"Кластер 2 среднее: {np.mean(cluster2):.4f}, размер: {len(cluster2)}")
print("Графики сохранены в папку 'plots/'.")