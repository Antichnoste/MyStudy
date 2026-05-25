import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

# 1. Граф дорог (Вариант 8)
graph = {
    'A': {'B': 17, 'D': 6, 'F': 3},
    'B': {'G': 40},
    'C': {'G': 7},
    'D': {'E': 7},
    'E': {'C': 6, 'G': 17},
    'F': {'C': 12, 'G': 34},
    'G': {}
}

# Координаты узлов для визуализации
positions = {
    'A': (0, 2),
    'B': (2, 4),
    'D': (2, 2),
    'F': (2, 0),
    'E': (4, 3),
    'C': (4, 1),
    'G': (6, 2),
}

# Все рёбра графа
edges = []
for u in graph:
    for v in graph[u]:
        edges.append((u, v))

# 2. Настройки симуляции
ANTS_COUNT = 50
ITERATIONS = 30
EVAPORATION = 0.3
Q = 100

pheromones = {u: {v: 1.0 for v in graph[u]} for u in graph}


def run_ant():
    path = ['A']
    current = 'A'
    path_length = 0
    while current != 'G':
        neighbors = graph[current]
        total_pheromone = sum(pheromones[current][n] for n in neighbors)
        rand = random.uniform(0, total_pheromone)
        upto = 0
        for n in neighbors:
            upto += pheromones[current][n]
            if upto >= rand:
                next_node = n
                break
        path_length += graph[current][next_node]
        path.append(next_node)
        current = next_node
    return path, path_length


# --- Запускаем симуляцию и сохраняем состояния феромонов ---
pheromone_history = []
best_path_history = []

for i in range(ITERATIONS):
    paths_taken = []
    for _ in range(ANTS_COUNT):
        path, length = run_ant()
        paths_taken.append((path, length))

    for u in pheromones:
        for v in pheromones[u]:
            pheromones[u][v] *= (1 - EVAPORATION)

    for path, length in paths_taken:
        pheromone_to_add = Q / length
        for j in range(len(path) - 1):
            u = path[j]
            v = path[j + 1]
            pheromones[u][v] += pheromone_to_add

    # Сохраняем снимок феромонов
    pheromone_history.append(copy.deepcopy(pheromones))

    # Лучший путь этой итерации
    best = min(paths_taken, key=lambda x: x[1])
    best_path_history.append(best)

# --- Анимация ---
fig, ax = plt.subplots(figsize=(10, 6))


def draw_frame(frame_idx):
    ax.clear()
    ax.set_xlim(-0.8, 7.3)
    ax.set_ylim(-0.8, 5)
    ax.set_aspect('equal')

    pher = pheromone_history[frame_idx]
    best_path, best_len = best_path_history[frame_idx]

    # Находим максимальный феромон для нормализации толщины
    all_pher = [pher[u][v] for u in pher for v in pher[u]]
    max_pher = max(all_pher) if all_pher else 1

    # Рисуем рёбра
    for u, v in edges:
        x0, y0 = positions[u]
        x1, y1 = positions[v]
        p = pher[u][v]

        # Толщина линии пропорциональна феромону (от 0.3 до 12)
        width = 0.3 + (p / max_pher) * 11.7

        # Цвет: от серого (мало феромона) до красного (много)
        intensity = p / max_pher
        color = (0.9, 0.3 * (1 - intensity), 0.1 * (1 - intensity), 0.3 + 0.7 * intensity)

        # Смещение для стрелки
        dx = x1 - x0
        dy = y1 - y0

        ax.annotate(
            '', xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(
                arrowstyle='->', color=color, lw=width,
                connectionstyle='arc3,rad=0.1',
                mutation_scale=15
            )
        )

        # Подпись расстояния на ребре
        mx = (x0 + x1) / 2 + 0.15
        my = (y0 + y1) / 2 + 0.15
        ax.text(mx, my, f'{graph[u][v]} км', fontsize=7, color='gray', ha='center')

    # Рисуем узлы
    for node, (x, y) in positions.items():
        circle_color = '#4CAF50' if node == 'A' else ('#FF5722' if node == 'G' else '#2196F3')
        circle = plt.Circle((x, y), 0.3, color=circle_color, zorder=5)
        ax.add_patch(circle)
        ax.text(x, y, node, fontsize=14, fontweight='bold', ha='center', va='center',
                color='white', zorder=6)

    # Подсветка лучшего пути
    for j in range(len(best_path) - 1):
        u = best_path[j]
        v = best_path[j + 1]
        x0, y0 = positions[u]
        x1, y1 = positions[v]
        ax.annotate(
            '', xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(
                arrowstyle='->', color='gold', lw=3,
                connectionstyle='arc3,rad=0.1',
                mutation_scale=20
            ),
            zorder=4
        )

    # Заголовок
    path_str = ' -> '.join(best_path)
    ax.set_title(
        f'Муравьиная колония (Вариант 8) — День {frame_idx + 1}/{ITERATIONS}\n'
        f'Лучший путь: {path_str} = {best_len} км',
        fontsize=13, fontweight='bold'
    )

    # Легенда феромонов на рёбрах из A
    legend_text = 'Феромон из A:'
    for neighbor in graph['A']:
        p_val = pher['A'][neighbor]
        legend_text += f'  {neighbor}={p_val:.1f}'
    ax.text(0.5, -0.5, legend_text, fontsize=9, fontstyle='italic', color='#333')

    ax.axis('off')


ani = animation.FuncAnimation(fig, draw_frame, frames=ITERATIONS, interval=500, repeat=True)

plt.tight_layout()
plt.show()
