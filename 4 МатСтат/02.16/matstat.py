import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# ЗАДАНИЕ: Первичная обработка выборки
# -------------------------------------------------
# ШАГ 0: Загрузите свою выборку (замените номер файла на ваш вариант)
data = np.loadtxt('16.02/variant_5.csv', delimiter=',')

print(f"Объём выборки: n = {len(data)}")
print()

# -------------------------------------------------
# ШАГ 1: Вариационный ряд
# -------------------------------------------------
# ДОПОЛНИТЕ КОД:
sorted_data = np.sort(data)

print("Вариационный ряд:")
print("  Первые 5:", sorted_data[:5])
print("  Последние 5:", sorted_data[-5:])
print()

# График вариационного ряда
plt.figure(figsize=(10, 5))
indices = np.arange(1, len(sorted_data) + 1)

plt.plot(indices, sorted_data, color='#5B8FF9', linewidth=1.5, alpha=0.7)
plt.scatter(indices, sorted_data, color='#E8684A', s=30, zorder=3, alpha=0.6)

plt.title('Вариационный ряд', fontsize=14)
plt.xlabel('Номер элемента в упорядоченной выборке', fontsize=11)
plt.ylabel('Значение', fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------------------------------
# ШАГ 2: Выборочные оценки
# -------------------------------------------------
# ДОПОЛНИТЕ КОД:
# x_bar = ...       # среднее
# s2 = ...          # дисперсия (несмещённая!)
# s = ...           # стандартное отклонение
# median = ...      # медиана
# x_min = ...       # минимум
# x_max = ...       # максимум

x_bar = np.mean(data)
s2 = np.var(data, ddof=1)
s = np.sqrt(s2)
median = np.median(data)
x_min = np.min(data)
x_max = np.max(data)

print("Выборочные оценки:")
print(f"  Среднее:      x̄ = {x_bar:.3f}")
print(f"  Дисперсия:    s² = {s2:.3f}")
print(f"  Ст. откл.:    s = {s:.3f}")
print(f"  Медиана:      x̃ = {median:.3f}")
print(f"  Размах:       [{x_min:.1f}, {x_max:.1f}]")
print()

# График отклонений от среднего
plt.figure(figsize=(10, 5))
indices = np.arange(len(data))
plt.vlines(indices, x_bar, data, colors='gray', linestyles='-', linewidth=0.5, alpha=0.5)
plt.scatter(indices, data, color='#5B8FF9', s=50, zorder=3, alpha=0.8)
plt.axhline(x_bar, color='red', linestyle='--', linewidth=1.5, label=f'Среднее = {x_bar:.2f}')
plt.axhline(median, color='green', linestyle='--', linewidth=1.5, label=f'Медиана = {median:.2f}')

plt.title('Отклонения от среднего', fontsize=14)
plt.xlabel('Номер наблюдения', fontsize=11)
plt.ylabel('Значение', fontsize=11)
plt.legend(loc='upper left')
plt.grid(alpha=0.3)
plt.text(0.02, 0.98, f'Размах: [{x_min:.1f}, {x_max:.1f}]', 
         transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
plt.tight_layout()
plt.show()

# -------------------------------------------------
# ШАГ 3: Правило Скотта и гистограмма
# -------------------------------------------------
# ДОПОЛНИТЕ КОД:
# n = len(data)
# s = ...  # уже посчитано в Шаге 2
# h = 3.5 * s * n**(-1/3)
# k = ...  # число интервалов (округлить вверх)

n = len(data)
h = 3.5 * s * n ** (-1 / 3)
k = int(np.ceil((x_max - x_min) / h))

print(f"Правило Скотта:")
print(f"  Ширина интервала: h = {h:.2f}")
print(f"  Число интервалов: k = {k}")
print()

# Постройте ДВЕ гистограммы рядом:
#  а) с числом интервалов по Скотту
#  б) с фиксированным числом интервалов = 5
# Добавьте на каждую вертикальную линию со средним значением

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(data, bins=k, color="#5B8FF9", edgecolor="#1F2D3D", alpha=0.85)
axes[0].axvline(x_bar, color="#E8684A", linestyle="--", linewidth=1.5)
axes[0].set_title("Гистограмма (Скотт)")
axes[0].set_xlabel("x")
axes[0].set_ylabel("Частота")

axes[1].hist(data, bins=5, color="#61DDAA", edgecolor="#1F2D3D", alpha=0.85)
axes[1].axvline(x_bar, color="#E8684A", linestyle="--", linewidth=1.5)
axes[1].set_title("Гистограмма (5 интервалов)")
axes[1].set_xlabel("x")
axes[1].set_ylabel("Частота")

plt.tight_layout()
plt.show()

# -------------------------------------------------
# ШАГ 4: Полигон частот
# -------------------------------------------------
# ДОПОЛНИТЕ КОД:
# Постройте полигон частот для интервального ряда
# (используйте те же интервалы, что и в гистограмме по Скотту)

hist_counts, bin_edges = np.histogram(data, bins=k)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

plt.figure(figsize=(8, 4))
plt.plot(bin_centers, hist_counts, marker="o", color="#5B8FF9")
plt.title("Полигон частот (интервалы Скотта)")
plt.xlabel("x")
plt.ylabel("Частота")
plt.grid(alpha=0.3)
plt.show()

# -------------------------------------------------
# ШАГ 5: Эмпирическая функция распределения
# -------------------------------------------------
# ДОПОЛНИТЕ КОД:
# Постройте график ЭФР с пунктирными вертикалями в точках скачков
# и точками на горизонтальных участках

ecdf_y = np.arange(1, n + 1) / n

plt.figure(figsize=(8, 4))
plt.step(sorted_data, ecdf_y, where="post", color="#5B8FF9")

for i, x in enumerate(sorted_data):
	y_prev = ecdf_y[i - 1] if i > 0 else 0
	plt.vlines(x, y_prev, ecdf_y[i], colors="gray", linestyles="dashed", linewidth=0.8)

plt.scatter(sorted_data, ecdf_y, color="#E8684A", s=20, zorder=3)
plt.title("Эмпирическая функция распределения")
plt.xlabel("x")
plt.ylabel("F_n(x)")
plt.ylim(0, 1.05)
plt.grid(alpha=0.3)
plt.show()

# -------------------------------------------------
# ШАГ 6: Сравнение с истинными параметрами
# -------------------------------------------------
# Истинные параметры вашего варианта:
mu_true = 70   # подставьте μ для вышего варианта
sigma2_true = 121  # подставьте σ² для вышего варианта

print("Сравнение с истинными параметрами:")
print(f"  Истинное μ = {mu_true}, выборочное x̄ = {x_bar:.3f}")
print(f"  Истинное σ² = {sigma2_true}, выборочное s² = {s2:.3f}")
print()
print("Вопрос: Почему выборочные оценки отличаются от истинных параметров?")
print("""
Выборочные оценки отличаются от истинных параметров, потому что выборка конечная и случайная. Из‑за случайных ошибкок выборки среднее и дисперсия “гуляют” вокруг истинных значений; чем меньше размер выборки, тем сильнее отклонения. При увеличении объема выборки оценки обычно приближаются к истинным параметрам (ЗБЧ).
	  """)
