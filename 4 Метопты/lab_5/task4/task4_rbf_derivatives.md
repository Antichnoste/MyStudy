# Задание 4. Аналитические производные для RBF-сети (Стратегия 2)

## Модель RBF-сети с двумя базисными функциями

$$
\hat z(x,y) = w_1\,\exp\left(-\frac{(x-c_{1x})^2 + (y-c_{1y})^2}{2\sigma_1^2}\right) + w_2\,\exp\left(-\frac{(x-c_{2x})^2 + (y-c_{2y})^2}{2\sigma_2^2}\right) + w_0
$$

где
- $(c_{1x}, c_{1y})$ и $(c_{2x}, c_{2y})$ — центры двух базисных функций,
- $\sigma_1$ и $\sigma_2$ — параметры масштаба (ширина Гауссианов),
- $w_1, w_2, w_0$ — веса модели.

## Лосс-функция

Для одного объекта $(x, y, z)$:
$$
L = \frac12(\hat z - z)^2
$$

По правилу цепочки:
$$
\frac{\partial L}{\partial \theta} = (\hat z - z)\,\frac{\partial \hat z}{\partial \theta}
$$

## Частные производные первой итерации

Обозначим:
- $\varepsilon = \hat z - z$ — ошибка предсказания,
- $\varphi_1 = \exp\left(-\frac{(x-c_{1x})^2 + (y-c_{1y})^2}{2\sigma_1^2}\right)$,
- $\varphi_2 = \exp\left(-\frac{(x-c_{2x})^2 + (y-c_{2y})^2}{2\sigma_2^2}\right)$,
- $r_1^2 = (x-c_{1x})^2 + (y-c_{1y})^2$,
- $r_2^2 = (x-c_{2x})^2 + (y-c_{2y})^2$.

Тогда:

$$\frac{\partial L}{\partial w_0} = \varepsilon,$$

$$\frac{\partial L}{\partial w_1} = \varepsilon \cdot \varphi_1,$$

$$\frac{\partial L}{\partial w_2} = \varepsilon \cdot \varphi_2,$$

$$\frac{\partial L}{\partial c_{1x}} = \varepsilon \cdot w_1 \cdot \varphi_1 \cdot \frac{x - c_{1x}}{\sigma_1^2},$$

$$\frac{\partial L}{\partial c_{1y}} = \varepsilon \cdot w_1 \cdot \varphi_1 \cdot \frac{y - c_{1y}}{\sigma_1^2},$$

$$\frac{\partial L}{\partial c_{2x}} = \varepsilon \cdot w_2 \cdot \varphi_2 \cdot \frac{x - c_{2x}}{\sigma_2^2},$$

$$\frac{\partial L}{\partial c_{2y}} = \varepsilon \cdot w_2 \cdot \varphi_2 \cdot \frac{y - c_{2y}}{\sigma_2^2},$$

$$\frac{\partial L}{\partial \sigma_1} = \varepsilon \cdot w_1 \cdot \varphi_1 \cdot \frac{r_1^2}{\sigma_1^3},$$

$$\frac{\partial L}{\partial \sigma_2} = \varepsilon \cdot w_2 \cdot \varphi_2 \cdot \frac{r_2^2}{\sigma_2^3}.$$

## Для полной обучающей выборки

Для MSE на всей выборке из $N$ объектов:
$$
L_{MSE} = \frac{1}{N}\sum_{i=1}^{N}\frac12(\hat z_i - z_i)^2
$$

Каждая производная — это среднее значение соответствующей производной по всем объектам.