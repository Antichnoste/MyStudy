"""
============================================================================
ДЗ3.1 — отбор значимых признаков для задачи регрессии двумя методами:
  1) Gradient Boosting (sklearn) — как чёрный ящик; берём важности
     признаков из обученной модели.
  2) UFSACO (муравьиная колония, unsupervised feature selection) —
     код 1-в-1 из материалов лекции (UFSACO.ipynb).

Датасет: CarPrice_clean.csv (Geely Auto / Kaggle), 205 строк × 25
столбцов (24 признака + целевая переменная price).

Запуск:  python ufsaco_hw3.py
============================================================================
"""

# ----------------------------------------------------------------------------
# 0. Импорты
# ----------------------------------------------------------------------------
import copy                            # глубокое копирование feature_importances_
import json                            # запись финальных результатов
from collections import Counter        # подсчёт частот в 5 запусках UFSACO

import numpy as np                     # численные операции
import pandas as pd                    # загрузка CSV, табличные операции

import matplotlib                      # рисование графиков
matplotlib.use("Agg")                  # бэкенд без GUI — рисуем сразу в файлы
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn import ensemble           # GradientBoostingRegressor


# ----------------------------------------------------------------------------
# Настройки внешнего вида графиков и фиксация генератора случайных чисел
# ----------------------------------------------------------------------------
plt.style.use("bmh")                   # стиль из ноутбука лекции
sns.set_style("whitegrid")
np.random.seed(42)                     # воспроизводимость GB и UFSACO


# ============================================================================
# ЭТАП 1. Загрузка датасета и выбор целевого признака
# ============================================================================
# CSV получен ранее из CarPrice_Assignment.xls: убраны car_ID и CarName,
# из CarName извлечена марка (carbrand), категориальные признаки
# label-encoded, словесные числа ('two', 'four', ...) переведены в int.
df = pd.read_csv("CarPrice_clean.csv")

# >>> Здесь явно объявляем целевой признак <<<
# Согласно условию ДЗ ("Выберите также целевой признак...") и постановке
# исходной задачи Geely Auto — мы предсказываем розничную цену автомобиля.
TARGET = "price"

# Список признаков = все столбцы DataFrame, кроме целевого.
FEATURES = [c for c in df.columns if c != TARGET]

print(f"Данные: {df.shape[0]} объектов, "
      f"{len(FEATURES)} признаков, целевой: {TARGET}")


# ============================================================================
# ЭТАП 2. Краткий разведочный анализ (EDA)
# ============================================================================
# 2.1. Описательные статистики (среднее, std, min, max) — для отчёта.
desc = df.describe().T[["mean", "std", "min", "max"]].round(3)
desc.to_csv("eda_describe_hw3.csv")
print("EDA: описательные статистики -> eda_describe_hw3.csv")

# 2.2. Гистограммы распределений всех столбцов (признаки + цель).
#      Помогают увидеть скос, нетипичные значения, бинарные категориальные.
n = len(df.columns)
cols = 5                                  # сетка 5 столбцов
rows = (n + cols - 1) // cols             # сколько строк нужно (округление вверх)
fig, axes = plt.subplots(rows, cols, figsize=(18, 3 * rows))
for ax, col in zip(axes.flat, df.columns):
    ax.hist(df[col], bins=30, color="#86bf91", edgecolor="white")
    ax.set_title(col, fontsize=10)
for ax in axes.flat[n:]:                  # лишние пустые ячейки сетки прячем
    ax.axis("off")
plt.tight_layout()
plt.savefig("img/hist_hw3.png", dpi=110)
plt.close()

# 2.3. Корреляции Пирсона признаков с целевым (отсортированы по |r|).
#      Это «классическая» оценка предсказательной силы линейной части
#      зависимости — даёт быстрое представление о структуре данных.
corr_target = (
    df.corr()[TARGET]                     # столбец корреляций с price
      .drop(TARGET)                       # убираем корреляцию price с самим собой
      .sort_values(key=lambda s: s.abs(), ascending=False)
)
corr_target.to_csv("corr_with_price_hw3.csv")

# 2.4. Тепловая карта корреляций между всеми переменными.
#      Видно «размерный» кластер: enginesize ↔ curbweight ↔ carlength ↔ horsepower.
plt.figure(figsize=(14, 12))
sns.heatmap(df.corr(), cmap="coolwarm", center=0, square=True,
            cbar_kws={"shrink": 0.7})
plt.title("Корреляционная матрица")
plt.tight_layout()
plt.savefig("img/corr_heatmap_hw3.png", dpi=110)
plt.close()


# ============================================================================
# ЭТАП 3. Масштабирование признаков
# ============================================================================
# 3.1. Для градиентного бустинга — Min-Max в диапазон [0, 1]
#      (как в исходном ноутбуке UFSACO.ipynb).
x_train = df[FEATURES].copy()             # матрица X — без целевого столбца
y_train = df[TARGET].copy()               # вектор y — целевая переменная

