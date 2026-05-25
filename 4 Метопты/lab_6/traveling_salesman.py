import random

random.seed(42)

# Матрица расстояний между городами (Вариант 8)
matrix = {
    1: {1: 0, 2: 1, 3: 1, 4: 11, 5: 10},
    2: {1: 1, 2: 0, 3: 5, 4: 1, 5: 9},
    3: {1: 1, 2: 5, 3: 0, 4: 6, 5: 10},
    4: {1: 11, 2: 1, 3: 6, 4: 0, 5: 7},
    5: {1: 10, 2: 9, 3: 10, 4: 7, 5: 0}
}

# Параметры генетического алгоритма
POPULATION_SIZE = 4
MUTATION_PROB = 0.01       # Вероятность мутации
CROSSOVER_PROB = 0.9       # Вероятность применения двухточечного оператора скрещивания
NUM_GENERATIONS = 5        # Количество поколений


def calculate_fitness(chromosome):
    """
    Вычисляет значение целевой функции (сумму расстояний).
    Включает путь от последнего города обратно к первому.
    """
    path = [int(gene) for gene in str(chromosome)]
    distance = 0
    for i in range(len(path) - 1):
        distance += matrix[path[i]][path[i + 1]]
    # Возврат в исходный город
    distance += matrix[path[-1]][path[0]]
    return distance


def get_selection_weights(population):
    """
    Вычисляет веса для рулеточного отбора (задача минимизации).
    Формула: weight_i = max_f + min_f - f_i
    Чем меньше путь, тем выше вес (и выше шанс быть выбранным).
    """
    fitnesses = [calculate_fitness(ch) for ch in population]
    max_f = max(fitnesses)
    min_f = min(fitnesses)
    # Если все значения одинаковы, даем равные веса
    if max_f == min_f:
        weights = [1 for _ in fitnesses]
    else:
        weights = [max_f + min_f - f for f in fitnesses]
    total = sum(weights)
    return weights, total, fitnesses


def roulette_select(weights, total):
    """Рулеточный отбор: чем больше вес, тем выше шанс быть выбранным"""
    r = random.uniform(0, total)
    cumulative = 0
    for i, w in enumerate(weights):
        cumulative += w
        if r <= cumulative:
            return i
    return len(weights) - 1


def two_point_crossover(parent1_str, parent2_str):
    """
    Двухточечный оператор скрещивания для перестановок (из лекции).
    1) Выбираются две точки разрыва
    2) Средние сегменты обмениваются
    3) Оставшиеся позиции заполняются из исходного родителя,
       начиная со второго числа выделенного фрагмента, по кругу,
       пропуская уже имеющиеся числа.
    """
    p1 = [int(g) for g in parent1_str]
    p2 = [int(g) for g in parent2_str]
    n = len(p1)

    # Выбираем две точки разрыва случайно
    pts = sorted(random.sample(range(1, n), 2))
    pt1, pt2 = pts

    # Средние сегменты родителей
    mid1 = p1[pt1:pt2]
    mid2 = p2[pt1:pt2]

    # --- Потомок 1: берёт середину от родителя 2 ---
    child1_set = set(mid2)
    # Начинаем со второго числа фрагмента родителя 1 (или первого, если фрагмент из 1 элемента)
    start_elem = mid1[1] if len(mid1) > 1 else mid1[0]
    start_idx = p1.index(start_elem)
    remaining = []
    for offset in range(n):
        elem = p1[(start_idx + offset) % n]
        if elem not in child1_set:
            remaining.append(elem)
    child1 = remaining[:pt1] + mid2 + remaining[pt1:]

    # --- Потомок 2: берёт середину от родителя 1 ---
    child2_set = set(mid1)
    start_elem2 = mid2[1] if len(mid2) > 1 else mid2[0]
    start_idx2 = p2.index(start_elem2)
    remaining2 = []
    for offset in range(n):
        elem = p2[(start_idx2 + offset) % n]
        if elem not in child2_set:
            remaining2.append(elem)
    child2 = remaining2[:pt1] + mid1 + remaining2[pt1:]

    return ''.join(map(str, child1)), ''.join(map(str, child2)), pt1, pt2


def mutate(chromosome):
    """Мутация: случайная перестановка двух генов в хромосоме"""
    genes = list(str(chromosome))
    i, j = random.sample(range(len(genes)), 2)
    genes[i], genes[j] = genes[j], genes[i]
    return ''.join(genes)


def format_with_cuts(chrom_str, pt1, pt2):
    """Форматирует хромосому с разделителями | в точках разрыва"""
    return chrom_str[:pt1] + '|' + chrom_str[pt1:pt2] + '|' + chrom_str[pt2:]


def print_table_header(title, columns):
    print(f"\n{title}")
    print("-" * 75)
    print(columns)
    print("-" * 75)


def generate_initial_population():
    """Генерация начальной популяции случайных перестановок"""
    cities = [1, 2, 3, 4, 5]
    population = []
    used = set()
    while len(population) < POPULATION_SIZE:
        perm = cities[:]
        random.shuffle(perm)
        code = ''.join(map(str, perm))
        if code not in used:
            used.add(code)
            population.append(code)
    return population


