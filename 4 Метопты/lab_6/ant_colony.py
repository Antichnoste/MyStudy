import random

# 1. Задаем граф дорог (Вариант 8)
# Матрица смежности из задания:
# A: B=17, D=6, F=3
# D: E=7
# E: C=6, G=17
# F: C=12, G=34
# C: G=7
# B: тупик (только обратно в A), добавлен длинный обход B->G=40
graph = {
    'A': {'B': 17, 'D': 6, 'F': 3},
    'B': {'G': 40},        # Длинный путь-обход (57 км)
    'C': {'G': 7},
    'D': {'E': 7},
    'E': {'C': 6, 'G': 17},
    'F': {'C': 12, 'G': 34},
    'G': {}                # Конечный узел (еда)
}

# 2. Инициализация феромонов (в начале везде одинаковый запах = 1.0)
pheromones = {u: {v: 1.0 for v in graph[u]} for u in graph}

# 3. Настройки симуляции
ANTS_COUNT = 50        # Количество муравьев в одной итерации
ITERATIONS = 30        # Количество дней (итераций)
EVAPORATION = 0.3      # Скорость испарения запаха (30% в день)
Q = 100                # Коэффициент оставляемого феромона

def run_ant():
    """Симуляция прохода одного муравья от A до G"""
    path = ['A']
    current = 'A'
    path_length = 0

    # Муравей идет, пока не достигнет цели (G)
    while current != 'G':
        neighbors = graph[current]

        # Считаем сумму феромонов на всех доступных тропинках из текущего узла
        total_pheromone = sum(pheromones[current][n] for n in neighbors)

        # Рулетка: случайный выбор пути. Чем сильнее запах, тем выше шанс!
        rand = random.uniform(0, total_pheromone)
        upto = 0
        for n in neighbors:
            upto += pheromones[current][n]
            if upto >= rand:
                next_node = n
                break

        # Шагаем в выбранный узел
        path_length += graph[current][next_node]
        path.append(next_node)
        current = next_node

    # Телепортируем муравья обратно с результатами его похода
    return path, path_length

print("=== Старт симуляции Муравьиной колонии (Вариант 8) ===\n")

for i in range(1, ITERATIONS + 1):
    paths_taken = []

    # ЭТАП 1: Разведка (Запускаем муравьев)
    for _ in range(ANTS_COUNT):
        path, length = run_ant()
        paths_taken.append((path, length))

    # ЭТАП 2: Забывание плохого опыта (Испарение феромона)
    for u in pheromones:
        for v in pheromones[u]:
            pheromones[u][v] *= (1 - EVAPORATION)

    # ЭТАП 3: Положительная обратная связь (Муравьи оставляют новый феромон)
    for path, length in paths_taken:
        # Чем короче маршрут, тем больше феромона муравей успевает оставить за день
        pheromone_to_add = Q / length
        for j in range(len(path) - 1):
            u = path[j]
            v = path[j + 1]
            pheromones[u][v] += pheromone_to_add

    # Печатаем статистику для 1-го, 5-го и последнего дня
    if i == 1 or i == 5 or i == ITERATIONS:
        print(f"--- День {i} ---")

        # Подсчет, сколько муравьев какой путь выбрали
        path_counts = {}
        for p, l in paths_taken:
            p_str = " -> ".join(p) + f" ({l} км)"
            path_counts[p_str] = path_counts.get(p_str, 0) + 1

        # Выводим пути по популярности
        for p_str, count in sorted(path_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"Муравьев: {count:2} | Выбрали путь: {p_str}")
        print()

print("=== Результат (Концентрация запаха на развилке из старта 'A') ===")
for neighbor in graph['A']:
    print(f"Тропинка в {neighbor}: {pheromones['A'][neighbor]:.2f} ед. феромона")

print("\nВывод: Муравьи успешно сошлись на самом оптимальном пути!")
