using System.Threading;

public interface IExternalDataService
{
    Task<string> GetUserDataAsync(int userId);
    Task<string> GetUserDataAsync(int userId, CancellationToken cancellationToken);
    
    Task<string> GetUserOrdersAsync(int userId);
    Task<string> GetUserOrdersAsync(int userId, CancellationToken cancellationToken);
    
    Task<string> GetAdsAsync();
    Task<string> GetAdsAsync(CancellationToken cancellationToken);
    
    Task<string> GetAdsFromBackupAsync(CancellationToken cancellationToken);
}