# ==========================================
# ЗАПУСК ГЕНЕТИЧЕСКОГО АЛГОРИТМА
# ==========================================
print("ГЕНЕТИЧЕСКИЙ АЛГОРИТМ: ЗАДАЧА О КОММИВОЯЖЕРЕ (Вариант 8)")
print(f"Размер популяции N = {POPULATION_SIZE}. Вероятность мутации {MUTATION_PROB}.")
print(f"Вероятность скрещивания (двухточечный оператор) {CROSSOVER_PROB}.")

# Этап 1: Формирование начальной популяции
population = generate_initial_population()
initial_fitnesses = [calculate_fitness(code) for code in population]
avg_start = sum(initial_fitnesses) / POPULATION_SIZE

for gen in range(1, NUM_GENERATIONS + 1):

    # ==========================================
    # Печать текущей популяции с вероятностями
    # ==========================================
    weights, total_w, fitnesses = get_selection_weights(population)

    if gen == 1:
        table_name = "Исходная популяция"
    else:
        table_name = f"Популяция {gen - 1}-го поколения после отсечения"

    print_table_header(
        f"Таблица. {table_name}",
        "№ строки | Код    | Значение ЦФ | Вероятность размножения"
    )
    for i, code in enumerate(population):
        f = fitnesses[i]
        w = weights[i]
        print(f"{i + 1:<9} | {code:<6} | {f:<11} | {w}/{total_w}")

    # ==========================================
    # Этап 2: Отбор пар (рулеточный отбор)
    # ==========================================
    selected = []
    for _ in range(POPULATION_SIZE):
        selected.append(roulette_select(weights, total_w))

    # Формируем пары из отобранных особей
    pairs = []
    for k in range(0, POPULATION_SIZE, 2):
        idx1 = selected[k]
        idx2 = selected[k + 1]
        # Если попались одинаковые — пере-выбираем второго
        while idx2 == idx1:
            idx2 = roulette_select(weights, total_w)
        pairs.append((idx1, idx2))

    # ==========================================
    # Этап 3: Скрещивание и мутация
    # ==========================================
    print_table_header(
        f"Таблица. Результат скрещивания {gen}-го поколения",
        "№ строки | Родители   | Потомки                  | Значение ЦФ"
    )

    offspring = []
    for idx1, idx2 in pairs:
        p1, p2 = population[idx1], population[idx2]

        # Применяем скрещивание с заданной вероятностью
        if random.random() < CROSSOVER_PROB:
            c1, c2, pt1, pt2 = two_point_crossover(p1, p2)
            p1_fmt = format_with_cuts(p1, pt1, pt2)
            p2_fmt = format_with_cuts(p2, pt1, pt2)
        else:
            # Без скрещивания — потомки = копии родителей
            c1, c2 = p1, p2
            p1_fmt = p1
            p2_fmt = p2

        # Мутация каждого потомка с заданной вероятностью
        children = [c1, c2]
        parent_fmts = [p1_fmt, p2_fmt]
        parent_idxs = [idx1, idx2]

        for k in range(2):
            child = children[k]
            original_child = child
            mutated = False
            if random.random() < MUTATION_PROB:
                child = mutate(child)
                mutated = True

            if mutated:
                display = f"{original_child} -> мутация {child}"
                print(f"{parent_idxs[k] + 1:<9} | {parent_fmts[k]:<10} | {display:<24} | {calculate_fitness(child)}")
            else:
                print(f"{parent_idxs[k] + 1:<9} | {parent_fmts[k]:<10} | {child:<24} | {calculate_fitness(child)}")

            offspring.append(child)

    # ==========================================
    # Этап 4: Редукция (отбираем лучших)
    # ==========================================
    # Собираем всех родителей и потомков
    all_individuals = []
    for code in population:
        all_individuals.append((code, calculate_fitness(code), 'old'))
    for code in offspring:
        all_individuals.append((code, calculate_fitness(code), 'new'))

    # Сортируем по возрастанию расстояния (лучшие — с наименьшим путем)
    all_individuals.sort(key=lambda x: x[1])

    # Берём лучших N
    new_population = []
    sources = []
    for code, f, src in all_individuals:
        if len(new_population) < POPULATION_SIZE:
            new_population.append(code)
            sources.append(src)

    print_table_header(
        f"Таблица. Популяция {gen}-го поколения после отсечения",
        "№ строки | Код    | Значение целевой функции"
    )

    old_indices_used = set()
    for i, (code, src) in enumerate(zip(new_population, sources)):
        f = calculate_fitness(code)
        if src == 'old' and code in population:
            old_idx = population.index(code)
            if old_idx not in old_indices_used:
                old_indices_used.add(old_idx)
                label = f"{i + 1} ({old_idx + 1})"
            else:
                label = f"{i + 1} (н)"
        else:
            label = f"{i + 1} (н)"
        print(f"{label:<9} | {code:<6} | {f}")

    population = new_population

# ==========================================
# Итоги
# ==========================================
final_fitnesses = [calculate_fitness(code) for code in population]
avg_end = sum(final_fitnesses) / POPULATION_SIZE

print("\n" + "=" * 50)
print("ВЫВОД:")
print(f"Среднее значение целевой функции изменилось с {avg_start} до {avg_end}.")
if avg_end < avg_start:
    print("Общее качество популяции улучшилось (значение уменьшилось)")
elif avg_end > avg_start:
    print("Общее качество популяции ухудшилось (значение увеличилось)")
else:
    print("Общее качество популяции не изменилось")