x_scaler = MinMaxScaler()
x_train_scaled = x_scaler.fit_transform(x_train)   # ndarray (205, 24)

# 3.2. Для UFSACO — StandardScaler (Z-score: вычесть среднее, делить на std).
#      Почему НЕ MinMax, как в ноутбуке: у нас несколько label-encoded
#      категориальных признаков (enginelocation, aspiration, doornumber)
#      почти константы — одно значение встречается у >=90% объектов.
#      После MinMax их вектор близок к нулевому, норма ≈ 0, и косинусная
#      близость становится численно неустойчивой → такие признаки получают
#      завышенные score и захватывают весь top-k. После центрирования
#      cos-similarity ≡ корреляция Пирсона и эта патология уходит.
#      Алгоритм UFSACO сам по себе не меняется — меняется только вход.
#
#      Важно: матрицу для UFSACO строим ТОЛЬКО ПО ПРИЗНАКАМ (без price) —
#      по требованию ДЗ: «отбирать признаки для задачи без целевого признака».
all_scaler = StandardScaler()
all_scaled = all_scaler.fit_transform(df[FEATURES])   # ndarray (205, 24)

print(f"x_train_scaled: {x_train_scaled.shape}, "
      f"all_scaled: {all_scaled.shape}")


# ============================================================================
# ЭТАП 4. МЕТОД 1 — Gradient Boosting (feature importance)
# ============================================================================
# Сколько признаков отбираем каждым методом.
# Требование ЛР: 7 <= N_FEATURES <= floor(d/2), здесь floor(24/2) = 12.
# При N=7 пересечение GB и UFSACO было пустым (0-2), т.к. GB-top-7 — это
# один «размерный» кластер скоррелированных признаков, а UFSACO по дизайну
# выбирает по одному представителю каждого кластера. При N=12 оба метода
# захватывают несколько кластеров → пересечение >= 4.
N_FEATURES = 12

# Параметры GBR в точности из лекционного ноутбука (плюс seed):
gb_params = dict(
    n_estimators=300,                     # M — число деревьев в композиции
    max_depth=4,                          # глубина каждого дерева
    min_samples_split=10,                 # минимум объектов для расщепления узла
    learning_rate=0.01,                   # ν — темп обучения (shrinkage)
    verbose=0,
    random_state=42,
)
model = ensemble.GradientBoostingRegressor(**gb_params)
model.fit(x_train_scaled, y_train)        # обучаем на масштабированных X и сыром y

# R^2 на train — для отчёта (даёт представление о качестве модели).
print(f"Gradient Boosting: R^2 (train) = "
      f"{model.score(x_train_scaled, y_train):.4f}")

# model.feature_importances_ — массив длины 24, нормированный к 1.
# Чем больше значение, тем чаще признак использовался для расщеплений и тем
# больше суммарное уменьшение функции потерь, которое он принёс.
base_imp = copy.deepcopy(model.feature_importances_)

# Индексы признаков, отсортированные по убыванию важности (берём top-N).
gb_top_idx = np.argsort(base_imp)[::-1][:N_FEATURES]

# Превращаем индексы в имена — этот список пойдёт в финальное сравнение.
boosting_names = [FEATURES[i] for i in gb_top_idx]
print(f"GB top-{N_FEATURES}: {boosting_names}")

# Горизонтальная столбчатая диаграмма важностей — для отчёта.
fimps = pd.DataFrame({"Name": boosting_names, "Vals": base_imp[gb_top_idx]})
plt.figure(figsize=(8, 5))
sns.barplot(x="Vals", y="Name", data=fimps, color="#176BA0")
plt.title(f"Gradient Boosting: top-{N_FEATURES} feature importance")
plt.tight_layout()
plt.savefig("img/gb_importance_hw3.png", dpi=110)
plt.close()


# ============================================================================
# ЭТАП 5. МЕТОД 2 — UFSACO (муравьиная колония)
# ============================================================================
# Гиперпараметры — финальные, подобранные так, чтобы |GB ∩ UFSACO| >= 4.
# Они отличаются от дефолтов ноутбука (NC_MAX=3, N_STEPS=4, N_ANTS=5,
# ALPHA=1, RO=0.2): мы увеличили число эпох/шагов/муравьёв для стабилизации
# феромона и понизили ALPHA, чтобы ослабить штраф за сходство признаков.
EPS = 1e-6                                # защита от деления на 0 в cos-similarity
N_START_FEATURES = all_scaled.shape[1]    # 24 — число вершин графа (= число признаков)
N_END_FEATURES = N_FEATURES               # 12 — сколько вершин берём в финальный top

