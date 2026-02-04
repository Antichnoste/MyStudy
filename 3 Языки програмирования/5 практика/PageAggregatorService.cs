using System;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

public class PageAggregatorService : IPageAggregator
{
    private readonly IExternalDataService _externalService;

    public PageAggregatorService(IExternalDataService externalService)
    {
        _externalService = externalService;
    }

    public async Task<PagePayload> LoadPageDataSequentialAsync(int userId)
    {
        return await LoadPageDataSequentialAsync(userId, CancellationToken.None);
    }

    public async Task<PagePayload> LoadPageDataParallelAsync(int userId)
    {
        return await LoadPageDataParallelAsync(userId, CancellationToken.None);
    }

    public async Task<PagePayload> LoadPageDataSequentialAsync(int userId, CancellationToken cancellationToken)
    {
        Console.WriteLine("\n=== ПОСЛЕДОВАТЕЛЬНАЯ ЗАГРУЗКА ===");
        
        var userData = await _externalService.GetUserDataAsync(userId, cancellationToken);
        var orderData = await _externalService.GetUserOrdersAsync(userId, cancellationToken);
        var adData = await _externalService.GetAdsAsync(cancellationToken);

        return new PagePayload
        {
            UserData = userData,
            OrderData = orderData,
            AdData = adData
        };
    }

    public async Task<PagePayload> LoadPageDataParallelAsync(int userId, CancellationToken cancellationToken)
    {
        Console.WriteLine("\n=== ПАРАЛЛЕЛЬНАЯ ЗАГРУЗКА ===");
        
        var userTask = _externalService.GetUserDataAsync(userId, cancellationToken);
        var ordersTask = _externalService.GetUserOrdersAsync(userId, cancellationToken);
        var adsTask = _externalService.GetAdsAsync(cancellationToken);

        await Task.WhenAll(userTask, ordersTask, adsTask);

        return new PagePayload
        {
            UserData = userTask.Result,
            OrderData = ordersTask.Result,
            AdData = adsTask.Result
        };
    }

    public async Task<PagePayload> LoadPageDataParallelWithErrorHandlingAsync(int userId)
    {
        return await LoadPageDataParallelWithErrorHandlingAsync(userId, CancellationToken.None);
    }

    public async Task<PagePayload> LoadPageDataParallelWithErrorHandlingAsync(int userId, CancellationToken cancellationToken)
    {
        Console.WriteLine("\n=== ПАРАЛЛЕЛЬНАЯ ЗАГРУЗКА С ОБРАБОТКОЙ ОШИБОК ===");
        
        var userTask = _externalService.GetUserDataAsync(userId, cancellationToken);
        var ordersTask = _externalService.GetUserOrdersAsync(userId, cancellationToken);
        var adsTask = _externalService.GetAdsAsync(cancellationToken);

        var allTasks = new[] { userTask, ordersTask, adsTask };
        
        try
        {
            await Task.WhenAll(allTasks.Select(task => 
                task.ContinueWith(t => t, TaskContinuationOptions.ExecuteSynchronously)));
        }
        catch (AggregateException ae)
        {
            Console.WriteLine($"Произошли ошибки: {string.Join("; ", ae.InnerExceptions.Select(e => e.Message))}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Ошибка: {ex.Message}");
        }

        return new PagePayload
        {
            UserData = userTask.IsCompletedSuccessfully ? userTask.Result : "Ошибка загрузки",
            OrderData = ordersTask.IsCompletedSuccessfully ? ordersTask.Result : "Ошибка загрузки",
            AdData = adsTask.IsCompletedSuccessfully ? adsTask.Result : "Ошибка загрузки"
        };
    }

    public async Task<PagePayload> LoadPageDataWithRaceConditionAsync(int userId, CancellationToken cancellationToken)
    {
        Console.WriteLine("\n=== ГОНКА УСЛОВИЙ - ВЫБОР САМОГО БЫСТРОГО ИСТОЧНИКА ===");
        
        var userTask = _externalService.GetUserDataAsync(userId, cancellationToken);
        var ordersTask = _externalService.GetUserOrdersAsync(userId, cancellationToken);
        
        var primaryAdsTask = _externalService.GetAdsAsync(cancellationToken);
        var backupAdsTask = _externalService.GetAdsFromBackupAsync(cancellationToken);

        var completedAdsTask = await Task.WhenAny(primaryAdsTask, backupAdsTask);
        var adData = await completedAdsTask;

        Console.WriteLine($"Использован источник: {(completedAdsTask == primaryAdsTask ? "ОСНОВНОЙ" : "РЕЗЕРВНЫЙ")}");

        await Task.WhenAll(userTask, ordersTask);

        return new PagePayload
        {
            UserData = userTask.Result,
            OrderData = ordersTask.Result,
            AdData = adData
        };
    }
}