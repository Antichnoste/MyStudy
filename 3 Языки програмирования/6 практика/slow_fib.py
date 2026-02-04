import time

def fib_py(n):
    if n <= 1:
        return n
    return fib_py(n-1) + fib_py(n-2)

if __name__ == "__main__":
    number = 35
    start = time.time()
    result = fib_py(number)
    end = time.time()
    print(f"[Python] Fib({number}) = {result}")
    print(f"[Python] Время: {end - start:.4f} сек")