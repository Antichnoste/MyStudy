import time


start_time = time.time()
for i in range(100):
    import main.main as main
end_time = time.time()

print(f"Основа - {end_time - start_time}")

start_time = time.time()
for i in range(100):
    import task1.task1 as task1
end_time = time.time()

print(f"Доп 1  - {end_time - start_time}")

start_time = time.time()
for i in range(100):
    import task2.task2 as task2
end_time = time.time()

print(f"Доп 2  - {end_time - start_time}")

start_time = time.time()
for i in range(100):
    import task3.task3
end_time = time.time()

print(f"Доп 3  - {end_time - start_time}")