import numpy as np

# Квадратичная регрессия: y = a + bx + cx^2
c_quad, b_quad, a_quad = np.polyfit(x, y, 2)
y_pred_quad = a_quad + b_quad * x + c_quad * (x**2)

print(f"Квадратичная модель: y = {a_quad:.4f} + {b_quad:.4f}x + {c_quad:.6f}x²")
print(f"Параметры: a = {a_quad:.4f}, b = {b_quad:.4f}, c = {c_quad:.6f}")
