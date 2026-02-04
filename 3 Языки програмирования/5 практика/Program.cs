using System;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        await RunBasicTests();
        await RunAdvancedTests();
    }

    static async Task RunBasicTests()
    {
        Console.WriteLine("ОСНОВНЫЕ ТЕСТЫ");
        
        var externalService = new SlowExternalDataService();
        var aggregator = new PageAggregatorService(externalService);

        int testUserId = 123;

        var stopwatch = Stopwatch.StartNew();
        var sequentialResult = await aggregator.LoadPageDataSequentialAsync(testUserId);
        stopwatch.Stop();
        
        Console.WriteLine(sequentialResult);
        Console.WriteLine($"\n|| Последовательная загрузка: {stopwatch.ElapsedMilliseconds} ms   ||");

        await Task.Delay(500);

        stopwatch.Restart();
        var parallelResult = await aggregator.LoadPageDataParallelAsync(testUserId);
        stopwatch.Stop();
        
        Console.WriteLine(parallelResult);
        Console.WriteLine($"\n|| Параллельная загрузка: {stopwatch.ElapsedMilliseconds} ms   ||");
    }

    static async Task RunAdvancedTests()
    {
        Console.WriteLine("\n\nДОПОЛНИТЕЛЬНЫЕ ЗАДАНИЯ");

        await TestErrorHandling();
        
        await TestCancellation();
        
        await TestRaceCondition();
    }

    static async Task TestErrorHandling()
    {
        Console.WriteLine("\n--- ДОП 1: ОБРАБОТКА ОШИБОК ---");
        
        var faultyService = new SlowExternalDataService(simulateErrors: true);
        var aggregator = new PageAggregatorService(faultyService);

        var stopwatch = Stopwatch.StartNew();
        var result = await aggregator.LoadPageDataParallelWithErrorHandlingAsync(123);
        stopwatch.Stop();
        
        Console.WriteLine(result);
        Console.WriteLine($"Время выполнения с обработкой ошибок: {stopwatch.ElapsedMilliseconds} ms");
    }

    static async Task TestCancellation()
    {
        Console.WriteLine("\n--- ДОП 2: ОТМЕНА ОПЕРАЦИЙ ---");
        
        var externalService = new SlowExternalDataService();
        var aggregator = new PageAggregatorService(externalService);

        var cts = new CancellationTokenSource();
        
        cts.CancelAfter(1500);

        try
        {
            var stopwatch = Stopwatch.StartNew();
            var result = await aggregator.LoadPageDataParallelAsync(123, cts.Token);
            stopwatch.Stop();
            
            Console.WriteLine(result);
            Console.WriteLine($"Операция завершена: {stopwatch.ElapsedMilliseconds} ms");
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("ОПЕРАЦИЯ ОТМЕНЕНА! Превышено время ожидания (1500 ms)");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Произошла ошибка: {ex.Message}");
        }
    }

    static async Task TestRaceCondition()
    {
        Console.WriteLine("\n--- ДОП 3: ГОНКА УСЛОВИЙ ---");
        
        var externalService = new SlowExternalDataService();
        var aggregator = new PageAggregatorService(externalService);

        var stopwatch = Stopwatch.StartNew();
        var result = await aggregator.LoadPageDataWithRaceConditionAsync(123, CancellationToken.None);
        stopwatch.Stop();
        
        Console.WriteLine(result);
        Console.WriteLine($"Время выполнения с гонкой условий: {stopwatch.ElapsedMilliseconds} ms");
        
        Console.WriteLine("\nАнализ гонки условий:");
        Console.WriteLine("Основной сервис рекламы: 1000ms");
        Console.WriteLine("Резервный сервис рекламы: 1500ms");
        Console.WriteLine("Победитель: ОСНОВНОЙ сервис (должен всегда выигрывать)");
    }

}