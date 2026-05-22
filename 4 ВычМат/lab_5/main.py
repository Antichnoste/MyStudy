import os
import math
import numpy as np
import matplotlib.pyplot as plt

MIN_INPUT_VALUE = -150.0
MAX_INPUT_VALUE = 150.0
MAX_FUNC_POINTS = 50
MAX_DECIMALS = 6

def _validate_precision(tokens):
    for token in tokens:
        normalized = token.strip().replace(",", ".")
        if "." in normalized:
            decimals = normalized.split(".", 1)[1]
            if len(decimals) > MAX_DECIMALS:
                raise ValueError(
                    f"Слишком много знаков после запятой. Допустимо не более {MAX_DECIMALS}."
                )

def get_finite_differences(y):
    n = len(y)
    diffs = np.zeros((n, n))
    diffs[:, 0] = y
    for k in range(1, n):
        for i in range(n - k):
            diffs[i, k] = diffs[i+1, k-1] - diffs[i, k-1]
    return diffs

def print_diff_table(x, diffs):
    print("\n--- Таблица конечных разностей ---")
    n = len(x)
    header = "x_i\t\ty_i\t\t" + "\t\t".join([f"Δ^{i}y" for i in range(1, n)])
    print(header)
    for i in range(n):
        row = f"{x[i]:.4f}\t\t"
        for k in range(n - i):
            row += f"{diffs[i, k]:.4f}\t\t"
        print(row)
    print("-" * 60)

def is_equidistant(x):
    if len(x) < 2: return True
    h = x[1] - x[0]
    return all(math.isclose(x[i] - x[i-1], h, rel_tol=1e-5) for i in range(1, len(x)))


def _validate_range(values):
    for value in values:
        if value < MIN_INPUT_VALUE or value > MAX_INPUT_VALUE:
            raise ValueError(
                f"Введено {value}. Допустимый диапазон: "
                f"[{MIN_INPUT_VALUE}, {MAX_INPUT_VALUE}]."
            )


def parse_floats(text):
    if not text.strip():
        raise ValueError("Пустой ввод. Нужно ввести хотя бы одно число.")
    tokens = text.split()
    _validate_precision(tokens)
    values = [float(token.replace(",", ".")) for token in tokens]
    _validate_range(values)
    return values


def parse_float(text):
    if not text.strip():
        raise ValueError("Пустой ввод. Нужно ввести число.")
    _validate_precision([text])
    value = float(text.replace(",", "."))
    _validate_range([value])
    return value


def lagrange(x, y, x_target):
    n = len(x)
    res = 0.0
    for i in range(n):
        term = y[i]
        for j in range(n):
            if i != j:
                term *= (x_target - x[j]) / (x[i] - x[j])
        res += term
    return res

