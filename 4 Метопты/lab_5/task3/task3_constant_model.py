import numpy as np


DATA = np.array([
    [0.95, 1.00, 0.44],
    [1.80, 1.86, 1.88],
    [3.04, 2.97, 4.29],
    [3.96, 4.14, 2.60],
    [4.99, 4.91, 0.76],
])

Z = DATA[:, 2]


def mse_loss(constant_value):
    return np.mean((Z - constant_value) ** 2)


def mae_loss(constant_value):
    return np.mean(np.abs(Z - constant_value))


def main():
    mse_constant = float(np.mean(Z))
    mae_constant = float(np.median(Z))

    mse_value = float(mse_loss(mse_constant))
    mae_value = float(mae_loss(mae_constant))

    print("Задание 3. Константная модель")
    print("=" * 60)
    print(f"MSE-оптимальная константа: {mse_constant:.6f}")
    print(f"  MSE = {mse_value:.6f}")
    print()
    print(f"MAE-оптимальная константа: {mae_constant:.6f}")
    print(f"  MAE = {mae_value:.6f}")
    print()
    print("Резюме:")
    print("  Для MSE лучшая константа — среднее значение Z.")
    print("  Для MAE лучшая константа — медиана Z.")


if __name__ == "__main__":
    main()