NC_MAX = 50                               # число «эпох» (внешних циклов)
N_STEPS = 10                              # длина пути одного муравья (число шагов)
N_ANTS = 25                               # число муравьёв в колонии
INIT_PHEROMONE = 0.2                      # τ_0 — начальный феромон на каждой вершине
RO = 0.1                                  # ρ — коэф. испарения феромона
EXPLOITATION_PROB = 0.7                   # q_0 — вероятность жадного шага (argmax)
ALPHA = 1.0                               # вес «некоррелированности» в η
                                          # (фактически переопределим ниже = 0.2)
ALPHA = 0.2                               # ослабленный штраф за сходство:
                                          # при α→0 знаменатель η→1, выбор по τ
BETA = 1.0                                # параметр не используется (оставлен для совм.)


# ----------------------------------------------------------------------------
# 5.1. Кэш косинусных близостей между признаками
# ----------------------------------------------------------------------------
# Близость считается один раз на пару и хранится в словаре sim,
# чтобы не пересчитывать на каждом шаге каждого муравья.
sim = {}

def set_sim(i, j):
    """Вычислить и закэшировать |cos(x_i, x_j)| для столбцов i, j."""
    a = all_scaled[:, i]                  # вектор-столбец признака i
    b = all_scaled[:, j]                  # вектор-столбец признака j
    res = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + EPS)
    # Берём модуль: антикорреляция (cos≈-1) тоже означает избыточность.
    sim[(min(i, j), max(i, j))] = np.abs(res)
    return res

def get_sim(i, j):
    """Получить близость из кэша; посчитать, если её там ещё нет."""
    key = (min(i, j), max(i, j))          # симметричный ключ: sim(i,j)=sim(j,i)
    if key not in sim:
        set_sim(i, j)
    return sim[key]


# ----------------------------------------------------------------------------
# 5.2. Сам алгоритм UFSACO — 1-в-1 из ноутбука лекции
# ----------------------------------------------------------------------------
def UFSACO(verbose=False):
    """
    Возвращает вектор τ длины N_START_FEATURES — итоговый феромон на каждой
    вершине. Признаки с наибольшим τ считаются отобранными.
    """
    # ---- Инициализация феромона ----
    # На каждой вершине одинаковое начальное значение τ_0.
    tau = INIT_PHEROMONE * np.ones((N_START_FEATURES,))

    # ============ ВНЕШНИЙ ЦИКЛ: эпохи ============
    for count in range(NC_MAX):
        # Случайно размещаем муравьёв по вершинам с вероятностью,
        # пропорциональной текущему феромону τ.
        ants_pos = np.random.choice(
            N_START_FEATURES, size=N_ANTS, p=tau / sum(tau)
        )

        # Счётчик визитов каждой вершины за текущую эпоху.
        visits = np.zeros((N_START_FEATURES,))

        # Для каждого муравья k и каждой стартовой вершины i — множество
        # уже посещённых вершин (чтобы не возвращаться).
        nodes_visited = {(k, i): set()
                         for k in range(N_ANTS)
                         for i in range(N_START_FEATURES)}

        # ============ СРЕДНИЙ ЦИКЛ: шаги пути ============
        for it in range(N_STEPS):

            # ============ ВНУТРЕННИЙ ЦИКЛ: каждый муравей ============
            for k in range(N_ANTS):
                # Где сейчас стоит k-й муравей.
                i = ants_pos[k]
                # Какие вершины он уже посещал, начиная с i.
                visited = nodes_visited[(k, i)]
                # Кандидаты для следующего шага: всё кроме посещённого и i.
                unvisited = list((set(range(N_START_FEATURES)) - visited) - {i})

                # «Желательность» η каждого кандидата j:
                #   η(j|i) = τ_j / (sim(i,j) + ε)^α
                # Чем меньше похожи признаки i и j, и чем выше феромон,
                # тем выгоднее перейти в j.
                node_score = [
                    tau[j] / np.power(get_sim(i, j) + EPS, ALPHA)
                    for j in unvisited
                ]

                # Стохастический выбор: exploitation vs exploration.
                q = np.random.uniform()
                if q <= EXPLOITATION_PROB:
                    # EXPLOITATION: жадно — максимум η.
                    jj = int(np.argmax(node_score))
                else:
                    # EXPLORATION: с вероятностью, пропорциональной η.
                    p = np.array(node_score) / sum(node_score)
                    jj = int(np.random.choice(len(unvisited), size=1, p=p)[0])

                # Делаем шаг i → j: переносим муравья и обновляем счётчики.
                j = unvisited[jj]
                ants_pos[k] = j
                nodes_visited[(k, i)].add(j)
                visits[j] += 1

                if verbose:
                    print(f"count={count}, iter={it}, k={k}, i={i}, j={j}")

        # ---- Обновление феромона по итогам эпохи ----
        #   τ ← (1-ρ)·τ + visits / Σ visits
        # Первое слагаемое — испарение; второе — подкрепление вершин,
        # которые часто посещались на этой эпохе.
        total = sum(visits)
        if total > 0:
            tau = (1 - RO) * tau + (visits / total)

    return tau


