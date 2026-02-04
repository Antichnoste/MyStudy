using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using Python.Runtime; // Библиотека Python.NET
namespace InteropDemo

{
    // --- БЛОК 1: Обертка для P/Invoke ---
    static class NativeLib
    {
        // Имя библиотеки без расширения (система сама подставит .dll или .so)
        const string LibName = "fib_native";

        [DllImport(LibName, CallingConvention = CallingConvention.Cdecl)]
        public static extern long fib_c_recursive(int n);

        [DllImport(LibName, CallingConvention = CallingConvention.Cdecl)]
        public static extern long fib_c_iterative(int n);
    }

    static void RunPythonIntegration()
    {
        Console.WriteLine("[Part 2] Интеграция с Python (Аналитика)");
        try
        {
            // ==========================================================
            // !!! ВАЖНО: ЗАДАНИЕ ПУТИ К PYTHON DLL !!!
            // ЗАМЕНИТЕ ЭТОТ ПУТЬ НА ТОТ, КОТОРЫЙ ВЫ НАШЛИ В СИСТЕМЕ.
            // ==========================================================
            const string PythonDllPath = @"C:\Users\anti\AppData\Local\Microsoft\WindowsApps\python3.exe"; 

            if (File.Exists(PythonDllPath))
            {
                // Устанавливаем путь к DLL
                Runtime.PythonDLL = PythonDllPath;
                Console.WriteLine($"[Python.NET] Установлен путь: {PythonDllPath}");
            }
            else
            {
                // Если файл не найден по указанному пути, выдаем предупреждение
                Console.WriteLine($"[Python.NET] ОШИБКА: Файл DLL не найден по пути: {PythonDllPath}");
                return; // Выходим, чтобы избежать ошибки инициализации
            }

            // Инициализация движка Python
            if (!PythonEngine.IsInitialized)
            {
                // Теперь эта строка должна сработать, так как путь указан выше
                PythonEngine.Initialize();
                Console.WriteLine("[Python.NET] Движок успешно инициализирован.");
            }

            using (Py.GIL()) 
            {
                // ... Ваш код для работы с Python (импорт, вызовы функций и т.д.)
                dynamic builtins = Py.Import("builtins");
                builtins.print("[Python] Успешная работа из C#!");

                // ... (остальной код)
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[Критическая ошибка Python] {ex.Message}");
        }
    }


    class Program
    {
        static void Main(string[] args)
        {
            // Установка путей для Python (Если нужно, раскомментируйте и укажите свой путь)
            // Runtime.PythonDLL = @"C:\Path\To\Python3x\python3x.dll";

            Console.WriteLine("=== ЛАБОРАТОРНАЯ РАБОТА: C# + C + Python ===\n");

            // --- ЗАПУСК ЧАСТИ 1 (C vs C#) ---
            RunPerformanceBenchmark();

            Console.WriteLine("\n---------------------------------------------\n");

            // --- ЗАПУСК ЧАСТИ 2 (Python.NET) ---
            RunPythonIntegration();
            
            Console.WriteLine("\nНажмите любую клавишу для выхода...");
            Console.ReadKey();
        }

        // ==========================================
        // Часть 1: Сравнение производительности
        // ==========================================
        static void RunPerformanceBenchmark()
        {
            int n = 42; // Достаточно большое число для заметной разницы в рекурсии
            Console.WriteLine($"[Part 1] Сравнение производительности вычисления Fibonacci({n})");

            // 1. Managed C# (Recursive)
            var sw = Stopwatch.StartNew();
            long resCs = FibCsRecursive(n);
            sw.Stop();
            Console.WriteLine($"C# (Managed) Recursive: {resCs} \t| Время: {sw.ElapsedMilliseconds} мс");

            // 2. Unmanaged C (Recursive)
            try
            {
                sw.Restart();
                long resC = NativeLib.fib_c_recursive(n);
                sw.Stop();
                Console.WriteLine($"C  (Native)  Recursive: {resC} \t| Время: {sw.ElapsedMilliseconds} мс");
                
                // Сравнение ускорения
                double ratio = (double)resCs / (resC == 0 ? 1 : resC); // Просто проверка корректности
                Console.WriteLine(">> Комментарий: Нативный C обычно быстрее в рекурсии за счет отсутствия проверок CLR.");
            }
            catch (DllNotFoundException)
            {
                Console.WriteLine("ОШИБКА: Не найдена библиотека fib_native.dll (или .so). Скопируйте её в папку с .exe!");
            }
        }

        // Чистая C# реализация для сравнения
        static long FibCsRecursive(int n)
        {
            if (n <= 1) return n;
            return FibCsRecursive(n - 1) + FibCsRecursive(n - 2);
        }

        // ==========================================
        // Часть 2: Взаимодействие с Python
        // ==========================================
        static void RunPythonIntegration()
        {
            Console.WriteLine("[Part 2] Интеграция с Python (Аналитика)");

            try
            {
                if (!PythonEngine.IsInitialized)
                {
                    PythonEngine.Initialize();
                }

                using (Py.GIL())
                {
                    // 1. Использование стандартной математики
                    dynamic math = Py.Import("math");
                    double result = math.pow(2, 10);
                    Console.WriteLine($"[Python] math.pow(2, 10) = {result}");

                    // 2. Обработка списка данных
                    // Представим, что мы передаем данные из C# в Python для статистики
                    dynamic statistics = Py.Import("statistics");
                    
                    // Создаем Python список из массива C#
                    var cSharpData = new double[] { 10.5, 20.1, 15.3, 99.9, 5.0 };
                    dynamic pyList = new PyList();
                    foreach (var item in cSharpData) pyList.append(item);

                    double mean = statistics.mean(pyList);
                    double median = statistics.median(pyList);

                    Console.WriteLine("[Python] Анализ массива данных:");
                    Console.WriteLine($"   -> Входные данные (C#): [{string.Join(", ", cSharpData)}]");
                    Console.WriteLine($"   -> Среднее (statistics.mean): {mean}");
                    Console.WriteLine($"   -> Медиана (statistics.median): {median}");

                    PythonEngine.RunSimpleString("print('[Python Internals] Привет! Я работаю внутри процесса .NET')");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Ошибка Python]: {ex.Message}");
                Console.WriteLine("Убедитесь, что Python установлен и добавлен в PATH, либо задайте Runtime.PythonDLL.");
            }
            finally
            {
                PythonEngine.Shutdown();
            }
        }
    }
}