import numpy as np

# Степенная регрессия: y = a * x^b => ln(y) = ln(a) + b*ln(x)
b_pow, ln_a_pow = np.polyfit(np.log(x), np.log(y), 1)
a_pow = np.exp(ln_a_pow)
y_pred_pow = a_pow * (x**b_pow)

print(f"Степенная модель: y = {a_pow:.4f} * x^{b_pow:.4f}")
print(f"Параметры: ln(a) = {ln_a_pow:.4f}, a = {a_pow:.4f}, b = {b_pow:.4f}")