def newton_finite(x, y, x_target):
    diffs = get_finite_differences(y)
    n = len(x)
    h = x[1] - x[0]
    
    if x_target <= x[n//2]:
        t = (x_target - x[0]) / h
        res, t_term = diffs[0, 0], 1.0
        for k in range(1, n):
            t_term *= (t - k + 1) / k
            res += t_term * diffs[0, k]
    else:
        t = (x_target - x[-1]) / h
        res, t_term = diffs[-1, 0], 1.0
        for k in range(1, n):
            t_term *= (t + k - 1) / k
            res += t_term * diffs[n - 1 - k, k]
    return res

def gauss(x, y, x_target, center_idx=None):
    diffs = get_finite_differences(y)
    n = len(x)
    h = x[1] - x[0]

    if center_idx is None:
        idx = n // 2
    else:
        idx = center_idx
    t = (x_target - x[idx]) / h
    
    res = diffs[idx, 0]
    t_term = 1.0
    
    for k in range(1, n):
        if t > 0: 
            shift = k // 2
        else:     
            shift = (k + 1) // 2
            
        row = idx - shift
        if row < 0 or row >= n - k:
            break
        
        if t > 0: t_term *= (t - k//2) if k % 2 != 0 else (t + k//2)
        else:     t_term *= (t + k//2) if k % 2 != 0 else (t - k//2)
            
        res += (t_term / math.factorial(k)) * diffs[row, k]
    return res

def stirling(x, y, x_target):
    diffs = get_finite_differences(y)
    n = len(x)
    h = x[1] - x[0]
    
    idx = np.argmin(np.abs(np.array(x) - x_target))
    t = (x_target - x[idx]) / h
    
    res = diffs[idx, 0]
    t_prod = t
    
    for k in range(1, (n // 2) + 1):
        if idx - k < 0 or idx - k + 1 >= n - (2*k - 1): 
            break
        diff_avg = (diffs[idx - k, 2*k - 1] + diffs[idx - k + 1, 2*k - 1]) / 2.0
        res += (t_prod / math.factorial(2*k - 1)) * diff_avg
        
        if idx - k < 0 or idx - k >= n - 2*k:
            break
        res += (t_prod * t / math.factorial(2*k)) * diffs[idx - k, 2*k]
        
        t_prod *= (t**2 - k**2)
    return res

def bessel(x, y, x_target):
    diffs = get_finite_differences(y)
    n = len(x)
    h = x[1] - x[0]
    
    idx = np.argmin(np.abs(np.array(x) - x_target))
    if x_target < x[idx] and idx > 0: 
        idx -= 1
        
    t = (x_target - x[idx]) / h
    if idx + 1 >= n: return y[-1]
    
    res = (diffs[idx, 0] + diffs[idx + 1, 0]) / 2.0 + (t - 0.5) * diffs[idx, 1]
    t_prod = t * (t - 1)
    
    for k in range(1, n // 2):
        if idx - k < 0 or idx - k + 1 >= n - 2*k: break
        diff_avg = (diffs[idx - k, 2*k] + diffs[idx - k + 1, 2*k]) / 2.0
        res += (t_prod / math.factorial(2*k)) * diff_avg
        
        if idx - k < 0 or idx - k >= n - (2*k + 1): break
        res += (t_prod * (t - 0.5) / math.factorial(2*k + 1)) * diffs[idx - k, 2*k + 1]
        
        t_prod *= (t + k) * (t - k - 1)
    return res


def plot_results(x, y, x_target, methods_results):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'o-', color='blue', label='Узлы интерполяции', markersize=6)
    
    x_dense = np.linspace(min(x) - 0.1, max(x) + 0.1, 200)
    y_dense =[lagrange(x, y, xi) for xi in x_dense]
    plt.plot(x_dense, y_dense, '--', color='gray', label='Глобальный полином P_n(x)', alpha=0.7)

    if methods_results.get("Ньютон") is not None:
        y_newton = [newton_finite(x, y, xi) for xi in x_dense]
        plt.plot(x_dense, y_newton, '-', color='green', label='Полином Ньютона')

    if methods_results.get("Гаусс") is not None:
        center_idx = len(x) // 2
        y_gauss = [gauss(x, y, xi, center_idx=center_idx) for xi in x_dense]
        plt.plot(x_dense, y_gauss, '-', color='orange', label='Полином Гаусса')
    
    colors =['red', 'green', 'orange', 'purple', 'cyan']
    for i, (name, val) in enumerate(methods_results.items()):
        if val is not None:
            plt.plot(x_target, val, 'X', color=colors[i % len(colors)], label=f'{name}: {val:.5f}', markersize=9)
        
    plt.title('Интерполяция функции')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(script_dir, "img")
    os.makedirs(img_dir, exist_ok=True)
    out_path = os.path.join(img_dir, "interpolation.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()

def validate_data(x, y):
    if len(x) != len(y):
        print("Ошибка: Количества x и y не совпадают!")
        return False
    if len(x) < 2:
        print("Ошибка: Для интерполяции нужно минимум 2 точки.")
        return False
    if len(set(x)) != len(x):
        print("Ошибка: Узлы интерполяции (x) должны быть уникальными.")
        return False
    return True

def main():
    while True:
        print("--- Лабораторная работа №5: Интерполяция функции ---")
        print("1. Ввести данные с клавиатуры")
        print("2. Загрузить из файла (по умолчанию test1.txt)")
        print("3. Использовать встроенную функцию (sin, x^3)")
        print("0. Выход")

        while True:
            choice = input("Выберите действие (0-3): ")
            if choice in {"0", "1", "2", "3"}:
                break
            print("Неверный выбор. Попробуйте снова.")
        if choice == '0':
            print("Завершение программы.")
            break
            
        x, y = [],[]
        
        if choice == '1':
            while True:
                try:
                    x = parse_floats(input("Введите узлы X через пробел: "))
                    y = parse_floats(input("Введите значения Y через пробел: "))
                    break
                except ValueError as exc:
                    print(f'Ошибка ввод: {exc}')
                
        elif choice == '2':
            while True:
                fname = input("Введите имя файла (Enter для test1.txt): ")
                if not fname: fname = "test1.txt"
                base_name = os.path.basename(fname)
                if not (base_name.startswith("test") and base_name.endswith(".txt")):
                    print("Доступ разрешен только к файлам вида test*.txt")
                    continue
                if not os.path.exists(fname):
                    print("Файл не найден!")
                    continue
                try:
                    with open(fname, 'r') as f:
                        lines = f.readlines()
                        x = parse_floats(lines[0])
                        y = parse_floats(lines[1])
                    break
                except (ValueError, IndexError) as exc:
                    if isinstance(exc, IndexError):
                        print("Ошибка формата файла: ожидались две строки с числами.")
                    else:
                        print("Ошибка формата файла.")
                
        elif choice == '3':
            print("1. sin(x)\n2. x^3")
            while True:
                func_choice = input("Выберите функцию (1-2): ")
                if func_choice not in {"1", "2"}:
                    print("Неизвестная функция.")
                    continue
                while True:
                    try:
                        a, b = parse_floats(input("Введите границы интервала A B через пробел: "))
                        break
                    except ValueError as exc:
                        print("Ошибка ввода параметров.")

                while True:
                    try:
                        pts = int(input("Введите количество узлов: "))
                        if pts < 2 or pts > MAX_FUNC_POINTS:
                            raise ValueError(
                                f"Количество узлов должно быть от 2 до {MAX_FUNC_POINTS}."
                            )
                        break
                    except ValueError as exc:
                        print("Ошибка ввода параметров.")

                x = list(np.linspace(a, b, pts))
                if func_choice == '1':   y = [math.sin(xi) for xi in x]
                elif func_choice == '2': y = [xi**3 for xi in x]
                break
        else:
            continue

        if not validate_data(x, y):
            continue

        equidistant = is_equidistant(x)
        if not equidistant:
            print("Внимание: Узлы не равноотстоящие! Будет посчитан только Лагранж")

        diffs = get_finite_differences(y)
        print_diff_table(x, diffs)

        while True:
            try:
                x_target = parse_float(input("Введите значение аргумента (X) для интерполяции: "))
                break
            except ValueError as exc:
                print("Некорректный ввод X.")

        results = {"Лагранж": lagrange(x, y, x_target)}
        if equidistant:
            results["Ньютон"] = newton_finite(x, y, x_target)
            results["Гаусс"] = gauss(x, y, x_target, center_idx=len(x) // 2)
            results["Стирлинг"] = stirling(x, y, x_target)
            results["Бессель"] = bessel(x, y, x_target)

        print(f"\n--- Результаты интерполяции для X = {x_target} ---")
        for name, val in results.items():
            print(f"{name:10}: {val:.6f}")

        plot_results(x, y, x_target, results)

if __name__ == "__main__":
    main()