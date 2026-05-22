import pandas as pd
import numpy as np

# Загрузка данных
df = pd.read_csv('data.csv', sep=',')
x = df['x'].values
y = df['y'].values
n = len(x)

# Линейная регрессия: y = a + bx
b_lin, a_lin = np.polyfit(x, y, 1)
y_pred_lin = a_lin + b_lin * x

print(f"Линейная модель: y = {a_lin:.4f} + {b_lin:.4f}x")
print(f"Параметры: a = {a_lin:.4f}, b = {b_lin:.4f}")