# ----------------------------------------------------------------------------
# 5.3. Прогон UFSACO 5 раз для оценки устойчивости
# ----------------------------------------------------------------------------
# Имена признаков в порядке столбцов all_scaled (это просто FEATURES).
all_input_names = list(FEATURES)

ufsaco_runs = []                          # списки top-N по каждому запуску
print("\nUFSACO — 5 запусков:")
for r in range(5):
    sim = {}                              # сбрасываем кэш близостей между прогонами
                                          # (не критично, но чище для воспроизводимости)
    tau = UFSACO(verbose=False)           # запускаем алгоритм
    # Берём индексы N_END_FEATURES вершин с наибольшим феромоном.
    top_idx = np.array(tau.argsort()[::-1])[:N_END_FEATURES]
    names = [all_input_names[i] for i in top_idx]
    ufsaco_runs.append(names)
    print(f"  run {r + 1}: {names}")

# Финальный набор UFSACO — N_END_FEATURES признаков, чаще всего попавших
# в top по совокупности 5 запусков. Это робастная агрегация: уменьшает
# шум одного запуска.
freq = Counter([n for run in ufsaco_runs for n in run])
ufsaco_names = [n for n, _ in freq.most_common(N_END_FEATURES)]
print(f"\nUFSACO итоговый top-{N_END_FEATURES} (по частоте): {ufsaco_names}")


# ============================================================================
# ЭТАП 6. Сравнение множеств и проверка требования ДЗ
# ============================================================================
gb_set = set(boosting_names)
aco_set = set(ufsaco_names)
inter = gb_set & aco_set                  # пересечение двух множеств

print(f"\nGB:    {sorted(gb_set)}")
print(f"UFSACO:{sorted(aco_set)}")
print(f"ПЕРЕСЕЧЕНИЕ ({len(inter)}): {sorted(inter)}")

# Требование ЛР: |S_GB ∩ S_ACO| >= 4. Если падает — значит, гиперпараметры
# ACO нужно подкрутить ещё раз.
assert len(inter) >= 4, \
    f"Пересечение слишком маленькое: {len(inter)} < 4. Поварьируйте гиперпараметры ACO."
print("OK: |пересечения| >= 4")


# ============================================================================
# ЭТАП 7. Анализ пар признаков по UFSACO-метрике (для отчёта)
# ============================================================================
# Самые «похожие» и самые «различные» пары признаков по |cos|.
# Top-10 sim ≈ кластеры избыточности; bottom-10 ≈ независимые пары.
all_sims, all_pairs = [], []
for i, n1 in enumerate(all_input_names):
    for j, n2 in enumerate(all_input_names):
        if j > i:                         # каждую пару считаем один раз (i<j)
            all_sims.append(get_sim(i, j))
            all_pairs.append(f"{n1} + {n2}")

series = pd.Series(all_sims, index=all_pairs)
top_sim = series.sort_values(ascending=False).head(10)
bot_sim = series.sort_values(ascending=True).head(10)
top_sim.to_csv("sim_top10_hw3.csv", header=["sim"])
bot_sim.to_csv("sim_bot10_hw3.csv", header=["sim"])


# ============================================================================
# ЭТАП 8. Запись финальных результатов в JSON (для отчёта и проверки)
# ============================================================================
result = {
    "n_objects": int(df.shape[0]),
    "n_features": int(len(FEATURES)),
    "target": TARGET,
    "n_selected": N_END_FEATURES,
    "gb_top": boosting_names,
    "ufsaco_runs": ufsaco_runs,
    "ufsaco_top": ufsaco_names,
    "intersection": sorted(inter),
    "intersection_size": len(inter),
    "gb_train_r2": float(model.score(x_train_scaled, y_train)),
    "hyperparams_aco": dict(
        NC_MAX=NC_MAX, N_STEPS=N_STEPS, INIT_PHEROMONE=INIT_PHEROMONE,
        RO=RO, EXPLOITATION_PROB=EXPLOITATION_PROB, ALPHA=ALPHA, BETA=BETA,
        N_ANTS=N_ANTS,
    ),
    "corr_with_target_top10": corr_target.head(10).round(4).to_dict(),
}
with open("results_hw3.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\nГотово. Артефакты:")
for f in [
    "eda_describe_hw3.csv", "hist_hw3.png", "corr_with_price_hw3.csv",
    "corr_heatmap_hw3.png", "gb_importance_hw3.png",
    "sim_top10_hw3.csv", "sim_bot10_hw3.csv", "results_hw3.json",
]:
    print(" -", f)
