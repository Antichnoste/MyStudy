import ctypes, time, os
from slow_fib import fib_py

lib_name = "fast_lib.dll"
lib_path = "./fast_lib.dll"

c_lib = ctypes.CDLL(lib_path)

c_lib.fib_c.argtypes = [ctypes.c_int]
c_lib.fib_c.restype = ctypes.c_longlong

c_lib.fib_c_iterative.argtypes = [ctypes.c_int]
c_lib.fib_c_iterative.restype = ctypes.c_longlong

class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]

c_lib.process_point.argtypes = [ctypes.POINTER(Point)]
c_lib.process_point.restype = None

if __name__ == "__main__":
    n = 35

    # Python
    t0 = time.time()
    r_py = fib_py(n)
    t1 = time.time()

    # C recursive
    t2 = time.time()
    r_c = c_lib.fib_c(n)
    t3 = time.time()

    # C iterative
    t4 = time.time()
    r_iter = c_lib.fib_c_iterative(n)
    t5 = time.time()

    print(f"[Python] Fib({n}) = {r_py}, время: {t1 - t0:.4f} сек")
    print(f"[C-рекурсия] Fib({n}) = {r_c}, время: {t3 - t2:.4f} сек")
    print(f"[C-итеративно] Fib({n}) = {r_iter}, время: {t5 - t4:.6f} сек")

    py_time = t1 - t0
    c_time = t3 - t2
    speedup = py_time / c_time if c_time > 0 else float('inf')
    print(f"\nC-рекурсия быстрее Python в {speedup:.0f} раз")

    # --- Тест структуры ---
    print("\n--- Тест структуры Point ---")
    p = Point(x=3, y=7)
    print(f"[Python] До: x={p.x}, y={p.y}")
    c_lib.process_point(ctypes.byref(p))
    print(f"[Python] После: x={p.x}, y={p.y}")