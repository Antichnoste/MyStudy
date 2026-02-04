using System.Threading;

public interface IPageAggregator
{
    Task<PagePayload> LoadPageDataSequentialAsync(int userId);
    Task<PagePayload> LoadPageDataParallelAsync(int userId);
    
    Task<PagePayload> LoadPageDataSequentialAsync(int userId, CancellationToken cancellationToken);
    Task<PagePayload> LoadPageDataParallelAsync(int userId, CancellationToken cancellationToken);
    
    Task<PagePayload> LoadPageDataParallelWithErrorHandlingAsync(int userId);
    Task<PagePayload> LoadPageDataParallelWithErrorHandlingAsync(int userId, CancellationToken cancellationToken);
    
    Task<PagePayload> LoadPageDataWithRaceConditionAsync(int userId, CancellationToken cancellationToken);
}