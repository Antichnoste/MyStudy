using System;
using System.Threading;
using System.Threading.Tasks;

public class SlowExternalDataService : IExternalDataService
{
    private readonly bool _simulateErrors;
    private readonly Random _random = new Random();

    public SlowExternalDataService(bool simulateErrors = false)
    {
        _simulateErrors = simulateErrors;
    }
    
    public async Task<string> GetUserDataAsync(int userId)
    {
        return await GetUserDataAsync(userId, CancellationToken.None);
    }

    public async Task<string> GetUserOrdersAsync(int userId)
    {
        return await GetUserOrdersAsync(userId, CancellationToken.None);
    }

    public async Task<string> GetAdsAsync()
    {
        return await GetAdsAsync(CancellationToken.None);
    }

    public async Task<string> GetUserDataAsync(int userId, CancellationToken cancellationToken)
    {
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Начало GetUserDataAsync (2000мс)");
        
        try
        {
            await Task.Delay(2000, cancellationToken);
            
            if (_simulateErrors && _random.Next(0, 10) < 3)
                throw new Exception("Сервис пользователей временно недоступен");
                
            string result = $"Данные пользователя {userId}";
            Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Завершение GetUserDataAsync: {result}");
            return result;
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] GetUserDataAsync отменён");
            throw;
        }
    }

    public async Task<string> GetUserOrdersAsync(int userId, CancellationToken cancellationToken)
    {
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Начало GetUserOrdersAsync (3000мс)");
        
        try
        {
            await Task.Delay(3000, cancellationToken);
            
            if (_simulateErrors && _random.Next(0, 10) < 4)
                throw new Exception("Сервис заказов перегружен");
                
            string result = $"Заказы пользователя {userId}";
            Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Завершение GetUserOrdersAsync: {result}");
            return result;
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] GetUserOrdersAsync отменён");
            throw;
        }
    }

    public async Task<string> GetAdsAsync(CancellationToken cancellationToken)
    {
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Начало GetAdsAsync (1000мс)");
        
        try
        {
            await Task.Delay(1000, cancellationToken);
            
            if (_simulateErrors && _random.Next(0, 10) < 2)
                throw new Exception("Рекламный сервис не отвечает");
                
            string result = "Рекламный контент (основной)";
            Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Завершение GetAdsAsync: {result}");
            return result;
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] GetAdsAsync отменён");
            throw;
        }
    }

    public async Task<string> GetAdsFromBackupAsync(CancellationToken cancellationToken)
    {
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Начало GetAdsFromBackupAsync (1500мс)");
        
        try
        {
            await Task.Delay(1500, cancellationToken);
            string result = "Рекламный контент (резервный)";
            Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Завершение GetAdsFromBackupAsync: {result}");
            return result;
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] GetAdsFromBackupAsync отменён");
            throw;
        }
    }
}