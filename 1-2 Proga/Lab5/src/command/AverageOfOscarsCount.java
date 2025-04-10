package command;

import managers.CollectionManager;
import models.Movie;
import utility.Console;
import utility.ExecutionResponse;

/**
 * Команды для подсчёта среднего кол-ва Оскаров в коллекции
 */
public class AverageOfOscarsCount extends Command{
    private final Console console;
    private final CollectionManager manager;

    /**
     * Конструктор
     * @param console консоль
     * @param manager менеджер коллекции
     */
    public AverageOfOscarsCount(Console console, CollectionManager manager) {
        super("average_of_oscars_count", "вывести среднее значение поля oscarsCount для всех элементов коллекции");
        this.console = console;
        this.manager = manager;
    }


    /**
     * Исполение команды
     * @param arguments массив с аргументами
     * @return среднее значение кол-ва оскаров у фильмов
     */
    @Override
    public ExecutionResponse apply(String[] arguments) {

        if (!arguments[1].isEmpty()) {
            return new ExecutionResponse(false, "Неправильное кол-во аргументов \nИспользование: '" + getName() + "'");
        }

        console.println("Считаем среднее кол-во оскаров в коллекции...");

        if (manager.getCollection().isEmpty()){
            return new ExecutionResponse(false, "Коллекция пуста!");
        }

        int CountOfMovie = manager.getCollection().size();
        float SumOfOscars = 0;

        for(Movie movie : manager.getCollection()){
            SumOfOscars += movie.getOscarsCount();
        }

        return new ExecutionResponse("Среднее кол-во Оскаров в коллекции: " + Float.toString(SumOfOscars / CountOfMovie));

    }
}
