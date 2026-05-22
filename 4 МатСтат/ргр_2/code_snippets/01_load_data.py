import csv
import numpy as np


def read_columns(path: str) -> dict[str, np.ndarray]:
    columns = {"X1": [], "X2": [], "X3": [], "X4": []}
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            for key in columns:
                columns[key].append(float(row[key]))
    return {k: np.asarray(v, dtype=float) for k, v in columns.items()}


data = read_columns("data.csv")
x1, x2, x3, x4 = data["X1"], data["X2"], data["X3"], data["X4"]